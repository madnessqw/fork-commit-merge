#!/usr/bin/env python3
"""Archive stale analysis files into date-partitioned subdirectories.

Moves files matching configurable age/pattern criteria from analysis/ into
analysis/archive/YYYY-MM/ to keep the working directory clean.

Usage:
    python3 scripts/analysis_archive.py --dry-run   # preview only
    python3 scripts/analysis_archive.py              # actually move
    python3 scripts/analysis_archive.py --age 48     # files older than 48h
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "analysis"
ARCHIVE_ROOT = ANALYSIS_DIR / "archive"

ARCHIVE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^kimi_rapor_\d{8}_\d{4}\.md$"),
    re.compile(r"^polar_checkout_plan_cycle\d+\.md$"),
    re.compile(r"^polar_checkout_sync_report_\d{8}_\d{4}\.md$"),
    re.compile(r"^polar_checkout_plan_\d{8}_\d{4}\.md$"),
    re.compile(r"^polar_plan_cycle\d+\.md$"),
    re.compile(r"^unhealthy_report_\d+\.md$"),
    re.compile(r"^cycle_\d+_plan\.md$"),
)

PROTECTED_FILES: frozenset[str] = frozenset({
    "oneri.md",
    "glm_fix_brief.md",
    "glm_code_result.md",
    "codex_task.md",
    "codex_result.md",
    "sorun_analizi.md",
    "team_status.md",
    "qa_result.md",
    "kullanici_gereksinim.md",
    "oneri_cycle967.md",
})

DEFAULT_MAX_AGE_HOURS = 24


def _is_archivable(name: str) -> bool:
    if name in PROTECTED_FILES:
        return False
    return any(p.match(name) for p in ARCHIVE_PATTERNS)


def _archive_dest(mtime: float) -> Path:
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return ARCHIVE_ROOT / f"{dt.year:04d}-{dt.month:02d}"


def scan_archivable(
    max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
) -> list[dict[str, Any]]:
    if not ANALYSIS_DIR.exists():
        return []
    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=max_age_hours)
    results: list[dict[str, Any]] = []
    for f in ANALYSIS_DIR.iterdir():
        if not f.is_file() or not _is_archivable(f.name):
            continue
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            results.append({
                "path": f,
                "name": f.name,
                "mtime": mtime,
                "dest_dir": _archive_dest(f.stat().st_mtime),
                "size_kb": round(f.stat().st_size / 1024, 1),
            })
    results.sort(key=lambda x: x["mtime"])
    return results


def archive_files(
    max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
    dry_run: bool = False,
) -> dict[str, Any]:
    files = scan_archivable(max_age_hours)
    moved = 0
    freed_kb = 0.0
    errors: list[str] = []

    for entry in files:
        dest_dir: Path = entry["dest_dir"]
        dest_file = dest_dir / entry["name"]
        if dry_run:
            moved += 1
            freed_kb += entry["size_kb"]
            continue
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(entry["path"]), str(dest_file))
            moved += 1
            freed_kb += entry["size_kb"]
        except Exception as exc:
            errors.append(f"{entry['name']}: {exc}")

    return {
        "total_scanned": len(files),
        "moved": moved,
        "freed_kb": round(freed_kb, 1),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive stale analysis files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    parser.add_argument("--age", type=int, default=DEFAULT_MAX_AGE_HOURS, help="Min age in hours")
    args = parser.parse_args()

    result = archive_files(max_age_hours=args.age, dry_run=args.dry_run)
    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"[{mode}] Archived {result['moved']}/{result['total_scanned']} files, {result['freed_kb']} KB")
    if result["errors"]:
        for e in result["errors"]:
            print(f"  ERROR: {e}", file=sys.stderr)
    if result["moved"] == 0:
        print("Nothing to archive.")


if __name__ == "__main__":
    main()
