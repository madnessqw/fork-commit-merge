#!/usr/bin/env python3
"""Clean waste directories (node_modules, .vercel, dist, etc.) from products.

Scans product directories for reclaimable waste and removes it safely.
Supports dry-run mode (default) and targeted cleaning by waste type or slug.

Usage:
    python3 scripts/product_waste_cleaner.py --dry-run
    python3 scripts/product_waste_cleaner.py --apply
    python3 scripts/product_waste_cleaner.py --apply --type node_modules
    python3 scripts/product_waste_cleaner.py --apply --slug jwt-generator
    python3 scripts/product_waste_cleaner.py --apply --min-size-kb 1024
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STATE_PATH = ROOT / "STATE.json"
PRODUCTS_DIR = ROOT / "products"

WASTE_DIRS = {
    "node_modules": "Node.js dependencies — reinstall with npm install",
    ".next": "Next.js build cache — regenerates on build",
    ".nuxt": "Nuxt.js build cache — regenerates on build",
    "dist": "Build output — regenerates on build",
    ".cache": "Generic cache directory",
    "__pycache__": "Python bytecode cache — auto-regenerates",
    ".turbo": "Turborepo cache",
    "coverage": "Test coverage output",
    ".vercel": "Vercel CLI local config",
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


def _active_slugs(state_path: Path = STATE_PATH) -> set[str]:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {
        p.get("slug") or p.get("s") or ""
        for p in data.get("products", {}).get("active", [])
    } - {""}


def _fmt_kb(kb: float) -> str:
    if kb < 1024:
        return f"{kb:.1f} KB"
    return f"{kb / 1024:.1f} MB"


def scan_waste(
    products_dir: Path = PRODUCTS_DIR,
    state_path: Path = STATE_PATH,
    waste_types: list[str] | None = None,
    slug_filter: str | None = None,
    min_size_kb: int = 0,
) -> list[dict[str, Any]]:
    active = _active_slugs(state_path)
    types_to_scan = waste_types or list(WASTE_DIRS.keys())

    results: list[dict[str, Any]] = []

    if not products_dir.is_dir():
        return results

    product_dirs = sorted(
        d for d in products_dir.iterdir()
        if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
    )

    for pdir in product_dirs:
        slug = pdir.name
        if slug_filter and slug != slug_filter:
            continue

        for wtype in types_to_scan:
            waste_path = pdir / wtype
            if not waste_path.is_dir():
                continue

            size_bytes = _dir_size(waste_path)
            size_kb = round(size_bytes / 1024, 1)

            if size_kb < min_size_kb:
                continue

            results.append({
                "slug": slug,
                "waste_type": wtype,
                "size_bytes": size_bytes,
                "size_kb": size_kb,
                "path": str(waste_path),
                "is_active": slug in active,
                "description": WASTE_DIRS.get(wtype, ""),
            })

    results.sort(key=lambda r: r["size_bytes"], reverse=True)
    return results


def clean_waste(
    entries: list[dict[str, Any]],
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    cleaned: list[dict[str, Any]] = []
    errors: list[str] = []
    total_reclaimed = 0

    for entry in entries:
        path = Path(entry["path"])
        if not path.is_dir():
            errors.append(f"{entry['slug']}/{entry['waste_type']}: not found")
            continue

        if dry_run:
            cleaned.append(entry)
            total_reclaimed += entry["size_bytes"]
        else:
            try:
                shutil.rmtree(str(path))
                cleaned.append(entry)
                total_reclaimed += entry["size_bytes"]
            except OSError as e:
                errors.append(f"{entry['slug']}/{entry['waste_type']}: {e}")

    return {
        "cleaned_count": len(cleaned),
        "total_reclaimed_bytes": total_reclaimed,
        "total_reclaimed_kb": round(total_reclaimed / 1024, 1),
        "total_reclaimed_mb": round(total_reclaimed / 1024 / 1024, 1),
        "errors": errors,
        "dry_run": dry_run,
    }


def format_report(
    entries: list[dict[str, Any]],
    clean_result: dict[str, Any] | None = None,
) -> str:
    lines = [
        "# Product Waste Cleaner Report",
        "",
        f"**Waste entries found:** {len(entries)}",
    ]

    if not entries:
        lines.append("")
        lines.append("No waste directories found. Portfolio is clean.")
        return "\n".join(lines)

    total_kb = sum(e["size_kb"] for e in entries)
    lines.append(f"**Total waste:** {_fmt_kb(total_kb)}")
    lines.append("")

    by_type: dict[str, float] = {}
    for e in entries:
        by_type[e["waste_type"]] = by_type.get(e["waste_type"], 0) + e["size_kb"]

    lines.append("## Waste by Type")
    lines.append("")
    for wtype, kb in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        desc = WASTE_DIRS.get(wtype, "")
        lines.append(f"- **{wtype}**: {_fmt_kb(kb)} — {desc}")
    lines.append("")

    lines.append("## Top 20 Waste Entries")
    lines.append("")
    for i, e in enumerate(entries[:20], 1):
        status = "active" if e["is_active"] else "orphan"
        lines.append(
            f"{i}. **{e['slug']}**/{e['waste_type']} — {_fmt_kb(e['size_kb'])} [{status}]"
        )
    if len(entries) > 20:
        lines.append(f"... +{len(entries) - 20} more")
    lines.append("")

    if clean_result:
        mode = "DRY RUN" if clean_result["dry_run"] else "APPLIED"
        lines.append(f"## Cleanup Result ({mode})")
        lines.append("")
        lines.append(f"- **Cleaned:** {clean_result['cleaned_count']} entries")
        lines.append(f"- **Reclaimed:** {clean_result['total_reclaimed_mb']} MB")
        if clean_result.get("errors"):
            lines.append(f"- **Errors:** {len(clean_result['errors'])}")
            for err in clean_result["errors"][:5]:
                lines.append(f"  - {err}")
        lines.append("")

    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Product waste cleaner")
    parser.add_argument("--apply", action="store_true", help="Actually delete waste dirs (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview only (default)")
    parser.add_argument("--type", dest="waste_type", action="append", help="Filter by waste type (repeatable)")
    parser.add_argument("--slug", help="Only scan specific product slug")
    parser.add_argument("--min-size-kb", type=int, default=0, help="Minimum size in KB to consider")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    entries = scan_waste(
        waste_types=args.waste_type,
        slug_filter=args.slug,
        min_size_kb=args.min_size_kb,
    )

    clean_result = None
    if entries:
        clean_result = clean_waste(entries, dry_run=not args.apply)

    if args.json:
        output = {"entries": entries}
        if clean_result:
            output["clean_result"] = clean_result
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_report(entries, clean_result))

    return {"entries": entries, "clean_result": clean_result}


if __name__ == "__main__":
    main()
