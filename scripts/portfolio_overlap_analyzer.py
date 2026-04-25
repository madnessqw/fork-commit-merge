#!/usr/bin/env python3
"""Analyze portfolio for functional product overlap and SEO cannibalization risk.

Identifies product groups solving the same problem, scores overlap severity,
and recommends which product should be the primary (best slug, cleanest URL).

Usage:
    python3 scripts/portfolio_overlap_analyzer.py
    python3 scripts/portfolio_overlap_analyzer.py --json
    python3 scripts/portfolio_overlap_analyzer.py --write
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
OUTPUT_PATH = ROOT / "analysis" / "portfolio_overlap.md"

OVERLAP_GROUPS: list[dict[str, Any]] = [
    {
        "name": "Cron Tools",
        "keywords": ["cron"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "JWT Tools",
        "keywords": ["jwt"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "HTML Entity Tools",
        "keywords": ["html-entity", "html-entit"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "TOML Tools",
        "keywords": ["toml"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "YAML Tools",
        "keywords": ["yaml"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "Diff Tools",
        "keywords": ["diff"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Base64 Tools",
        "keywords": ["base64"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Markdown Tools",
        "keywords": ["markdown", "md2", "md-to"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "Docker Compose Tools",
        "keywords": ["docker-compose", "dockerfile", "docker-run", "docker-command"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "HMAC Tools",
        "keywords": ["hmac"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Email Signature Tools",
        "keywords": ["email-signature"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Lorem Ipsum Tools",
        "keywords": ["lorem-ipsum"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Timestamp Tools",
        "keywords": ["timestamp"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Nginx Tools",
        "keywords": ["nginx"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "SQL Tools",
        "keywords": ["sql"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "XML Tools",
        "keywords": ["xml"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "Color Tools",
        "keywords": ["color-", "color-", "colour"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "SSL Tools",
        "keywords": ["ssl-"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Regex Tools",
        "keywords": ["regex"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "URL Tools",
        "keywords": ["url-parser", "url-builder", "url-forge"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "Case Converter Tools",
        "keywords": ["case-convert", "text-case"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "MCP Tools",
        "keywords": ["mcp-"],
        "exclude": [],
        "max_primary": 2,
    },
    {
        "name": "API Mock Tools",
        "keywords": ["api-mock"],
        "exclude": [],
        "max_primary": 1,
    },
    {
        "name": "Password Tools",
        "keywords": ["password-"],
        "exclude": [],
        "max_primary": 1,
    },
]


def slug_quality_score(slug: str) -> int:
    score = 100
    if re.search(r"-\d+", slug):
        score -= 30
    if slug.endswith("-pro"):
        score += 5
    if len(slug) > 25:
        score -= 10
    dash_count = slug.count("-")
    if dash_count > 2:
        score -= 10 * (dash_count - 2)
    if re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", slug):
        score += 5
    return max(0, min(100, score))


def url_quality_score(url: str) -> int:
    score = 100
    domain = url.split("//")[1].split("/")[0] if "//" in url else url
    subdomain = domain.split(".")[0]

    if "madnessqws-projects" in subdomain:
        score -= 40
    if re.search(r"-[a-z0-9]*\d[a-z0-9]{4,}-", subdomain):
        score -= 50
    elif subdomain.count("-") > 2:
        score -= 20
    if "-five" in subdomain or "-green" in subdomain or "-coral" in subdomain:
        score -= 15
    if "-beryl" in subdomain or "-flax" in subdomain:
        score -= 15
    return max(0, min(100, score))


def select_primary(products: list[dict]) -> dict:
    def score_key(p: dict) -> tuple[int, int, int]:
        slug = p.get("s", "")
        url = p.get("v", "")
        s_score = slug_quality_score(slug)
        u_score = url_quality_score(url)
        name_bonus = 0
        if "-pro" in slug:
            name_bonus += 10
        if not any(x in slug for x in ["-pro", "-express", "-master", "-builder"]):
            name_bonus += 5
        return (s_score + u_score + name_bonus, s_score, u_score)

    return max(products, key=score_key)


def analyze_overlaps(products: list[dict]) -> list[dict]:
    results = []
    for group_def in OVERLAP_GROUPS:
        group_name = group_def["name"]
        keywords = group_def["keywords"]
        exclude = group_def.get("exclude", [])
        max_primary = group_def.get("max_primary", 1)

        matched = []
        for p in products:
            slug = p.get("s", "")
            name = p.get("n", "").lower()
            if slug in exclude:
                continue
            if any(kw in slug for kw in keywords) or any(kw in name for kw in keywords):
                matched.append(p)

        if len(matched) <= 1:
            continue

        primary = select_primary(matched)
        secondary = [p for p in matched if p["s"] != primary["s"]]

        overlap_score = min(100, len(matched) * 20)

        severity = "low"
        if len(matched) >= 4:
            severity = "critical"
        elif len(matched) >= 3:
            severity = "high"
        elif len(matched) >= 2:
            severity = "medium"

        results.append({
            "group": group_name,
            "count": len(matched),
            "overlap_score": overlap_score,
            "severity": severity,
            "primary": {"name": primary["n"], "slug": primary["s"], "url": primary["v"]},
            "secondary": [{"name": p["n"], "slug": p["s"], "url": p["v"]} for p in secondary],
            "recommendation": f"Keep {primary['s']} as primary, redirect {len(secondary)} others" if len(matched) > max_primary else "Acceptable overlap",
        })

    results.sort(key=lambda x: x["overlap_score"], reverse=True)
    return results


def format_markdown(results: list[dict]) -> str:
    lines = ["# Portfolio Overlap Analysis\n"]
    lines.append(f"**Overlap Groups:** {len(results)}\n")

    critical = [r for r in results if r["severity"] == "critical"]
    high = [r for r in results if r["severity"] == "high"]
    medium = [r for r in results if r["severity"] == "medium"]

    if critical:
        lines.append("## Critical Overlap (4+ products)")
        for r in critical:
            lines.append(f"### {r['group']} ({r['count']} products, score: {r['overlap_score']})")
            lines.append(f"- **Primary:** {r['primary']['slug']} — {r['primary']['url']}")
            for s in r["secondary"]:
                lines.append(f"- Secondary: {s['slug']} — {s['url']}")
            lines.append(f"- **Action:** {r['recommendation']}\n")

    if high:
        lines.append("## High Overlap (3 products)")
        for r in high:
            lines.append(f"### {r['group']} ({r['count']} products)")
            lines.append(f"- **Primary:** {r['primary']['slug']}")
            for s in r["secondary"]:
                lines.append(f"- Secondary: {s['slug']}")
            lines.append(f"- **Action:** {r['recommendation']}\n")

    if medium:
        lines.append("## Medium Overlap (2 products)")
        for r in medium:
            lines.append(f"- **{r['group']}:** keep `{r['primary']['slug']}`, redirect {len(r['secondary'])} others — {r['recommendation']}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Portfolio overlap analyzer")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--write", action="store_true", help="Write to analysis/portfolio_overlap.md")
    args = parser.parse_args()

    if not SUMMARY_PATH.exists():
        print("ERROR: STATE_SUMMARY.json not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(SUMMARY_PATH.read_text())
    products = data.get("products", [])

    results = analyze_overlaps(products)

    if args.json:
        print(json.dumps(results, indent=2))
    elif args.write:
        md = format_markdown(results)
        OUTPUT_PATH.write_text(md)
        print(f"Written to {OUTPUT_PATH}")
        print(f"Groups: {len(results)} | Critical: {sum(1 for r in results if r['severity']=='critical')} | High: {sum(1 for r in results if r['severity']=='high')}")
    else:
        md = format_markdown(results)
        print(md)

    total_secondary = sum(r["count"] - 1 for r in results)
    print(f"\nSummary: {len(results)} overlap groups, {total_secondary} consolidation candidates")


if __name__ == "__main__":
    main()
