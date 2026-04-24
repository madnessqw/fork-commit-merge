#!/usr/bin/env python3
"""Generic STATE.json updater — CLI-driven, no hardcoded values."""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


def load_state(path="STATE.json"):
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def save_state(state, path="STATE.json"):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)
    return state


def update_cycle(state, cycle=None):
    if cycle is not None:
        state["cycle"] = cycle
    state["timestamp"] = datetime.now(timezone.utc).isoformat()
    return state


def update_message(state, message=None, next_priority=None):
    if message:
        state["message"] = message
    if next_priority:
        state["next_priority"] = next_priority
    return state


def set_agent_status(state, names, status):
    agents = state.get("team", {}).get("agents", [])
    updated = 0
    for agent in agents:
        if agent.get("name") in names:
            agent["status"] = status
            updated += 1
    return state, updated


def add_learning(state, text):
    state.setdefault("learnings", []).append(text)
    return state


def main():
    parser = argparse.ArgumentParser(description="Update STATE.json generically")
    parser.add_argument("--state-file", default="STATE.json", help="Path to STATE.json")
    parser.add_argument("--cycle", type=int, help="Set cycle number")
    parser.add_argument("--message", help="Set status message")
    parser.add_argument("--next-priority", help="Set next priority")
    parser.add_argument("--agent-status", nargs=2, metavar=("NAMES", "STATUS"),
                        help="Set agent statuses (comma-separated names, status)")
    parser.add_argument("--learning", help="Add a learning entry")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    args = parser.parse_args()

    state = load_state(args.state_file)
    state = update_cycle(state, args.cycle)
    state = update_message(state, args.message, args.next_priority)

    updated_agents = 0
    if args.agent_status:
        names = [n.strip() for n in args.agent_status[0].split(",")]
        status = args.agent_status[1]
        state, updated_agents = set_agent_status(state, names, status)

    if args.learning:
        state = add_learning(state, args.learning)

    if args.dry_run:
        print(json.dumps(state, indent=2))
        return

    save_state(state, args.state_file)
    print(f"STATE.json updated | cycle={state.get('cycle')} | agents_updated={updated_agents}")


if __name__ == "__main__":
    main()
