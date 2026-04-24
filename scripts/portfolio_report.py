#!/usr/bin/env python3
"""
Unified portfolio report generator.

Combines health score, triage, price audit, and checkout coverage into a
single CLI command so downstream agents (GLM, Codex) can get a full picture
without running four separate scripts.

Usage:
    python3 scripts/portfolio_report.py [--json] [--markdown]
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.unhealthy_triage import (
    generate_triage,
    portfolio_health_score,
    sort_by_severity,
    triage_summary,
)
from scripts.price_audit import audit_product_prices
from scripts.checkout_duplicate_detector import detect_duplicates


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def _checkout_coverage(summary: dict) -> dict:
    live = summary.get("live_count", 0)
    gap = summary.get("checkout_gap_count", 0)
    covered = live - gap if live > 0 else 0
    pct = round(covered / live * 100, 1) if live > 0 else 0.0
    missing = summary.get("gaps", {}).get("missing_checkout", [])
    return {
        "live_count": live,
        "covered_count": covered,
        "gap_count": gap,
        "coverage_pct": pct,
        "missing_slugs": [m if isinstance(m, str) else m.get("slug", "") for m in missing],
    }


def generate_report(summary_path: Path | None = None) -> dict:
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"
    try:
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"error": "STATE_SUMMARY.json unreadable", "ts": _utc_now_iso()}

    health = portfolio_health_score(summary_path)
    triage = triage_summary(summary_path)
    checkout = _checkout_coverage(summary)
    try:
        price_issues = audit_product_prices(summary_path)
    except Exception:
        price_issues = []
    try:
        dup_result = detect_duplicates()
        checkout_dups = dup_result.get("duplicate_checkout_urls", {})
    except Exception:
        checkout_dups = {}

    deploy_gap = summary.get("deploy_missing_or_bad_url", 0)
    canonical_drift = len(summary.get("gaps", {}).get("canonical_url_drift", []))

    return {
        "ts": _utc_now_iso(),
        "cycle": summary.get("cycle", 0),
        "mode": summary.get("mode", "UNKNOWN"),
        "health": health,
        "triage": {
            "total_unhealthy": triage.get("total_unhealthy", 0),
            "high": triage.get("high", 0),
            "medium": triage.get("medium", 0),
            "low": triage.get("low", 0),
            "top_high_slugs": triage.get("top_high_slugs", []),
            "codex_handoff": triage.get("codex_handoff_recommended", False),
        },
        "checkout": checkout,
        "price_issues_count": len(price_issues) if isinstance(price_issues, list) else 0,
        "checkout_duplicates": len(checkout_dups),
        "deploy_gap": deploy_gap,
        "canonical_drift": canonical_drift,
        "active_products": summary.get("active_count", 0),
        "live_products": summary.get("live_count", 0),
    }


def format_markdown(report: dict) -> str:
    lines = [
        "# Portfolio Report",
        f"**Generated:** {report.get('ts', '?')} | **Cycle:** {report.get('cycle', '?')}",
        f"**Mode:** {report.get('mode', '?')}",
        "",
        "## Health Overview",
        f"- Grade: **{report['health'].get('grade', '?')}** ({report['health'].get('health_pct', 0)}%)",
        f"- Live: {report.get('live_products', 0)} | Healthy: {report['health'].get('healthy_count', 0)}",
        f"- Unhealthy: {report['health'].get('unhealthy_count', 0)}",
        f"- Deploy gap: {report.get('deploy_gap', 0)} | Canonical drift: {report.get('canonical_drift', 0)}",
        "",
        "## Triage",
        f"- Total unhealthy: {report['triage'].get('total_unhealthy', 0)}",
        f"- Severity: {report['triage'].get('high', 0)}H / {report['triage'].get('medium', 0)}M / {report['triage'].get('low', 0)}L",
        f"- Codex handoff: {'YES' if report['triage'].get('codex_handoff') else 'no'}",
    ]
    high_slugs = report["triage"].get("top_high_slugs", [])
    if high_slugs:
        lines.append(f"- Critical: {', '.join(high_slugs)}")

    lines += [
        "",
        "## Checkout Coverage",
        f"- Covered: {report['checkout'].get('covered_count', 0)}/{report['checkout'].get('live_count', 0)} ({report['checkout'].get('coverage_pct', 0)}%)",
        f"- Duplicates: {report.get('checkout_duplicates', 0)}",
    ]
    missing = report["checkout"].get("missing_slugs", [])
    if missing:
        lines.append(f"- Missing: {', '.join(missing)}")

    lines += [
        "",
        "## Price & Quality",
        f"- Price issues: {report.get('price_issues_count', 0)}",
        "",
    ]
    return "\n".join(lines)


def main():
    report = generate_report()
    fmt = "markdown"
    if "--json" in sys.argv:
        fmt = "json"
    if "--markdown" in sys.argv:
        fmt = "markdown"

    if fmt == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(report))

    output_path = ROOT / "analysis" / "portfolio_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(format_markdown(report), encoding="utf-8")

    unhealthy = report.get("triage", {}).get("total_unhealthy", 0)
    return {"unhealthy": unhealthy, "grade": report.get("health", {}).get("grade", "?")}


if __name__ == "__main__":
    result = main()
    sys.exit(1 if result.get("unhealthy", 0) > 0 else 0)
