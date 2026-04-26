#!/usr/bin/env python3
"""Generate a changelog summary from product state history.

Analyzes STATE.json products and produces a structured changelog covering:
- Products by status (live, building, pending, etc.)
- Checkout coverage metrics
- Health score breakdown
- Deploy readiness summary

Usage::

    python3 -m scripts.product_release_changelog
    python3 -m scripts.product_release_changelog --json
    python3 -m scripts.product_release_changelog --verbose
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text())


def load_summary() -> dict[str, Any]:
    if not SUMMARY_PATH.exists():
        return {}
    return json.loads(SUMMARY_PATH.read_text())


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def status_breakdown(products: list[dict[str, Any]]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for p in products:
        counter[p.get("status", "unknown")] += 1
    return dict(counter.most_common())


def checkout_coverage(products: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(products)
    with_co = sum(1 for p in products if (p.get("checkout_url") or "").startswith("http"))
    without_co = total - with_co
    pct = (with_co / total * 100) if total else 0.0
    return {
        "total": total,
        "with_checkout": with_co,
        "without_checkout": without_co,
        "coverage_pct": round(pct, 1),
    }


def health_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "healthy": summary.get("healthy_count", 0),
        "live": summary.get("live_count", 0),
        "unhealthy": summary.get("unhealthy_count", 0),
        "deploy_missing": summary.get("deploy_missing_or_bad_url", 0),
        "canonical_drift": summary.get("canonical_url_drift", 0),
    }


def generate_changelog(verbose: bool = False) -> dict[str, Any]:
    state = load_state()
    summary = load_summary()
    products = state.get("products", {}).get("active", [])
    if not products:
        products = summary.get("products", [])

    changelog: dict[str, Any] = {
        "generated_at": _ts(),
        "cycle": summary.get("cycle", 0),
        "mode": summary.get("mode", "unknown"),
        "status_breakdown": status_breakdown(products),
        "checkout_coverage": checkout_coverage(products),
        "health": health_summary(summary),
    }

    if verbose and products:
        changelog["products_sample"] = [
            {
                "name": p.get("name") or p.get("n"),
                "slug": p.get("slug") or p.get("s"),
                "status": p.get("status") or p.get("st"),
                "url": p.get("url") or p.get("v"),
            }
            for p in products[:10]
        ]

    return changelog


def format_markdown(changelog: dict[str, Any]) -> str:
    lines: list[str] = [
        f"# Product Release Changelog",
        f"Generated: {changelog['generated_at']}",
        f"Cycle: {changelog['cycle']} | Mode: {changelog['mode']}",
        "",
        "## Status Breakdown",
    ]
    for status, count in changelog.get("status_breakdown", {}).items():
        lines.append(f"- {status}: {count}")

    co = changelog.get("checkout_coverage", {})
    lines.extend([
        "",
        "## Checkout Coverage",
        f"- Total products: {co.get('total', 0)}",
        f"- With checkout: {co.get('with_checkout', 0)}",
        f"- Coverage: {co.get('coverage_pct', 0)}%",
    ])

    h = changelog.get("health", {})
    lines.extend([
        "",
        "## Health Summary",
        f"- Healthy: {h.get('healthy', 0)}/{h.get('live', 0)}",
        f"- Unhealthy: {h.get('unhealthy', 0)}",
        f"- Deploy missing: {h.get('deploy_missing', 0)}",
        f"- Canonical drift: {h.get('canonical_drift', 0)}",
    ])

    if changelog.get("products_sample"):
        lines.extend(["", "## Sample Products"])
        for p in changelog["products_sample"]:
            lines.append(f"- {p['name']} ({p['slug']}) — {p['status']}")

    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Product release changelog")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--verbose", action="store_true", help="Include sample products")
    args = parser.parse_args()

    changelog = generate_changelog(verbose=args.verbose)
    if args.json:
        print(json.dumps(changelog, indent=2))
    else:
        print(format_markdown(changelog))


if __name__ == "__main__":
    main()
