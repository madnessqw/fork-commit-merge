"""Tests for scripts.revenue_forecast"""

import json
from pathlib import Path

from scripts.revenue_forecast import (
    _parse_price,
    compute_forecast,
    format_forecast_markdown,
    format_forecast_telegram,
    load_portfolio,
)


def _make_products():
    return [
        {"slug": "tool-a", "status": "live", "price": "$19", "health": "healthy",
         "checkout_url": "https://checkout.polar.sh/a"},
        {"slug": "tool-b", "status": "live", "price": 9, "health": "healthy",
         "checkout_url": "https://checkout.polar.sh/b"},
        {"slug": "tool-c", "status": "live", "price": 29, "health": "unhealthy",
         "checkout_url": "https://checkout.polar.sh/c"},
        {"slug": "tool-d", "status": "live", "price": "$14", "health": "healthy",
         "checkout_url": ""},
        {"slug": "tool-e", "status": "live", "price": 0, "health": "healthy",
         "checkout_url": "https://checkout.polar.sh/e"},
        {"slug": "tool-f", "status": "pending", "price": 49, "health": "healthy",
         "checkout_url": "https://checkout.polar.sh/f"},
        {"slug": "tool-g", "status": "live", "price": None, "health": "healthy",
         "checkout_url": "https://checkout.polar.sh/g"},
    ]


def test_parse_price_none():
    assert _parse_price(None) is None


def test_parse_price_int():
    assert _parse_price(19) == 19


def test_parse_price_string_dollar():
    assert _parse_price("$29") == 29


def test_parse_price_float_string():
    assert _parse_price("14.99") == 14


def test_parse_price_invalid():
    assert _parse_price("free") is None


def test_parse_price_zero():
    assert _parse_price(0) == 0


def test_parse_price_whitespace():
    assert _parse_price("  15  ") == 15


def test_compute_forecast_basic():
    prods = _make_products()
    fc = compute_forecast(prods, conversion=0.01)
    assert fc["total_products"] == 7
    assert fc["live_with_price"] == 4
    assert fc["sellable_count"] == 2
    assert fc["sellable_revenue"] == 19 + 9
    assert fc["checkout_ready"] == 3
    assert fc["healthy_count"] == 3


def test_compute_forecast_max_revenue():
    prods = _make_products()
    fc = compute_forecast(prods)
    assert fc["max_revenue"] == 19 + 9 + 29 + 14


def test_compute_forecast_avg_price():
    prods = _make_products()
    fc = compute_forecast(prods)
    prices = [19, 9, 29, 14]
    assert fc["avg_price"] == sum(prices) / len(prices)


def test_compute_forecast_price_tiers():
    prods = _make_products()
    fc = compute_forecast(prods)
    assert fc["price_tiers"]["budget"] == 1  # $9
    assert fc["price_tiers"]["mid"] == 2     # $14, $19
    assert fc["price_tiers"]["premium"] == 1  # $29


def test_compute_forecast_tier_revenue():
    prods = _make_products()
    fc = compute_forecast(prods)
    assert fc["tier_revenue"]["budget"] == 9
    assert fc["tier_revenue"]["mid"] == 14 + 19
    assert fc["tier_revenue"]["premium"] == 29


def test_compute_forecast_estimates():
    prods = _make_products()
    fc = compute_forecast(prods, conversion=0.05)
    assert fc["conversion_rate"] == 0.05
    assert fc["estimated_monthly"] == round((19 + 9) * 0.05, 2)
    assert fc["estimated_annual"] == round(fc["estimated_monthly"] * 12, 2)


def test_compute_forecast_empty():
    fc = compute_forecast([])
    assert fc["total_products"] == 0
    assert fc["max_revenue"] == 0
    assert fc["sellable_revenue"] == 0
    assert fc["avg_price"] == 0
    assert fc["median_price"] == 0


def test_compute_forecast_no_checkout():
    prods = [
        {"slug": "a", "status": "live", "price": 19, "health": "healthy",
         "checkout_url": ""},
    ]
    fc = compute_forecast(prods)
    assert fc["sellable_count"] == 0
    assert fc["sellable_revenue"] == 0
    assert fc["estimated_monthly"] == 0


def test_compute_forecast_unhealthy_not_sellable():
    prods = [
        {"slug": "a", "status": "live", "price": 19, "health": "unhealthy",
         "checkout_url": "https://checkout.polar.sh/a"},
    ]
    fc = compute_forecast(prods)
    assert fc["sellable_count"] == 0


def test_compute_forecast_median_price():
    prods = [
        {"slug": "a", "status": "live", "price": 10, "health": "healthy", "checkout_url": ""},
        {"slug": "b", "status": "live", "price": 20, "health": "healthy", "checkout_url": ""},
        {"slug": "c", "status": "live", "price": 30, "health": "healthy", "checkout_url": ""},
    ]
    fc = compute_forecast(prods)
    assert fc["median_price"] == 20


def test_compute_forecast_zero_price_excluded():
    prods = [
        {"slug": "free", "status": "live", "price": 0, "health": "healthy",
         "checkout_url": "https://checkout.polar.sh/free"},
    ]
    fc = compute_forecast(prods)
    assert fc["live_with_price"] == 0
    assert fc["sellable_count"] == 0


def test_load_portfolio_missing_file(tmp_path):
    result = load_portfolio(tmp_path / "nope.json")
    assert result == []


def test_load_portfolio_valid(tmp_path):
    state = {"products": {"active": [{"slug": "x", "status": "live"}]}}
    p = tmp_path / "STATE.json"
    p.write_text(json.dumps(state))
    result = load_portfolio(p)
    assert len(result) == 1


def test_load_portfolio_invalid_json(tmp_path):
    p = tmp_path / "STATE.json"
    p.write_text("{bad")
    result = load_portfolio(p)
    assert result == []


def test_format_forecast_markdown():
    fc = compute_forecast(_make_products())
    md = format_forecast_markdown(fc)
    assert "Revenue Forecast" in md
    assert "Sellable" in md
    assert "$" in md
    assert "Price Tiers" in md
    assert "budget" in md.lower() or "Budget" in md


def test_format_forecast_markdown_empty():
    fc = compute_forecast([])
    md = format_forecast_markdown(fc)
    assert "Revenue Forecast" in md


def test_format_forecast_telegram():
    fc = compute_forecast(_make_products())
    text = format_forecast_telegram(fc)
    assert "Revenue Forecast" in text
    assert "sellable" in text.lower() or "sellable" in text
    assert "$" in text


def test_compute_forecast_custom_conversion():
    prods = [
        {"slug": "a", "status": "live", "price": 100, "health": "healthy",
         "checkout_url": "https://co.sh/a"},
    ]
    fc = compute_forecast(prods, conversion=0.1)
    assert fc["estimated_monthly"] == 10.0
    assert fc["estimated_annual"] == 120.0


def test_compute_forecast_all_sellable():
    prods = [
        {"slug": f"p{i}", "status": "live", "price": 19, "health": "healthy",
         "checkout_url": f"https://co.sh/p{i}"}
        for i in range(10)
    ]
    fc = compute_forecast(prods)
    assert fc["sellable_count"] == 10
    assert fc["sellable_revenue"] == 190
    assert fc["max_revenue"] == 190
