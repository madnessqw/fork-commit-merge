#!/usr/bin/env python3
"""Category normalizer for UniverseCreator product portfolio.

Detects inconsistent category names across products and provides
normalization mappings. Reads STATE.json, reports category distribution,
and can write normalized categories back to product.json files.

Usage:
    python3 scripts/category_normalizer.py audit          # Show category issues
    python3 scripts/category_normalizer.py normalize       # Normalize categories in product.json files
    python3 scripts/category_normalizer.py --dry-run normalize  # Preview changes
"""

import json
import os
import sys
import argparse
from collections import Counter
from pathlib import Path

CANONICAL_CATEGORIES = {
    "developer-tools": ["Developer Tools", "developer-tools", "developer_tools", "devtools", "dev-tools"],
    "security": ["security", "security_tools", "security-tools"],
    "devops": ["devops", "devops_tools", "devops-tools"],
    "design-tools": ["design_tools", "design-tools", "creative-tools", "creative_tools"],
    "utilities": ["Utilities", "utilities", "utility", "tools"],
    "api-services": ["API Services", "api-services", "api_services", "api"],
    "ai-tools": ["ai_tools", "ai-tools", "AI Tools", "artificial-intelligence"],
}

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / "STATE.json"
PRODUCTS_DIR = REPO_ROOT / "products"


def build_reverse_map():
    reverse = {}
    for canonical, aliases in CANONICAL_CATEGORIES.items():
        for alias in aliases:
            reverse[alias.lower().strip()] = canonical
    return reverse


def normalize_category(raw, reverse_map):
    if not raw or raw == "uncategorized":
        return "uncategorized"
    return reverse_map.get(raw.lower().strip(), raw.lower().strip())


def load_state_products():
    if not STATE_FILE.exists():
        return []
    with open(STATE_FILE) as f:
        state = json.load(f)
    return state.get("products", {}).get("active", [])


def audit(products=None, reverse_map=None):
    if reverse_map is None:
        reverse_map = build_reverse_map()
    if products is None:
        products = load_state_products()

    raw_counter = Counter()
    norm_counter = Counter()
    mismatches = []
    uncategorized = []

    for p in products:
        slug = p.get("slug", "?")
        raw_cat = p.get("category", "uncategorized") or "uncategorized"
        raw_counter[raw_cat] += 1
        norm = normalize_category(raw_cat, reverse_map)
        norm_counter[norm] += 1
        if raw_cat != norm:
            mismatches.append({"slug": slug, "raw": raw_cat, "normalized": norm})
        if norm == "uncategorized":
            uncategorized.append(slug)

    return {
        "total": len(products),
        "raw_categories": dict(raw_counter.most_common()),
        "normalized_categories": dict(norm_counter.most_common()),
        "canonical_count": len(norm_counter),
        "mismatches": mismatches,
        "mismatch_count": len(mismatches),
        "uncategorized": uncategorized,
        "uncategorized_count": len(uncategorized),
    }


def normalize_products(dry_run=False):
    reverse_map = build_reverse_map()
    products_dir = PRODUCTS_DIR
    if not products_dir.exists():
        return {"error": "products/ directory not found", "updated": 0}

    updated = 0
    unchanged = 0
    errors = []
    details = []

    for product_dir in sorted(products_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        pj = product_dir / "product.json"
        if not pj.exists():
            continue
        try:
            with open(pj) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            errors.append({"slug": product_dir.name, "error": str(e)})
            continue

        raw_cat = data.get("category", "") or ""
        if not raw_cat:
            unchanged += 1
            continue

        norm = normalize_category(raw_cat, reverse_map)
        if norm == raw_cat or norm == "uncategorized":
            unchanged += 1
            continue

        details.append({
            "slug": product_dir.name,
            "old": raw_cat,
            "new": norm,
        })

        if not dry_run:
            data["category"] = norm
            with open(pj, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        updated += 1

    return {
        "updated": updated,
        "unchanged": unchanged,
        "errors": errors,
        "details": details,
        "dry_run": dry_run,
    }


def main():
    parser = argparse.ArgumentParser(description="Category normalizer for product portfolio")
    parser.add_argument("action", choices=["audit", "normalize"], help="Action to perform")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if args.action == "audit":
        result = audit()
        print(f"Total products: {result['total']}")
        print(f"Raw categories: {len(result['raw_categories'])}")
        print(f"Canonical categories: {result['canonical_count']}")
        print(f"Mismatches (need normalize): {result['mismatch_count']}")
        print(f"Uncategorized: {result['uncategorized_count']}")
        print()
        print("Normalized distribution:")
        for cat, cnt in sorted(result["normalized_categories"].items(), key=lambda x: -x[1]):
            print(f"  {cat}: {cnt}")
        if result["mismatches"]:
            print()
            print(f"Mismatches ({len(result['mismatches'])}):")
            for m in result["mismatches"]:
                print(f"  {m['slug']}: '{m['raw']}' -> '{m['normalized']}'")
        if result["uncategorized"]:
            print(f"\nUncategorized ({result['uncategorized_count']}): {', '.join(result['uncategorized'][:10])}{'...' if len(result['uncategorized']) > 10 else ''}")

    elif args.action == "normalize":
        result = normalize_products(dry_run=args.dry_run)
        mode = "DRY RUN" if args.dry_run else "LIVE"
        print(f"[{mode}] Normalization complete")
        print(f"  Updated: {result['updated']}")
        print(f"  Unchanged: {result['unchanged']}")
        if result["errors"]:
            print(f"  Errors: {len(result['errors'])}")
        for d in result["details"]:
            print(f"  {d['slug']}: '{d['old']}' -> '{d['new']}'")


if __name__ == "__main__":
    main()
