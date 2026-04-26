#!/usr/bin/env python3
"""Generate cleanup plans from orphan scanner results.

Reads orphan scan data (or runs scanner) and produces actionable cleanup
plans: archive dead products, integrate deployable ones, flag spec-only
orphans for review.

Usage:
    python3 scripts/orphan_cleanup_planner.py
    python3 scripts/orphan_cleanup_planner.py --json
    python3 scripts/orphan_cleanup_planner.py --apply-archive
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = ROOT / "products" / "_archived"

CATEGORY_ACTION = {
    "dead": "archive",
    "minimal": "archive",
    "has_spec": "review",
    "has_code": "review",
    "deployable": "integrate",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def plan_cleanup(orphans: list[dict[str, Any]]) -> dict[str, Any]:
    plans: dict[str, list[dict[str, Any]]] = {
        "archive": [],
        "review": [],
        "integrate": [],
    }
    total_reclaimable = 0

    for orphan in orphans:
        cat = orphan.get("category", "dead")
        action = CATEGORY_ACTION.get(cat, "archive")
        slug = orphan["slug"]
        size_kb = orphan.get("size_kb", 0)

        entry: dict[str, Any] = {
            "slug": slug,
            "category": cat,
            "action": action,
            "size_kb": size_kb,
        }

        if cat in ("dead", "minimal"):
            entry["reason"] = "no valuable content"
            total_reclaimable += int(orphan.get("size_bytes", size_kb * 1024))
        elif cat == "has_spec":
            entry["reason"] = "has spec but no code — evaluate for building"
        elif cat == "has_code":
            entry["reason"] = "has code but no vercel config — needs deploy setup"
        elif cat == "deployable":
            entry["reason"] = "code + vercel config present — candidate for STATE restore"

        plans[action].append(entry)

    return {
        "ts": _utc_now_iso(),
        "total_orphans": len(orphans),
        "archive_count": len(plans["archive"]),
        "review_count": len(plans["review"]),
        "integrate_count": len(plans["integrate"]),
        "reclaimable_bytes": total_reclaimable,
        "reclaimable_mb": round(total_reclaimable / 1024 / 1024, 1),
        "plans": plans,
    }


def apply_archive(plan_result: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
    archive_entries = plan_result.get("plans", {}).get("archive", [])
    if not archive_entries:
        return {"archived": 0, "dry_run": dry_run}

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archived: list[str] = []
    errors: list[str] = []

    for entry in archive_entries:
        slug = entry["slug"]
        src = ROOT / "products" / slug
        dst = ARCHIVE_DIR / slug

        if not src.is_dir():
            errors.append(f"{slug}: source dir missing")
            continue

        if dst.exists():
            errors.append(f"{slug}: already archived")
            continue

        if dry_run:
            archived.append(slug)
        else:
            try:
                shutil.move(str(src), str(dst))
                archived.append(slug)
            except OSError as e:
                errors.append(f"{slug}: {e}")

    return {
        "archived": len(archived),
        "archived_slugs": archived,
        "errors": errors,
        "dry_run": dry_run,
    }


def format_plan(plan_result: dict[str, Any]) -> str:
    lines = [
        "# Orphan Cleanup Plan",
        f"**Generated:** {plan_result['ts']}",
        f"**Total orphans:** {plan_result['total_orphans']}",
        "",
    ]

    if plan_result.get("reclaimable_mb"):
        lines.append(f"**Reclaimable space:** {plan_result['reclaimable_mb']} MB")
        lines.append("")

    for action in ("archive", "review", "integrate"):
        items = plan_result.get("plans", {}).get(action, [])
        count = len(items)
        label = action.upper()
        lines.append(f"## {label} ({count})")
        lines.append("")
        if not items:
            lines.append("  (none)")
        else:
            for item in items[:20]:
                lines.append(f"  - **{item['slug']}** [{item['category']}] — {item['reason']}")
            if count > 20:
                lines.append(f"  ... +{count - 20} more")
        lines.append("")

    lines.append("## Next Steps")
    lines.append("")
    ac = plan_result.get("archive_count", 0)
    ic = plan_result.get("integrate_count", 0)
    rc = plan_result.get("review_count", 0)
    if ac:
        lines.append(f"- Run `--apply-archive` to move {ac} dead/minimal dirs to `_archived/`")
    if ic:
        lines.append(f"- Review {ic} deployable orphans for STATE.json reintegration")
    if rc:
        lines.append(f"- Evaluate {rc} spec/code orphans for build or archive")

    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Orphan cleanup planner")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--apply-archive", action="store_true", help="Actually archive dead/minimal dirs")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview only (default)")
    args = parser.parse_args()

    from scripts.portfolio_orphan_scanner import scan_orphans

    scan_result = scan_orphans(calc_size=True)
    orphans = scan_result.get("orphans", [])

    plan_result = plan_cleanup(orphans)

    if args.apply_archive:
        archive_result = apply_archive(plan_result, dry_run=args.dry_run)
        plan_result["archive_result"] = archive_result

    if args.json:
        print(json.dumps(plan_result, indent=2, ensure_ascii=False))
    else:
        print(format_plan(plan_result))

    return plan_result


if __name__ == "__main__":
    main()
