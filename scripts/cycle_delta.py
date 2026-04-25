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
    "needs_fix",
    "fallback_healthy",
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


def format_delta_telegram(delta: dict[str, Any]) -> str:
    """Format a delta dict as a compact Telegram-friendly line."""
    parts: list[str] = []
    direction = delta.get("direction", "?")
    emoji = "📈" if direction == "improving" else "📉" if direction == "degrading" else "➡️"
    parts.append(f"{emoji} {delta.get('older_cycle', '?')}→{delta.get('newer_cycle', '?')}")
    parts.append(f"HP {delta.get('health_pct_delta', 0):+.1f}%")
    changes = delta.get("changes", {})
    for key in METRIC_KEYS:
        if key in changes:
            c = changes[key]
            sign = "+" if c["delta"] > 0 else ""
            short = key[:3].upper()
            parts.append(f"{short}:{sign}{c['delta']}")
    return " | ".join(parts)


DELTA_OUTPUT_PATH = ROOT / "analysis" / "cycle_delta.md"


def health_streak_analysis(
    threshold: float = 100.0,
    trend_path: Path = TREND_FILE,
) -> dict[str, Any]:
    """Analyse health streaks from the trend log.

    Returns:
        current_streak: consecutive cycles at or above *threshold*
        longest_streak: longest such run
        total_perfect: total snapshots at or above threshold
        total_snapshots: total snapshots analysed
        pct_perfect: percentage of snapshots at threshold
        last_degradation: most recent snapshot below threshold (or None)
        first_snapshot_ts / last_snapshot_ts: time range
    """
    snapshots = _load_snapshots(trend_path)
    if not snapshots:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_perfect": 0,
            "total_snapshots": 0,
            "pct_perfect": 0.0,
            "last_degradation": None,
            "first_snapshot_ts": None,
            "last_snapshot_ts": None,
        }

    current = 0
    longest = 0
    total_perfect = 0
    last_degradation = None

    for snap in snapshots:
        pct = snap.get("health_pct", 0.0)
        if pct >= threshold:
            current += 1
            total_perfect += 1
        else:
            if current > longest:
                longest = current
            current = 0
            last_degradation = {
                "cycle": snap.get("cycle"),
                "ts": snap.get("ts"),
                "health_pct": pct,
                "unhealthy": snap.get("unhealthy", 0),
            }

    if current > longest:
        longest = current

    total = len(snapshots)
    return {
        "current_streak": current,
        "longest_streak": longest,
        "total_perfect": total_perfect,
        "total_snapshots": total,
        "pct_perfect": round(total_perfect / total * 100, 1) if total else 0.0,
        "last_degradation": last_degradation,
        "first_snapshot_ts": snapshots[0].get("ts"),
        "last_snapshot_ts": snapshots[-1].get("ts"),
    }


def format_streak_markdown(analysis: dict[str, Any]) -> str:
    lines = [
        "## Health Streak Analysis",
        f"**Snapshots:** {analysis['total_snapshots']} | "
        f"**Perfect:** {analysis['total_perfect']} ({analysis['pct_perfect']}%)",
        f"**Current streak:** {analysis['current_streak']} cycles @ 100%",
        f"**Longest streak:** {analysis['longest_streak']} cycles",
    ]
    deg = analysis.get("last_degradation")
    if deg:
        lines.append(
            f"**Last degradation:** cycle {deg['cycle']} "
            f"({deg['health_pct']}%, {deg.get('unhealthy', '?')} unhealthy) "
            f"@ {deg.get('ts', '?')}"
        )
    else:
        lines.append("**Last degradation:** none (all perfect)")
    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Cycle-over-cycle delta metrics")
    parser.add_argument("--last", type=int, default=2, help="Number of recent snapshots to compare (default: 2)")
    parser.add_argument("--write", action="store_true", help="Write markdown report to analysis/cycle_delta.md")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of markdown")
    parser.add_argument("--telegram", action="store_true", help="Compact Telegram-friendly output")
    parser.add_argument("--streak", action="store_true", help="Show health streak analysis")
    args = parser.parse_args()

    if args.streak:
        analysis = health_streak_analysis()
        if args.json:
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            print(format_streak_markdown(analysis))
        return analysis

    n = args.last
    deltas = last_n_deltas(n)
    if not deltas:
        print("No delta data available.")
        return {"error": "no_data"}

    if args.json:
        summary = delta_summary(n)
        print(json.dumps({"deltas": deltas, "summary": summary}, indent=2, ensure_ascii=False))
        return summary

    if args.telegram:
        for delta in deltas:
            print(format_delta_telegram(delta))
        return delta_summary(n)

    md_parts: list[str] = []
    for delta in deltas:
        md = format_delta_markdown(delta)
        md_parts.append(md)
        print(md)
        print()

    if args.write:
        full_md = "# Cycle Delta Report\n\n" + "\n\n".join(md_parts) + "\n"
        DELTA_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        DELTA_OUTPUT_PATH.write_text(full_md, encoding="utf-8")
        print(f"Written: {DELTA_OUTPUT_PATH}")

    summary = delta_summary(n)
    return summary


if __name__ == "__main__":
    main()
