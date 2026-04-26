#!/usr/bin/env python3
"""Analyze disk usage across all product directories.

Scans every product folder (active + orphan), reports size breakdown,
identifies bloated directories, and finds optimization opportunities
like node_modules, .next caches, or oversized assets.

Usage:
    python3 scripts/product_size_analyzer.py
    python3 scripts/product_size_analyzer.py --json
    python3 scripts/product_size_analyzer.py --top 20
    python3 scripts/product_size_analyzer.py --waste
"""

from __future__ import annotations

import json
import os
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

SIZE_TIERS = {
    "tiny": (0, 10),
    "small": (10, 100),
    "medium": (100, 1024),
    "large": (1024, 10 * 1024),
    "huge": (10 * 1024, float("inf")),
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


def _dir_size(path: Path) -> int:
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass
    return total


def _subdir_sizes(path: Path) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for entry in path.iterdir():
        if entry.is_dir():
            sizes[entry.name] = _dir_size(entry)
    return sizes


def _tier_for_kb(kb: float) -> str:
    for tier, (lo, hi) in SIZE_TIERS.items():
        if lo <= kb < hi:
            return tier
    return "huge"


def _fmt_kb(kb: float) -> str:
    if kb < 1024:
        return f"{kb:.1f} KB"
    return f"{kb / 1024:.1f} MB"


def scan_products(
    products_dir: Path = PRODUCTS_DIR,
    state_path: Path = STATE_PATH,
    top: int = 30,
) -> dict[str, Any]:
    active = _active_slugs(state_path)

    if not products_dir.is_dir():
        return {"error": "products directory not found", "products": []}

    entries: list[dict[str, Any]] = []
    total_active_size = 0
    total_orphan_size = 0
    total_waste = 0
    waste_details: dict[str, int] = {}

    product_dirs = sorted(
        d for d in products_dir.iterdir()
        if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
    )

    for pdir in product_dirs:
        slug = pdir.name
        is_active = slug in active
        size_bytes = _dir_size(pdir)
        size_kb = round(size_bytes / 1024, 1)

        subdir_sizes = _subdir_sizes(pdir)
        waste_found: dict[str, int] = {}
        entry_waste = 0
        for waste_name in WASTE_DIRS:
            if waste_name in subdir_sizes:
                w = subdir_sizes[waste_name]
                waste_found[waste_name] = w
                entry_waste += w
                total_waste += w
                waste_details[waste_name] = waste_details.get(waste_name, 0) + w

        if is_active:
            total_active_size += size_bytes
        else:
            total_orphan_size += size_bytes

        entries.append({
            "slug": slug,
            "is_active": is_active,
            "size_kb": size_kb,
            "size_bytes": size_bytes,
            "tier": _tier_for_kb(size_kb),
            "waste_kb": round(entry_waste / 1024, 1),
            "waste_types": list(waste_found.keys()),
            "subdirs": len(subdir_sizes),
        })

    entries.sort(key=lambda e: e["size_bytes"], reverse=True)

    tier_counts: dict[str, int] = {}
    for t in SIZE_TIERS:
        tier_counts[t] = 0
    for e in entries:
        tier_counts[e["tier"]] = tier_counts.get(e["tier"], 0) + 1

    return {
        "total_products": len(entries),
        "active_count": sum(1 for e in entries if e["is_active"]),
        "orphan_count": sum(1 for e in entries if not e["is_active"]),
        "total_size_kb": round((total_active_size + total_orphan_size) / 1024, 1),
        "active_size_kb": round(total_active_size / 1024, 1),
        "orphan_size_kb": round(total_orphan_size / 1024, 1),
        "total_waste_kb": round(total_waste / 1024, 1),
        "waste_breakdown_kb": {
            k: round(v / 1024, 1) for k, v in sorted(
                waste_details.items(), key=lambda x: x[1], reverse=True
            )
        },
        "tier_distribution": tier_counts,
        "top_largest": entries[:top],
        "top_waste": sorted(entries, key=lambda e: e.get("waste_kb", 0), reverse=True)[:top],
    }


def format_report(result: dict[str, Any]) -> str:
    if "error" in result:
        return f"Error: {result['error']}"

    lines = [
        "# Product Size Analysis",
        "",
        f"**Total products:** {result['total_products']} "
        f"({result['active_count']} active, {result['orphan_count']} orphan)",
        f"**Total size:** {_fmt_kb(result['total_size_kb'])} "
        f"(active: {_fmt_kb(result['active_size_kb'])}, "
        f"orphan: {_fmt_kb(result['orphan_size_kb'])})",
    ]

    waste_total = result.get("total_waste_kb", 0)
    if waste_total > 0:
        lines.append(f"**Reclaimable waste:** {_fmt_kb(waste_total)}")
    lines.append("")

    tiers = result.get("tier_distribution", {})
    if tiers:
        lines.append("## Size Distribution")
        lines.append("")
        for tier in ("huge", "large", "medium", "small", "tiny"):
            count = tiers.get(tier, 0)
            lo, hi = SIZE_TIERS[tier]
            label = _fmt_kb(lo)
            if hi < float("inf"):
                label = f"{_fmt_kb(lo)} - {_fmt_kb(hi)}"
            else:
                label = f"> {_fmt_kb(lo)}"
            lines.append(f"- **{tier}** ({label}): {count}")
        lines.append("")

    top = result.get("top_largest", [])
    if top:
        lines.append("## Top 15 Largest Products")
        lines.append("")
        for i, entry in enumerate(top[:15], 1):
            status = "active" if entry["is_active"] else "orphan"
            waste_str = ""
            if entry.get("waste_kb", 0) > 0:
                waste_str = f" (waste: {_fmt_kb(entry['waste_kb'])})"
            lines.append(
                f"{i}. **{entry['slug']}** — {_fmt_kb(entry['size_kb'])} "
                f"[{status}]{waste_str}"
            )
        lines.append("")

    waste_breakdown = result.get("waste_breakdown_kb", {})
    if waste_breakdown:
        lines.append("## Waste Breakdown")
        lines.append("")
        for waste_type, kb in waste_breakdown.items():
            desc = WASTE_DIRS.get(waste_type, "")
            lines.append(f"- **{waste_type}**: {_fmt_kb(kb)} — {desc}")
        lines.append("")

    top_waste = result.get("top_waste", [])
    if top_waste:
        lines.append("## Top 10 Waste Contributors")
        lines.append("")
        for i, entry in enumerate(top_waste[:10], 1):
            if entry.get("waste_kb", 0) > 0:
                lines.append(
                    f"{i}. **{entry['slug']}** — {_fmt_kb(entry['waste_kb'])} "
                    f"waste ({', '.join(entry.get('waste_types', []))})"
                )
        lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    orphan_size = result.get("orphan_size_kb", 0)
    if orphan_size > 100:
        lines.append(
            f"- Orphan products use {_fmt_kb(orphan_size)} — "
            "run `orphan_cleanup_planner.py --apply-archive` to reclaim"
        )
    if waste_total > 100:
        lines.append(
            f"- {_fmt_kb(waste_total)} reclaimable from cache/build dirs"
        )
    huge = tiers.get("huge", 0)
    if huge > 0:
        lines.append(
            f"- {huge} products are >10MB — review for oversized assets or dependencies"
        )

    if not any(lines[-3:] if len(lines) > 3 else []):
        lines.append("- Portfolio size is healthy — no immediate action needed")

    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Product size analyzer")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--top", type=int, default=30, help="Top N largest (default 30)")
    parser.add_argument("--waste", action="store_true", help="Focus on waste report")
    args = parser.parse_args()

    result = scan_products(top=args.top)

    if args.waste:
        result.pop("top_largest", None)
        result["focus"] = "waste"

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_report(result))

    return result


if __name__ == "__main__":
    main()
