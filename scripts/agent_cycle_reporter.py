#!/usr/bin/env python3
"""Generate per-agent cycle productivity reports from run_ledger + git history.

Combines logs/run_ledger.jsonl with git commit data to produce:
  - Per-agent success rate, avg duration, task breakdown
  - Agent activity heatmap by hour
  - Cycle efficiency score (commits / runs)
  - Markdown report + Telegram summary

Usage:
    python3 scripts/agent_cycle_reporter.py
    python3 scripts/agent_cycle_reporter.py --json
    python3 scripts/agent_cycle_reporter.py --markdown
    python3 scripts/agent_cycle_reporter.py --telegram
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER_FILE = ROOT / "logs" / "run_ledger.jsonl"

AGENT_PATTERNS = [
    ("glm", re.compile(r"^glm\s*:", re.IGNORECASE)),
    ("codex", re.compile(r"^codex\s*:", re.IGNORECASE)),
    ("kimi", re.compile(r"^kimi\s*:", re.IGNORECASE)),
    ("claude", re.compile(r"^claude\s*:", re.IGNORECASE)),
]


def _identify_agent(msg: str) -> str:
    for name, pat in AGENT_PATTERNS:
        if pat.match(msg):
            return name
    return "unknown"


def load_ledger(limit: int = 200) -> list[dict[str, Any]]:
    if not LEDGER_FILE.exists():
        return []
    entries = []
    with open(LEDGER_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries[-limit:]


def load_git_commits(last: int = 100) -> list[dict[str, Any]]:
    try:
        result = subprocess.run(
            ["git", "log", f"-{last}", "--format=%H%x00%ai%x00%s"],
            capture_output=True, text=True, cwd=ROOT, timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\x00")
        if len(parts) < 3:
            continue
        h, date_str, msg = parts[0].strip(), parts[1].strip(), parts[2].strip()
        try:
            dt = datetime.fromisoformat(date_str.split("+")[0].strip())
        except (ValueError, IndexError):
            continue
        commits.append({
            "hash": h[:7],
            "date": dt.isoformat(),
            "message": msg,
            "agent": _identify_agent(msg),
            "hour": dt.hour,
        })
    return commits


def compute_ledger_stats(entries: list[dict]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "runs": 0,
        "success": 0,
        "fail": 0,
        "total_duration_min": 0.0,
        "total_cost": 0.0,
        "modes": Counter(),
        "tasks": [],
    })

    for e in entries:
        run_id = e.get("run_id", "")
        agent = "unknown"
        for name in ("glm", "codex", "kimi", "claude"):
            if run_id.startswith(name):
                agent = name
                break

        s = stats[agent]
        s["runs"] += 1
        status = e.get("status", "")
        if status in ("done", "success"):
            s["success"] += 1
        elif status in ("fail", "failure", "error"):
            s["fail"] += 1
        s["total_duration_min"] += e.get("duration_min", 0) or 0
        s["total_cost"] += e.get("cost_est", 0) or 0
        mode = e.get("mode", "")
        if mode:
            s["modes"][mode] += 1
        task = e.get("task", "")
        if task:
            s["tasks"].append(task[:60])

    result = {}
    for agent, data in stats.items():
        runs = data["runs"]
        result[agent] = {
            "runs": runs,
            "success_rate": round(data["success"] / runs * 100, 1) if runs else 0,
            "fail_count": data["fail"],
            "avg_duration_min": round(data["total_duration_min"] / runs, 1) if runs else 0,
            "total_cost": round(data["total_cost"], 2),
            "top_modes": dict(data["modes"].most_common(5)),
            "latest_tasks": data["tasks"][-3:],
        }
    return result


def compute_commit_stats(commits: list[dict]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "commits": 0,
        "hours": Counter(),
        "messages": [],
    })

    for c in commits:
        agent = c.get("agent", "unknown")
        s = stats[agent]
        s["commits"] += 1
        s["hours"][c.get("hour", 0)] += 1
        s["messages"].append(c.get("message", "")[:80])

    result = {}
    for agent, data in stats.items():
        peak = data["hours"].most_common(1)
        result[agent] = {
            "commits": data["commits"],
            "peak_hour": peak[0][0] if peak else None,
            "latest_messages": data["messages"][-3:],
        }
    return result


def compute_efficiency(
    ledger_stats: dict[str, dict],
    commit_stats: dict[str, dict],
) -> dict[str, dict[str, Any]]:
    result = {}
    all_agents = set(ledger_stats) | set(commit_stats)
    for agent in all_agents:
        ls = ledger_stats.get(agent, {})
        cs = commit_stats.get(agent, {})
        runs = ls.get("runs", 0)
        commits = cs.get("commits", 0)
        efficiency = round(commits / runs, 2) if runs > 0 else 0
        result[agent] = {
            "runs": runs,
            "commits": commits,
            "efficiency": efficiency,
            "success_rate": ls.get("success_rate", 0),
            "avg_duration_min": ls.get("avg_duration_min", 0),
        }
    return result


def format_markdown(
    ledger_stats: dict,
    commit_stats: dict,
    efficiency: dict,
) -> str:
    lines = [
        "# Agent Cycle Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Efficiency Summary",
        "",
        "| Agent | Runs | Commits | Efficiency | Success% | Avg Min |",
    ]
    lines.append("|-------|------|---------|------------|----------|---------|")
    for agent in sorted(efficiency):
        e = efficiency[agent]
        lines.append(
            f"| {agent} | {e['runs']} | {e['commits']} | "
            f"{e['efficiency']} | {e['success_rate']}% | {e['avg_duration_min']} |"
        )

    lines.append("")
    lines.append("## Ledger Stats")
    for agent in sorted(ledger_stats):
        s = ledger_stats[agent]
        modes = ", ".join(f"{k}({v})" for k, v in s.get("top_modes", {}).items())
        lines.append(f"### {agent}")
        lines.append(f"- Runs: {s['runs']} | Success: {s['success_rate']}% | Cost: ${s['total_cost']}")
        lines.append(f"- Modes: {modes or 'n/a'}")
        if s.get("latest_tasks"):
            for t in s["latest_tasks"]:
                lines.append(f"  - {t}")

    lines.append("")
    lines.append("## Commit Stats")
    for agent in sorted(commit_stats):
        s = commit_stats[agent]
        peak = s.get("peak_hour")
        peak_str = f"{peak:02d}:00" if isinstance(peak, int) else "n/a"
        lines.append(f"### {agent}")
        lines.append(f"- Commits: {s['commits']} | Peak hour: {peak_str}")

    return "\n".join(lines)


def format_telegram(efficiency: dict) -> str:
    parts = ["📊 <b>Agent Cycle Report</b>", ""]
    for agent in sorted(efficiency):
        e = efficiency[agent]
        parts.append(
            f"<b>{agent}</b>: {e['runs']} runs, {e['commits']} commits, "
            f"eff={e['efficiency']}, ok={e['success_rate']}%"
        )
    return "\n".join(parts)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Agent cycle productivity reporter")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--telegram", action="store_true")
    args = parser.parse_args()

    ledger = load_ledger()
    commits = load_git_commits()

    ledger_stats = compute_ledger_stats(ledger)
    commit_stats = compute_commit_stats(commits)
    efficiency = compute_efficiency(ledger_stats, commit_stats)

    if args.json:
        output = {
            "ledger_stats": ledger_stats,
            "commit_stats": commit_stats,
            "efficiency": efficiency,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return output

    if args.telegram:
        print(format_telegram(efficiency))
        return efficiency

    md = format_markdown(ledger_stats, commit_stats, efficiency)
    print(md)

    if args.markdown:
        out_path = ROOT / "analysis" / "agent_cycle_report.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8")
        print(f"\nWritten: {out_path}")

    return efficiency


if __name__ == "__main__":
    main()
