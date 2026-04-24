#!/usr/bin/env python3
"""
Portfolio health dashboard — terminal-friendly CLI summary.

Reads STATE_SUMMARY.json and produces a colour-coded dashboard
showing live/healthy counts, grade, checkout coverage, deploy gap,
canonical drift, and per-category breakdowns.

Usage:
    python3 scripts/health_dashboard.py           # full dashboard
    python3 scripts/health_dashboard.py --compact  # one-line summary
    python3 scripts/health_dashboard.py --json     # machine-readable
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.summary_visibility import canonical_drift_count, canonical_drift_entries


BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

GRADE_COLORS = {
    "A": GREEN,
    "B": CYAN,
    "C": YELLOW,
    "D": RED,
    "F": RED,
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _pct(value: float) -> str:
    return f"{value:.1f}%"


def _grade(pct: float) -> str:
    if pct >= 95:
        return "A"
    if pct >= 85:
        return "B"
    if pct >= 70:
        return "C"
    if pct >= 50:
        return "D"
    return "F"


def _bar(pct: float, width: int = 20) -> str:
    filled = int(pct / 100 * width)
    empty = width - filled
    color = GREEN if pct >= 95 else CYAN if pct >= 85 else YELLOW if pct >= 70 else RED
    return f"{color}{'█' * filled}{DIM}{'░' * empty}{RESET}"


def _status_icon(ok: bool) -> str:
    return f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"


def load_summary(path: Path | None = None) -> dict:
    if path is None:
        path = ROOT / "STATE_SUMMARY.json"
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def compute_metrics(summary: dict) -> dict:
    live = summary.get("live_count", 0)
    healthy = summary.get("healthy_count", 0)
    active = summary.get("active_count", 0)
    unhealthy = summary.get("unhealthy_count", 0)
    pending = summary.get("pending_health_count", 0)

    health_pct = round(healthy / live * 100, 1) if live > 0 else 0.0
    grade = _grade(health_pct)

    checkout_gap = summary.get("checkout_gap_count", 0)
    deploy_gap = summary.get("deploy_missing_or_bad_url", 0)
    drift = canonical_drift_count(summary)
    needs_fix = summary.get("needs_fix_count", 0)
    spec_ready = summary.get("spec_ready_count", 0)
    deploy_ready = summary.get("deploy_readiness_count", 0)

    gaps = summary.get("gaps", {})
    unhealthy_live = gaps.get("unhealthy_live", [])
    drift_entries = canonical_drift_entries(summary)

    return {
        "active": active,
        "live": live,
        "healthy": healthy,
        "unhealthy": unhealthy,
        "pending": pending,
        "health_pct": health_pct,
        "grade": grade,
        "checkout_ok": checkout_gap == 0,
        "checkout_gap": checkout_gap,
        "deploy_gap": deploy_gap,
        "canonical_drift": drift,
        "needs_fix": needs_fix,
        "spec_ready": spec_ready,
        "deploy_ready": deploy_ready,
        "unhealthy_live": unhealthy_live,
        "drift_entries": drift_entries,
        "cycle": summary.get("cycle", 0),
        "mode": summary.get("mode", "?"),
    }


def render_compact(m: dict) -> str:
    gc = GRADE_COLORS.get(m["grade"], RESET)
    check = _status_icon(m["checkout_ok"])
    health = f"{m['healthy']}/{m['live']}"
    return (
        f"{BOLD}Portfolio{RESET} {gc}{m['grade']}{RESET} "
        f"{_bar(m['health_pct'], 10)} "
        f"{health} ({_pct(m['health_pct'])}) "
        f"{check}CO "
        f"DG:{m['deploy_gap']} "
        f"CD:{m['canonical_drift']} "
        f"NF:{m['needs_fix']}"
    )


def render_full(m: dict) -> str:
    gc = GRADE_COLORS.get(m["grade"], RESET)
    lines = [
        "",
        f"{BOLD}{'═' * 52}{RESET}",
        f"{BOLD}  UNIVERSECREATOR PORTFOLIO HEALTH DASHBOARD{RESET}",
        f"  {_utc_now_iso()} | Cycle {m['cycle']} | Mode: {m['mode']}",
        f"{BOLD}{'═' * 52}{RESET}",
        "",
        f"  {BOLD}GRADE{RESET}  {gc}{BOLD}{m['grade']}{RESET}  {_bar(m['health_pct'], 30)}  {_pct(m['health_pct'])}",
        "",
        f"  {BOLD}PRODUCTS{RESET}",
        f"    Active:   {m['active']}",
        f"    Live:     {m['live']}",
        f"    Healthy:  {GREEN}{m['healthy']}{RESET}",
        f"    Unhealthy:{RED}{m['unhealthy']}{RESET}",
        f"    Pending:  {YELLOW}{m['pending']}{RESET}",
        "",
        f"  {BOLD}COVERAGE{RESET}",
        f"    Checkout: {_status_icon(m['checkout_ok'])}  {('gap: ' + str(m['checkout_gap'])) if m['checkout_gap'] else 'full coverage'}",
        f"    Deploy:   {YELLOW}{m['deploy_gap']}{RESET} missing/bad URL",
        f"    Drift:    {YELLOW}{m['canonical_drift']}{RESET} canonical URL drift",
        f"    Needs fix:{RED}{m['needs_fix']}{RESET}",
        "",
        f"  {BOLD}PIPELINE{RESET}",
        f"    Spec ready:    {CYAN}{m['spec_ready']}{RESET}",
        f"    Deploy ready:  {CYAN}{m['deploy_ready']}{RESET}",
        "",
    ]

    if m["unhealthy_live"]:
        lines.append(f"  {BOLD}{RED}UNHEALTHY LIVE{RESET}")
        for item in m["unhealthy_live"][:8]:
            slug = item.get("slug", "?")
            code = item.get("code", "?")
            lines.append(f"    {RED}•{RESET} {slug:30s} HTTP {code}")
        if len(m["unhealthy_live"]) > 8:
            lines.append(f"    {DIM}... +{len(m['unhealthy_live']) - 8} more{RESET}")
        lines.append("")

    if m["drift_entries"]:
        lines.append(f"  {BOLD}{YELLOW}CANONICAL DRIFT{RESET}")
        for item in m["drift_entries"][:6]:
            slug = item.get("slug", "?")
            url = item.get("url", "")
            ideal = item.get("ideal_url", "")
            short_url = url.replace("https://", "") if url else "?"
            short_ideal = ideal.replace("https://", "") if ideal else "?"
            lines.append(f"    {YELLOW}•{RESET} {slug:25s} {short_url} → {short_ideal}")
        if len(m["drift_entries"]) > 6:
            lines.append(f"    {DIM}... +{len(m['drift_entries']) - 6} more{RESET}")
        lines.append("")

    lines.append(f"{BOLD}{'═' * 52}{RESET}")
    lines.append("")
    return "\n".join(lines)


def render_json(m: dict) -> str:
    export = {k: v for k, v in m.items() if k not in ("unhealthy_live", "drift_entries")}
    export["unhealthy_live_count"] = len(m.get("unhealthy_live", []))
    export["drift_entries_count"] = len(m.get("drift_entries", []))
    export["unhealthy_slugs"] = [
        i.get("slug", "?") for i in m.get("unhealthy_live", [])
    ]
    export["drift_slugs"] = [
        i.get("slug", "?") for i in m.get("drift_entries", [])
    ]
    return json.dumps(export, indent=2)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Portfolio health dashboard")
    parser.add_argument("--compact", action="store_true", help="One-line summary")
    parser.add_argument("--json", action="store_true", dest="json_output", help="JSON output")
    args = parser.parse_args(argv)

    summary = load_summary()
    if not summary:
        print(f"{RED}ERROR: STATE_SUMMARY.json not found or empty{RESET}", file=sys.stderr)
        return 1

    m = compute_metrics(summary)

    if args.json_output:
        print(render_json(m))
    elif args.compact:
        print(render_compact(m))
    else:
        print(render_full(m))

    return 0


if __name__ == "__main__":
    sys.exit(main())
