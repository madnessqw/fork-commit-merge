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
    },
    402: {
        "label": "deployment_disabled",
        "action": "Redeploy via Vercel CLI or dashboard; check billing",
    },
    404: {
        "label": "not_found",
        "action": "Verify deployment exists; re-link Vercel project to correct slug",
    },
    451: {
        "label": "geo_block",
        "action": "Check Vercel firewall/geo rules; may need region whitelist",
    },
    500: {
        "label": "server_error",
        "action": "Check Vercel build/runtime logs; redeploy if transient",
    },
    0: {"label": "timeout", "action": "Increase timeout or verify DNS resolution"},
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def _triage_entry(slug: str, code: int) -> dict:
    rule = TRIAGE_RULES.get(
        code, {"label": f"error_{code}", "action": "Investigate manually"}
    )
    return {
        "slug": slug,
        "http_code": code,
        "label": rule["label"],
        "suggested_action": rule["action"],
    }


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

    lines = [
        f"# Unhealthy Live Triage Report",
        f"**Generated:** {_utc_now_iso()} UTC",
        f"**Count:** {len(entries)}",
        "",
        "| Slug | HTTP | Label | Suggested Action |",
        "|------|------|-------|-----------------|",
    ]
    for e in entries:
        lines.append(
            f"| {e['slug']} | {e['http_code']} | {e['label']} | {e['suggested_action']} |"
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
