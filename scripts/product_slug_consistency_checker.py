#!/usr/bin/env python3
"""Check slug naming consistency across the UniverseCreator portfolio.

Identifies products whose slug deviates from expected patterns:
- display name → slug conversion mismatches
- mixed separators (hyphens vs underscores vs spaces)
- trailing/leading dashes or digits
- unusually short or long slugs
- non-lowercase slugs

Usage::

    python3 -m scripts.product_slug_consistency_checker
    python3 -m scripts.product_slug_consistency_checker --json
    python3 -m scripts.product_slug_consistency_checker --verbose
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DISPLAY_TO_SLUG_BLACKLIST = {"pro", "the", "and", "or", "for", "to", "a", "an"}


def _load_products() -> list[dict[str, Any]]:
    raw = json.loads(SUMMARY_PATH.read_text()) if SUMMARY_PATH.exists() else {}
    return raw.get("products", [])


def _slugify(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    cleaned = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", cleaned)
    return cleaned.lower().strip("-")


def check_slug_format(slug: str) -> list[str]:
    issues: list[str] = []
    if not slug:
        issues.append("empty_slug")
        return issues
    if not SLUG_PATTERN.match(slug):
        issues.append("invalid_chars")
    if slug.startswith("-") or slug.endswith("-"):
        issues.append("dangling_dash")
    if "--" in slug:
        issues.append("double_dash")
    if len(slug) < 3:
        issues.append("too_short")
    if len(slug) > 60:
        issues.append("too_long")
    if any(c.isupper() for c in slug):
        issues.append("uppercase_chars")
    if "_" in slug:
        issues.append("underscore_separator")
    return issues


def check_name_slug_match(name: str, slug: str) -> dict[str, Any]:
    expected = _slugify(name)
    match_score = _similarity(expected, slug)
    return {
        "name": name,
        "slug": slug,
        "expected": expected,
        "match_score": match_score,
        "mismatch": match_score < 0.6,
    }


def _similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    max_len = max(len(a), len(b))
    matches = sum(1 for ca, cb in zip(a, b) if ca == cb)
    return matches / max_len


def analyze(products: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if products is None:
        products = _load_products()

    format_issues: list[dict[str, Any]] = []
    name_mismatches: list[dict[str, Any]] = []
    duplicate_slugs: dict[str, int] = {}
    slug_counts: dict[str, list[str]] = {}

    for p in products:
        name = p.get("n") or p.get("name") or ""
        slug = p.get("s") or p.get("slug") or ""

        fmt = check_slug_format(slug)
        if fmt:
            format_issues.append({"slug": slug, "name": name, "issues": fmt})

        match = check_name_slug_match(name, slug)
        if match["mismatch"]:
            name_mismatches.append(match)

        slug_counts.setdefault(slug, []).append(name)

    for slug, names in slug_counts.items():
        if len(names) > 1:
            duplicate_slugs[slug] = len(names)

    return {
        "total_products": len(products),
        "format_issues": format_issues,
        "format_issue_count": len(format_issues),
        "name_mismatches": name_mismatches,
        "name_mismatch_count": len(name_mismatches),
        "duplicate_slugs": duplicate_slugs,
        "duplicate_slug_count": len(duplicate_slugs),
        "consistency_score": round(
            (1 - len(format_issues) / max(len(products), 1)) * 100, 1
        ),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Check product slug consistency")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", action="store_true", help="Show all details")
    args = parser.parse_args()

    result = analyze()

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"Slug Consistency Report — {result['total_products']} products")
    print(f"  Consistency score: {result['consistency_score']}%")
    print(f"  Format issues: {result['format_issue_count']}")
    print(f"  Name mismatches: {result['name_mismatch_count']}")
    print(f"  Duplicate slugs: {result['duplicate_slug_count']}")

    if args.verbose:
        if result["format_issues"]:
            print("\nFormat Issues:")
            for item in result["format_issues"]:
                print(f"  {item['slug']}: {', '.join(item['issues'])}")

        if result["name_mismatches"]:
            print("\nName/Slug Mismatches:")
            for item in result["name_mismatches"]:
                print(f"  '{item['name']}' → '{item['slug']}' (expected: '{item['expected']}', score: {item['match_score']:.2f})")

        if result["duplicate_slugs"]:
            print("\nDuplicate Slugs:")
            for slug, count in result["duplicate_slugs"].items():
                print(f"  {slug}: {count} products")


if __name__ == "__main__":
    main()
