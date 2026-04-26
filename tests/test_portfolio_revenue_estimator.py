import json
import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from portfolio_revenue_estimator import (
    parse_price,
    classify_tier,
    estimate_monthly_revenue,
    load_products,
    audit_prices,
    generate_report,
    suggest_optimizations,
    PRICE_TIERS,
    CATEGORY_REVENUE_MULTIPLIERS,
)


class TestParsePrice:
    def test_integer(self):
        assert parse_price(29) == 29.0

    def test_float(self):
        assert parse_price(19.99) == 19.99

    def test_string_with_dollar(self):
        assert parse_price("$29") == 29.0

    def test_string_with_euro(self):
        assert parse_price("€19") == 19.0

    def test_string_plain(self):
        assert parse_price("9") == 9.0

    def test_none(self):
        assert parse_price(None) == 0.0

    def test_empty_string(self):
        assert parse_price("") == 0.0

    def test_invalid_string(self):
        assert parse_price("free") == 0.0


class TestClassifyTier:
    def test_budget(self):
        assert classify_tier(5) == "budget"
        assert classify_tier(0) == "budget"

    def test_standard(self):
        assert classify_tier(9) == "standard"
        assert classify_tier(15) == "standard"

    def test_premium(self):
        assert classify_tier(19) == "premium"
        assert classify_tier(25) == "premium"

    def test_enterprise(self):
        assert classify_tier(29) == "enterprise"
        assert classify_tier(99) == "enterprise"


class TestEstimateMonthlyRevenue:
    def test_basic_product(self):
        products = [{"slug": "test-tool", "name": "Test Tool", "price": 19,
                      "status": "live", "checkout_status": "active"}]
        results = estimate_monthly_revenue(products)
        assert len(results) == 1
        assert results[0]["price"] == 19.0
        assert results[0]["tier"] == "premium"
        assert results[0]["est_monthly_revenue"] > 0

    def test_no_price_product(self):
        products = [{"slug": "free-tool", "name": "Free Tool", "price": 0,
                      "status": "live", "checkout_status": "inactive"}]
        results = estimate_monthly_revenue(products)
        assert results[0]["price"] == 0.0
        assert results[0]["est_monthly_revenue"] == 0.0

    def test_category_multiplier_applied(self):
        p_dev = {"slug": "dev-tool", "name": "Dev", "price": 19,
                 "category": "developer-tools", "status": "live", "checkout_status": "active"}
        p_util = {"slug": "util-tool", "name": "Util", "price": 19,
                  "category": "utilities", "status": "live", "checkout_status": "active"}
        results = estimate_monthly_revenue([p_dev, p_util])
        dev_rev = results[0]["est_monthly_revenue"]
        util_rev = results[1]["est_monthly_revenue"]
        assert dev_rev > util_rev

    def test_compact_keys(self):
        products = [{"s": "test", "n": "Test", "price": "$9",
                      "st": "live", "checkout_status": "active"}]
        results = estimate_monthly_revenue(products)
        assert results[0]["slug"] == "test"
        assert results[0]["name"] == "Test"


class TestAuditPrices:
    def test_audit_output(self, capsys):
        products = [
            {"slug": "a", "name": "A", "price": 9, "status": "live"},
            {"slug": "b", "name": "B", "price": 29, "status": "live"},
            {"slug": "c", "name": "C", "price": 0, "status": "live"},
        ]
        results = audit_prices(products)
        assert len(results) == 3
        out = capsys.readouterr().out
        assert "Tier Distribution" in out
        assert "budget" in out

    def test_audit_all_priced(self, capsys):
        products = [{"slug": f"p{i}", "name": f"P{i}", "price": 19, "status": "live"}
                     for i in range(5)]
        results = audit_prices(products)
        assert len(results) == 5
        out = capsys.readouterr().out
        assert "No price: 0" in out


class TestGenerateReport:
    def test_report_creates_file(self, tmp_path):
        products = [
            {"slug": "top", "name": "Top Earner", "price": 29, "status": "live",
             "checkout_status": "active", "category": "developer-tools"},
            {"slug": "mid", "name": "Mid Earner", "price": 9, "status": "live",
             "checkout_status": "active", "category": "utilities"},
        ]
        with patch("portfolio_revenue_estimator.ANALYSIS_DIR", tmp_path):
            report = generate_report(products)

        assert "summary" in report
        assert report["summary"]["total_products"] == 2
        assert report["summary"]["checkout_active"] == 2
        assert report["summary"]["estimated_annual_revenue"] > 0
        assert len(report["top_earners"]) == 2
        assert report["top_earners"][0]["est_monthly_revenue"] >= report["top_earners"][1]["est_monthly_revenue"]

    def test_report_empty_products(self, tmp_path, capsys):
        with patch("portfolio_revenue_estimator.ANALYSIS_DIR", tmp_path):
            report = generate_report([])
        assert report["summary"]["total_products"] == 0
        assert report["summary"]["estimated_monthly_revenue"] == 0


class TestSuggestOptimizations:
    def test_missing_price_suggestion(self, capsys):
        products = [{"slug": "free", "name": "Free", "price": 0, "status": "live",
                     "category": "developer-tools", "checkout_status": "inactive"}]
        suggestions = suggest_optimizations(products)
        assert any(s["type"] == "missing_price" for s in suggestions)

    def test_underpriced_suggestion(self, capsys):
        products = [{"slug": "cheap-dev", "name": "Cheap Dev", "price": 5, "status": "live",
                     "category": "developer-tools", "checkout_status": "active"}]
        suggestions = suggest_optimizations(products)
        assert any(s["type"] == "underpriced" for s in suggestions)

    def test_no_suggestions_for_good_pricing(self, capsys):
        products = [{"slug": "ok", "name": "OK", "price": 19, "status": "live",
                     "category": "developer-tools", "checkout_status": "active"}]
        suggestions = suggest_optimizations(products)
        assert len(suggestions) == 0

    def test_overpriced_utility(self, capsys):
        products = [{"slug": "expensive-util", "name": "Expensive", "price": 25, "status": "live",
                     "category": "utilities", "checkout_status": "active"}]
        suggestions = suggest_optimizations(products)
        assert any(s["type"] == "overpriced" for s in suggestions)


class TestConstants:
    def test_price_tiers_complete(self):
        assert "budget" in PRICE_TIERS
        assert "standard" in PRICE_TIERS
        assert "premium" in PRICE_TIERS
        assert "enterprise" in PRICE_TIERS

    def test_category_multipliers(self):
        assert "developer-tools" in CATEGORY_REVENUE_MULTIPLIERS
        assert "ai-tools" in CATEGORY_REVENUE_MULTIPLIERS
        assert all(v > 0 for v in CATEGORY_REVENUE_MULTIPLIERS.values())
