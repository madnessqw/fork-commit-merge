#!/usr/bin/env python3
"""Cycle-over-cycle delta metrics from health_trend.jsonl.

Reads the last N snapshots and computes what changed between cycles,
making it easy to see if the portfolio is improving, stable, or degrading.

Usage:
    python3 scripts/cycle_delta.py          # last 2 snapshots
    python3 scripts/cycle_delta.py --last 5  # last 5 snapshots
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TREND_FILE = ROOT / "logs" / "health_trend.jsonl"

METRIC_KEYS = (
    "live",
    "healthy",
    "unhealthy",
    "checkout_gap",
    "deploy_gap",
    "canonical_drift",
)


def _load_snapshots(trend_path: Path = TREND_FILE) -> list[dict[str, Any]]:
    if not trend_path.exists():
        return []
    snapshots: list[dict[str, Any]] = []
    for line in trend_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            snapshots.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return snapshots


def compute_delta(
    older: dict[str, Any],
    newer: dict[str, Any],
) -> dict[str, Any]:
    """Compute the delta between two snapshots.

    Returns a dict with:
        - ``older_cycle``, ``newer_cycle``: cycle identifiers
        - ``older_ts``, ``newer_ts``: timestamps
        - ``health_pct_delta``: signed float change in health percentage
        - ``changes``: dict of metric -> {old, new, delta} for changed metrics
        - ``direction``: "improving" | "degrading" | "stable"
    """
    changes: dict[str, dict[str, Any]] = {}
    for key in METRIC_KEYS:
        old_val = older.get(key, 0)
        new_val = newer.get(key, 0)
        if old_val != new_val:
            changes[key] = {
                "old": old_val,
                "new": new_val,
                "delta": new_val - old_val,
            }

    old_pct = older.get("health_pct", 0.0)
    new_pct = newer.get("health_pct", 0.0)
    pct_delta = round(new_pct - old_pct, 1)

    if pct_delta > 0.5:
        direction = "improving"
    elif pct_delta < -0.5:
        direction = "degrading"
    else:
        direction = "stable"

    return {
        "older_cycle": older.get("cycle"),
        "newer_cycle": newer.get("cycle"),
        "older_ts": older.get("ts"),
        "newer_ts": newer.get("ts"),
        "health_pct_delta": pct_delta,
        "changes": changes,
        "direction": direction,
    }


def last_n_deltas(
    n: int = 2,
    trend_path: Path = TREND_FILE,
) -> list[dict[str, Any]]:
    """Return deltas for the last N consecutive snapshot pairs.

    Returns up to (n-1) delta records (n snapshots yield n-1 pairs).
    Ordered oldest-to-newest.
    """
    snapshots = _load_snapshots(trend_path)
    if len(snapshots) < 2:
        return []

    tail = snapshots[-(n):]
    deltas: list[dict[str, Any]] = []
    for i in range(len(tail) - 1):
        deltas.append(compute_delta(tail[i], tail[i + 1]))
    return deltas


def delta_summary(
    n: int = 2,
    trend_path: Path = TREND_FILE,
) -> dict[str, Any]:
    """Produce a single summary delta between the (n)-th last and most recent snapshot.

    Useful for a one-line status report.
    """
    snapshots = _load_snapshots(trend_path)
    if len(snapshots) < 2:
        return {"error": "insufficient data", "snapshot_count": len(snapshots)}

    older = snapshots[-n] if n <= len(snapshots) else snapshots[0]
    newer = snapshots[-1]
    delta = compute_delta(older, newer)

    return {
        "from_cycle": delta["older_cycle"],
        "to_cycle": delta["newer_cycle"],
        "direction": delta["direction"],
        "health_pct_delta": delta["health_pct_delta"],
        "total_changes": len(delta["changes"]),
        "changes": delta["changes"],
    }


def format_delta_markdown(delta: dict[str, Any]) -> str:
    """Format a delta dict as a short markdown table."""
    lines = [
        f"## Cycle Delta: {delta.get('older_cycle', '?')} → {delta.get('newer_cycle', '?')}",
        f"**Direction:** {delta.get('direction', '?')} | "
        f"**Health Δ:** {delta.get('health_pct_delta', 0):+.1f}%",
        "",
    ]

    changes = delta.get("changes", {})
    if not changes:
        lines.append("_No metric changes._")
        return "\n".join(lines)

    lines.append("| Metric | Old | New | Delta |")
    lines.append("|--------|-----|-----|-------|")
    for key in METRIC_KEYS:
        if key in changes:
            c = changes[key]
            sign = "+" if c["delta"] > 0 else ""
            lines.append(
                f"| {key} | {c['old']} | {c['new']} | {sign}{c['delta']} |"
            )

    return "\n".join(lines)


def main() -> dict[str, Any]:
    n = 2
    if len(sys.argv) > 1 and sys.argv[1] == "--last":
        try:
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        except ValueError:
            n = 5

    deltas = last_n_deltas(n)
    if not deltas:
        print("No delta data available.")
        return {"error": "no_data"}

    for delta in deltas:
        print(format_delta_markdown(delta))
        print()

    summary = delta_summary(n)
    return summary


if __name__ == "__main__":
    main()
