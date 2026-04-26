#!/usr/bin/env python3
"""Scan orphan product directories not tracked in STATE.json active products.

Identifies untracked product folders, categorizes them by content richness,
calculates disk usage, and generates cleanup recommendations.

Usage:
    python3 scripts/portfolio_orphan_scanner.py
    python3 scripts/portfolio_orphan_scanner.py --json
    python3 scripts/portfolio_orphan_scanner.py --size
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
PRODUCTS_DIR = ROOT / "products"

RICHNESS_FILES = {
    "has_product_json": "product.json",
    "has_vercel_json": "vercel.json",
    "has_package_json": "package.json",
    "has_spec_json": "spec.json",
    "has_readme": "README.md",
}


def _active_slugs(state_path: Path = STATE_PATH) -> set[str]:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {
        p.get("slug") or p.get("s") or ""
        for p in data.get("products", {}).get("active", [])
    } - {""}


def _folder_slugs(products_dir: Path = PRODUCTS_DIR) -> set[str]:
    if not products_dir.is_dir():
        return set()
    return {
        d.name
        for d in products_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }


def _dir_size(path: Path) -> int:
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass
    return total


def _check_richness(slug_dir: Path) -> dict[str, bool]:
    result = {}
    for key, filename in RICHNESS_FILES.items():
        result[key] = (slug_dir / filename).exists()
    return result


def _categorize(richness: dict[str, bool]) -> str:
    has_code = richness.get("has_package_json", False)
    has_spec = richness.get("has_spec_json", False)
    has_product = richness.get("has_product_json", False)
    has_vercel = richness.get("has_vercel_json", False)

    if has_code and has_vercel:
        return "deployable"
    if has_code:
        return "has_code"
    if has_spec or has_product:
        return "has_spec"
    if richness.get("has_readme", False):
        return "minimal"
    return "dead"


def scan_orphans(
    state_path: Path = STATE_PATH,
    products_dir: Path = PRODUCTS_DIR,
    calc_size: bool = False,
) -> dict[str, Any]:
    active = _active_slugs(state_path)
    folders = _folder_slugs(products_dir)
    orphans = sorted(folders - active)

    results: list[dict[str, Any]] = []
    categories: dict[str, list[str]] = {
        "deployable": [],
        "has_code": [],
        "has_spec": [],
        "minimal": [],
        "dead": [],
    }
    total_size = 0

    for slug in orphans:
        slug_dir = products_dir / slug
        richness = _check_richness(slug_dir)
        category = _categorize(richness)
        size = _dir_size(slug_dir) if calc_size else 0
        total_size += size

        entry: dict[str, Any] = {
            "slug": slug,
            "category": category,
            **richness,
        }
        if calc_size:
            entry["size_bytes"] = size
            entry["size_kb"] = round(size / 1024, 1)

        results.append(entry)
        categories[category].append(slug)

    return {
        "total_orphans": len(orphans),
        "categories": {k: len(v) for k, v in categories.items()},
        "category_lists": categories,
        "orphans": results,
        "total_size_bytes": total_size if calc_size else None,
        "total_size_mb": round(total_size / 1024 / 1024, 1) if calc_size else None,
    }


def format_report(result: dict[str, Any]) -> str:
    lines = [
        "# Portfolio Orphan Scanner Report",
        "",
        f"**Total orphans:** {result['total_orphans']}",
        "",
    ]
    if result.get("total_size_mb") is not None:
        lines.append(f"**Total size:** {result['total_size_mb']} MB")
        lines.append("")

    cats = result["categories"]
    lines.append("## Categories")
    lines.append("")
    for cat in ["deployable", "has_code", "has_spec", "minimal", "dead"]:
        count = cats.get(cat, 0)
        lines.append(f"- **{cat}:** {count}")
    lines.append("")

    cat_lists = result.get("category_lists", {})
    for cat in ["deployable", "has_code", "has_spec"]:
        slugs = cat_lists.get(cat, [])
        if slugs:
            lines.append(f"## {cat} ({len(slugs)})")
            for s in slugs[:15]:
                lines.append(f"  - {s}")
            if len(slugs) > 15:
                lines.append(f"  ... +{len(slugs) - 15} more")
            lines.append("")

    dead = cat_lists.get("dead", [])
    if dead:
        lines.append(f"## Dead/Empty ({len(dead)})")
        for s in dead[:15]:
            lines.append(f"  - {s}")
        if len(dead) > 15:
            lines.append(f"  ... +{len(dead) - 15} more")
        lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    deployable = cats.get("deployable", 0)
    has_code = cats.get("has_code", 0)
    dead_count = cats.get("dead", 0)
    if dead_count > 0:
        lines.append(f"- **Archive {dead_count} dead products** to reduce clutter")
    if deployable > 0:
        lines.append(f"- **Review {deployable} deployable orphans** — may be worth restoring")
    if has_code > 0:
        lines.append(f"- **Evaluate {has_code} code-only orphans** — spec + deploy needed")

    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Portfolio orphan scanner")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--size", action="store_true", help="Calculate directory sizes")
    args = parser.parse_args()

    result = scan_orphans(calc_size=args.size)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_report(result))

    return result


if __name__ == "__main__":
    main()
