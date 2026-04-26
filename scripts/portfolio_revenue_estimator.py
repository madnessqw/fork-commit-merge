#!/usr/bin/env python3
"""Portfolio revenue estimator for UniverseCreator product portfolio.

Analyzes product pricing, estimates revenue potential, and provides
pricing strategy recommendations based on category and feature analysis.

Usage:
    python3 scripts/portfolio_revenue_estimator.py audit        # Show pricing analysis
    python3 scripts/portfolio_revenue_estimator.py report        # Full revenue estimate report
    python3 scripts/portfolio_revenue_estimator.py optimize      # Suggest price optimizations
"""

import json
import os
import sys
import argparse
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / "STATE.json"
ANALYSIS_DIR = REPO_ROOT / "analysis"

PRICE_TIERS = {
    "budget": (0, 9),
    "standard": (9, 19),
    "premium": (19, 29),
    "enterprise": (29, float("inf")),
}

CATEGORY_REVENUE_MULTIPLIERS = {
    "developer-tools": 1.2,
    "security": 1.3,
    "devops": 1.4,
    "api-services": 1.1,
    "utilities": 0.8,
    "design-tools": 0.9,
    "ai-tools": 1.5,
}


def load_products():
    if not STATE_FILE.exists():
        print(f"STATE.json not found: {STATE_FILE}")
        return []
    with open(STATE_FILE) as f:
        state = json.load(f)
    return state.get("products", {}).get("active", [])


def parse_price(price_val):
    if isinstance(price_val, (int, float)):
        return float(price_val)
    if isinstance(price_val, str):
        cleaned = price_val.replace("$", "").replace("€", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0


def classify_tier(price):
    for tier, (low, high) in PRICE_TIERS.items():
        if low <= price < high:
            return tier
    return "unknown"


def estimate_monthly_revenue(products):
    results = []
    for p in products:
        price = parse_price(p.get("price", 0))
        tier = classify_tier(price)
        category = p.get("category", "uncategorized")
        multiplier = CATEGORY_REVENUE_MULTIPLIERS.get(category, 1.0)

        estimated_monthly_units = {
            "budget": 30,
            "standard": 15,
            "premium": 8,
            "enterprise": 3,
        }.get(tier, 10)

        estimated_monthly_revenue = price * estimated_monthly_units * multiplier
        results.append({
            "slug": p.get("slug", p.get("s", "unknown")),
            "name": p.get("name", p.get("n", "unknown")),
            "price": price,
            "tier": tier,
            "category": category,
            "multiplier": multiplier,
            "est_monthly_units": estimated_monthly_units,
            "est_monthly_revenue": round(estimated_monthly_revenue, 2),
            "status": p.get("status", p.get("st", "unknown")),
            "checkout_active": p.get("checkout_status", "") == "active",
        })
    return results


def audit_prices(products):
    results = estimate_monthly_revenue(products)
    prices = [r["price"] for r in results if r["price"] > 0]
    no_price = [r for r in results if r["price"] <= 0]

    tier_dist = Counter(r["tier"] for r in results)
    category_dist = Counter(r["category"] for r in results)

    print(f"=== Portfolio Price Audit ===")
    print(f"Total products: {len(results)}")
    print(f"With price: {len(prices)} | No price: {len(no_price)}")
    print()

    if prices:
        print(f"Price range: ${min(prices):.0f} - ${max(prices):.0f}")
        print(f"Average: ${sum(prices)/len(prices):.1f}")
        print(f"Median: ${sorted(prices)[len(prices)//2]:.0f}")
    print()

    print("Tier Distribution:")
    for tier in ["budget", "standard", "premium", "enterprise"]:
        count = tier_dist.get(tier, 0)
        pct = count / len(results) * 100 if results else 0
        bar = "#" * int(pct / 2)
        print(f"  {tier:12s}: {count:3d} ({pct:5.1f}%) {bar}")
    print()

    if no_price:
        print(f"Products without price ({len(no_price)}):")
        for r in no_price[:10]:
            print(f"  - {r['slug']}")
        if len(no_price) > 10:
            print(f"  ... and {len(no_price) - 10} more")

    return results


def generate_report(products):
    results = estimate_monthly_revenue(products)
    total_monthly = sum(r["est_monthly_revenue"] for r in results)
    total_annual = total_monthly * 12

    checkout_active = sum(1 for r in results if r["checkout_active"])
    checkout_inactive = sum(1 for r in results if not r["checkout_active"])

    top_earners = sorted(results, key=lambda x: x["est_monthly_revenue"], reverse=True)[:10]

    by_category = defaultdict(list)
    for r in results:
        by_category[r["category"]].append(r)

    category_revenue = {}
    for cat, items in by_category.items():
        cat_rev = sum(i["est_monthly_revenue"] for i in items)
        category_revenue[cat] = {
            "count": len(items),
            "monthly_revenue": round(cat_rev, 2),
            "avg_price": round(sum(i["price"] for i in items) / len(items), 2) if items else 0,
        }

    report = {
        "summary": {
            "total_products": len(results),
            "checkout_active": checkout_active,
            "checkout_inactive": checkout_inactive,
            "estimated_monthly_revenue": round(total_monthly, 2),
            "estimated_annual_revenue": round(total_annual, 2),
        },
        "top_earners": top_earners,
        "category_breakdown": dict(sorted(category_revenue.items(), key=lambda x: x[1]["monthly_revenue"], reverse=True)),
    }

    print(f"=== Revenue Estimate Report ===")
    print(f"Monthly estimate: ${total_monthly:,.2f}")
    print(f"Annual estimate:  ${total_annual:,.2f}")
    print(f"Checkout active:  {checkout_active}/{len(results)}")
    print()
    print("Top 10 Revenue Potential:")
    for i, r in enumerate(top_earners, 1):
        print(f"  {i:2d}. {r['name']:30s} ${r['price']:5.0f} → ${r['est_monthly_revenue']:8.2f}/mo")
    print()
    print("Category Revenue:")
    for cat, data in sorted(category_revenue.items(), key=lambda x: x[1]["monthly_revenue"], reverse=True):
        print(f"  {cat:20s}: {data['count']:3d} products, ${data['monthly_revenue']:8.2f}/mo, avg ${data['avg_price']:5.1f}")

    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    report_path = ANALYSIS_DIR / "revenue_estimate.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved: {report_path}")

    return report


