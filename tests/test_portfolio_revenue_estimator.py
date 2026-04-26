#!/usr/bin/env python3
"""Tests for portfolio_revenue_estimator.py — price parsing, tier classification,
revenue estimation, optimization suggestions, and report generation."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.portfolio_revenue_estimator import (
    CATEGORY_REVENUE_MULTIPLIERS,
    PRICE_TIERS,
    audit_prices,
    classify_tier,
    estimate_monthly_revenue,
    generate_report,
    load_products,
    parse_price,
    suggest_optimizations,
)


SAMPLE_PRODUCTS = [
    {
        "slug": "budget-tool",
        "name": "Budget Tool",
        "status": "live",
        "price": "$5",
        "category": "utilities",
        "checkout_status": "active",
        "health_status": "healthy",
    },
    {
        "slug": "standard-tool",
        "name": "Standard Tool",
        "status": "live",
        "price": "$15",
        "category": "developer-tools",
        "checkout_status": "active",
        "health_status": "healthy",
    },
    {
        "slug": "premium-tool",
        "name": "Premium Tool",
        "status": "live",
        "price": "$25",
        "category": "security",
        "checkout_status": "active",
        "health_status": "healthy",
    },
    {
        "slug": "enterprise-tool",
        "name": "Enterprise Tool",
        "status": "live",
        "price": "$49",
        "category": "devops",
        "checkout_status": "inactive",
        "health_status": "healthy",
    },
    {
        "slug": "free-tool",
        "name": "Free Tool",
        "status": "live",
        "price": 0,
        "category": "utilities",
        "checkout_status": "inactive",
        "health_status": "healthy",
    },
    {
        "slug": "numeric-price",
        "name": "Numeric Price Tool",
        "status": "live",
        "price": 12,
        "category": "api-services",
        "checkout_status": "active",
        "health_status": "healthy",
    },
    {
        "slug": "euro-price",
        "name": "Euro Price Tool",
        "status": "live",
        "price": "€10",
        "category": "design-tools",
        "checkout_status": "active",
        "health_status": "healthy",
    },
]


class TestParsePrice:
    def test_string_dollar(self):
        assert parse_price("$29") == 29.0

    def test_string_euro(self):
        assert parse_price("€10") == 10.0

    def test_string_plain_number(self):
        assert parse_price("15") == 15.0

    def test_integer(self):
        assert parse_price(25) == 25.0

    def test_float(self):
        assert parse_price(9.99) == 9.99

    def test_zero_int(self):
        assert parse_price(0) == 0.0

    def test_zero_string(self):
        assert parse_price("$0") == 0.0

    def test_none_returns_zero(self):
        assert parse_price(None) == 0.0

    def test_invalid_string_returns_zero(self):
        assert parse_price("free") == 0.0

    def test_empty_string_returns_zero(self):
        assert parse_price("") == 0.0


class TestClassifyTier:
    def test_budget(self):
        assert classify_tier(5) == "budget"

    def test_budget_upper_edge(self):
        assert classify_tier(8.99) == "budget"

    def test_standard(self):
        assert classify_tier(15) == "standard"

    def test_standard_upper_edge(self):
        assert classify_tier(18.99) == "standard"

    def test_premium(self):
        assert classify_tier(25) == "premium"

    def test_premium_upper_edge(self):
        assert classify_tier(28.99) == "premium"

    def test_enterprise(self):
        assert classify_tier(49) == "enterprise"

    def test_zero_is_budget(self):
        assert classify_tier(0) == "budget"


class TestEstimateMonthlyRevenue:
    def test_basic_estimation(self):
        results = estimate_monthly_revenue(SAMPLE_PRODUCTS)
        assert len(results) == len(SAMPLE_PRODUCTS)

    def test_budget_tier_units(self):
        results = estimate_monthly_revenue([
            {"slug": "b1", "name": "B", "price": "$5", "category": "utilities",
             "status": "live", "checkout_status": "active"}
        ])
        assert results[0]["est_monthly_units"] == 30

    def test_standard_tier_units(self):
        results = estimate_monthly_revenue([
            {"slug": "s1", "name": "S", "price": "$15", "category": "utilities",
             "status": "live", "checkout_status": "active"}
        ])
        assert results[0]["est_monthly_units"] == 15

    def test_premium_tier_units(self):
        results = estimate_monthly_revenue([
            {"slug": "p1", "name": "P", "price": "$25", "category": "utilities",
             "status": "live", "checkout_status": "active"}
        ])
        assert results[0]["est_monthly_units"] == 8

    def test_enterprise_tier_units(self):
        results = estimate_monthly_revenue([
            {"slug": "e1", "name": "E", "price": "$49", "category": "utilities",
             "status": "live", "checkout_status": "active"}
        ])
        assert results[0]["est_monthly_units"] == 3

    def test_category_multiplier_applied(self):
        base = {"slug": "x", "name": "X", "status": "live", "checkout_status": "active"}
        r_dev = estimate_monthly_revenue([{**base, "price": "$10", "category": "developer-tools"}])
        r_util = estimate_monthly_revenue([{**base, "price": "$10", "category": "utilities"}])
        assert r_dev[0]["multiplier"] == 1.2
        assert r_util[0]["multiplier"] == 0.8
        assert r_dev[0]["est_monthly_revenue"] > r_util[0]["est_monthly_revenue"]

    def test_ai_tools_highest_multiplier(self):
        results = estimate_monthly_revenue([
            {"slug": "ai1", "name": "AI", "price": "$10", "category": "ai-tools",
             "status": "live", "checkout_status": "active"}
        ])
        assert results[0]["multiplier"] == 1.5

    def test_checkout_active_flag(self):
        results = estimate_monthly_revenue(SAMPLE_PRODUCTS)
        active = [r for r in results if r["checkout_active"]]
        inactive = [r for r in results if not r["checkout_active"]]
        assert len(active) == 5
        assert len(inactive) == 2

    def test_free_product_revenue_is_zero(self):
        results = estimate_monthly_revenue([
            {"slug": "free1", "name": "Free", "price": 0, "category": "utilities",
             "status": "live", "checkout_status": "inactive"}
        ])
        assert results[0]["est_monthly_revenue"] == 0.0


class TestAuditPrices:
    def test_audit_output(self, capsys):
        audit_prices(SAMPLE_PRODUCTS)
        out = capsys.readouterr().out
        assert "Portfolio Price Audit" in out
        assert "Total products: 7" in out
        assert "Tier Distribution" in out

    def test_audit_returns_results(self):
        results = audit_prices(SAMPLE_PRODUCTS)
        assert len(results) == 7
        assert all("tier" in r for r in results)


class TestGenerateReport:
    def test_report_output(self, capsys, tmp_path):
        with patch("scripts.portfolio_revenue_estimator.ANALYSIS_DIR", tmp_path):
            report = generate_report(SAMPLE_PRODUCTS)
        out = capsys.readouterr().out
        assert "Revenue Estimate Report" in out
        assert "Monthly estimate:" in out
        assert "Annual estimate:" in out
        assert "Top 10 Revenue Potential" in out

    def test_report_structure(self, tmp_path):
        with patch("scripts.portfolio_revenue_estimator.ANALYSIS_DIR", tmp_path):
            report = generate_report(SAMPLE_PRODUCTS)
        assert "summary" in report
        assert "top_earners" in report
        assert "category_breakdown" in report
        assert report["summary"]["total_products"] == 7

    def test_report_saves_json(self, tmp_path):
        with patch("scripts.portfolio_revenue_estimator.ANALYSIS_DIR", tmp_path):
            generate_report(SAMPLE_PRODUCTS)
        report_file = tmp_path / "revenue_estimate.json"
        assert report_file.exists()
        data = json.loads(report_file.read_text())
        assert "summary" in data

    def test_annual_is_12x_monthly(self, tmp_path):
        with patch("scripts.portfolio_revenue_estimator.ANALYSIS_DIR", tmp_path):
            report = generate_report(SAMPLE_PRODUCTS)
        monthly = report["summary"]["estimated_monthly_revenue"]
        annual = report["summary"]["estimated_annual_revenue"]
        assert abs(annual - monthly * 12) < 0.01


class TestSuggestOptimizations:
    def test_missing_price_suggestion(self, capsys):
        products = [
            {"slug": "no-price", "name": "No Price", "price": 0, "category": "utilities",
             "status": "live", "checkout_status": "inactive"}
        ]
        suggestions = suggest_optimizations(products)
        assert len(suggestions) == 1
        assert suggestions[0]["type"] == "missing_price"

    def test_underpriced_high_value_category(self):
        products = [
            {"slug": "cheap-dev", "name": "Cheap Dev", "price": "$5", "category": "developer-tools",
             "status": "live", "checkout_status": "active"}
        ]
        suggestions = suggest_optimizations(products)
        assert any(s["type"] == "underpriced" for s in suggestions)

    def test_overpriced_utility(self):
        products = [
            {"slug": "expensive-util", "name": "Expensive Util", "price": "$25",
             "category": "utilities", "status": "live", "checkout_status": "active"}
        ]
        suggestions = suggest_optimizations(products)
        assert any(s["type"] == "overpriced" for s in suggestions)

    def test_no_suggestions_for_well_priced(self):
        products = [
            {"slug": "good-price", "name": "Good", "price": "$15",
             "category": "utilities", "status": "live", "checkout_status": "active"}
        ]
        suggestions = suggest_optimizations(products)
        assert len(suggestions) == 0

    def test_output_format(self, capsys):
        suggest_optimizations(SAMPLE_PRODUCTS)
        out = capsys.readouterr().out
        assert "Price Optimization Suggestions" in out


class TestLoadProducts:
    def test_loads_from_state(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps({
            "products": {"active": SAMPLE_PRODUCTS}
        }))
        with patch("scripts.portfolio_revenue_estimator.STATE_FILE", state_file):
            prods = load_products()
        assert len(prods) == 7

    def test_returns_empty_on_missing_file(self, capsys):
        with patch("scripts.portfolio_revenue_estimator.STATE_FILE", Path("/nonexistent")):
            prods = load_products()
        assert prods == []


class TestPriceTiers:
    def test_tier_ranges_valid(self):
        assert PRICE_TIERS["budget"] == (0, 9)
        assert PRICE_TIERS["standard"] == (9, 19)
        assert PRICE_TIERS["premium"] == (19, 29)
        assert PRICE_TIERS["enterprise"][0] == 29

    def test_all_categories_have_multipliers(self):
        expected = {"developer-tools", "security", "devops", "api-services", "utilities", "design-tools", "ai-tools"}
        assert set(CATEGORY_REVENUE_MULTIPLIERS.keys()) == expected
