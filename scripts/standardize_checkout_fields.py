#!/usr/bin/env python3
"""Normalize checkout metadata for product.json files.

Default mode is dry-run. Use `--write` to update files in place.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_metadata import normalize_checkout_metadata


def iter_product_files() -> list[Path]:
    return sorted((ROOT / "products").glob("*/product.json"))


def normalize_file(path: Path, *, write: bool, keep_legacy: bool = False) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    normalized = normalize_checkout_metadata(
        data,
        force_canonical_key=True,
        prune_legacy=not keep_legacy,
    )
    changed = normalized != data
    if changed and write:
        path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write normalized metadata back to product.json files.")
    parser.add_argument(
        "--keep-legacy",
        action="store_true",
        help="Keep legacy checkout aliases instead of pruning them during normalization.",
    )
    args = parser.parse_args()

    changed_paths: list[Path] = []
    for path in iter_product_files():
        if normalize_file(path, write=args.write, keep_legacy=args.keep_legacy):
            changed_paths.append(path)

    mode = "updated" if args.write else "would_update"
    print(f"{mode}={len(changed_paths)} scanned={len(iter_product_files())}")
    for path in changed_paths[:20]:
        print(path.relative_to(ROOT))
    if len(changed_paths) > 20:
        print(f"... {len(changed_paths) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
