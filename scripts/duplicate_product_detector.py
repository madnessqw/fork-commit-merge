#!/usr/bin/env python3
"""Detect products with duplicate or near-duplicate names in the portfolio.

Identifies products that share the same display name, helping surface
redundant entries that inflate portfolio count without adding value.

Usage::

    python3 -m scripts.duplicate_product_detector
    python3 -m scripts.duplicate_product_detector --json
    python3 -m scripts.duplicate_product_detector --verbose
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"


def _load_products() -> list[dict[str, Any]]:
    raw = json.loads(SUMMARY_PATH.read_text()) if SUMMARY_PATH.exists() else {}
    return raw.get("products", [])


def _normalize(name: str) -> str:
    return name.lower().strip()


def find_name_duplicates(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    name_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in products:
        name = p.get("n") or p.get("name") or ""
        norm = _normalize(name)
        name_groups[norm].append(p)

    results = []
    for norm_name, group in sorted(name_groups.items()):
        if len(group) < 2:
            continue
        slugs = [p.get("s") or p.get("slug") or "?" for p in group]
        urls = [p.get("v") or p.get("url") or "" for p in group]
        checkouts = [p.get("c") or p.get("checkout_url") or "" for p in group]
        same_checkout = len(set(c for c in checkouts if c)) == 1 and len(checkouts) == len(group)
        same_url = len(set(u for u in urls if u)) == 1 and len(urls) == len(group)
        results.append({
            "name": group[0].get("n") or group[0].get("name") or norm_name,
            "normalized": norm_name,
            "count": len(group),
            "slugs": slugs,
            "urls": urls,
            "checkouts": checkouts,
            "same_checkout": same_checkout,
            "same_url": same_url,
            "products": group,
        })
    return results


def find_slug_similarities(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slug_map: dict[str, dict[str, Any]] = {}
    for p in products:
        slug = p.get("s") or p.get("slug") or ""
        if slug:
            slug_map[slug] = p

    base_slugs: dict[str, list[str]] = defaultdict(list)
    suffixes = ("-pro", "-plus", "-lite", "-free")
    for slug in slug_map:
        base = slug
        for suffix in suffixes:
            if slug.endswith(suffix):
                base = slug[: -len(suffix)]
                break
        if base != slug:
            base_slugs[base].append(slug)

    results = []
    for base, variants in sorted(base_slugs.items()):
        if len(variants) < 2 and base not in slug_map:
            continue
        all_related = sorted(set([base] + variants) & set(slug_map.keys()))
        if len(all_related) < 2:
            continue
        results.append({
            "base": base,
            "variants": all_related,
            "count": len(all_related),
        })
    return results


def generate_report(name_dupes: list[dict[str, Any]], slug_groups: list[dict[str, Any]], products: list[dict[str, Any]]) -> str:
    lines = [
        f"# Duplicate Product Report",
        f"**Total products:** {len(products)}",
        f"**Duplicate name groups:** {len(name_dupes)}",
        f"**Similar slug groups:** {len(slug_groups)}",
        "",
    ]

    if name_dupes:
        lines.append("## Name Duplicates")
        lines.append("")
        total_duped = sum(d["count"] for d in name_dupes)
        lines.append(f"**{total_duped} products** share names with at least one other product.")
        lines.append("")
        lines.append("| Name | Count | Slugs | Same Checkout | Same URL |")
        lines.append("|------|-------|-------|---------------|----------|")
        for d in name_dupes:
            co = "YES" if d["same_checkout"] else "no"
            url = "YES" if d["same_url"] else "no"
            slugs_str = ", ".join(d["slugs"])
            lines.append(f"| {d['name']} | {d['count']} | {slugs_str} | {co} | {url} |")
        lines.append("")

    if slug_groups:
        lines.append("## Similar Slug Groups")
        lines.append("")
        lines.append("| Base | Variants | Count |")
        lines.append("|------|----------|-------|")
        for g in slug_groups[:20]:
            variants_str = ", ".join(g["variants"])
            lines.append(f"| {g['base']} | {variants_str} | {g['count']} |")
        lines.append("")

    unique_count = len(products) - sum(d["count"] - 1 for d in name_dupes)
    lines.append(f"**Effective unique products:** {unique_count}")
    return "\n".join(lines)


def main() -> None:
    products = _load_products()
    if not products:
        print("No products found in STATE_SUMMARY.json")
        sys.exit(1)

    name_dupes = find_name_duplicates(products)
    slug_groups = find_slug_similarities(products)

    json_mode = "--json" in sys.argv
    verbose = "--verbose" in sys.argv

    if json_mode:
        output = {
            "total_products": len(products),
            "duplicate_name_groups": len(name_dupes),
            "similar_slug_groups": len(slug_groups),
            "name_duplicates": name_dupes,
            "slug_groups": slug_groups,
        }
        print(json.dumps(output, indent=2))
    else:
        report = generate_report(name_dupes, slug_groups, products)
        print(report)

    if verbose:
        print(f"\n--- Details ---")
        for d in name_dupes:
            print(f"\n## {d['name']} (x{d['count']})")
            for p in d["products"]:
                slug = p.get("s") or "?"
                url = p.get("v") or ""
                co = p.get("c") or ""
                print(f"  slug={slug}  url={url}  checkout={co}")


if __name__ == "__main__":
    main()
