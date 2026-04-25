#!/usr/bin/env python3
"""Categorize products by function and detect overlap opportunities.

Groups products from STATE_SUMMARY.json into functional categories,
identifies clusters with multiple products, and reports consolidation
candidates.  Useful for strategic decisions and SEO optimization.

Usage:
    python3 scripts/product_category_map.py
    python3 scripts/product_category_map.py --json
    python3 scripts/product_category_map.py --consolidation
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

CATEGORY_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("cron", re.compile(r"cron", re.I)),
    ("jwt", re.compile(r"jwt", re.I)),
    ("toml", re.compile(r"toml", re.I)),
    ("yaml", re.compile(r"yaml", re.I)),
    ("json", re.compile(r"json", re.I)),
    ("xml", re.compile(r"\bxml\b", re.I)),
    ("csv", re.compile(r"\bcsv\b", re.I)),
    ("markdown", re.compile(r"markdown|md\b", re.I)),
    ("html", re.compile(r"html|htm\b|htaccess|htpasswd", re.I)),
    ("css", re.compile(r"\bcss\b", re.I)),
    ("docker", re.compile(r"docker", re.I)),
    ("nginx", re.compile(r"nginx", re.I)),
    ("ssl", re.compile(r"\bssl\b|tls\b|cipher|certificate", re.I)),
    ("security", re.compile(r"security|secret|password|hmac|hash", re.I)),
    ("regex", re.compile(r"regex|regexp", re.I)),
    ("api", re.compile(r"\bapi\b|openapi|graphql|webhook|rest", re.I)),
    ("diff", re.compile(r"\bdiff\b", re.I)),
    ("base64", re.compile(r"base64", re.I)),
    ("email", re.compile(r"\bemail\b", re.I)),
    ("url", re.compile(r"\burl\b|uri\b|link", re.I)),
    ("color", re.compile(r"\bcolor\b|colour|palette|gradient|contrast", re.I)),
    ("svg", re.compile(r"\bsvg\b", re.I)),
    ("timestamp", re.compile(r"timestamp|date.?time|time.?zone", re.I)),
    ("uuid", re.compile(r"\buuid\b|nanoid|id.?gen", re.I)),
    ("sql", re.compile(r"\bsql\b", re.I)),
    ("env", re.compile(r"\benv\b|environment", re.I)),
    ("mcp", re.compile(r"\bmcp\b", re.I)),
    ("seo", re.compile(r"\bseo\b|og.?tag|meta|sitemap", re.I)),
    ("git", re.compile(r"\bgit\b", re.I)),
    ("code", re.compile(r"\bcode\b|snippet|screenshot|beautif|format|minif", re.I)),
    ("image", re.compile(r"\bimage\b|favicon|qr\b", re.I)),
    ("http", re.compile(r"http|curl|webhook|load.?test", re.I)),
    ("text", re.compile(r"\btext\b|case.?conv|lorem|signature", re.I)),
    ("number", re.compile(r"\bnumber\b|binary|base.?conv|chmod", re.I)),
    ("terminal", re.compile(r"terminal|shell|bash", re.I)),
    ("agent", re.compile(r"\bagent\b|browser.?use|prompt.?eng", re.I)),
    ("geo", re.compile(r"\bgeo\b|ip.?net|subdomain", re.I)),
    ("pdf", re.compile(r"\bpdf\b", re.I)),
    ("chart", re.compile(r"\bchart\b", re.I)),
]


def _load_products(path: Path = SUMMARY_PATH) -> list[dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    products = raw.get("products", [])
    if not isinstance(products, list):
        return []
    return products


def _product_name(p: dict[str, Any]) -> str:
    return p.get("n") or p.get("name") or ""


def _product_slug(p: dict[str, Any]) -> str:
    return p.get("s") or p.get("slug") or ""


def _product_checkout(p: dict[str, Any]) -> str:
    return (p.get("c") or p.get("checkout_url") or "").strip()


def categorize_product(p: dict[str, Any]) -> list[str]:
    name = _product_name(p)
    slug = _product_slug(p)
    text = f"{name} {slug}"
    categories: list[str] = []
    for cat, pattern in CATEGORY_RULES:
        if pattern.search(text):
            categories.append(cat)
    if not categories:
        categories.append("other")
    return categories


def build_category_map(
    products: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, str]]]:
    if products is None:
        products = _load_products()

    cat_map: dict[str, list[dict[str, str]]] = {}
    for p in products:
        slug = _product_slug(p)
        name = _product_name(p)
        checkout = _product_checkout(p)
        for cat in categorize_product(p):
            cat_map.setdefault(cat, []).append({
                "slug": slug,
                "name": name,
                "checkout": checkout,
            })

    for entries in cat_map.values():
        entries.sort(key=lambda e: e["slug"])
    return cat_map


def find_overlap_categories(
    cat_map: dict[str, list[dict[str, str]]],
    threshold: int = 3,
) -> list[dict[str, Any]]:
    overlaps: list[dict[str, Any]] = []
    for cat, entries in sorted(cat_map.items()):
        if len(entries) >= threshold:
            overlaps.append({
                "category": cat,
                "count": len(entries),
                "products": entries,
            })
    overlaps.sort(key=lambda o: (-o["count"], o["category"]))
    return overlaps


def find_shared_checkout(
    products: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if products is None:
        products = _load_products()

    url_groups: dict[str, list[str]] = {}
    for p in products:
        checkout = _product_checkout(p)
        slug = _product_slug(p)
        if checkout.startswith("http"):
            url_groups.setdefault(checkout, []).append(slug)

    shared: list[dict[str, Any]] = []
    for url, slugs in sorted(url_groups.items()):
        if len(slugs) >= 2:
            shared.append({"checkout_url": url, "count": len(slugs), "slugs": slugs})
    shared.sort(key=lambda s: (-s["count"], s["slugs"][0]))
    return shared


def consolidation_report(
    cat_map: dict[str, list[dict[str, str]]] | None = None,
    shared: list[dict[str, Any]] | None = None,
    products: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if cat_map is None:
        cat_map = build_category_map(products)
    if shared is None:
        shared = find_shared_checkout(products)

    overlaps = find_overlap_categories(cat_map)
    total_products = sum(len(e) for e in cat_map.values())
    unique_slugs: set[str] = set()
    for entries in cat_map.values():
        for e in entries:
            unique_slugs.add(e["slug"])

    return {
        "total_unique_products": len(unique_slugs),
        "total_categories": len(cat_map),
        "overlaps": overlaps,
        "shared_checkout_groups": len(shared),
        "shared_checkout_products": sum(s["count"] for s in shared),
        "categories": {
            cat: len(entries)
            for cat, entries in sorted(cat_map.items(), key=lambda x: -len(x[1]))
        },
        "shared_checkout_details": shared,
    }


def report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Product Category Map",
        f"**Unique products:** {report['total_unique_products']}",
        f"**Categories:** {report['total_categories']}",
        f"**Shared checkout groups:** {report['shared_checkout_groups']}",
        f"**Products sharing checkout:** {report['shared_checkout_products']}",
        "",
        "## Category Distribution",
        "| Category | Products |",
        "|----------|----------|",
    ]
    for cat, count in report["categories"].items():
        marker = " **OVERLAP**" if count >= 3 else ""
        lines.append(f"| {cat} | {count}{marker} |")
    lines.append("")

    if report["overlaps"]:
        lines.append("## Consolidation Candidates (3+ products)")
        for o in report["overlaps"]:
            lines.append(f"### {o['category']} ({o['count']} products)")
            for p in o["products"]:
                lines.append(f"- **{p['slug']}** — {p['name']}")
            lines.append("")

    if report["shared_checkout_details"]:
        lines.append("## Shared Checkout URLs")
        for s in report["shared_checkout_details"]:
            lines.append(f"- {s['slugs']} ({s['count']} products)")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    as_json = "--json" in sys.argv
    as_consolidation = "--consolidation" in sys.argv

    report = consolidation_report()

    if as_consolidation:
        report_markdown(report)
        for o in report["overlaps"]:
            print(f"[{o['category']}] {o['count']} products: {[p['slug'] for p in o['products']]}")
        print(f"\nShared checkout groups: {report['shared_checkout_groups']}")
        for s in report["shared_checkout_details"]:
            print(f"  {s['slugs']}")
    elif as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(report_markdown(report))

    return 0


if __name__ == "__main__":
    sys.exit(main())
