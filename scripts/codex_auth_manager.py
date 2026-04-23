#!/usr/bin/env python3
"""Manage Codex account preference for the UniverseCreator loop.

This helper keeps the Codex auth loop deterministic:

- remember the last preferred account
- try that account first on the next cycle
- if usage-limit / high-demand style errors happen, switch to the other one
- persist the new preferred account for the next cycle

The loop script uses this helper so account switching is stateful instead of
hard-coded "1 then 2" forever.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


DEFAULT_STATE_FILE = Path("/home/gokhan/UniverseCreator/.signals/codex_auth_state.json")
AUTH_SWITCH_PATTERNS = (
    "usage limit",
    "high demand",
    "reconnecting",
    "429",
    "rate limit",
)


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def normalize_account(value: Any) -> int:
    try:
        account = int(str(value).strip())
    except Exception:
        return 1
    return 1 if account == 1 else 2 if account == 2 else 1


def other_account(account: Any) -> int:
    return 2 if normalize_account(account) == 1 else 1


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

    return data if isinstance(data, dict) else {}


def save_state(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def choose_state(path: Path) -> dict[str, Any]:
    state = load_state(path)
    preferred = normalize_account(
        state.get("preferred_account", state.get("last_active_account", 1))
    )
    fallback = other_account(preferred)
    return {
        "preferred_account": preferred,
        "fallback_account": fallback,
        "state": state,
    }


def record_state(
    path: Path,
    *,
    preferred_account: Any,
    active_account: Any,
    attempted_accounts: list[Any],
    outcome: str,
    cycle: int = 0,
    exit_code: int = 0,
    last_error: str = "",
) -> dict[str, Any]:
    state = load_state(path)
    preferred = normalize_account(preferred_account)
    active = normalize_account(active_account)
    attempted = [normalize_account(a) for a in attempted_accounts] or [preferred]

    state["preferred_account"] = active if outcome != "failure" else preferred
    state["last_active_account"] = active
    state["last_attempted_accounts"] = attempted
    state["last_result"] = outcome
    state["last_error"] = last_error
    state["last_exit_code"] = int(exit_code)
    state["cycle"] = int(cycle)
    state["updated_at"] = utc_now()

    if outcome.startswith("auth_switch"):
        state["last_switch_from_account"] = preferred
        state["last_switch_to_account"] = active
        state["last_switch_reason"] = last_error or "auth_limit"
        state["switch_count"] = int(state.get("switch_count", 0) or 0) + 1
    elif outcome == "failure":
        state["last_failure_account"] = preferred
        state["last_failure_reason"] = last_error
    else:
        state["last_success_account"] = active

    save_state(path, state)
    return state


def classify_output(output: str, exit_code: int) -> str:
    text = output.lower()
    if any(pattern in text for pattern in AUTH_SWITCH_PATTERNS):
        return "auth_switch"
    if exit_code != 0:
        return "failure"
    return "success"


def init_state(path: Path, preferred: int = 1) -> dict[str, Any]:
    state = load_state(path)
    if state:
        return state
    now = utc_now()
    state = {
        "preferred_account": normalize_account(preferred),
        "last_active_account": normalize_account(preferred),
        "last_attempted_accounts": [normalize_account(preferred)],
        "last_result": "initialized",
        "last_error": "",
        "last_exit_code": 0,
        "switch_count": 0,
        "cycle": 0,
        "created_at": now,
        "updated_at": now,
    }
    save_state(path, state)
    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage Codex auth preference state.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Initialize state file if missing."
    )
    init_parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Path to the JSON state file.",
    )
    init_parser.add_argument(
        "--preferred", type=int, default=1, help="Preferred account (1 or 2)."
    )

    choose_parser = subparsers.add_parser(
        "choose", help="Print the preferred and fallback accounts."
    )
    choose_parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Path to the JSON state file.",
    )
    choose_parser.add_argument("--format", choices=("json", "shell"), default="shell")

    record_parser = subparsers.add_parser(
        "record", help="Persist the result of a Codex cycle."
    )
    record_parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Path to the JSON state file.",
    )
    record_parser.add_argument("--preferred-account", required=True)
    record_parser.add_argument("--active-account", required=True)
    record_parser.add_argument("--outcome", required=True)
    record_parser.add_argument("--cycle", type=int, default=0)
    record_parser.add_argument("--exit-code", type=int, default=0)
    record_parser.add_argument("--last-error", default="")
    record_parser.add_argument("--attempted-accounts", nargs="+", required=True)

    classify_parser = subparsers.add_parser(
        "classify", help="Classify raw Codex output."
    )
    classify_parser.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Path to the JSON state file.",
    )
    classify_parser.add_argument("--exit-code", type=int, default=0)
    classify_parser.add_argument("--text", default="")
    classify_parser.add_argument("--text-file", default="")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state_file = Path(args.state_file)

    if args.command == "init":
        state = init_state(state_file, preferred=args.preferred)
        print(json.dumps(state, ensure_ascii=False))
        return 0

    if args.command == "choose":
        chosen = choose_state(state_file)
        if args.format == "json":
            print(json.dumps(chosen, ensure_ascii=False))
        else:
            print(f"{chosen['preferred_account']} {chosen['fallback_account']}")
        return 0

    if args.command == "record":
        state = record_state(
            state_file,
            preferred_account=args.preferred_account,
            active_account=args.active_account,
            attempted_accounts=args.attempted_accounts,
            outcome=args.outcome,
            cycle=args.cycle,
            exit_code=args.exit_code,
            last_error=args.last_error,
        )
        print(json.dumps(state, ensure_ascii=False))
        return 0

    if args.command == "classify":
        text = args.text
        if args.text_file:
            text = Path(args.text_file).read_text(encoding="utf-8")
        print(classify_output(text, args.exit_code))
        return 0

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
