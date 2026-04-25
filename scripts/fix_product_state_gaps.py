#!/usr/bin/env python3
"""
Fix missing state fields (created_cycle, deployed_cycle) in product.json files.
Scans products/ directory and patches products with null/missing state fields.

Supports --dry-run to preview changes without writing.
"""
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_DIR = os.path.join(REPO_ROOT, "products")
SUMMARY_PATH = os.path.join(REPO_ROOT, "STATE_SUMMARY.json")
BATCH_DEPLOY_CYCLE = 1108

DATE_CYCLE_MAP = {
    "2026-04-21": 988,
    "2026-04-22": 1000,
    "2026-04-23": 1050,
    "2026-04-24": 1100,
    "2026-04-25": 1164,
}


def _current_cycle():
    try:
        with open(SUMMARY_PATH, "r") as f:
            return json.load(f).get("cycle", 1164)
    except (OSError, json.JSONDecodeError):
        return 1164


CURRENT_CYCLE = _current_cycle()


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def estimate_created_cycle(product):
    created_at = product.get("created_at")
    if created_at and isinstance(created_at, str):
        for date_prefix, cycle in DATE_CYCLE_MAP.items():
            if date_prefix in created_at:
                return cycle
    seo_at = product.get("seo_optimized_at", "")
    if seo_at:
        for date_prefix, cycle in DATE_CYCLE_MAP.items():
            if date_prefix in seo_at:
                return cycle + 2
    return None


def main(argv=None):
    dry_run = "--dry-run" in (argv or sys.argv)

    if not os.path.isdir(PRODUCTS_DIR):
        print(f"ERROR: {PRODUCTS_DIR} not found")
        return 1

    slugs = sorted(
        d for d in os.listdir(PRODUCTS_DIR)
        if os.path.isdir(os.path.join(PRODUCTS_DIR, d))
    )

    patched = 0
    for slug in slugs:
        pj = os.path.join(PRODUCTS_DIR, slug, "product.json")
        if not os.path.exists(pj):
            continue

        product = load_json(pj)
        changed = False

        cc = product.get("created_cycle")
        if cc is None or "created_cycle" not in product:
            est = estimate_created_cycle(product)
            product["created_cycle"] = est if est else CURRENT_CYCLE
            changed = True
            print(f"  {slug}: created_cycle={product['created_cycle']}")

        dc = product.get("deployed_cycle")
        if dc is None or "deployed_cycle" not in product:
            status = product.get("status", "")
            if status in ("live", "ready_to_deploy"):
                product["deployed_cycle"] = BATCH_DEPLOY_CYCLE
                changed = True
                print(f"  {slug}: deployed_cycle={BATCH_DEPLOY_CYCLE}")

        if changed:
            if dry_run:
                print(f"  [DRY-RUN] would patch {slug}")
            else:
                save_json(pj, product)
            patched += 1

    suffix = " (dry-run)" if dry_run else ""
    print(f"\nPatched{suffix}: {patched} products")
    return 0


if __name__ == "__main__":
    sys.exit(main())
