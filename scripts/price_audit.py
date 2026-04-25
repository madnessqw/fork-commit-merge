#!/usr/bin/env python3
"""Price consistency audit for UniverseCreator products.

Scans STATE.json for products with price values, detects format
inconsistencies, normalizes them to a canonical integer representation,
and reports products with non-standard or suspicious pricing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"

_PRICE_RE = re.compile(r"[^\d.]")
CANONICAL_FORMAT = "int_cents"


def parse_price(raw: Any) -> int | None:
    """Parse a price value into integer cents.

    Accepts:
        - int already in cents or dollars (heuristic: < 1000 → dollars)
        - str like "9", "$19", "$9.99", "29.00"
    Returns integer cents or None if unparseable.
    """
    if raw is None:
        return None
    if isinstance(raw, int):
        return raw * 100 if raw < 1000 else raw
    if isinstance(raw, float):
        return int(round(raw * 100))
    text = str(raw).strip()
    if not text:
        return None
    cleaned = _PRICE_RE.sub("", text)
    if not cleaned:
        return None
    try:
        dollars = float(cleaned)
    except ValueError:
        return None
    return int(round(dollars * 100))


def format_price_dollars(cents: int) -> str:
    """Format cents as '$X' or '$X.99' string."""
    if cents % 100 == 0:
        return f"${cents // 100}"
    whole = cents // 100
    frac = cents % 100
    return f"${whole}.{frac:02d}"


def detect_price_format(raw: Any) -> str:
    """Classify the raw price format for auditing."""
    if raw is None:
        return "missing"
    if isinstance(raw, int):
        return "int_bare"
    if isinstance(raw, float):
        return "float_bare"
    text = str(raw).strip()
    if not text:
        return "empty_string"
    if text.startswith("$"):
        if "." in text:
            return "str_dollar_decimal"
        return "str_dollar_integer"
    if "." in text:
        return "str_decimal"
    if text.isdigit():
        return "str_integer"
    return "unknown"


def audit_product_prices(
    state_path: Path = STATE_PATH,
) -> dict[str, Any]:
    """Scan all active products for price consistency issues.

    Returns a dict with:
        - ``total``: total products scanned
        - ``format_counts``: how many products use each price format
        - ``inconsistencies``: products whose raw format is not canonical
        - ``missing_price``: products with no price at all
        - ``suggested_fixes``: slug → normalized price string
    """
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "total": 0,
            "format_counts": {},
            "inconsistencies": [],
            "missing_price": [],
            "suggested_fixes": {},
        }

    products = state.get("products", {})
    active: list[dict] = []
    if isinstance(products, dict):
        for key in ("active", "spec_ready"):
            coll = products.get(key, [])
            if isinstance(coll, list):
                active.extend(coll)
    elif isinstance(products, list):
        active = products

    format_counts: dict[str, int] = {}
    inconsistencies: list[dict[str, Any]] = []
    missing_price: list[str] = []
    suggested_fixes: dict[str, str] = {}

    for item in active:
        if not isinstance(item, dict):
            continue
        slug = item.get("slug") or item.get("s") or "unknown"
        raw_price = item.get("price")

        fmt = detect_price_format(raw_price)
        format_counts[fmt] = format_counts.get(fmt, 0) + 1

        if fmt == "missing":
            missing_price.append(slug)
            continue

        cents = parse_price(raw_price)
        if cents is None:
            inconsistencies.append({
                "slug": slug,
                "raw_price": raw_price,
                "format": fmt,
                "issue": "unparseable",
            })
            continue

        is_canonical = isinstance(raw_price, str) and str(raw_price).startswith("$") and "." not in str(raw_price)
        if not is_canonical:
            normalized = format_price_dollars(cents)
            inconsistencies.append({
                "slug": slug,
                "raw_price": raw_price,
                "format": fmt,
                "issue": "non_canonical",
                "normalized": normalized,
            })
            suggested_fixes[slug] = normalized

    inconsistencies.sort(key=lambda x: str(x["slug"]))

    return {
        "total": len(active),
        "format_counts": format_counts,
        "inconsistencies": inconsistencies,
        "missing_price": missing_price,
        "suggested_fixes": suggested_fixes,
    }


def fix_product_prices(
    state_path: Path = STATE_PATH,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Normalize all non-canonical prices in STATE.json to '$XX' format.

    Returns a dict with:
        - ``fixed_count``: number of prices normalized
        - ``fixed_products``: list of {slug, old_price, new_price}
        - ``dry_run``: whether this was a dry run
        - ``already_canonical``: count of already canonical prices
        - ``skipped``: count of products skipped (missing/unparseable)
    """
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "fixed_count": 0,
            "fixed_products": [],
            "dry_run": dry_run,
            "already_canonical": 0,
            "skipped": 0,
            "error": "STATE.json unreadable",
        }

    products = state.get("products", {})
    active: list[dict] = []
    if isinstance(products, dict):
        for key in ("active", "spec_ready"):
            coll = products.get(key, [])
            if isinstance(coll, list):
                active.extend(coll)
    elif isinstance(products, list):
        active = products

    fixed_products: list[dict[str, Any]] = []
    already_canonical = 0
    skipped = 0

    for item in active:
        if not isinstance(item, dict):
            continue
        slug = item.get("slug") or item.get("s") or "unknown"
        raw_price = item.get("price")

        if raw_price is None:
            skipped += 1
            continue

        fmt = detect_price_format(raw_price)
        cents = parse_price(raw_price)

        if cents is None:
            skipped += 1
            continue

        is_canonical = isinstance(raw_price, str) and str(raw_price).startswith("$") and "." not in str(raw_price)
        if is_canonical:
            already_canonical += 1
            continue

        normalized = format_price_dollars(cents)
        fixed_products.append({
            "slug": slug,
            "old_price": raw_price,
            "new_price": normalized,
        })
        if not dry_run:
            item["price"] = normalized

    if not dry_run and fixed_products:
        state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return {
        "fixed_count": len(fixed_products),
        "fixed_products": fixed_products,
        "dry_run": dry_run,
        "already_canonical": already_canonical,
        "skipped": skipped,
    }


