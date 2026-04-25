#!/usr/bin/env python3
"""Analyze product lifecycle stages across the UniverseCreator portfolio.

Categorizes products into lifecycle stages based on health status,
checkout coverage, and deployment metadata. Produces a summary that
helps identify stale, zombie, or underperforming products.

Usage:
    python3 scripts/product_lifecycle_analyzer.py
    python3 scripts/product_lifecycle_analyzer.py --json
    python3 scripts/product_lifecycle_analyzer.py --by-stage live
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
STATE_PATH = ROOT / "STATE.json"

STAGE_ORDER = ("healthy", "no_checkout", "no_url", "unhealthy", "zombie")


def _slug(p: dict[str, Any]) -> str:
    return p.get("s") or p.get("slug") or p.get("n") or "unknown"


def _checkout(p: dict[str, Any]) -> str:
    return (p.get("c") or p.get("checkout_url") or "").strip()


def _url(p: dict[str, Any]) -> str:
    return (p.get("v") or p.get("vercel_url") or "").strip()


def _status(p: dict[str, Any]) -> str:
    return (p.get("st") or p.get("status") or "").strip()


def _name(p: dict[str, Any]) -> str:
    return p.get("n") or p.get("name") or _slug(p)


def classify_product(product: dict[str, Any]) -> str:
    status = _status(product).lower()
    checkout = _checkout(product)
    url = _url(product)

    if status != "live":
        return "zombie"
    if not url.startswith("http"):
        return "no_url"
    if not checkout.startswith("http"):
        return "no_checkout"
    return "healthy"


def analyze_portfolio(
    summary_path: Path = SUMMARY_PATH,
) -> dict[str, list[dict[str, str]]]:
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    products = data.get("products", [])

    stages: dict[str, list[dict[str, str]]] = {s: [] for s in STAGE_ORDER}
    for p in products:
        stage = classify_product(p)
        entry = {
            "name": _name(p),
            "slug": _slug(p),
            "stage": stage,
            "url": _url(p),
            "checkout": _checkout(p),
        }
        stages.setdefault(stage, []).append(entry)

    return stages


def lifecycle_summary(
    stages: dict[str, list[dict[str, str]]],
) -> dict[str, int]:
    return {stage: len(items) for stage, items in stages.items()}


def stage_health_score(stages: dict[str, list[dict[str, str]]]) -> float:
    total = sum(len(v) for v in stages.values())
    if total == 0:
        return 0.0
    healthy = len(stages.get("healthy", []))
    return round(healthy / total * 100, 1)


def find_at_risk(
    stages: dict[str, list[dict[str, str]]],
    limit: int = 10,
) -> list[dict[str, str]]:
    at_risk = []
    for stage in ("no_checkout", "no_url", "unhealthy", "zombie"):
        at_risk.extend(stages.get(stage, []))
    return at_risk[:limit]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Product lifecycle analyzer")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument(
        "--by-stage",
        choices=STAGE_ORDER,
        help="List products in a specific stage",
    )
    args = parser.parse_args()

    stages = analyze_portfolio()
    summary = lifecycle_summary(stages)
    score = stage_health_score(stages)

    if args.by_stage:
        items = stages.get(args.by_stage, [])
        if args.json:
            print(json.dumps(items, indent=2))
        else:
            for it in items:
                print(f"  {it['slug']:40s}  {it['name']}")
        return

    if args.json:
        print(
            json.dumps(
                {"summary": summary, "health_score": score, "stages": stages},
                indent=2,
            )
        )
        return

    total = sum(summary.values())
    print(f"Product Lifecycle Report  ({total} products, health: {score}%)")
    print("=" * 55)
    for stage in STAGE_ORDER:
        count = summary.get(stage, 0)
        bar = "#" * count if count else ""
        print(f"  {stage:15s} {count:4d}  {bar}")
    print()

    at_risk = find_at_risk(stages)
    if at_risk:
        print(f"At-risk products ({len(at_risk)}):")
        for it in at_risk:
            print(f"  - {it['slug']:40s} [{it['stage']}]")


if __name__ == "__main__":
    main()
