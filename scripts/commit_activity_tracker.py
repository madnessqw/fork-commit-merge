#!/usr/bin/env python3
"""Track commit activity per agent from git history.

Parses git log to produce per-agent commit statistics: frequency,
files changed, lines added/removed, and time-of-day patterns.
Useful for Z.AI coding plan compliance monitoring and agent productivity analysis.

Usage:
    python3 scripts/commit_activity_tracker.py                # last 50 commits
    python3 scripts/commit_activity_tracker.py --last 200     # last 200 commits
    python3 scripts/commit_activity_tracker.py --json         # JSON output
    python3 scripts/commit_activity_tracker.py --markdown     # Markdown report
    python3 scripts/commit_activity_tracker.py --by-day       # Daily breakdown
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

AGENT_PATTERNS = [
    ("glm", re.compile(r"^glm\s*:", re.IGNORECASE)),
    ("codex", re.compile(r"^codex\s*:", re.IGNORECASE)),
    ("kimi", re.compile(r"^kimi\s*:", re.IGNORECASE)),
    ("claude", re.compile(r"^claude\s*:", re.IGNORECASE)),
]


def _identify_agent(message: str) -> str:
    for name, pattern in AGENT_PATTERNS:
        if pattern.match(message):
            return name
    return "unknown"


def _parse_git_log(last: int = 50, repo_path: Path = ROOT) -> list[dict[str, Any]]:
    fmt = "%H%x00%ai%x00%s%x00"
    try:
        result = subprocess.run(
            ["git", "log", f"--last={last}", f"--format={fmt}", "--shortstat"],
            capture_output=True,
            text=True,
            cwd=repo_path,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    if result.returncode != 0:
        fmt_simple = "%H%x00%ai%x00%s"
        try:
            result = subprocess.run(
                ["git", "log", f"-{last}", f"--format={fmt_simple}"],
                capture_output=True,
                text=True,
                cwd=repo_path,
                timeout=30,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []

    commits: list[dict[str, Any]] = []
    lines = result.stdout.strip().split("\n") if result.stdout.strip() else []

    for line in lines:
        if not line.strip():
            continue
        parts = line.split("\x00")
        if len(parts) < 3:
            continue
        commit_hash = parts[0].strip()
        date_str = parts[1].strip()
        message = parts[2].strip()

        try:
            dt = datetime.fromisoformat(date_str.split("+")[0].strip())
        except (ValueError, IndexError):
            continue

        agent = _identify_agent(message)
        commits.append({
            "hash": commit_hash[:7],
            "date": dt.isoformat(),
            "message": message,
            "agent": agent,
        })

    return commits


def _parse_git_log_with_stats(last: int = 50, repo_path: Path = ROOT) -> list[dict[str, Any]]:
    try:
        result = subprocess.run(
            ["git", "log", f"-{last}", "--format=%H%x00%ai%x00%s", "--numstat"],
            capture_output=True,
            text=True,
            cwd=repo_path,
            timeout=60,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    if result.returncode != 0:
        return []

    commits: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in result.stdout.split("\n"):
        if not line.strip():
            continue

        if "\x00" in line:
            if current:
                commits.append(current)
            parts = line.split("\x00")
            if len(parts) < 3:
                current = None
                continue
            commit_hash = parts[0].strip()
            date_str = parts[1].strip()
            message = parts[2].strip()

            try:
                dt = datetime.fromisoformat(date_str.split("+")[0].strip())
            except (ValueError, IndexError):
                current = None
                continue

            agent = _identify_agent(message)
            current = {
                "hash": commit_hash[:7],
                "date": dt.isoformat(),
                "message": message,
                "agent": agent,
                "files_changed": 0,
                "lines_added": 0,
                "lines_removed": 0,
                "file_list": [],
            }
        elif current:
            stat_parts = line.split("\t")
            if len(stat_parts) == 3:
                try:
                    added = int(stat_parts[0]) if stat_parts[0] != "-" else 0
                    removed = int(stat_parts[1]) if stat_parts[1] != "-" else 0
                    current["lines_added"] += added
                    current["lines_removed"] += removed
                    current["files_changed"] += 1
                    current["file_list"].append(stat_parts[2])
                except ValueError:
                    pass

    if current:
        commits.append(current)

    return commits


def compute_agent_stats(commits: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "commits": 0,
        "files_changed": 0,
        "lines_added": 0,
        "lines_removed": 0,
        "first_commit": None,
        "last_commit": None,
        "messages": [],
        "file_types": Counter(),
        "hour_distribution": Counter(),
    })

    for c in commits:
        agent = c["agent"]
        s = stats[agent]
        s["commits"] += 1
        s["files_changed"] += c.get("files_changed", 0)
        s["lines_added"] += c.get("lines_added", 0)
        s["lines_removed"] += c.get("lines_removed", 0)

        dt_str = c.get("date", "")
        if dt_str:
            try:
                dt = datetime.fromisoformat(dt_str)
                if s["first_commit"] is None:
                    s["first_commit"] = dt_str
                s["last_commit"] = dt_str
                s["hour_distribution"][dt.hour] += 1
            except ValueError:
                pass

        s["messages"].append(c.get("message", "")[:80])

        for f in c.get("file_list", []):
            ext = Path(f).suffix.lower()
            if ext:
                s["file_types"][ext] += 1

    result: dict[str, dict[str, Any]] = {}
    for agent, data in stats.items():
        result[agent] = {
            "commits": data["commits"],
            "files_changed": data["files_changed"],
            "lines_added": data["lines_added"],
            "lines_removed": data["lines_removed"],
            "first_commit": data["first_commit"],
            "last_commit": data["last_commit"],
            "top_file_types": dict(data["file_types"].most_common(5)),
            "peak_hour": data["hour_distribution"].most_common(1)[0][0] if data["hour_distribution"] else None,
            "latest_messages": data["messages"][-3:],
        }

    return result


def compute_daily_breakdown(commits: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    daily: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "total_commits": 0,
        "agents": Counter(),
        "files_changed": 0,
        "lines_added": 0,
    })

    for c in commits:
        dt_str = c.get("date", "")
        if not dt_str:
            continue
        try:
            dt = datetime.fromisoformat(dt_str)
        except ValueError:
            continue

        day_key = dt.strftime("%Y-%m-%d")
        d = daily[day_key]
        d["total_commits"] += 1
        d["agents"][c["agent"]] += 1
        d["files_changed"] += c.get("files_changed", 0)
        d["lines_added"] += c.get("lines_added", 0)

    result: dict[str, dict[str, Any]] = {}
    for day, data in sorted(daily.items()):
        result[day] = {
            "total_commits": data["total_commits"],
            "agents": dict(data["agents"]),
            "files_changed": data["files_changed"],
            "lines_added": data["lines_added"],
        }

    return result


def compute_summary(commits: list[dict[str, Any]]) -> dict[str, Any]:
    if not commits:
        return {"total_commits": 0, "agents": {}, "error": "no commits"}

    agent_counter = Counter(c["agent"] for c in commits)
    total_files = sum(c.get("files_changed", 0) for c in commits)
    total_added = sum(c.get("lines_added", 0) for c in commits)
    total_removed = sum(c.get("lines_removed", 0) for c in commits)

    first_date = commits[-1].get("date", "?") if commits else "?"
    last_date = commits[0].get("date", "?") if commits else "?"

    return {
        "total_commits": len(commits),
        "total_files_changed": total_files,
        "total_lines_added": total_added,
        "total_lines_removed": total_removed,
        "date_range": f"{first_date[:10]} → {last_date[:10]}",
        "agent_breakdown": dict(agent_counter),
        "most_active_agent": agent_counter.most_common(1)[0][0] if agent_counter else None,
    }


def format_markdown_report(
    agent_stats: dict[str, dict[str, Any]],
    summary: dict[str, Any],
) -> str:
    lines = [
        "# Commit Activity Report",
        f"**Period:** {summary.get('date_range', '?')}",
        f"**Total commits:** {summary.get('total_commits', 0)}",
        f"**Files changed:** {summary.get('total_files_changed', 0)}",
        f"**Lines added/removed:** +{summary.get('total_lines_added', 0)}/-{summary.get('total_lines_removed', 0)}",
        "",
        "## Agent Breakdown",
        "",
        "| Agent | Commits | Files | +Lines | -Lines | Peak Hour |",
        "|-------|---------|-------|--------|--------|-----------|",
    ]

    for agent in sorted(agent_stats):
        s = agent_stats[agent]
        peak = s.get("peak_hour", "?")
        if isinstance(peak, int):
            peak = f"{peak:02d}:00"
        lines.append(
            f"| {agent} | {s['commits']} | {s['files_changed']} | "
            f"+{s['lines_added']} | -{s['lines_removed']} | {peak} |"
        )

    lines.append("")
    most_active = summary.get("most_active_agent", "?")
    lines.append(f"**Most active agent:** {most_active}")

    for agent, s in agent_stats.items():
        top_types = s.get("top_file_types", {})
        if top_types:
            types_str = ", ".join(f"{ext}({cnt})" for ext, cnt in top_types.items())
            lines.append(f"- **{agent}** top file types: {types_str}")

    return "\n".join(lines)


def format_telegram_summary(summary: dict[str, Any], agent_stats: dict[str, dict[str, Any]]) -> str:
    parts = [
        f"📊 <b>Commit Activity</b>",
        f"Total: {summary.get('total_commits', 0)} commits | +{summary.get('total_lines_added', 0)}/-{summary.get('total_lines_removed', 0)} lines",
    ]
    for agent in sorted(agent_stats):
        s = agent_stats[agent]
        parts.append(f"  {agent}: {s['commits']} commits, {s['files_changed']} files, +{s['lines_added']}/-{s['lines_removed']}")
    return "\n".join(parts)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Track commit activity per agent")
    parser.add_argument("--last", type=int, default=50, help="Number of recent commits to analyse")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--markdown", action="store_true", help="Output as Markdown")
    parser.add_argument("--telegram", action="store_true", help="Compact Telegram-friendly output")
    parser.add_argument("--by-day", action="store_true", help="Daily breakdown")
    args = parser.parse_args()

    commits = _parse_git_log_with_stats(args.last)

    if not commits:
        fallback_commits = _parse_git_log(args.last)
        if fallback_commits:
            commits = fallback_commits

    if not commits:
        print("No commits found.")
        return {"error": "no_commits"}

    agent_stats = compute_agent_stats(commits)
    summary = compute_summary(commits)

    if args.json:
        output = {"summary": summary, "agents": agent_stats}
        if args.by_day:
            output["daily"] = compute_daily_breakdown(commits)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return output

    if args.telegram:
        print(format_telegram_summary(summary, agent_stats))
        return summary

    if args.by_day:
        daily = compute_daily_breakdown(commits)
        print(json.dumps(daily, indent=2, ensure_ascii=False))
        return {"daily": daily, "summary": summary}

    md = format_markdown_report(agent_stats, summary)
    print(md)

    if args.markdown:
        output_path = ROOT / "analysis" / "commit_activity.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(md, encoding="utf-8")
        print(f"\nWritten: {output_path}")

    return summary


if __name__ == "__main__":
    main()
