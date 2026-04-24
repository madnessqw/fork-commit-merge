#!/usr/bin/env python3
"""
Single-command portfolio health snapshot for downstream agents.

Combines triage, health score, deploy readiness, and canonical drift
into one JSON or Markdown report. Designed for GLM/Codex cycle boots.

Usage:
    python3 scripts/portfolio_snapshot.py              # JSON to stdout
    python3 scripts/portfolio_snapshot.py --markdown    # Markdown to stdout
    python3 scripts/portfolio_snapshot.py --write       # Write to analysis/portfolio_snapshot.md
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
OUTPUT_PATH = ROOT / "analysis" / "portfolio_snapshot.md"


def _load_summary(path: Path = SUMMARY_PATH) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _pct(part: int, whole: int) -> float:
    return round(part / whole * 100, 1) if whole > 0 else 0.0


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


def snapshot(summary: dict | None = None) -> dict:
    if summary is None:
        summary = _load_summary()

    gaps = summary.get("gaps", {})
    live = summary.get("live_count", 0)
    healthy = summary.get("healthy_count", 0)
    canonical_healthy = summary.get("canonical_healthy_count", 0)
    fallback_healthy = summary.get("fallback_healthy_count", 0)
    active = summary.get("active_count", 0)
    unhealthy = summary.get("unhealthy_count", 0)
    checkout_gap = summary.get("checkout_gap_count", 0)
    deploy_gap = summary.get("deploy_missing_or_bad_url", 0)
    spec_ready = summary.get("spec_ready_count", 0)
    deploy_readiness = summary.get("deploy_readiness_count", 0)
    cycle = summary.get("cycle", 0)
    mode = summary.get("mode", "UNKNOWN")

    health_pct = _pct(healthy, live)
    canonical_pct = _pct(canonical_healthy, live)

    unhealthy_items = gaps.get("unhealthy_live", [])
    drift_items = gaps.get("canonical_url_drift", [])
    fallback_items = gaps.get("fallback_healthy", [])
    deploy_readiness_items = gaps.get("deploy_readiness", [])

    unhealthy_slugs = [
        {"slug": u.get("slug"), "code": u.get("code"), "status": u.get("health_status")}
        for u in unhealthy_items
    ]

    drift_slugs = [
        {
            "slug": d.get("slug"),
            "current_url": d.get("url"),
            "ideal_url": d.get("ideal_url"),
            "canonical_code": d.get("canonical_code"),
            "canonical_status": d.get("canonical_status"),
        }
        for d in drift_items
    ]

    fallback_slugs = [f.get("slug") for f in fallback_items]

    deploy_gap_slugs = [
        {
            "slug": dr.get("slug"),
            "missing_urls": dr.get("missing_url_fields", []),
            "missing_state": dr.get("missing_state_fields", []),
        }
        for dr in deploy_readiness_items
    ]

    needs_codex_handoff = len(unhealthy_items) > 0 or len(drift_items) > 0

    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "cycle": cycle,
        "mode": mode,
        "active": active,
        "live": live,
        "healthy": healthy,
        "health_pct": health_pct,
        "grade": _grade(health_pct),
        "canonical_healthy": canonical_healthy,
        "canonical_pct": canonical_pct,
        "fallback_healthy": fallback_healthy,
        "unhealthy": unhealthy,
        "checkout_gap": checkout_gap,
        "deploy_gap": deploy_gap,
        "spec_ready": spec_ready,
        "deploy_readiness": deploy_readiness,
        "unhealthy_detail": unhealthy_slugs,
        "drift_detail": drift_slugs,
        "fallback_slugs": fallback_slugs,
        "deploy_gap_detail": deploy_gap_slugs,
        "codex_handoff": needs_codex_handoff,
        "next_actions": _next_actions(
            unhealthy, checkout_gap, deploy_gap, drift_items, fallback_healthy
        ),
    }


def _next_actions(
    unhealthy: int,
    checkout_gap: int,
    deploy_gap: int,
    drift: list,
    fallback: int,
) -> list[str]:
    actions = []
    if unhealthy > 0:
        actions.append(f"Fix {unhealthy} unhealthy live products")
    if checkout_gap > 0:
        actions.append(f"Add checkout to {checkout_gap} products")
    if deploy_gap > 0:
        actions.append(f"Deploy {deploy_gap} ready products")
    if drift:
        actions.append(f"Resolve {len(drift)} canonical URL drifts")
    if fallback > 0:
        actions.append(f"Normalize {fallback} fallback alias products")
    if not actions:
        actions.append("Portfolio healthy — focus on new products")
    return actions


def to_markdown(snap: dict) -> str:
    lines = [
        f"# Portfolio Snapshot",
        f"**Cycle:** {snap['cycle']} | **Mode:** {snap['mode']}",
        f"**Generated:** {snap['ts']}",
        f"**Grade:** {snap['grade']} ({snap['health_pct']}%)",
        "",
        "## Overview",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Active | {snap['active']} |",
        f"| Live | {snap['live']} |",
        f"| Healthy | {snap['healthy']} |",
        f"| Canonical healthy | {snap['canonical_healthy']} ({snap['canonical_pct']}%) |",
        f"| Fallback healthy | {snap['fallback_healthy']} |",
        f"| Unhealthy | {snap['unhealthy']} |",
        f"| Checkout gap | {snap['checkout_gap']} |",
        f"| Deploy gap | {snap['deploy_gap']} |",
        f"| Spec ready | {snap['spec_ready']} |",
        f"| Deploy readiness | {snap['deploy_readiness']} |",
        f"| Codex handoff | {'YES' if snap['codex_handoff'] else 'no'} |",
        "",
    ]

    if snap["unhealthy_detail"]:
        lines.append("## Unhealthy Live Products")
        lines.append("| Slug | HTTP | Status |")
        lines.append("|------|------|--------|")
        for u in snap["unhealthy_detail"]:
            lines.append(f"| {u['slug']} | {u['code']} | {u['status']} |")
        lines.append("")

    if snap["drift_detail"]:
        lines.append("## Canonical URL Drift")
        lines.append("| Slug | Canonical Status | Ideal URL |")
        lines.append("|------|-----------------|-----------|")
        for d in snap["drift_detail"]:
            lines.append(
                f"| {d['slug']} | {d['canonical_status']} | {d['ideal_url']} |"
            )
        lines.append("")

    if snap["deploy_gap_detail"]:
        lines.append("## Deploy Readiness Gap")
        lines.append(f"**{len(snap['deploy_gap_detail'])} products** with missing fields:")
        for dg in snap["deploy_gap_detail"]:
            missing = ", ".join(dg.get("missing_urls", [])[:3])
            lines.append(f"- **{dg['slug']}** — missing: {missing}")
        lines.append("")

    lines.append("## Next Actions")
    for i, action in enumerate(snap["next_actions"], 1):
        lines.append(f"{i}. {action}")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Portfolio health snapshot")
    parser.add_argument("--markdown", action="store_true", help="Output as Markdown")
    parser.add_argument(
        "--write", action="store_true", help="Write to analysis/portfolio_snapshot.md"
    )
    args = parser.parse_args()

    snap = snapshot()

    if args.write:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        md = to_markdown(snap)
        OUTPUT_PATH.write_text(md, encoding="utf-8")
        json_path = OUTPUT_PATH.with_suffix(".json")
        json_path.write_text(
            json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Written: {OUTPUT_PATH} + {json_path}")
        return 0

    if args.markdown:
        print(to_markdown(snap))
    else:
        print(json.dumps(snap, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
