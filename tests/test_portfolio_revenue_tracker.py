#!/usr/bin/env python3
"""Tests for portfolio_revenue_tracker.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.portfolio_revenue_tracker import (
    analyze,
    telegram_summary,
    to_markdown,
)


def _make_products(n: int, *, checkout: bool = True, price: bool = True) -> list[dict]:
    products = []
    for i in range(n):
        p = {
            "slug": f"product-{i}",
            "name": f"Product {i}",
            "status": "live",
        }
        if checkout:
            p["checkout_url"] = f"https://buy.polar.sh/checkout_{i}"
        else:
            p["checkout_url"] = ""
        if price:
            p["price"] = f"${(i % 5 + 1) * 5}"
        else:
            p["price"] = ""
        products.append(p)
    return products


class TestAnalyze:
    def test_empty_products(self):
        report = analyze([])
        assert report["total_products"] == 0
        assert report["live_count"] == 0
        assert report["has_checkout"] == 0
        assert report["checkout_coverage_pct"] == 0.0

    def test_all_live_with_checkout_and_price(self):
        products = _make_products(10)
        report = analyze(products)
        assert report["live_count"] == 10
        assert report["has_checkout"] == 10
        assert report["no_checkout"] == 0
        assert report["checkout_coverage_pct"] == 100.0
        assert report["has_price"] == 10
        assert report["price_coverage_pct"] == 100.0

    def test_mixed_checkout(self):
        products = _make_products(10, checkout=False)
        products[:4] = _make_products(4)
        all_prods = products
        report = analyze(all_prods)
        assert report["has_checkout"] == 4
        assert report["no_checkout"] == 6
        assert 0 < report["checkout_coverage_pct"] < 100

    def test_no_price_products(self):
        products = _make_products(5, price=False)
        report = analyze(products)
        assert report["has_price"] == 0
        assert report["no_price"] == 5
        assert report["price_stats"]["avg"] == 0.0

    def test_price_stats(self):
        products = _make_products(3)
        products[0]["price"] = "$10"
        products[1]["price"] = "$20"
        products[2]["price"] = "$30"
        report = analyze(products)
        assert report["price_stats"]["avg"] == 20.0
        assert report["price_stats"]["min"] == 10.0
        assert report["price_stats"]["max"] == 30.0
        assert report["revenue_potential"]["total_catalog_value"] == 60.0

    def test_price_buckets(self):
        products = []
        for p_val in [0, 3, 7, 15, 25]:
            products.append({"slug": f"p-{p_val}", "status": "live", "checkout_url": "https://x.com", "price": f"${p_val}"})
        report = analyze(products)
        buckets = report["price_stats"]["buckets"]
        assert buckets.get("$1-5", 0) == 1
        assert buckets.get("$6-10", 0) == 1
        assert buckets.get("$11-20", 0) == 1
        assert buckets.get("$20+", 0) == 1

    def test_revenue_potential(self):
        products = _make_products(2)
        products[0]["price"] = "$10"
        products[1]["price"] = "$20"
        report = analyze(products)
        assert report["revenue_potential"]["1_sale_per_product"] == 30.0
        assert report["revenue_potential"]["10_sales_per_product"] == 300.0
        assert report["revenue_potential"]["50_sales_per_product"] == 1500.0

    def test_no_checkout_sample(self):
        products = _make_products(5, checkout=False)
        report = analyze(products)
        assert len(report["no_checkout_sample"]) == 5

    def test_non_live_excluded(self):
        products = [{"slug": "draft", "status": "draft", "checkout_url": "https://x.com", "price": "$5"}]
        report = analyze(products)
        assert report["live_count"] == 0
        assert report["has_checkout"] == 0

    def test_invalid_price_handled(self):
        products = [{"slug": "bad-price", "status": "live", "checkout_url": "https://x.com", "price": "free"}]
        report = analyze(products)
        assert report["has_price"] == 0
        assert report["no_price"] == 1

    def test_timestamp_present(self):
        report = analyze([])
        assert "ts" in report
        assert len(report["ts"]) > 10

    def test_large_portfolio(self):
        products = _make_products(200)
        report = analyze(products)
        assert report["live_count"] == 200
        assert report["checkout_coverage_pct"] == 100.0

    def test_mixed_status_products(self):
        products = [
            {"slug": "live-1", "status": "live", "checkout_url": "https://x.com", "price": "$5"},
            {"slug": "draft-1", "status": "draft", "checkout_url": "https://x.com", "price": "$5"},
            {"slug": "live-2", "status": "live", "checkout_url": "", "price": "$10"},
        ]
        report = analyze(products)
        assert report["total_products"] == 3
        assert report["live_count"] == 2
        assert report["has_checkout"] == 1

    def test_no_checkout_sample_limited(self):
        products = _make_products(30, checkout=False)
        report = analyze(products)
        assert len(report["no_checkout_sample"]) == 20


class TestToMarkdown:
    def test_basic_markdown(self):
        report = analyze(_make_products(5))
        md = to_markdown(report)
        assert "# Revenue Tracker Report" in md
        assert "Checkout Coverage" in md
        assert "Price Coverage" in md
        assert "Revenue Potential" in md

    def test_empty_report_markdown(self):
        report = analyze([])
        md = to_markdown(report)
        assert "Live:** 0" in md


class TestTelegramSummary:
    def test_basic_summary(self):
        report = analyze(_make_products(10))
        msg = telegram_summary(report)
        assert "Revenue Tracker" in msg
        assert "10 live" in msg

    def test_empty_summary(self):
        report = analyze([])
        msg = telegram_summary(report)
        assert "0 live" in msg

    def test_no_checkout_summary(self):
        products = _make_products(5, checkout=False)
        report = analyze(products)
        msg = telegram_summary(report)
        assert "0% checkout" in msg


class TestMainCLI:
    def test_default_json_output(self, capsys):
        with patch.object(sys, "argv", ["portfolio_revenue_tracker.py"]):
            from scripts.portfolio_revenue_tracker import main
            main()
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "live_count" in data

    def test_markdown_flag(self, capsys):
        with patch.object(sys, "argv", ["portfolio_revenue_tracker.py", "--markdown"]):
            from scripts.portfolio_revenue_tracker import main
            main()
        out = capsys.readouterr().out
        assert "# Revenue Tracker Report" in out

    def test_telegram_flag(self, capsys):
        with patch.object(sys, "argv", ["portfolio_revenue_tracker.py", "--telegram"]):
            from scripts.portfolio_revenue_tracker import main
            main()
        out = capsys.readouterr().out
        assert "Revenue Tracker" in out

    def test_json_flag(self, capsys):
        with patch.object(sys, "argv", ["portfolio_revenue_tracker.py", "--json"]):
            from scripts.portfolio_revenue_tracker import main
            main()
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "ts" in data
