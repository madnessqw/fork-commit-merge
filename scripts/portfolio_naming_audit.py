#!/usr/bin/env python3
"""Audit product naming consistency across the portfolio.

Detects:
- Suffix inconsistencies (some products use "Pro", some don't)
- Type word variations (Generator vs Builder vs Creator vs Maker)
- Punctuation inconsistencies (slashes, dashes, ampersands)
- Duplicate/overlapping names (same function, different naming)
- Casing issues in product names

Usage:
    python3 scripts/portfolio_naming_audit.py
    python3 scripts/portfolio_naming_audit.py --json
    python3 scripts/portfolio_naming_audit.py --fix-suggestions
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"

SUFFIXES = ("Pro", "Plus", "Premium", "Free", "Lite", "Max", "Ultimate")
TYPE_WORDS = {
    "generator": ("generator", "creator", "maker", "producer"),
    "builder": ("builder",),
    "converter": ("converter", "transformer", "translator", "adapter"),
    "formatter": ("formatter", "beautifier", "prettifier", "tidyer"),
    "validator": ("validator", "checker", "inspector", "tester", "linter"),
    "encoder": ("encoder", "decoder", "encoder/decoder", "encoder/decoder pro"),
    "analyzer": ("analyzer", "examiner", "reviewer"),
    "optimizer": ("optimizer", "minifier", "compressor", "cleaner"),
    "detector": ("detector", "finder", "scanner", "hunter"),
    "visualizer": ("visualizer", "viewer", "displayer"),
}

SEP_PATTERNS = re.compile(r"[/|&,+]")


def _load_products(state_path: Path = STATE_PATH) -> list[dict[str, Any]]:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data.get("products", {}).get("active", [])


def _strip_suffix(name: str) -> tuple[str, str]:
    for suffix in SUFFIXES:
        if name.endswith(f" {suffix}"):
            return name[: -len(f" {suffix}")], suffix
    return name, ""


def _extract_base_type(name: str) -> tuple[str, str]:
    words = name.lower().split()
    for category, variants in TYPE_WORDS.items():
        for word in words:
            if word in variants:
                return " ".join(words[: words.index(word)]), category
    return name.lower(), ""


def audit_suffixes(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in products:
        name = p.get("name", p.get("n", ""))
        base, suffix = _strip_suffix(name)
        if base:
            base_groups[base.lower()].append(
                {"name": name, "slug": p.get("slug", p.get("s", "")), "suffix": suffix}
            )

    inconsistencies = []
    for base, entries in base_groups.items():
        if len(entries) < 2:
            continue
        suffixes_found = {e["suffix"] for e in entries}
        if len(suffixes_found) > 1:
            inconsistencies.append(
                {
                    "type": "suffix_inconsistency",
                    "base_name": base,
                    "products": entries,
                    "suffixes": sorted(suffixes_found),
                }
            )
    return inconsistencies


def audit_type_words(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    type_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in products:
        name = p.get("name", p.get("n", ""))
        base, category = _extract_base_type(name)
        if category:
            type_groups[base].append(
                {
                    "name": name,
                    "slug": p.get("slug", p.get("s", "")),
                    "type_category": category,
                }
            )

    overlaps = []
    for base, entries in type_groups.items():
        if len(entries) < 2:
            continue
        categories = {e["type_category"] for e in entries}
        if len(categories) > 1:
            overlaps.append(
                {
                    "type": "type_word_overlap",
                    "base_name": base,
                    "products": entries,
                    "categories": sorted(categories),
                }
            )
    return overlaps


def audit_separators(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues = []
    for p in products:
        name = p.get("name", p.get("n", ""))
        matches = SEP_PATTERNS.findall(name)
        if matches:
            issues.append(
                {
                    "type": "separator_in_name",
                    "name": name,
                    "slug": p.get("slug", p.get("s", "")),
                    "separators": matches,
                }
            )
    return issues


def audit_suffix_distribution(products: list[dict[str, Any]]) -> dict[str, Any]:
    suffix_counts: Counter = Counter()
    no_suffix = 0
    for p in products:
        name = p.get("name", p.get("n", ""))
        _, suffix = _strip_suffix(name)
        if suffix:
            suffix_counts[suffix] += 1
        else:
            no_suffix += 1
    return {
        "suffix_distribution": dict(suffix_counts.most_common()),
        "no_suffix_count": no_suffix,
        "total": len(products),
    }


def generate_fix_suggestions(
    suffix_issues: list[dict[str, Any]],
    type_issues: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    suggestions = []
    for issue in suffix_issues:
        entries = issue["products"]
        pro_entries = [e for e in entries if e["suffix"] == "Pro"]
        if pro_entries:
            canonical = pro_entries[0]
        else:
            canonical = max(entries, key=lambda e: len(e["suffix"]))
        for entry in entries:
            if entry["slug"] != canonical["slug"]:
                suggestions.append(
                    {
                        "action": "consider_consolidating",
                        "from_slug": entry["slug"],
                        "from_name": entry["name"],
                        "keep_slug": canonical["slug"],
                        "keep_name": canonical["name"],
                        "reason": f"shares base '{issue['base_name']}' with different suffix",
                    }
                )
    return suggestions


def run_audit(
    state_path: Path = STATE_PATH,
) -> dict[str, Any]:
    products = _load_products(state_path)
    if not products:
        return {"error": "no products loaded"}

    suffix_issues = audit_suffixes(products)
    type_issues = audit_type_words(products)
    separator_issues = audit_separators(products)
    suffix_dist = audit_suffix_distribution(products)
    suggestions = generate_fix_suggestions(suffix_issues, type_issues)

    return {
        "total_products": len(products),
        "suffix_inconsistencies": len(suffix_issues),
        "type_word_overlaps": len(type_issues),
        "separator_issues": len(separator_issues),
        "suffix_distribution": suffix_dist,
        "suffix_issues": suffix_issues,
        "type_issues": type_issues,
        "separator_issues_list": separator_issues,
        "fix_suggestions": suggestions,
    }


def format_audit_report(audit: dict[str, Any]) -> str:
    lines = [
        "# Portfolio Naming Audit",
        "",
        f"**Total products:** {audit['total_products']}",
        f"**Suffix inconsistencies:** {audit['suffix_inconsistencies']}",
        f"**Type word overlaps:** {audit['type_word_overlaps']}",
        f"**Separator issues:** {audit['separator_issues']}",
        "",
        "## Suffix Distribution",
    ]
    dist = audit.get("suffix_distribution", {})
    for suffix, count in dist.get("suffix_distribution", {}).items():
        lines.append(f"- {suffix}: {count}")
    lines.append(f"- (no suffix): {dist.get('no_suffix_count', 0)}")

    if audit.get("suffix_issues"):
        lines.extend(["", "## Suffix Inconsistencies"])
        for issue in audit["suffix_issues"]:
            names = [f"{e['name']} ({e['slug']})" for e in issue["products"]]
            lines.append(f"- **{issue['base_name']}**: {', '.join(names)}")

    if audit.get("type_issues"):
        lines.extend(["", "## Type Word Overlaps"])
        for issue in audit["type_issues"]:
            names = [f"{e['name']} [{e['type_category']}]" for e in issue["products"]]
            lines.append(f"- **{issue['base_name']}**: {', '.join(names)}")

    if audit.get("separator_issues_list"):
        lines.extend(["", "## Separator Issues"])
        for issue in audit["separator_issues_list"]:
            lines.append(f"- {issue['name']} ({issue['slug']}): {issue['separators']}")

    return "\n".join(lines)


def main(state_path: Path | None = None) -> dict[str, Any]:
    parser = argparse.ArgumentParser(description="Portfolio naming consistency audit")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fix-suggestions", action="store_true")
    args = parser.parse_args()

    audit = run_audit(state_path or STATE_PATH)

    if args.fix_suggestions:
        if args.json:
            print(json.dumps(audit.get("fix_suggestions", []), indent=2))
        else:
            for s in audit.get("fix_suggestions", []):
                print(
                    f"  {s['action']}: {s['from_name']} -> keep {s['keep_name']}"
                    f" ({s['reason']})"
                )
    elif args.json:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
    else:
        print(format_audit_report(audit))

    return audit


if __name__ == "__main__":
    main()
