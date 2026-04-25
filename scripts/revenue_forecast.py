#!/usr/bin/env python3
"""Revenue forecast calculator for UniverseCreator portfolio.

Estimates potential revenue based on product prices, health status,
checkout coverage, and configurable conversion assumptions.

Usage:
    python3 scripts/revenue_forecast.py
    python3 scripts/revenue_forecast.py --json
    python3 scripts/revenue_forecast.py --conversion 0.02
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

DEFAULT_CONVERSION = 0.01
DEFAULT_MONTHLY_VISITORS = 100


def _parse_price(raw) -> int | None:
    if raw is None:
        return None
    s = str(raw).strip().lstrip("$")
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def load_portfolio(state_path: Path = STATE_PATH) -> list[dict[str, Any]]:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data.get("products", {}).get("active", [])


def compute_forecast(
    products: list[dict[str, Any]],
    *,
    conversion: float = DEFAULT_CONVERSION,
    monthly_visitors: int = DEFAULT_MONTHLY_VISITORS,
) -> dict[str, Any]:
    total_products = len(products)
    live = [p for p in products if p.get("status") == "live"]
    live_with_price = []
    for p in live:
        price = _parse_price(p.get("price"))
        if price is not None and price > 0:
            p_copy = {**p, "_parsed_price": price}
            live_with_price.append(p_copy)

    checkout_ready = [
        p for p in live_with_price
        if p.get("checkout_url", "").startswith("http")
    ]

    healthy = [p for p in live_with_price if p.get("health") == "healthy"]

    sellable = [
        p for p in checkout_ready
        if p.get("health") == "healthy" and p.get("checkout_url", "").startswith("http")
    ]

    prices = [p["_parsed_price"] for p in live_with_price]
    sellable_prices = [p["_parsed_price"] for p in sellable]

    max_revenue = sum(prices) if prices else 0
    sellable_revenue = sum(sellable_prices) if sellable_prices else 0

    avg_price = sum(prices) / len(prices) if prices else 0
    avg_sellable = sum(sellable_prices) / len(sellable_prices) if sellable_prices else 0

    estimated_monthly = round(sellable_revenue * conversion, 2)
    estimated_annual = round(estimated_monthly * 12, 2)

    from collections import Counter

    price_tiers: dict[str, int] = {"budget": 0, "mid": 0, "premium": 0}
    tier_revenue: dict[str, int] = {"budget": 0, "mid": 0, "premium": 0}
    for p in live_with_price:
        price = p["_parsed_price"]
        if price <= 9:
            tier = "budget"
        elif price <= 19:
            tier = "mid"
        else:
            tier = "premium"
        price_tiers[tier] += 1
        tier_revenue[tier] += price

    return {
        "total_products": total_products,
        "live_count": len(live),
        "live_with_price": len(live_with_price),
        "checkout_ready": len(checkout_ready),
        "healthy_count": len(healthy),
        "sellable_count": len(sellable),
        "max_revenue": max_revenue,
        "sellable_revenue": sellable_revenue,
        "avg_price": round(avg_price, 2),
        "avg_sellable_price": round(avg_sellable, 2),
        "conversion_rate": conversion,
        "estimated_monthly": estimated_monthly,
        "estimated_annual": estimated_annual,
        "price_tiers": price_tiers,
        "tier_revenue": tier_revenue,
        "median_price": sorted(prices)[len(prices) // 2] if prices else 0,
    }


def format_forecast_markdown(fc: dict[str, Any]) -> str:
    lines = [
        "# Revenue Forecast",
        "",
        f"**Total products:** {fc['total_products']}",
        f"**Live with price:** {fc['live_with_price']}",
        f"**Checkout ready:** {fc['checkout_ready']}",
        f"**Sellable (healthy + checkout):** {fc['sellable_count']}",
        "",
        "## Revenue Potential",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Max (1 sale each) | ${fc['max_revenue']:,} |",
        f"| Sellable subset | ${fc['sellable_revenue']:,} |",
        f"| Avg price | ${fc['avg_price']:.2f} |",
        f"| Median price | ${fc['median_price']} |",
        "",
        "## Price Tiers",
        f"| Tier | Products | Revenue |",
        f"|------|----------|---------|",
    ]
    for tier in ("budget", "mid", "premium"):
        lines.append(
            f"| {tier.capitalize()} | {fc['price_tiers'][tier]} | "
            f"${fc['tier_revenue'][tier]:,} |"
        )
    lines.extend([
        "",
        "## Estimate",
        f"**Conversion:** {fc['conversion_rate']:.1%}",
        f"**Monthly:** ${fc['estimated_monthly']:,.2f}",
        f"**Annual:** ${fc['estimated_annual']:,.2f}",
    ])
    return "\n".join(lines)


def format_forecast_telegram(fc: dict[str, Any]) -> str:
    return (
        f"💰 Revenue Forecast\n"
        f"📦 {fc['sellable_count']}/{fc['live_with_price']} sellable\n"
        f"💵 Max: ${fc['max_revenue']:,} | Sellable: ${fc['sellable_revenue']:,}\n"
        f"📊 Est: ${fc['estimated_monthly']:,.0f}/mo @ {fc['conversion_rate']:.0%}"
    )


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Revenue forecast calculator")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--telegram", action="store_true", help="Telegram format")
    parser.add_argument(
        "--conversion",
        type=float,
        default=DEFAULT_CONVERSION,
        help=f"Conversion rate (default: {DEFAULT_CONVERSION})",
    )
    args = parser.parse_args()

    products = load_portfolio()
    fc = compute_forecast(products, conversion=args.conversion)

    if args.json:
        print(json.dumps(fc, indent=2, ensure_ascii=False))
    elif args.telegram:
        print(format_forecast_telegram(fc))
    else:
        print(format_forecast_markdown(fc))

    return fc


if __name__ == "__main__":
    main()
