#!/usr/bin/env python3
"""Vercel auth and deployment pipeline monitor.

Checks Vercel authentication status, Codex auth state, and deployment
pipeline health.  Produces a diagnostic report and optional JSON output
for downstream tooling.

Usage:
    python3 scripts/vercel_auth_monitor.py
    python3 scripts/vercel_auth_monitor.py --json
    python3 scripts/vercel_auth_monitor.py --log          # append to logs/auth_monitor.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SIGNALS_DIR = ROOT / ".signals"
AUTH_STATE_PATH = SIGNALS_DIR / "codex_auth_state.json"
HEALTH_SIGNAL_PATH = SIGNALS_DIR / "health.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
AUTH_LOG_DIR = ROOT / "logs"
AUTH_LOG_PATH = AUTH_LOG_DIR / "auth_monitor.jsonl"


@dataclass
class VercelAuthStatus:
    vercel_cli_available: bool = False
    vercel_token_env: bool = False
    vercel_token_preview: str = ""
    vercel_whoami: str = ""
    vercel_whoami_ok: bool = False


@dataclass
class CodexAuthStatus:
    preferred_account: int = 0
    last_result: str = ""
    reason: str = ""
    account_1_status: str = "unknown"
    account_2_status: str = "unknown"
    blocked: bool = False
    blocked_until: str = ""
    switch_count: int = 0
    last_error_snippet: str = ""


@dataclass
class DeploymentPipelineStatus:
    total_products: int = 0
    live_products: int = 0
    healthy_products: int = 0
    deploy_gap: int = 0
    vercel_auth_issue: bool = False
    next_action: str = ""


@dataclass
class AuthMonitorReport:
    timestamp: str = ""
    vercel: VercelAuthStatus = field(default_factory=VercelAuthStatus)
    codex: CodexAuthStatus = field(default_factory=CodexAuthStatus)
    pipeline: DeploymentPipelineStatus = field(default_factory=DeploymentPipelineStatus)
    blockers: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _truncate(s: str, max_len: int = 120) -> str:
    if len(s) <= max_len:
        return s
    return s[:max_len - 3] + "..."


def check_vercel_auth() -> VercelAuthStatus:
    status = VercelAuthStatus()

    try:
        result = subprocess.run(
            ["vercel", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        status.vercel_cli_available = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        status.vercel_cli_available = False

    token = os.environ.get("VERCEL_TOKEN", "")
    status.vercel_token_env = bool(token)
    if token:
        status.vercel_token_preview = token[:8] + "..." if len(token) > 8 else "***"

    if status.vercel_cli_available:
        try:
            env = os.environ.copy()
            if token:
                env["VERCEL_TOKEN"] = token
            result = subprocess.run(
                ["vercel", "whoami"],
                capture_output=True, text=True, timeout=15,
                env=env,
            )
            output = (result.stdout or "") + (result.stderr or "")
            status.vercel_whoami = output.strip()
            status.vercel_whoami_ok = result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    return status


def check_codex_auth() -> CodexAuthStatus:
    status = CodexAuthStatus()

    if AUTH_STATE_PATH.exists():
        try:
            data = json.loads(AUTH_STATE_PATH.read_text())
            status.preferred_account = data.get("preferred_account", 0)
            status.last_result = data.get("last_result", "")
            status.reason = data.get("reason", "")
            status.account_1_status = data.get("account_1_status", "unknown")
            status.account_2_status = data.get("account_2_status", "unknown")
            status.switch_count = data.get("switch_count", 0)

            err = data.get("last_error", "")
            status.last_error_snippet = _truncate(err)

            blocked_keywords = ("usage limit", "blocked", "upgrade to pro")
            if any(kw in err.lower() for kw in blocked_keywords):
                status.blocked = True

            for keyword in ("until", "blocked_until"):
                for part in err.split():
                    if "apr" in part.lower() and "2026" in part:
                        status.blocked_until = part
                        break
                if status.blocked_until:
                    break

            for phrase in err.split(". "):
                lower = phrase.lower()
                if "try again at" in lower or "blocked until" in lower:
                    for word in phrase.split():
                        if word.startswith("Apr"):
                            status.blocked_until = word
                            break
        except (json.JSONDecodeError, KeyError):
            pass

    return status


def check_deployment_pipeline() -> DeploymentPipelineStatus:
    status = DeploymentPipelineStatus()

    if SUMMARY_PATH.exists():
        try:
            data = json.loads(SUMMARY_PATH.read_text())
            status.total_products = data.get("active_count", 0)
            status.live_products = data.get("live_count", 0)
            status.healthy_products = data.get("healthy_count", 0)
            status.deploy_gap = data.get("deploy_missing_or_bad_url", 0)
            status.vercel_auth_issue = data.get("vercel_auth_issue", False)
            status.next_action = data.get("next_action", "")
        except (json.JSONDecodeError, KeyError):
            pass

    return status


def build_report() -> AuthMonitorReport:
    report = AuthMonitorReport(timestamp=_utc_now_iso())
    report.vercel = check_vercel_auth()
    report.codex = check_codex_auth()
    report.pipeline = check_deployment_pipeline()

    if report.codex.blocked:
        report.blockers.append(
            f"Codex usage limit blocked (until ~{report.codex.blocked_until})"
        )

    if report.pipeline.vercel_auth_issue:
        report.blockers.append("Vercel auth issue flagged in STATE_SUMMARY")

    if not report.vercel.vercel_cli_available:
        report.blockers.append("Vercel CLI not installed or not in PATH")

    if report.blockers:
        if report.codex.blocked:
            report.recommendations.append(
                "Wait for Codex usage limit reset (~Apr 28) or upgrade to Pro"
            )
        if report.pipeline.vercel_auth_issue:
            report.recommendations.append(
                "Re-authenticate Vercel: vercel login or update VERCEL_TOKEN"
            )
        if not report.vercel.vercel_cli_available:
            report.recommendations.append(
                "Install Vercel CLI: npm i -g vercel"
            )
    else:
        report.recommendations.append(
            "All systems operational — continue normal cycle"
        )

    return report


def format_report(report: AuthMonitorReport) -> str:
    lines = [
        f"=== Vercel Auth Monitor — {report.timestamp} ===",
        "",
        "--- Vercel CLI ---",
        f"  CLI available: {report.vercel.vercel_cli_available}",
        f"  Token in env:  {report.vercel.vercel_token_env}",
    ]
    if report.vercel.vercel_token_preview:
        lines.append(f"  Token preview: {report.vercel.vercel_token_preview}")
    if report.vercel.vercel_whoami:
        lines.append(f"  whoami:        {report.vercel.vercel_whoami}")
    lines.append(f"  whoami OK:     {report.vercel.vercel_whoami_ok}")

    lines.extend([
        "",
        "--- Codex Auth ---",
        f"  Preferred account: {report.codex.preferred_account}",
        f"  Last result:       {report.codex.last_result}",
        f"  Account 1:         {report.codex.account_1_status}",
        f"  Account 2:         {report.codex.account_2_status}",
        f"  Blocked:           {report.codex.blocked}",
        f"  Blocked until:     {report.codex.blocked_until or 'N/A'}",
        f"  Switch count:      {report.codex.switch_count}",
    ])
    if report.codex.last_error_snippet:
        lines.append(f"  Last error:        {report.codex.last_error_snippet}")

    lines.extend([
        "",
        "--- Deployment Pipeline ---",
        f"  Products:          {report.pipeline.total_products} total, "
        f"{report.pipeline.live_products} live, "
        f"{report.pipeline.healthy_products} healthy",
        f"  Deploy gap:        {report.pipeline.deploy_gap}",
        f"  Vercel auth issue: {report.pipeline.vercel_auth_issue}",
    ])
    if report.pipeline.next_action:
        lines.append(f"  Next action:       {report.pipeline.next_action}")

    if report.blockers:
        lines.extend(["", "--- Active Blockers ---"])
        for i, b in enumerate(report.blockers, 1):
            lines.append(f"  {i}. {b}")

    if report.recommendations:
        lines.extend(["", "--- Recommendations ---"])
        for r in report.recommendations:
            lines.append(f"  -> {r}")

    return "\n".join(lines)


def report_to_dict(report: AuthMonitorReport) -> dict[str, Any]:
    d: dict[str, Any] = {
        "timestamp": report.timestamp,
        "blockers": report.blockers,
        "recommendations": report.recommendations,
        "vercel": asdict(report.vercel),
        "codex": asdict(report.codex),
        "pipeline": asdict(report.pipeline),
    }
    return d


def append_log(report: AuthMonitorReport) -> None:
    AUTH_LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = report_to_dict(report)
    with AUTH_LOG_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vercel auth and pipeline monitor")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--log", action="store_true", help="Append to auth log")
    args = parser.parse_args(argv)

    report = build_report()

    if args.json:
        print(json.dumps(report_to_dict(report), indent=2))
    else:
        print(format_report(report))

    if args.log:
        append_log(report)

    return 1 if report.blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
