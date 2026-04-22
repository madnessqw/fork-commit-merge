#!/usr/bin/env python3
"""Dispatch qa_pending to the qa-tester inbox and reconcile completed QA.

This is the missing hard trigger between .signals/qa_pending and the
qa-tester Claude subagent. It does two jobs:

1. When qa_pending exists, write a task into qa-tester + team-lead inboxes.
2. When a matching qa_result.md appears, clear the pending signal and
   reset the local team status snapshot.

The script is intentionally idempotent. Re-running it with the same pending
signal will not spam duplicate inbox messages.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any


TEAM_STATUS_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_inbox_message(inbox_path: Path, message: dict[str, Any]) -> None:
    payload = read_json(inbox_path, {"messages": []})
    if isinstance(payload, list):
        payload.append(message)
        write_json(inbox_path, payload)
        return

    messages = payload.get("messages")
    if not isinstance(messages, list):
        messages = []
        payload["messages"] = messages

    messages.append(message)
    write_json(inbox_path, payload)


def read_cycle(work_dir: Path) -> int:
    for candidate in (work_dir / "STATE_SUMMARY.json", work_dir / "STATE.json"):
        data = read_json(candidate, {})
        if isinstance(data, dict) and isinstance(data.get("cycle"), int):
            return int(data["cycle"])
    return 0


def load_pending(pending_path: Path) -> dict[str, Any] | None:
    if not pending_path.exists():
        return None
    data = read_json(pending_path, {})
    if not isinstance(data, dict):
        return None
    return data


def qa_result_matches_slug(result_path: Path, slug: str, pending_mtime: float) -> bool:
    if not result_path.exists():
        return False
    if result_path.stat().st_mtime < pending_mtime:
        return False
    try:
        content = result_path.read_text(encoding="utf-8")
    except Exception:
        return False
    return slug in content and "## Durum:" in content


def update_team_status(team_status_path: Path, cycle: int, slug: str, pending: bool) -> bool:
    if not team_status_path.exists():
        return False

    try:
        raw = team_status_path.read_text(encoding="utf-8")
        match = TEAM_STATUS_RE.search(raw)
        if not match:
            return False

        data = json.loads(match.group(1))
        if not isinstance(data, dict):
            return False

        data["cycle_count"] = cycle
        data["last_updated"] = utc_now()
        data.setdefault("signals", {})["qa_pending"] = pending
        teammates = data.setdefault("teammates", {})
        qa = teammates.setdefault("qa-tester", {})

        if pending:
            qa["status"] = "active"
            qa["last_prompt"] = utc_now()
            qa["prompt_count"] = int(qa.get("prompt_count", 0) or 0) + 1
            qa["last_slug"] = slug
        else:
            qa["status"] = "idle"
            qa["last_done"] = utc_now()

        new_raw = "```json\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n```\n"
        team_status_path.write_text(new_raw, encoding="utf-8")
        return True
    except Exception:
        return False


def dispatch_qa_pending(work_dir: Path, team_home: Path, dry_run: bool = False) -> str:
    signals_dir = work_dir / ".signals"
    pending_path = signals_dir / "qa_pending"
    dispatch_path = signals_dir / "qa_dispatch.json"
    qa_result_path = work_dir / "analysis" / "qa_result.md"
    team_status_path = work_dir / "analysis" / "team_status.md"
    team_inbox_dir = team_home / "inboxes"
    qa_inbox = team_inbox_dir / "qa-tester.json"
    lead_inbox = team_inbox_dir / "team-lead.json"

    pending = load_pending(pending_path)
    if not pending:
        if dispatch_path.exists() and qa_result_path.exists():
            dispatch_path.unlink(missing_ok=True)
            update_team_status(team_status_path, read_cycle(work_dir), "unknown", pending=False)
            return "NO_QA_PENDING_BUT_RESULT_EXISTS"
        return "NO_QA_PENDING"

    slug = str(pending.get("slug") or "unknown")
    pending_ts = str(pending.get("ts") or "")
    cycle = read_cycle(work_dir)
    pending_mtime = pending_path.stat().st_mtime

    if qa_result_matches_slug(qa_result_path, slug, pending_mtime):
        if not dry_run:
            pending_path.unlink(missing_ok=True)
            dispatch_path.unlink(missing_ok=True)
            update_team_status(team_status_path, cycle, slug, pending=False)
        return f"QA_COMPLETED slug={slug}"

    dispatch_state = read_json(dispatch_path, {})
    if isinstance(dispatch_state, dict) and dispatch_state.get("slug") == slug and dispatch_state.get("ts") == pending_ts:
        return f"QA_ALREADY_DISPATCHED slug={slug}"

    timestamp = utc_now()
    qa_message = {
        "from": "team-lead",
        "timestamp": timestamp,
        "cycle": cycle,
        "type": "qa_request",
        "slug": slug,
        "pending_ts": pending_ts,
        "message": (
            f"qa_pending detected for {slug}. "
            "Read skills/agents/qa_tester.md, analysis/codex_result.md, and "
            f"products/{slug}/spec.md if present. Run the QA checks, write "
            "analysis/qa_result.md, remove .signals/qa_pending, and if PASS "
            "write .signals/deploy_ready. Soru sorma."
        ),
        "read": False,
    }
    lead_message = {
        "from": "system",
        "timestamp": timestamp,
        "cycle": cycle,
        "type": "qa_dispatched",
        "slug": slug,
        "message": f"QA-TESTER dispatched for {slug}.",
        "read": False,
    }

    if not dry_run:
        team_inbox_dir.mkdir(parents=True, exist_ok=True)
        append_inbox_message(qa_inbox, qa_message)
        append_inbox_message(lead_inbox, lead_message)
        update_team_status(team_status_path, cycle, slug, pending=True)
        write_json(
            dispatch_path,
            {
                "slug": slug,
                "ts": pending_ts,
                "dispatched_at": timestamp,
                "cycle": cycle,
                "qa_inbox": str(qa_inbox),
            },
        )

    return f"QA_DISPATCHED slug={slug}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dispatch qa_pending to qa-tester.")
    parser.add_argument(
        "--work-dir",
        default=os.environ.get("UNIVERSECREATOR_HOME", "/home/gokhan/UniverseCreator"),
    )
    parser.add_argument(
        "--team-home",
        default=os.environ.get("CLAUDE_TEAM_HOME", str(Path.home() / ".claude/teams/universe-prime")),
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = dispatch_qa_pending(Path(args.work_dir), Path(args.team_home), dry_run=args.dry_run)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
