#!/usr/bin/env python3
"""Analyze Codex cycle efficiency from run_ledger.jsonl.

Reports success/fail rates, average duration, cost, mode distribution,
and identifies bottlenecks or repeated stuck tasks.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LEDGER_FILE = ROOT / "logs" / "run_ledger.jsonl"


def load_entries(limit: int = 0) -> list[dict]:
    if not LEDGER_FILE.exists():
        return []
    entries: list[dict] = []
    with open(LEDGER_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if limit > 0:
        entries = entries[-limit:]
    return entries


def _pct(part: int, whole: int) -> float:
    return round(part / whole * 100, 1) if whole > 0 else 0.0


def summary(entries: list[dict] | None = None, *, window: int = 0) -> dict:
    if entries is None:
        entries = load_entries()
    if window > 0:
        entries = entries[-window:]
    if not entries:
        return {"total": 0}

    total = len(entries)
    status_counts: dict[str, int] = Counter(e.get("status", "unknown") for e in entries)
    done = status_counts.get("done", 0)
    fail = status_counts.get("fail", 0) + status_counts.get("failed", 0)

    durations = [e.get("duration_min", 0) for e in entries if e.get("duration_min")]
    avg_dur = round(sum(durations) / len(durations), 1) if durations else 0
    max_dur = max(durations) if durations else 0
    min_dur = min(durations) if durations else 0

    costs = [e.get("cost_est", 0) for e in entries if e.get("cost_est")]
    total_cost = round(sum(costs), 2) if costs else 0
    avg_cost = round(total_cost / len(costs), 3) if costs else 0

    mode_counts: dict[str, int] = Counter(e.get("mode", "unknown") for e in entries)
    slug_counts: dict[str, int] = Counter(e.get("slug", "") for e in entries if e.get("slug"))
    top_slugs = slug_counts.most_common(5)

    return {
        "total": total,
        "done": done,
        "fail": fail,
        "other": total - done - fail,
        "success_rate": _pct(done, total),
        "avg_duration_min": avg_dur,
        "min_duration_min": min_dur,
        "max_duration_min": max_dur,
        "total_cost_est": total_cost,
        "avg_cost_est": avg_cost,
        "modes": dict(mode_counts),
        "top_slugs": top_slugs,
    }


def repeated_tasks(entries: list[dict] | None = None, *, min_repeats: int = 3) -> dict:
    if entries is None:
        entries = load_entries()
    if not entries:
        return {"repeated": [], "total_entries": 0}

    task_counts: dict[str, int] = Counter(e.get("task", "") for e in entries if e.get("task"))
    repeated = [
        {"task": task, "count": count}
        for task, count in task_counts.most_common()
        if count >= min_repeats
    ]

    return {
        "repeated": repeated[:10],
        "total_entries": len(entries),
        "unique_tasks": len(task_counts),
    }


def recent_failures(entries: list[dict] | None = None, *, limit: int = 10) -> dict:
    if entries is None:
        entries = load_entries()
    failures = [
        {
            "run_id": e.get("run_id", ""),
            "task": e.get("task", ""),
            "slug": e.get("slug", ""),
            "mode": e.get("mode", ""),
            "ts": e.get("ts", ""),
        }
        for e in entries
        if e.get("status") in ("fail", "failed")
    ]
    return {"fail_count": len(failures), "recent": failures[-limit:]}


def daily_breakdown(entries: list[dict] | None = None) -> dict:
    if entries is None:
        entries = load_entries()
    if not entries:
        return {"days": {}, "total_days": 0}

    day_data: dict[str, dict] = {}
    for e in entries:
        ts = e.get("ts", e.get("run_id", ""))
        day = ts[:10] if len(ts) >= 10 else "unknown"
        if day not in day_data:
            day_data[day] = {"total": 0, "done": 0, "fail": 0, "cost": 0.0}
        day_data[day]["total"] += 1
        if e.get("status") in ("done",):
            day_data[day]["done"] += 1
        if e.get("status") in ("fail", "failed"):
            day_data[day]["fail"] += 1
        day_data[day]["cost"] += e.get("cost_est", 0)

    for d in day_data.values():
        d["cost"] = round(d["cost"], 2)

    return {"days": day_data, "total_days": len(day_data)}


def main() -> int:
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "repeated":
            print(json.dumps(repeated_tasks(), indent=2, ensure_ascii=False))
            return 0
        if cmd == "failures":
            print(json.dumps(recent_failures(), indent=2, ensure_ascii=False))
            return 0
        if cmd == "daily":
            print(json.dumps(daily_breakdown(), indent=2, ensure_ascii=False))
            return 0
        if cmd == "summary":
            w = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            print(json.dumps(summary(window=w), indent=2, ensure_ascii=False))
            return 0

    s = summary()
    rep = repeated_tasks(min_repeats=4)
    fails = recent_failures(limit=3)
    print(json.dumps({"summary": s, "repeated_tasks": rep, "recent_failures": fails}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
