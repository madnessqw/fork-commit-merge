#!/usr/bin/env python3
"""Generate a unified portfolio summary by combining multiple analysis tools.

Aggregates results from readiness scorer, lifecycle analyzer, overlap analyzer,
and price audit into a single comprehensive report with actionable insights.

Usage:
    python3 scripts/portfolio_summary_reporter.py
    python3 scripts/portfolio_summary_reporter.py --json
    python3 scripts/portfolio_summary_reporter.py --write
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
OUTPUT_PATH = ROOT / "analysis" / "portfolio_summary.md"


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _collect_readiness(state_path: Path = STATE_PATH) -> dict[str, Any]:
    from product_readiness_scorer import score_portfolio

    return score_portfolio(state_path)


def _collect_lifecycle(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    from product_lifecycle_analyzer import (
        analyze_portfolio,
        find_at_risk,
        lifecycle_summary,
        stage_health_score,
    )

    stages = analyze_portfolio(summary_path)
    return {
        "summary": lifecycle_summary(stages),
        "health_score": stage_health_score(stages),
        "at_risk_count": len(find_at_risk(stages)),
        "at_risk": find_at_risk(stages, limit=10),
    }


def _collect_overlap(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    try:
        from portfolio_overlap_analyzer import analyze_overlaps

        groups = analyze_overlaps(summary_path)
        high_severity = [g for g in groups if g.get("severity") == "high"]
        return {
            "total_groups": len(groups),
            "high_severity_count": len(high_severity),
            "groups": groups[:5],
        }
    except Exception:
        return {"total_groups": 0, "high_severity_count": 0, "groups": []}


def _collect_state_meta(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "cycle": state.get("cycle", 0),
        "mode": state.get("mode", "UNKNOWN"),
        "active_count": state.get("active_count", 0),
        "live_count": state.get("live_count", 0),
        "healthy_count": state.get("healthy_count", 0),
        "missing_checkout": state.get("missing_checkout", 0),
        "deploy_missing_or_bad_url": state.get("deploy_missing_or_bad_url", 0),
        "canonical_url_drift": state.get("canonical_url_drift", 0),
        "balance": state.get("balance", 0.0),
        "last_updated": state.get("last_updated", ""),
    }


def generate_report(
    state_path: Path = STATE_PATH,
    summary_path: Path = SUMMARY_PATH,
) -> dict[str, Any]:
    state = _load_json(state_path)
    state_meta = _collect_state_meta(state)
    readiness = _collect_readiness(state_path)
    lifecycle = _collect_lifecycle(summary_path)
    overlap = _collect_overlap(summary_path)

    insights: list[str] = []
    if readiness.get("needs_attention_count", 0) > 0:
        insights.append(
            f"{readiness['needs_attention_count']} products below 100% readiness"
        )
    if lifecycle.get("at_risk_count", 0) > 0:
        insights.append(f"{lifecycle['at_risk_count']} at-risk products")
    if overlap.get("high_severity_count", 0) > 0:
        insights.append(
            f"{overlap['high_severity_count']} high-severity overlap groups"
        )
    if state_meta["missing_checkout"] > 0:
        insights.append(f"{state_meta['missing_checkout']} missing checkout")
    if state_meta["deploy_missing_or_bad_url"] > 0:
        insights.append(f"{state_meta['deploy_missing_or_bad_url']} deploy gaps")
    if state_meta["canonical_url_drift"] > 0:
        insights.append(f"{state_meta['canonical_url_drift']} canonical drifts")

    if not insights:
        insights.append("Portfolio fully healthy - no action needed")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": state_meta,
        "readiness": {
            "avg_score": readiness.get("avg_score", 0),
            "ready_count": readiness.get("ready_count", 0),
            "total": readiness.get("total", 0),
            "failing_dimensions": readiness.get("failing_dimensions", {}),
        },
        "lifecycle": {
            "health_score": lifecycle.get("health_score", 0),
            "summary": lifecycle.get("summary", {}),
            "at_risk_count": lifecycle.get("at_risk_count", 0),
        },
        "overlap": {
            "total_groups": overlap.get("total_groups", 0),
            "high_severity_count": overlap.get("high_severity_count", 0),
        },
        "insights": insights,
    }


def format_report(report: dict[str, Any]) -> str:
    s = report["state"]
    r = report["readiness"]
    lc = report["lifecycle"]
    ov = report["overlap"]
    now = report["generated_at"][:16]

    lines = [
        "# Portfolio Summary Report",
        f"**Generated:** {now} | **Cycle:** {s['cycle']} | **Mode:** {s['mode']}",
        "",
        "## State Overview",
        f"- Products: {s['active_count']} active / {s['live_count']} live / {s['healthy_count']} healthy",
        f"- Missing checkout: {s['missing_checkout']} | Deploy gaps: {s['deploy_missing_or_bad_url']}",
        f"- Canonical drift: {s['canonical_url_drift']} | Balance: ${s['balance']:.2f}",
        "",
        "## Readiness Score",
        f"- Average: {r['avg_score']}% | Ready (90%+): {r['ready_count']}/{r['total']}",
    ]

    if r.get("failing_dimensions"):
        lines.append("- Failing dimensions:")
        for dim, count in list(r["failing_dimensions"].items())[:5]:
            lines.append(f"  - {dim}: {count} products")

    lines.extend(
        [
            "",
            "## Lifecycle",
            f"- Health score: {lc['health_score']}%",
        ]
    )

    if lc.get("summary"):
        for stage, count in lc["summary"].items():
            if count > 0:
                lines.append(f"  - {stage}: {count}")

    if lc.get("at_risk_count", 0) > 0:
        lines.append(f"- At-risk: {lc['at_risk_count']}")

    lines.extend(
        [
            "",
            "## Portfolio Overlap",
            f"- Overlap groups: {ov['total_groups']} | High severity: {ov['high_severity_count']}",
            "",
            "## Insights",
        ]
    )
    for insight in report["insights"]:
        lines.append(f"- {insight}")

    return "\n".join(lines)


def main() -> int:
    as_json = "--json" in sys.argv
    do_write = "--write" in sys.argv

    report = generate_report()

    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        formatted = format_report(report)
        print(formatted)

    if do_write:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(format_report(report), encoding="utf-8")
        print(f"\nWritten to {OUTPUT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
