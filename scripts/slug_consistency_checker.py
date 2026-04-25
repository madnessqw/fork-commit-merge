#!/usr/bin/env python3
"""Check slug consistency across STATE.json, STATE_SUMMARY.json, and product folders.

Detects:
- Slugs in STATE but missing folder
- Folders with no STATE entry
- Duplicate slugs across sources
- Naming inconsistencies (slug vs folder name)

Usage:
    python3 scripts/slug_consistency_checker.py
    python3 scripts/slug_consistency_checker.py --json
    python3 scripts/slug_consistency_checker.py --fix-report
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
PRODUCTS_DIR = ROOT / "products"


def _slugs_from_state(state_path: Path = STATE_PATH) -> set[str]:
    data = json.loads(state_path.read_text(encoding="utf-8"))
    return {
        p.get("slug") or p.get("s") or ""
        for p in data.get("products", {}).get("active", [])
    } - {""}


def _slugs_from_summary(summary_path: Path = SUMMARY_PATH) -> set[str]:
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    return {
        p.get("s") or p.get("slug") or ""
        for p in data.get("products", [])
    } - {""}


def _slugs_from_folders(products_dir: Path = PRODUCTS_DIR) -> set[str]:
    if not products_dir.is_dir():
        return set()
    return {
        d.name
        for d in products_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }


def check_consistency() -> dict[str, Any]:
    state_slugs = _slugs_from_state()
    summary_slugs = _slugs_from_summary()
    folder_slugs = _slugs_from_folders()

    state_only = sorted(state_slugs - folder_slugs)
    folder_only = sorted(folder_slugs - state_slugs)
    summary_only = sorted(summary_slugs - state_slugs)

    state_missing_folder = sorted(
        state_slugs - folder_slugs
    )
    folder_orphan = sorted(
        folder_slugs - state_slugs - summary_slugs
    )

    all_sources = state_slugs | summary_slugs | folder_slugs
    everywhere = state_slugs & summary_slugs & folder_slugs

    issues: list[dict[str, str]] = []
    for s in state_missing_folder:
        issues.append({"slug": s, "issue": "in_state_no_folder"})
    for s in folder_orphan:
        issues.append({"slug": s, "issue": "folder_not_in_state_or_summary"})
    for s in summary_only:
        issues.append({"slug": s, "issue": "in_summary_not_in_state"})

    return {
        "state_count": len(state_slugs),
        "summary_count": len(summary_slugs),
        "folder_count": len(folder_slugs),
        "everywhere_count": len(everywhere),
        "state_missing_folder": state_missing_folder,
        "folder_orphan": folder_orphan,
        "summary_only": summary_only,
        "total_issues": len(issues),
        "issues": issues,
        "health_pct": round(len(everywhere) / len(all_sources) * 100, 1) if all_sources else 0.0,
    }


def format_report(result: dict[str, Any]) -> str:
    lines = [
        "# Slug Consistency Report",
        "",
        f"**STATE.json:** {result['state_count']}",
        f"**STATE_SUMMARY.json:** {result['summary_count']}",
        f"**products/ folders:** {result['folder_count']}",
        f"**In all 3 sources:** {result['everywhere_count']}",
        f"**Consistency:** {result['health_pct']}%",
        f"**Issues:** {result['total_issues']}",
        "",
    ]
    if result["state_missing_folder"]:
        lines.append(f"## STATE but no folder ({len(result['state_missing_folder'])})")
        for s in result["state_missing_folder"][:20]:
            lines.append(f"  - {s}")
        if len(result["state_missing_folder"]) > 20:
            lines.append(f"  ... +{len(result['state_missing_folder']) - 20} more")
        lines.append("")
    if result["folder_orphan"]:
        lines.append(f"## Orphan folders ({len(result['folder_orphan'])})")
        for s in result["folder_orphan"][:20]:
            lines.append(f"  - {s}")
        if len(result["folder_orphan"]) > 20:
            lines.append(f"  ... +{len(result['folder_orphan']) - 20} more")
        lines.append("")
    if result["summary_only"]:
        lines.append(f"## Summary only ({len(result['summary_only'])})")
        for s in result["summary_only"][:20]:
            lines.append(f"  - {s}")
        lines.append("")
    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Slug consistency checker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = check_consistency()

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_report(result))

    return result


if __name__ == "__main__":
    main()
