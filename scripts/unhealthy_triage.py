#!/usr/bin/env python3
"""
Triage report generator for unhealthy live products.

Reads STATE_SUMMARY.json, categorises each unhealthy item by HTTP code,
and produces a short remediation brief that downstream agents (GLM, Codex)
can act on immediately.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRIAGE_RULES = {
    401: {
        "label": "sso_protection",
        "action": "Check Vercel project settings -> disable Vercel Authentication",
        "severity": "high",
    },
    402: {
        "label": "deployment_disabled",
        "action": "Redeploy via Vercel CLI or dashboard; check billing",
        "severity": "medium",
    },
    404: {
        "label": "not_found",
        "action": "Verify deployment exists; re-link Vercel project to correct slug",
        "severity": "medium",
    },
    451: {
        "label": "geo_block",
        "action": "Check Vercel firewall/geo rules; may need region whitelist",
        "severity": "low",
    },
    500: {
        "label": "server_error",
        "action": "Check Vercel build/runtime logs; redeploy if transient",
        "severity": "high",
    },
    0: {
        "label": "timeout",
        "action": "Increase timeout or verify DNS resolution",
        "severity": "medium",
    },
}

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def _triage_entry(slug: str, code: int) -> dict:
    rule = TRIAGE_RULES.get(
        code,
        {
            "label": f"error_{code}",
            "action": "Investigate manually",
            "severity": "medium",
        },
    )
    return {
        "slug": slug,
        "http_code": code,
        "label": rule["label"],
        "suggested_action": rule["action"],
        "severity": rule.get("severity", "medium"),
    }


def sort_by_severity(entries: list[dict]) -> list[dict]:
    return sorted(
        entries, key=lambda e: SEVERITY_ORDER.get(e.get("severity", "medium"), 1)
    )


def generate_triage(summary_path: Path | None = None) -> list[dict]:
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"
    with open(summary_path, encoding="utf-8") as f:
        summary = json.load(f)

    unhealthy = summary.get("gaps", {}).get("unhealthy_live", [])
    entries = []
    for item in unhealthy:
        code = item.get("code", 0)
        if isinstance(code, str) and code.isdigit():
            code = int(code)
        entries.append(_triage_entry(item.get("slug", "unknown"), code))
    return entries


def write_triage_report(entries: list[dict], output_path: Path | None = None) -> str:
    if output_path is None:
        output_path = ROOT / "analysis" / "unhealthy_triage.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sorted_entries = sort_by_severity(entries)
    lines = [
        f"# Unhealthy Live Triage Report",
        f"**Generated:** {_utc_now_iso()} UTC",
        f"**Count:** {len(sorted_entries)}",
        "",
        "| Slug | HTTP | Label | Severity | Suggested Action |",
        "|------|------|-------|----------|-----------------|",
    ]
    for e in sorted_entries:
        lines.append(
            f"| {e['slug']} | {e['http_code']} | {e['label']} | {e['severity']} | {e['suggested_action']} |"
        )
    lines.append("")
    if sorted_entries:
        high_count = sum(1 for e in sorted_entries if e.get("severity") == "high")
        med_count = sum(1 for e in sorted_entries if e.get("severity") == "medium")
        low_count = sum(1 for e in sorted_entries if e.get("severity") == "low")
        lines.append(
            f"**Severity breakdown:** {high_count} high / {med_count} medium / {low_count} low"
        )
        lines.append("")

    report = "\n".join(lines)
    output_path.write_text(report, encoding="utf-8")
    return report


def main():
    entries = generate_triage()
    if not entries:
        print("All live products healthy.")
        return {"unhealthy": 0}

    report = write_triage_report(entries)
    print(report)
    return {"unhealthy": len(entries)}


if __name__ == "__main__":
    result = main()
    sys.exit(1 if result["unhealthy"] > 0 else 0)
