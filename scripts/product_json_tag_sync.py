#!/usr/bin/env python3
"""Sync category and tags from STATE.json into each product's product.json file.

STATE.json is the canonical source for category/tags (set by product_tag_analyzer).
This script propagates those values into individual product.json files so each
product is self-describing without needing STATE.json lookup.

Usage:
    python3 scripts/product_json_tag_sync.py --dry-run    # Preview changes
    python3 scripts/product_json_tag_sync.py               # Apply changes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "STATE.json"
PRODUCTS_DIR = ROOT / "products"


def load_state() -> dict[str, Any]:
    with open(STATE_FILE) as f:
        return json.load(f)


def get_products(state: dict[str, Any]) -> list[dict[str, Any]]:
    return state.get("products", {}).get("active", [])


def sync_tags(
    products: list[dict[str, Any]],
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    updated = []
    skipped = []
    errors = []

    for p in products:
        slug = p.get("slug", p.get("s", ""))
        category = p.get("category", "")
        tags = p.get("tags", [])

        if not slug:
            continue

        pj_path = PRODUCTS_DIR / slug / "product.json"
        if not pj_path.exists():
            skipped.append({"slug": slug, "reason": "no product.json"})
            continue

        try:
            data = json.loads(pj_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append({"slug": slug, "reason": str(exc)})
            continue

        changed = False

        if category and data.get("category") != category:
            data["category"] = category
            changed = True

        if tags and data.get("tags") != tags:
            data["tags"] = tags
            changed = True

        if not changed:
            skipped.append({"slug": slug, "reason": "already synced"})
            continue

        updated.append({
            "slug": slug,
            "category": category,
            "tags": tags,
        })

        if not dry_run:
            pj_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    return {
        "updated_count": len(updated),
        "skipped_count": len(skipped),
        "error_count": len(errors),
        "updated": updated,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync STATE.json tags to product.json files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    state = load_state()
    products = get_products(state)

    result = sync_tags(products, dry_run=args.dry_run)

    mode = "DRY RUN" if args.dry_run else "APPLIED"
    print(f"Product JSON Tag Sync [{mode}]")
    print(f"  Updated: {result['updated_count']}")
    print(f"  Skipped: {result['skipped_count']}")
    print(f"  Errors:  {result['error_count']}")

    if result["errors"]:
        print("\nErrors:")
        for e in result["errors"][:5]:
            print(f"  {e['slug']}: {e['reason']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
