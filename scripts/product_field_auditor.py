#!/usr/bin/env python3
"""Audit product.json fields across the entire portfolio.

Scans all products for missing, empty, or malformed fields.
Produces a structured JSON report + optional markdown summary.

Usage:
    python3 scripts/product_field_auditor.py
    python3 scripts/product_field_auditor.py --markdown
    python3 scripts/product_field_auditor.py --slug uuid-generator-pro
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "products"
OUTPUT_FILE = ROOT / "analysis" / "product_field_audit.json"

REQUIRED_FIELDS = [
    "name", "slug", "tagline", "description", "price", "features",
    "tech_stack", "status", "vercel_url", "github_url", "checkout_url",
]

URL_FIELDS = ["vercel_url", "github_url", "checkout_url"]

OPTIONAL_FIELDS = [
    "seo_optimized", "seo_optimized_at", "spec_version",
    "payment_provider", "polar_product_id", "polar_product_price_id",
    "polar_checkout_link_id", "created_cycle", "deployed_cycle",
]

VALID_STATUSES = {"live", "building", "pending", "archived", "draft"}


def load_product(slug: str) -> dict[str, Any] | None:
    p = PRODUCTS_DIR / slug / "product.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def find_all_slugs() -> list[str]:
    if not PRODUCTS_DIR.exists():
        return []
    return sorted(
        d.name for d in PRODUCTS_DIR.iterdir()
        if d.is_dir() and (d / "product.json").exists()
    )


def audit_slug(slug: str) -> dict[str, Any]:
    result: dict[str, Any] = {"slug": slug, "issues": [], "score": 100}
    data = load_product(slug)

    if data is None:
        result["issues"].append({"field": "product.json", "problem": "missing_or_unreadable"})
        result["score"] = 0
        return result

    for field in REQUIRED_FIELDS:
        val = data.get(field)
        if val is None:
            result["issues"].append({"field": field, "problem": "missing"})
            result["score"] -= 8
        elif isinstance(val, str) and not val.strip():
            result["issues"].append({"field": field, "problem": "empty"})
            result["score"] -= 5
        elif field == "features" and isinstance(val, list) and len(val) == 0:
            result["issues"].append({"field": field, "problem": "empty_list"})
            result["score"] -= 5

    for field in URL_FIELDS:
        val = data.get(field, "")
        if isinstance(val, str) and val and not val.startswith("http"):
            result["issues"].append({"field": field, "problem": "invalid_url", "value": val})
            result["score"] -= 5

    status = data.get("status", "")
    if status and status not in VALID_STATUSES:
        result["issues"].append({"field": "status", "problem": "invalid_status", "value": status})
        result["score"] -= 5

    slug_match = data.get("slug", "")
    if slug_match != slug:
        result["issues"].append({"field": "slug", "problem": "mismatch", "expected": slug, "actual": slug_match})
        result["score"] -= 10

    price = data.get("price", "")
    if isinstance(price, str) and price and not any(c.isdigit() for c in price):
        result["issues"].append({"field": "price", "problem": "no_numeric_value", "value": price})
        result["score"] -= 3

    result["score"] = max(result["score"], 0)
    return result


def run_audit(target_slug: str | None = None) -> dict[str, Any]:
    slugs = [target_slug] if target_slug else find_all_slugs()
    results = []
    for slug in slugs:
        results.append(audit_slug(slug))

    total = len(results)
    issue_counts = Counter()
    field_issue_counts: dict[str, int] = Counter()
    scores = []

    for r in results:
        scores.append(r["score"])
        for issue in r["issues"]:
            issue_counts[issue["problem"]] += 1
            field_issue_counts[issue["field"]] += 1

    perfect = sum(1 for s in scores if s == 100)
    avg_score = round(sum(scores) / total, 1) if total else 0

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_products": total,
        "perfect_count": perfect,
        "average_score": avg_score,
        "issue_summary": dict(issue_counts.most_common(10)),
        "field_issues": dict(field_issue_counts.most_common(10)),
        "products_with_issues": [r for r in results if r["issues"]],
        "all_results": results if total <= 20 else [r for r in results if r["issues"]],
    }
    return report


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Product Field Audit",
        f"**Date:** {report['timestamp'][:16]}",
        f"**Products:** {report['total_products']} | **Perfect:** {report['perfect_count']} | **Avg Score:** {report['average_score']}",
        "",
    ]

    if report["issue_summary"]:
        lines.append("## Issue Summary")
        for problem, count in report["issue_summary"].items():
            lines.append(f"- `{problem}`: {count} products")
        lines.append("")

    if report["field_issues"]:
        lines.append("## Field Issues")
        for field, count in report["field_issues"].items():
            lines.append(f"- `{field}`: {count} issues")
        lines.append("")

    if report["products_with_issues"]:
        lines.append("## Products with Issues")
        for r in report["products_with_issues"][:30]:
            issues_str = ", ".join(f"{i['field']}:{i['problem']}" for i in r["issues"])
            lines.append(f"- **{r['slug']}** (score {r['score']}): {issues_str}")

    return "\n".join(lines)


def main() -> None:
    args = sys.argv[1:]
    target_slug = None
    markdown_mode = False

    i = 0
    while i < len(args):
        if args[i] == "--slug" and i + 1 < len(args):
            target_slug = args[i + 1]
            i += 2
        elif args[i] == "--markdown":
            markdown_mode = True
            i += 1
        else:
            i += 1

    report = run_audit(target_slug)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if markdown_mode:
        print(format_markdown(report))
    else:
        perfect = report["perfect_count"]
        total = report["total_products"]
        avg = report["average_score"]
        issues = len(report["products_with_issues"])
        print(f"Audit: {perfect}/{total} perfect | avg score: {avg} | {issues} with issues")
        print(f"Report: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
