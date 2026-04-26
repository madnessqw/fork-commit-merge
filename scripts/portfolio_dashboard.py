#!/usr/bin/env python3
"""Portfolio Dashboard Generator — UniverseCreator portfoy ozet araci."""

import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = ROOT / "products"
STATE_SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
STATE_PATH = ROOT / "STATE.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_products():
    products = []
    if not PRODUCTS_DIR.exists():
        return products
    for d in PRODUCTS_DIR.iterdir():
        if not d.is_dir():
            continue
        pj = d / "product.json"
        if pj.exists():
            try:
                data = json.loads(pj.read_text())
                data["_dir"] = d.name
                products.append(data)
            except json.JSONDecodeError:
                pass
    return products


def category_breakdown(products):
    return Counter(p.get("category", "uncategorized") for p in products)


def status_breakdown(products):
    return Counter(p.get("status", "unknown") for p in products)


def checkout_coverage(products):
    total = len(products)
    with_checkout = sum(1 for p in products if (p.get("checkout_url") or "").startswith("http"))
    return {"total": total, "with_checkout": with_checkout, "without": total - with_checkout,
            "percentage": round(with_checkout / total * 100, 1) if total else 0}


def tag_analysis(products):
    tag_counter = Counter()
    for p in products:
        for t in p.get("tags", []):
            tag_counter[t.lower()] += 1
    return tag_counter.most_common(20)


def url_health(products):
    missing_vercel = [p["_dir"] for p in products if not (p.get("vercel_url") or "").startswith("http")]
    missing_checkout = [p["_dir"] for p in products if not (p.get("checkout_url") or "").startswith("http")]
    return {"missing_vercel_url": len(missing_vercel), "missing_checkout_url": len(missing_checkout),
            "missing_vercel_list": missing_vercel[:10], "missing_checkout_list": missing_checkout[:10]}


def stale_products(products, max_age_days=30):
    now = datetime.now().timestamp()
    stale = []
    for p in products:
        d = PRODUCTS_DIR / p["_dir"]
        try:
            spec = d / "spec.json"
            if spec.exists():
                mtime = spec.stat().st_mtime
                age_days = (now - mtime) / 86400
                if age_days > max_age_days:
                    stale.append({"slug": p["_dir"], "age_days": round(age_days)})
        except OSError:
            pass
    return stale


def generate_dashboard(include_details=False):
    products = load_products()
    summary = load_json(STATE_SUMMARY_PATH)
    state = load_json(STATE_PATH)

    dashboard = {
        "generated_at": datetime.now().isoformat(),
        "total_products": len(products),
        "status": status_breakdown(products),
        "categories": dict(category_breakdown(products)),
        "checkout": checkout_coverage(products),
        "top_tags": tag_analysis(products),
        "url_health": url_health(products),
    }

    if summary:
        dashboard["state_summary_cycle"] = summary.get("cycle")
        dashboard["state_summary_healthy"] = f"{summary.get('healthy_count', '?')}/{summary.get('live_count', '?')}"
        dashboard["state_summary_deploy_gap"] = summary.get("deploy_missing_or_bad_url", 0)

    if include_details:
        dashboard["stale_products"] = stale_products(products)

    return dashboard


def format_dashboard(dashboard):
    lines = [
        f"# Portfolio Dashboard — {dashboard['generated_at'][:16]}",
        f"",
        f"## Overview",
        f"- Total products: {dashboard['total_products']}",
        f"- Status: {dict(dashboard['status'])}",
        f"- Checkout: {dashboard['checkout']['with_checkout']}/{dashboard['checkout']['total']} ({dashboard['checkout']['percentage']}%)",
        f"",
        f"## Categories",
    ]
    for cat, count in sorted(dashboard["categories"].items(), key=lambda x: -x[1]):
        lines.append(f"- {cat}: {count}")

    lines.append("")
    lines.append("## Top Tags")
    for tag, count in dashboard["top_tags"][:10]:
        lines.append(f"- {tag}: {count}")

    uh = dashboard["url_health"]
    lines.append("")
    lines.append("## URL Health")
    lines.append(f"- Missing Vercel URL: {uh['missing_vercel_url']}")
    lines.append(f"- Missing Checkout URL: {uh['missing_checkout_url']}")

    if "state_summary_cycle" in dashboard:
        lines.append("")
        lines.append("## State Summary")
        lines.append(f"- Cycle: {dashboard['state_summary_cycle']}")
        lines.append(f"- Healthy: {dashboard['state_summary_healthy']}")
        lines.append(f"- Deploy gap: {dashboard['state_summary_deploy_gap']}")

    if dashboard.get("stale_products"):
        lines.append("")
        lines.append(f"## Stale Products (>30 days)")
        for sp in dashboard["stale_products"][:10]:
            lines.append(f"- {sp['slug']}: {sp['age_days']}d")

    return "\n".join(lines)


def main():
    include_details = "--details" in sys.argv
    output_format = "json"
    if "--markdown" in sys.argv or "--md" in sys.argv:
        output_format = "markdown"

    dashboard = generate_dashboard(include_details=include_details)

    if output_format == "markdown":
        print(format_dashboard(dashboard))
    else:
        print(json.dumps(dashboard, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
