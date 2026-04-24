#!/usr/bin/env python3
"""Detect products sharing the same Polar checkout URL.

Duplicate checkout URLs mean multiple product entries point to the same
Polar payment link, inflating the portfolio count and potentially confusing
customers.  This detector scans STATE_SUMMARY.json and reports every group
of products that share a checkout URL.

Typical usage::

    python3 -m scripts.checkout_duplicate_detector
    python3 -m scripts.checkout_duplicate_detector --json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"


def _slug_of(product: dict[str, Any]) -> str:
    return product.get("s") or product.get("slug") or product.get("n") or "unknown"


def _checkout_of(product: dict[str, Any]) -> str:
    return (product.get("c") or product.get("checkout_url") or "").strip()


def _status_of(product: dict[str, Any]) -> str:
    return (product.get("st") or product.get("status") or "").strip()


def _url_of(product: dict[str, Any]) -> str:
    return (product.get("v") or product.get("vercel_url") or "").strip()


def detect_duplicates(
    summary_path: Path = SUMMARY_PATH,
) -> list[dict[str, Any]]:
    """Return groups of products that share the same checkout URL.

    Each group dict contains:
        - ``checkout_url``: the shared Polar link
        - ``count``: number of products sharing this URL
        - ``products``: list of product records with slug, status, url
    """
    raw: dict[str, Any] = {}
    try:
        raw = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    products = raw.get("products", [])
    if not isinstance(products, list):
        return []

    url_groups: dict[str, list[dict[str, Any]]] = {}
    for product in products:
        if not isinstance(product, dict):
            continue
        checkout = _checkout_of(product)
        if not checkout.startswith("http"):
            continue
        slug = _slug_of(product)
        entry = {
            "slug": slug,
            "status": _status_of(product),
            "url": _url_of(product),
        }
        url_groups.setdefault(checkout, []).append(entry)

    duplicates: list[dict[str, Any]] = []
    for checkout_url, entries in url_groups.items():
        if len(entries) < 2:
            continue
        duplicates.append(
            {
                "checkout_url": checkout_url,
                "count": len(entries),
                "products": entries,
            }
        )

    duplicates.sort(key=lambda g: (-g["count"], g["checkout_url"]))
    return duplicates


def duplicate_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    """Compact summary for downstream agents."""
    dupes = detect_duplicates(summary_path)
    total_affected = sum(g["count"] for g in dupes)
    slugs: list[str] = []
    for group in dupes:
        for entry in group["products"]:
            slugs.append(entry["slug"])

    return {
        "duplicate_groups": len(dupes),
        "total_affected_products": total_affected,
        "redundant_products": total_affected - len(dupes),
        "slugs": slugs,
        "details": dupes,
    }


def cleanup_suggestions(
    summary_path: Path = SUMMARY_PATH,
) -> list[dict[str, Any]]:
    """For each duplicate group, suggest which slug to keep.

    Heuristic: keep the slug that matches the canonical Vercel URL pattern
    (``{slug}.vercel.app``).  If both match or neither matches, keep the
    one with ``status == live``.  Tie-break on alphabetical order.
    """
    dupes = detect_duplicates(summary_path)
    suggestions: list[dict[str, Any]] = []

    for group in dupes:
        checkout_url = group["checkout_url"]
        entries = group["products"]
        if len(entries) < 2:
            continue

        best = entries[0]
        for entry in entries[1:]:
            if _is_better_candidate(entry, best):
                best = entry

        removable = [e["slug"] for e in entries if e["slug"] != best["slug"]]

        suggestions.append(
            {
                "checkout_url": checkout_url,
                "keep_slug": best["slug"],
                "keep_status": best["status"],
                "remove_slugs": removable,
                "reason": "matches canonical vercel URL pattern"
                if best["url"].endswith(f".vercel.app")
                and f"https://{best['slug']}.vercel.app" == best["url"]
                else "live status preferred",
            }
        )

    return suggestions


def _is_better_candidate(candidate: dict[str, Any], current: dict[str, Any]) -> bool:
    c_slug = candidate["slug"]
    c_url = candidate["url"]
    c_status = candidate["status"]

    cu_slug = current["slug"]
    cu_url = current["url"]
    cu_status = current["status"]

    c_canonical = f"https://{c_slug}.vercel.app" == c_url
    cu_canonical = f"https://{cu_slug}.vercel.app" == cu_url

    if c_canonical and not cu_canonical:
        return True
    if cu_canonical and not c_canonical:
        return False

    if c_status == "live" and cu_status != "live":
        return True
    if cu_status == "live" and c_status != "live":
        return False

    return c_slug < cu_slug


if __name__ == "__main__":
    import sys

    as_json = "--json" in sys.argv
    result = duplicate_summary()

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Duplicate checkout groups: {result['duplicate_groups']}")
        print(f"Affected products: {result['total_affected_products']}")
        print(f"Redundant entries: {result['redundant_products']}")
        for group in result["details"]:
            slugs = [e["slug"] for e in group["products"]]
            print(f"  {slugs} -> ...{group['checkout_url'][-20:]}")
        suggestions = cleanup_suggestions()
        if suggestions:
            print("\nCleanup suggestions:")
            for s in suggestions:
                print(
                    f"  KEEP {s['keep_slug']} ({s['keep_status']})"
                    f" | REMOVE {s['remove_slugs']}"
                    f" | {s['reason']}"
                )
