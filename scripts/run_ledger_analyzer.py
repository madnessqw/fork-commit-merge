#!/usr/bin/env python3
"""Analyze run_ledger.jsonl for agent performance, success rates, and trends.

Usage:
    python3 scripts/run_ledger_analyzer.py                    # Summary to stdout
    python3 scripts/run_ledger_analyzer.py --json              # JSON output
    python3 scripts/run_ledger_analyzer.py --by-agent          # Per-agent breakdown
    python3 scripts/run_ledger_analyzer.py --trend             # Success rate over time
    python3 scripts/run_ledger_analyzer.py --write             # Write to analysis/
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "logs" / "run_ledger.jsonl"
OUTPUT_PATH = ROOT / "analysis" / "run_ledger_summary.md"


def load_entries(ledger_path: Path = LEDGER_PATH) -> list[dict]:
    entries: list[dict] = []
    try:
        raw = ledger_path.read_text(encoding="utf-8").strip().splitlines()
    except OSError:
        return entries
    for line in raw:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def agent_name(run_id: str) -> str:
    if not run_id:
        return "unknown"
    prefix = run_id.split("-")[0].lower()
    mapping = {
        "codex": "codex",
        "glm": "glm",
        "kimi": "kimi",
        "claude": "claude",
        "ledger": "system",
    }
    return mapping.get(prefix, prefix)


def compute_summary(entries: list[dict]) -> dict:
    if not entries:
        return {"total": 0}

    total = len(entries)
    done = sum(1 for e in entries if e.get("status") == "done")
    fail = sum(1 for e in entries if e.get("status") == "fail")
    other = total - done - fail

    durations = [e.get("duration_min", 0) for e in entries if e.get("duration_min")]
    costs = [e.get("cost_est", 0) for e in entries if e.get("cost_est")]

    modes = Counter(e.get("mode", "UNKNOWN") for e in entries)
    agents = Counter(agent_name(e.get("run_id", "")) for e in entries)

    cycles = [e.get("cycle", 0) for e in entries if e.get("cycle")]
    cycle_min = min(cycles) if cycles else 0
    cycle_max = max(cycles) if cycles else 0

    return {
        "total": total,
        "done": done,
        "fail": fail,
        "other": other,
        "success_rate": round(done / total * 100, 1) if total else 0,
        "avg_duration_min": round(sum(durations) / len(durations), 1) if durations else 0,
        "total_cost_est": round(sum(costs), 2),
        "modes": dict(modes.most_common()),
        "agents": dict(agents.most_common()),
        "cycle_range": [cycle_min, cycle_max],
    }


def compute_by_agent(entries: list[dict]) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        name = agent_name(e.get("run_id", ""))
        grouped[name].append(e)

    result: dict[str, dict] = {}
    for name, agent_entries in sorted(grouped.items()):
        result[name] = compute_summary(agent_entries)
    return result


def compute_trend(entries: list[dict], window: int = 10) -> list[dict]:
    if len(entries) < window:
        window = len(entries)
    if window == 0:
        return []

    recent = entries[-window:]
    trend: list[dict] = []
    for e in recent:
        trend.append({
            "run_id": e.get("run_id", ""),
            "cycle": e.get("cycle", 0),
            "mode": e.get("mode", ""),
            "status": e.get("status", ""),
            "task": e.get("task", ""),
            "duration_min": e.get("duration_min", 0),
            "cost_est": e.get("cost_est", 0),
        })
    return trend


def summary_to_markdown(summary: dict) -> str:
    if summary.get("total", 0) == 0:
        return "No ledger entries found."

    lines = [
        "# Run Ledger Summary",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        "",
        f"**Total runs:** {summary['total']}",
        f"**Success:** {summary['done']} ({summary['success_rate']}%)",
        f"**Failed:** {summary['fail']} | **Other:** {summary['other']}",
        f"**Avg duration:** {summary['avg_duration_min']} min",
        f"**Total cost est:** ${summary['total_cost_est']}",
        f"**Cycle range:** {summary['cycle_range'][0]} → {summary['cycle_range'][1]}",
        "",
        "## By Mode",
    ]
    for mode, count in summary.get("modes", {}).items():
        lines.append(f"- {mode}: {count}")

    lines.append("")
    lines.append("## By Agent")
    for agent, count in summary.get("agents", {}).items():
        lines.append(f"- {agent}: {count}")

    return "\n".join(lines)


def by_agent_to_markdown(by_agent: dict[str, dict]) -> str:
    lines = [
        "# Run Ledger — Agent Breakdown",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        "",
    ]
    for name, data in by_agent.items():
        lines.append(f"## {name}")
        lines.append(f"- Runs: {data.get('total', 0)}")
        lines.append(f"- Success rate: {data.get('success_rate', 0)}%")
        lines.append(f"- Avg duration: {data.get('avg_duration_min', 0)} min")
        lines.append(f"- Total cost: ${data.get('total_cost_est', 0)}")
        lines.append("")

    return "\n".join(lines)


def trend_to_markdown(trend: list[dict]) -> str:
    lines = [
        "# Run Ledger — Recent Trend",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
        f"**Last {len(trend)} runs:**",
        "",
        "| # | Agent | Cycle | Mode | Status | Duration | Cost |",
        "|---|-------|-------|------|--------|----------|------|",
    ]
    for i, t in enumerate(trend, 1):
        agent = agent_name(t.get("run_id", ""))
        lines.append(
            f"| {i} | {agent} | {t.get('cycle', '')} | {t.get('mode', '')} | "
            f"{t.get('status', '')} | {t.get('duration_min', 0)}m | ${t.get('cost_est', 0):.2f} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ledger analyzer")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--by-agent", action="store_true", dest="by_agent")
    parser.add_argument("--trend", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--window", type=int, default=10)
    args = parser.parse_args()

    entries = load_entries()

    if args.as_json:
        print(json.dumps(compute_summary(entries), indent=2, ensure_ascii=False))
    elif args.by_agent:
        print(by_agent_to_markdown(compute_by_agent(entries)))
    elif args.trend:
        print(trend_to_markdown(compute_trend(entries, args.window)))
    elif args.write:
        md = summary_to_markdown(compute_summary(entries))
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(md, encoding="utf-8")
        print(f"Written: {OUTPUT_PATH}")
    else:
        print(summary_to_markdown(compute_summary(entries)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
