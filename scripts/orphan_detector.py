#!/usr/bin/env python3
"""Orphan directory detector for UniverseCreator product portfolio.

Finds product directories in products/ that are not tracked in STATE.json.
Reports disk usage and supports archiving orphans.

Usage:
    python3 scripts/orphan_detector.py scan           # List orphans with sizes
    python3 scripts/orphan_detector.py --dry-run prune # Preview archive
    python3 scripts/orphan_detector.py prune            # Archive orphans to .archived/
"""

import json
import os
import shutil
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "STATE.json"
PRODUCTS_DIR = ROOT / "products"
ARCHIVE_DIR = ROOT / "products" / ".archived"

PROTECTED_DIRS = {".archived", ".git", "__pycache__", "node_modules", ".next"}


def load_state_slugs():
    state = json.load(open(STATE_PATH))
    slugs = set()
    for p in state.get("products", {}).get("active", []):
        slugs.add(p.get("slug", ""))
    for p in state.get("products", {}).get("archived", []):
        slugs.add(p.get("slug", ""))
    slugs.discard("")
    return slugs


def get_dir_slugs():
    if not PRODUCTS_DIR.is_dir():
        return set()
    return {
        d
        for d in os.listdir(PRODUCTS_DIR)
        if (PRODUCTS_DIR / d).is_dir() and d not in PROTECTED_DIRS
    }


def dir_size(path):
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass
    return total


def format_size(bytes_size):
    if bytes_size < 1024:
        return f"{bytes_size}B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f}KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.1f}MB"
    return f"{bytes_size / (1024 * 1024 * 1024):.2f}GB"


def scan(detailed=False):
    state_slugs = load_state_slugs()
    dir_slugs = get_dir_slugs()
    orphans = sorted(dir_slugs - state_slugs)

    if not orphans:
        print("No orphan directories found.")
        return []

    total_size = 0
    results = []
    for slug in orphans:
        path = PRODUCTS_DIR / slug
        size = dir_size(path)
        total_size += size
        results.append({"slug": slug, "size": size, "path": str(path)})

    if detailed:
        for r in results:
            print(f"  {r['slug']:40s} {format_size(r['size']):>10s}")
        print(f"\n  Total: {len(orphans)} orphans, {format_size(total_size)}")
    else:
        print(f"Found {len(orphans)} orphan directories ({format_size(total_size)})")

    return results


def prune(dry_run=False):
    orphans = scan(detailed=True)
    if not orphans:
        return 0

    archived = 0
    if not dry_run:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    for entry in orphans:
        src = PRODUCTS_DIR / entry["slug"]
        dst = ARCHIVE_DIR / entry["slug"]
        if dry_run:
            print(f"  [DRY-RUN] Would archive: {entry['slug']}")
        else:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
            print(f"  Archived: {entry['slug']} → .archived/{entry['slug']}")
            archived += 1

    if dry_run:
        print(f"\n  [DRY-RUN] {len(orphans)} directories would be archived")
    else:
        print(f"\n  {archived} directories archived to {ARCHIVE_DIR}")

    return archived


def main():
    parser = argparse.ArgumentParser(description="Orphan directory detector")
    parser.add_argument(
        "command",
        choices=["scan", "prune"],
        help="scan: list orphans | prune: archive orphans",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without changes"
    )
    args = parser.parse_args()

    if not STATE_PATH.exists():
        print(f"ERROR: {STATE_PATH} not found", file=sys.stderr)
        sys.exit(1)

    if args.command == "scan":
        scan(detailed=True)
    elif args.command == "prune":
        if not args.dry_run:
            print("⚠️  This will MOVE orphan dirs to .archived/")
            confirm = input("Continue? [y/N] ").strip().lower()
            if confirm != "y":
                print("Aborted.")
                return
        prune(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
