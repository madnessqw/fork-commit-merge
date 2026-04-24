#!/usr/bin/env python3
"""Auto-fill missing spec_version in product.json manifests.

Many products were created before the spec_version field was standardised.
This script adds spec_version="1.0" to any product.json that lacks it,
reducing the manifest gap reported by deploy_readiness.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "products"
DEFAULT_SPEC_VERSION = "1.0"


def fill_missing_spec_versions(
    products_dir: Path = PRODUCTS_DIR,
    *,
    dry_run: bool = False,
) -> dict:
    fixed = []
    skipped = []
    errors = []

    for child in sorted(products_dir.iterdir()):
        if not child.is_dir():
            continue
        manifest_path = child / "product.json"
        if not manifest_path.exists():
            continue

        try:
            raw = manifest_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append({"slug": child.name, "error": str(exc)})
            continue

        if not isinstance(data, dict):
            errors.append({"slug": child.name, "error": "not a dict"})
            continue

        if data.get("spec_version"):
            skipped.append(child.name)
            continue

        if not dry_run:
            data["spec_version"] = DEFAULT_SPEC_VERSION
            manifest_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        fixed.append(child.name)

    return {
        "fixed": len(fixed),
        "skipped": len(skipped),
        "errors": len(errors),
        "fixed_slugs": fixed,
        "error_details": errors,
    }


def main():
    dry_run = "--dry-run" in sys.argv
    result = fill_missing_spec_versions(dry_run=dry_run)

    mode = "DRY-RUN" if dry_run else "LIVE"
    print(f"[{mode}] spec_version fill complete:")
    print(f"  Fixed:   {result['fixed']}")
    print(f"  Skipped: {result['skipped']}")
    print(f"  Errors:  {result['errors']}")

    if result["error_details"]:
        print("\nErrors:")
        for err in result["error_details"]:
            print(f"  {err['slug']}: {err['error']}")

    return result


if __name__ == "__main__":
    main()