def suggest_optimizations(products):
    results = estimate_monthly_revenue(products)
    suggestions = []

    for r in results:
        if r["price"] <= 0:
            suggestions.append({
                "slug": r["slug"],
                "type": "missing_price",
                "suggestion": f"Set a price for {r['name']}",
                "impact": "Enables checkout",
            })
        elif r["tier"] == "budget" and r["category"] in ("developer-tools", "security", "devops"):
            suggestions.append({
                "slug": r["slug"],
                "type": "underpriced",
                "suggestion": f"Consider raising ${r['price']:.0f} to $19 (high-value category)",
                "impact": f"+${(19 - r['price']) * r['est_monthly_units'] * r['multiplier']:.0f}/mo potential",
            })
        elif r["tier"] == "premium" and r["category"] in ("utilities",):
            suggestions.append({
                "slug": r["slug"],
                "type": "overpriced",
                "suggestion": f"Consider lowering ${r['price']:.0f} to $19 (utility category)",
                "impact": "Higher conversion expected",
            })

    print(f"=== Price Optimization Suggestions ({len(suggestions)}) ===")
    for s in suggestions[:20]:
        print(f"  [{s['type']:12s}] {s['slug']:30s} → {s['suggestion']}")
        print(f"                  Impact: {s['impact']}")
    if len(suggestions) > 20:
        print(f"  ... and {len(suggestions) - 20} more")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Portfolio revenue estimator")
    parser.add_argument("command", choices=["audit", "report", "optimize"],
                        help="audit=price analysis, report=revenue estimate, optimize=suggestions")
    args = parser.parse_args()

    products = load_products()
    if not products:
        print("No products found")
        sys.exit(1)

    if args.command == "audit":
        audit_prices(products)
    elif args.command == "report":
        generate_report(products)
    elif args.command == "optimize":
        suggest_optimizations(products)


if __name__ == "__main__":
    main()
