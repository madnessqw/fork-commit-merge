#!/usr/bin/env python3
"""Checkout sales readiness auditor for UniverseCreator product portfolio.

Analyzes product.json files to determine sales readiness based on:
- Checkout URL presence and format validity
- Product name/description quality for conversion
- Price setting and consistency
- SEO meta quality (title, description, OG tags)

Usage:
    python3 scripts/checkout_sales_readiness.py audit       # Full readiness audit
    python3 scripts/checkout_sales_readiness.py summary     # Quick summary
    python3 scripts/checkout_sales_readiness.py fix-dry-run # Preview fixes
"""

import json
import os
import sys
import argparse
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = REPO_ROOT / "products"
STATE_FILE = REPO_ROOT / "STATE.json"

READINESS_WEIGHTS = {
    "has_checkout_url": 25,
    "has_name": 10,
    "has_description": 15,
    "has_price": 15,
    "has_og_image": 10,
    "has_meta_title": 10,
    "has_meta_description": 15,
}

NAME_MIN_LENGTH = 5
DESC_MIN_LENGTH = 20
TITLE_MIN_LENGTH = 10
META_DESC_MIN_LENGTH = 30


def load_product_json(slug):
    pdir = PRODUCTS_DIR / slug
    if not pdir.is_dir():
        return None
    pj = pdir / "product.json"
    if not pj.exists():
        return None
    try:
        return json.loads(pj.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def check_checkout_url(data):
    url = data.get("checkout_url") or data.get("polar_checkout_url") or ""
    if not url:
        return False, "missing"
    if not url.startswith("https://"):
        return False, "invalid_scheme"
    if "polar.sh" not in url and "checkout" not in url.lower():
        return False, "non_polar"
    return True, "ok"


def check_name(data):
    name = data.get("name", "")
    if not name or len(name.strip()) < NAME_MIN_LENGTH:
        return False, "too_short"
    return True, "ok"


def check_description(data):
    desc = data.get("description", "") or data.get("short_description", "")
    if not desc or len(desc.strip()) < DESC_MIN_LENGTH:
        return False, "too_short"
    return True, "ok"


def check_price(data):
    price = data.get("price")
    if price is None:
        return False, "missing"
    try:
        p = float(str(price).replace("$", "").replace("€", "").strip())
        if p <= 0:
            return False, "zero"
        return True, "ok"
    except (ValueError, TypeError):
        return False, "invalid"


def check_og_image(data):
    og = data.get("og_image", "") or data.get("image", "")
    if not og or not og.startswith("http"):
        return False, "missing"
    return True, "ok"


def check_meta_title(data):
    title = data.get("meta_title", "") or data.get("title", "")
    if not title or len(title.strip()) < TITLE_MIN_LENGTH:
        return False, "too_short"
    return True, "ok"


def check_meta_description(data):
    desc = data.get("meta_description", "")
    if not desc or len(desc.strip()) < META_DESC_MIN_LENGTH:
        return False, "too_short"
    return True, "ok"


def score_product(data):
    checks = {
        "has_checkout_url": check_checkout_url(data),
        "has_name": check_name(data),
        "has_description": check_description(data),
        "has_price": check_price(data),
        "has_og_image": check_og_image(data),
        "has_meta_title": check_meta_title(data),
        "has_meta_description": check_meta_description(data),
    }
    score = 0
    issues = []
    for key, (passed, detail) in checks.items():
        weight = READINESS_WEIGHTS.get(key, 0)
        if passed:
            score += weight
        else:
            issues.append(f"{key}={detail}")
    return score, issues


def get_all_slugs():
    if not PRODUCTS_DIR.exists():
        return []
    return sorted(
        d.name for d in PRODUCTS_DIR.iterdir()
        if d.is_dir() and (d / "product.json").exists()
    )


def audit():
    slugs = get_all_slugs()
    if not slugs:
        print("No products found")
        return []

    results = []
    for slug in slugs:
        data = load_product_json(slug)
        if data is None:
            results.append({"slug": slug, "score": 0, "issues": ["no_product_json"]})
            continue
        score, issues = score_product(data)
        results.append({"slug": slug, "score": score, "issues": issues})

    results.sort(key=lambda x: x["score"])

    score_dist = Counter(r["score"] for r in results)
    ready = sum(1 for r in results if r["score"] >= 80)
    partial = sum(1 for r in results if 40 <= r["score"] < 80)
    not_ready = sum(1 for r in results if r["score"] < 40)

    print("=== Checkout Sales Readiness Audit ===")
    print(f"Total products: {len(results)}")
    print(f"Ready (80+): {ready} | Partial (40-79): {partial} | Not Ready (<40): {not_ready}")
    print()

    issue_counter = Counter()
    for r in results:
        for iss in r["issues"]:
            issue_counter[iss.split("=")[0]] += 1

    print("Common Issues:")
    for issue, count in issue_counter.most_common(10):
        print(f"  {issue:30s}: {count:3d}")
    print()

    not_ready_prods = [r for r in results if r["score"] < 80]
    if not_ready_prods:
        print(f"Products below 80 readiness ({len(not_ready_prods)}):")
        for r in not_ready_prods[:20]:
            print(f"  {r['slug']:40s} score={r['score']:3d} issues={', '.join(r['issues'][:3])}")
        if len(not_ready_prods) > 20:
            print(f"  ... and {len(not_ready_prods) - 20} more")

    return results


def summary():
    slugs = get_all_slugs()
    if not slugs:
        print("No products found")
        return

    scores = []
    for slug in slugs:
        data = load_product_json(slug)
        if data is None:
            scores.append(0)
            continue
        s, _ = score_product(data)
        scores.append(s)

    avg = sum(scores) / len(scores) if scores else 0
    ready = sum(1 for s in scores if s >= 80)
    print(f"=== Sales Readiness Summary ===")
    print(f"Products: {len(scores)}")
    print(f"Average readiness: {avg:.1f}/100")
    print(f"Ready (80+): {ready}/{len(scores)} ({ready/len(scores)*100:.1f}%)")
    print(f"Not ready (<80): {len(scores) - ready}/{len(scores)}")


def fix_dry_run():
    slugs = get_all_slugs()
    fixes = []
    for slug in slugs:
        data = load_product_json(slug)
        if data is None:
            continue
        suggestions = []

        name_ok, name_detail = check_name(data)
        if not name_ok:
            suggestions.append(f"name: needs {NAME_MIN_LENGTH}+ chars")

        desc_ok, desc_detail = check_description(data)
        if not desc_ok:
            suggestions.append(f"description: needs {DESC_MIN_LENGTH}+ chars")

        price_ok, price_detail = check_price(data)
        if not price_ok:
            suggestions.append(f"price: {price_detail}")

        og_ok, og_detail = check_og_image(data)
        if not og_ok:
            suggestions.append("og_image: missing")

        meta_ok, meta_detail = check_meta_title(data)
        if not meta_ok:
            suggestions.append(f"meta_title: needs {TITLE_MIN_LENGTH}+ chars")

        mdesc_ok, mdesc_detail = check_meta_description(data)
        if not mdesc_ok:
            suggestions.append(f"meta_description: needs {META_DESC_MIN_LENGTH}+ chars")

        if suggestions:
            fixes.append({"slug": slug, "suggestions": suggestions})

    print(f"=== Fix Dry Run ({len(fixes)} products need attention) ===")
    for f in fixes[:30]:
        print(f"  {f['slug']:40s} → {'; '.join(f['suggestions'])}")
    if len(fixes) > 30:
        print(f"  ... and {len(fixes) - 30} more")

    return fixes


def main():
    parser = argparse.ArgumentParser(description="Checkout sales readiness auditor")
    parser.add_argument("command", choices=["audit", "summary", "fix-dry-run"],
                        help="audit=full report, summary=quick stats, fix-dry-run=preview fixes")
    args = parser.parse_args()

    if args.command == "audit":
        audit()
    elif args.command == "summary":
        summary()
    elif args.command == "fix-dry-run":
        fix_dry_run()


if __name__ == "__main__":
    main()
