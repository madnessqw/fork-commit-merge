#!/usr/bin/env python3
"""Track revenue readiness across the portfolio.

Analyzes checkout coverage, pricing gaps, and revenue potential.
Produces a JSON report suitable for cycle boots and Telegram summaries.

Usage:
    python3 scripts/portfolio_revenue_tracker.py
    python3 scripts/portfolio_revenue_tracker.py --markdown
    python3 scripts/portfolio_revenue_tracker.py --telegram
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _load_products() -> list[dict]:
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return state.get("products", {}).get("active", [])


def _load_summary() -> dict:
    try:
        return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def analyze(products: list[dict] | None = None) -> dict[str, Any]:
    if products is None:
        products = _load_products()

    total = len(products)
    live = [p for p in products if p.get("status") == "live"]
    live_count = len(live)

    has_checkout = []
    no_checkout = []
    has_price = []
    no_price = []
    price_distribution: list[float] = []

    for p in live:
        co = p.get("checkout_url", "")
        if co and co.startswith("http"):
            has_checkout.append(p)
        else:
            no_checkout.append(p)

        price_str = str(p.get("price", "")).strip()
        price_val = 0.0
        try:
            price_val = float(price_str.replace("$", "").replace("€", "").strip())
        except (ValueError, AttributeError):
            pass

        if price_val > 0:
            has_price.append(p)
            price_distribution.append(price_val)
        else:
            no_price.append(p)

    checkout_coverage = round(len(has_checkout) / live_count * 100, 1) if live_count else 0.0
    price_coverage = round(len(has_price) / live_count * 100, 1) if live_count else 0.0

    avg_price = round(sum(price_distribution) / len(price_distribution), 2) if price_distribution else 0.0
    min_price = round(min(price_distribution), 2) if price_distribution else 0.0
    max_price = round(max(price_distribution), 2) if price_distribution else 0.0

    price_buckets = Counter()
    for p in price_distribution:
        if p <= 0:
            price_buckets["free"] += 1
        elif p <= 5:
            price_buckets["$1-5"] += 1
        elif p <= 10:
            price_buckets["$6-10"] += 1
        elif p <= 20:
            price_buckets["$11-20"] += 1
        else:
            price_buckets["$20+"] += 1

    revenue_potential_low = round(sum(price_distribution) * 1, 2)
    revenue_potential_mid = round(sum(price_distribution) * 10, 2)
    revenue_potential_high = round(sum(price_distribution) * 50, 2)

    no_checkout_slugs = sorted(p.get("slug", "") for p in no_checkout[:20])
    no_price_slugs = sorted(p.get("slug", "") for p in no_price[:20])

    return {
        "ts": _utc_now_iso(),
        "total_products": total,
        "live_count": live_count,
        "has_checkout": len(has_checkout),
        "no_checkout": len(no_checkout),
        "checkout_coverage_pct": checkout_coverage,
        "has_price": len(has_price),
        "no_price": len(no_price),
        "price_coverage_pct": price_coverage,
        "price_stats": {
            "avg": avg_price,
            "min": min_price,
            "max": max_price,
            "buckets": dict(sorted(price_buckets.items())),
        },
        "revenue_potential": {
            "1_sale_per_product": revenue_potential_low,
            "10_sales_per_product": revenue_potential_mid,
            "50_sales_per_product": revenue_potential_high,
            "total_catalog_value": round(sum(price_distribution), 2),
        },
        "no_checkout_sample": no_checkout_slugs,
        "no_price_sample": no_price_slugs,
    }


def to_markdown(report: dict) -> str:
    lines = [
        f"# Revenue Tracker Report",
        f"**Tarih:** {report['ts']} | **Live:** {report['live_count']}",
        "",
        f"## Checkout Coverage",
        f"- Has checkout: {report['has_checkout']} / {report['live_count']} ({report['checkout_coverage_pct']}%)",
        f"- Missing checkout: {report['no_checkout']}",
        "",
        f"## Price Coverage",
        f"- Has price: {report['has_price']} / {report['live_count']} ({report['price_coverage_pct']}%)",
        f"- Missing price: {report['no_price']}",
        f"- Avg price: ${report['price_stats']['avg']}",
        f"- Price range: ${report['price_stats']['min']} - ${report['price_stats']['max']}",
        "",
        f"## Revenue Potential",
        f"- Catalog value: ${report['revenue_potential']['total_catalog_value']}",
        f"- 1 sale/product: ${report['revenue_potential']['1_sale_per_product']}",
        f"- 10 sales/product: ${report['revenue_potential']['10_sales_per_product']}",
        f"- 50 sales/product: ${report['revenue_potential']['50_sales_per_product']}",
        "",
        f"## Price Distribution",
    ]
    for bucket, count in report["price_stats"]["buckets"].items():
        lines.append(f"- {bucket}: {count} products")
    if report["no_checkout_sample"]:
        lines.append("")
        lines.append("## Missing Checkout (sample)")
        for slug in report["no_checkout_sample"][:10]:
            lines.append(f"- {slug}")
    return "\n".join(lines)


def telegram_summary(report: dict) -> str:
    rev = report["revenue_potential"]
    ps = report["price_stats"]
    return (
        f"💰 <b>Revenue Tracker</b>\n"
        f"📦 {report['live_count']} live | {report['checkout_coverage_pct']:.0f}% checkout\n"
        f"💵 Avg: ${ps['avg']} | Range: ${ps['min']}-${ps['max']}\n"
        f"📊 Potential: ${rev['1_sale_per_product']} (1x) / ${rev['10_sales_per_product']} (10x)"
    )


def main() -> int:
    report = analyze()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--markdown":
            print(to_markdown(report))
            return 0
        if cmd == "--telegram":
            print(telegram_summary(report))
            return 0
        if cmd == "--json":
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
