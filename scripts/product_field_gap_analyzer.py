#!/usr/bin/env python3
"""Analyze missing or empty fields across the product portfolio.

Scans STATE.json active products and reports which fields are missing,
empty, or have placeholder values. Useful for sales readiness assessment.

Usage:
    python3 scripts/product_field_gap_analyzer.py
    python3 scripts/product_field_gap_analyzer.py --json
    python3 scripts/product_field_gap_analyzer.py --field description
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"

FIELDS = [
    "price",
    "description",
    "category",
    "tags",
    "checkout_url",
    "url",
    "name",
    "slug",
]

PLACEHOLDER_VALUES = {"", "none", "n/a", "todo", "tbd", "null", "undefined", "n/a", "-"}


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in PLACEHOLDER_VALUES:
        return True
    if isinstance(value, (list, dict)) and len(value) == 0:
        return True
    if isinstance(value, (int, float)) and value == 0:
        return False
    return False


def load_products(state_path: Path = STATE_PATH) -> list[dict[str, Any]]:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data.get("products", {}).get("active", [])


def analyze_gaps(
    products: list[dict[str, Any]],
    fields: list[str] | None = None,
) -> dict[str, Any]:
    if fields is None:
        fields = FIELDS

    total = len(products)
    field_gaps: dict[str, dict[str, Any]] = {}

    for field in fields:
        missing_slugs: list[str] = []
        for p in products:
            val = p.get(field)
            if _is_missing(val):
                missing_slugs.append(p.get("slug", f"unknown-{len(missing_slugs)}"))

        gap_pct = round(len(missing_slugs) / total * 100, 1) if total else 0
        field_gaps[field] = {
            "missing_count": len(missing_slugs),
            "total": total,
            "gap_pct": gap_pct,
            "missing_slugs": missing_slugs[:20],
        }

    gap_score = sum(g["missing_count"] for g in field_gaps.values())
    avg_gap_pct = round(
        sum(g["gap_pct"] for g in field_gaps.values()) / len(field_gaps), 1
    ) if field_gaps else 0

    readiness = "ready"
    if avg_gap_pct > 30:
        readiness = "critical"
    elif avg_gap_pct > 15:
        readiness = "needs_work"
    elif avg_gap_pct > 5:
        readiness = "good"

    return {
        "total_products": total,
        "fields_analyzed": len(fields),
        "gap_score": gap_score,
        "avg_gap_pct": avg_gap_pct,
        "readiness": readiness,
        "field_gaps": field_gaps,
    }


def format_gap_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Product Field Gap Analysis",
        "",
        f"**Products:** {report['total_products']}",
        f"**Fields analyzed:** {report['fields_analyzed']}",
        f"**Gap score:** {report['gap_score']} (lower is better)",
        f"**Avg gap:** {report['avg_gap_pct']}%",
        f"**Readiness:** {report['readiness']}",
        "",
        "## Field Details",
        "",
        "| Field | Missing | % |",
        "|-------|---------|---|",
    ]
    for field, data in sorted(
        report["field_gaps"].items(), key=lambda x: x[1]["missing_count"], reverse=True
    ):
        lines.append(f"| {field} | {data['missing_count']}/{data['total']} | {data['gap_pct']}% |")

    lines.append("")
    lines.append("## Most Gapped Products")
    slug_gap_count: dict[str, int] = {}
    for field, data in report["field_gaps"].items():
        for slug in data["missing_slugs"]:
            slug_gap_count[slug] = slug_gap_count.get(slug, 0) + 1

    top_gapped = sorted(slug_gap_count.items(), key=lambda x: x[1], reverse=True)[:10]
    if top_gapped:
        lines.append("")
        lines.append("| Product | Missing Fields |")
        lines.append("|---------|----------------|")
        for slug, count in top_gapped:
            lines.append(f"| {slug} | {count} |")

    return "\n".join(lines)


def format_gap_telegram(report: dict[str, Any]) -> str:
    top_fields = sorted(
        report["field_gaps"].items(), key=lambda x: x[1]["missing_count"], reverse=True
    )[:3]
    top_str = " | ".join(
        f"{f}: {d['missing_count']}" for f, d in top_fields if d["missing_count"] > 0
    )
    return (
        f"📋 Field Gap Analysis\n"
        f"📦 {report['total_products']} products | Score: {report['gap_score']}\n"
        f"📊 Avg gap: {report['avg_gap_pct']}% | {report['readiness']}\n"
        f"🔍 {top_str}"
    )


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Product field gap analyzer")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--telegram", action="store_true", help="Telegram format")
    parser.add_argument("--field", type=str, default=None, help="Analyze single field")
    args = parser.parse_args()

    fields = [args.field] if args.field else FIELDS
    products = load_products()
    report = analyze_gaps(products, fields=fields)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.telegram:
        print(format_gap_telegram(report))
    else:
        print(format_gap_markdown(report))

    return report


if __name__ == "__main__":
    main()