def price_coverage_report(
    state_path: Path = STATE_PATH,
) -> dict[str, Any]:
    """Generate a price coverage summary from audit results.

    Returns a dict with coverage percentage, format distribution,
    canonical compliance rate, and top format breakdown.
    """
    audit = audit_product_prices(state_path)
    total = audit["total"]
    if total == 0:
        return {
            "total": 0,
            "coverage_pct": 0.0,
            "canonical_pct": 0.0,
            "format_distribution": {},
            "missing_count": 0,
            "inconsistency_count": 0,
        }

    missing_count = len(audit["missing_price"])
    inconsistency_count = len(audit["inconsistencies"])
    priced = total - missing_count
    canonical_count = total - inconsistency_count - missing_count

    return {
        "total": total,
        "coverage_pct": round(priced / total * 100, 1),
        "canonical_pct": round(max(canonical_count, 0) / total * 100, 1),
        "format_distribution": audit["format_counts"],
        "missing_count": missing_count,
        "inconsistency_count": inconsistency_count,
    }


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Price consistency audit for UniverseCreator")
    parser.add_argument("--fix", action="store_true", help="Normalize non-canonical prices in STATE.json")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without writing")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--coverage", action="store_true", help="Show coverage report")
    args = parser.parse_args()

    if args.fix or args.dry_run:
        result = fix_product_prices(dry_run=args.dry_run)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            status = "DRY RUN" if args.dry_run else "FIXED"
            print(f"[{status}] {result['fixed_count']} prices normalized")
            print(f"  Already canonical: {result['already_canonical']}")
            print(f"  Skipped: {result['skipped']}")
            if result['fixed_products']:
                for fp in result['fixed_products'][:10]:
                    print(f"  {fp['slug']}: {fp['old_price']} → {fp['new_price']}")
                if len(result['fixed_products']) > 10:
                    print(f"  ... and {len(result['fixed_products']) - 10} more")
        return result

    if args.coverage:
        report = price_coverage_report()
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(f"Coverage: {report['coverage_pct']}% | Canonical: {report['canonical_pct']}%")
            print(f"Missing: {report['missing_count']} | Inconsistencies: {report['inconsistency_count']}")
        return report

    audit = audit_product_prices()
    if args.json:
        safe_audit = {k: v for k, v in audit.items() if k != "inconsistencies"}
        safe_audit["inconsistency_count"] = len(audit.get("inconsistencies", []))
        print(json.dumps(safe_audit, indent=2, ensure_ascii=False))
    else:
        print(f"Total: {audit['total']} | Inconsistencies: {len(audit['inconsistencies'])} | Missing: {len(audit['missing_price'])}")
        print(f"Formats: {audit['format_counts']}")
    return audit


if __name__ == "__main__":
    main()
