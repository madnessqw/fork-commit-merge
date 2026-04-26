#!/usr/bin/env python3
"""Analyze and auto-categorize uncategorized products based on slug/name keywords.

Scans STATE.json for products missing category/tags and assigns them using
keyword matching rules. Provides audit, auto-fix, and reporting modes.

Usage:
    python3 scripts/product_tag_analyzer.py audit          # Show uncategorized + suggestions
    python3 scripts/product_tag_analyzer.py apply           # Apply categories to STATE.json
    python3 scripts/product_tag_analyzer.py report          # Full tag/category report
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
STATE_FILE = ROOT / "STATE.json"
ANALYSIS_DIR = ROOT / "analysis"

CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("developer-tools", [
        "json", "yaml", "toml", "xml", "csv", "markdown", "code", "syntax",
        "formatter", "beautifier", "minifier", "lint", "regex", "base64",
        "encoder", "decoder", "parser", "validator", "converter", "transform",
        "uuid", "hash", "jwt", "token", "generator", "diff", "merge",
        "snippet", "template", "compiler", "transpiler", "prettier",
        "typescript", "javascript", "python", "sql", "query",
        "html", "css", "svg", "color", "font",
    ]),
    ("security", [
        "security", "encrypt", "decrypt", "cipher", "password", "hash",
        "firewall", "auth", "oauth", "jwt", "csrf", "xss", "ssl", "tls",
        "certificate", "vulnerability", "penetration", "scan", "audit",
        "hmac", "sha", "md5", "bcrypt", "argon", "rsa", "aes",
    ]),
    ("devops", [
        "deploy", "docker", "kubernetes", "k8s", "container", "ci", "cd",
        "pipeline", "monitor", "log", "alert", "cron", "schedule", "backup",
        "infrastructure", "terraform", "ansible", "nginx", "apache",
        "server", "proxy", "load", "uptime", "health", "ping",
        "terminal", "ssh", "shell", "bash",
    ]),
    ("api-services", [
        "api", "rest", "graphql", "endpoint", "webhook", "grpc",
        "request", "response", "http", "url", "mock",
        "postman", "swagger", "openapi", "rate", "limit",
    ]),
    ("utilities", [
        "calculator", "timer", "counter", "clock", "random", "math",
        "unit", "convert", "measure", "scale", "resize", "compress",
        "extract", "split", "join", "sort", "filter", "search",
        "timestamp", "date", "time", "calendar", "age",
        "qr", "barcode", "otp", "totp", "generator",
        "lorem", "placeholder", "fake", "mock",
    ]),
    ("design-tools", [
        "design", "ui", "ux", "mockup", "wireframe", "prototype",
        "gradient", "palette", "icon", "image", "photo", "editor",
        "canvas", "draw", "pixel", "animation", "figma",
    ]),
    ("ai-tools", [
        "ai ", "ml ", "machine learning", "neural", "model",
        "train", "predict", "classify", "nlp", "sentiment",
        "chatbot", "gpt", "llm", "prompt", "embedding", "vector",
        "ocr", "speech", "text to", "image gen",
    ]),
]

CATEGORY_PRIORITY = [
    "ai-tools", "security", "devops", "developer-tools",
    "api-services", "design-tools", "utilities",
]

TAG_RULES: dict[str, list[str]] = {
    "formatter": ["beautifier", "minifier", "prettier", "formatter", "format"],
    "encoder-decoder": ["encoder", "decoder", "base64", "url-encode"],
    "converter": ["converter", "transform", "translate", "transpiler"],
    "validator": ["validator", "lint", "check", "verify"],
    "generator": ["generator", "create", "builder", "maker"],
    "analyzer": ["analyzer", "inspector", "debugger", "profiler"],
    "security": ["encrypt", "decrypt", "hash", "password", "jwt", "token", "auth"],
    "devops": ["deploy", "docker", "k8s", "nginx", "cron", "terminal"],
    "api": ["api", "rest", "graphql", "webhook", "http"],
    "data": ["json", "yaml", "csv", "xml", "sql", "database"],
    "text": ["text", "markdown", "string", "regex", "diff"],
    "visual": ["color", "css", "svg", "image", "gradient", "palette"],
    "utility": ["calculator", "timer", "counter", "random", "uuid"],
}


def _slug_text(slug: str, name: str) -> str:
    import re as _re
    text = f"{slug} {name}".lower()
    text = text.replace("-", " ").replace("_", " ")
    text = _re.sub(r'([a-z])([A-Z])', r'\1 \2', text).lower()
    text = _re.sub(r'([a-z])(\d)', r'\1 \2', text)
    text = _re.sub(r'(\d)([a-z])', r'\1 \2', text)
    return f" {text} "


def _has_keyword(text: str, keyword: str) -> bool:
    return f" {keyword} " in text or text.strip().startswith(f"{keyword} ") or text.strip().endswith(f" {keyword}")


def classify_category(slug: str, name: str) -> str:
    text = _slug_text(slug, name)
    scores: dict[str, int] = Counter()
    for category, keywords in CATEGORY_RULES:
        for kw in keywords:
            if _has_keyword(text, kw):
                scores[category] += 1
    if not scores:
        return "utilities"
    for cat in CATEGORY_PRIORITY:
        if cat in scores:
            return cat
    return scores.most_common(1)[0][0]


def suggest_tags(slug: str, name: str) -> list[str]:
    text = _slug_text(slug, name)
    tags = []
    for tag, keywords in TAG_RULES.items():
        for kw in keywords:
            if _has_keyword(text, kw):
                tags.append(tag)
                break
    return tags


def load_state() -> dict[str, Any]:
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state: dict[str, Any]) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_products(state: dict[str, Any]) -> list[dict[str, Any]]:
    return state.get("products", {}).get("active", [])


def audit(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for p in products:
        slug = p.get("slug", p.get("s", "unknown"))
        name = p.get("name", p.get("n", "unknown"))
        category = p.get("category", "uncategorized")
        tags = p.get("tags", [])
        needs_category = category in ("uncategorized", "", None)
        needs_tags = len(tags) == 0

        if not needs_category and not needs_tags:
            continue

        suggested_cat = classify_category(slug, name) if needs_category else category
        suggested_tags = suggest_tags(slug, name) if needs_tags else tags

        results.append({
            "slug": slug,
            "name": name,
            "current_category": category,
            "suggested_category": suggested_cat,
            "needs_category": needs_category,
            "current_tags": tags,
            "suggested_tags": suggested_tags,
            "needs_tags": needs_tags,
        })
    return results


def apply_categories(products: list[dict[str, Any]], state: dict[str, Any]) -> int:
    changes = 0
    for p in products:
        slug = p.get("slug", p.get("s", ""))
        name = p.get("name", p.get("n", ""))
        category = p.get("category", "uncategorized")
        tags = p.get("tags", [])

        changed = False
        if category in ("uncategorized", "", None):
            p["category"] = classify_category(slug, name)
            changed = True
        if not tags:
            p["tags"] = suggest_tags(slug, name)
            changed = True

        if changed:
            changes += 1

    if changes > 0:
        save_state(state)
    return changes


def generate_report(products: list[dict[str, Any]]) -> dict[str, Any]:
    cat_dist = Counter(p.get("category", "uncategorized") for p in products)
    tag_dist = Counter(t for p in products for t in p.get("tags", []))
    uncat = sum(1 for p in products if p.get("category", "uncategorized") == "uncategorized")
    no_tags = sum(1 for p in products if not p.get("tags", []))

    by_cat: dict[str, list[str]] = defaultdict(list)
    for p in products:
        cat = p.get("category", "uncategorized")
        slug = p.get("slug", p.get("s", ""))
        by_cat[cat].append(slug)

    report = {
        "total": len(products),
        "uncategorized": uncat,
        "no_tags": no_tags,
        "category_distribution": dict(cat_dist.most_common()),
        "top_tags": dict(tag_dist.most_common(15)),
        "by_category": {k: v for k, v in sorted(by_cat.items())},
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Product tag/category analyzer")
    parser.add_argument("command", choices=["audit", "apply", "report"],
                        help="audit=show gaps, apply=auto-fix STATE.json, report=full stats")
    args = parser.parse_args()

    state = load_state()
    products = get_products(state)

    if args.command == "audit":
        results = audit(products)
        if not results:
            print("All products have categories and tags.")
            return 0

        print(f"=== Product Tag/Category Audit ({len(results)} need attention) ===\n")
        cat_only = [r for r in results if r["needs_category"]]
        tag_only = [r for r in results if r["needs_tags"]]
        both = [r for r in results if r["needs_category"] and r["needs_tags"]]

        print(f"Missing category: {len(cat_only)}")
        print(f"Missing tags: {len(tag_only)}")
        print(f"Missing both: {len(both)}\n")

        print("Suggestions (first 20):")
        for r in results[:20]:
            cat_str = f"{r['current_category']} → {r['suggested_category']}" if r["needs_category"] else "✓"
            tag_str = f"[] → {r['suggested_tags']}" if r["needs_tags"] else "✓"
            print(f"  {r['slug']:35s} cat={cat_str:30s} tags={tag_str}")
        if len(results) > 20:
            print(f"  ... and {len(results) - 20} more")

    elif args.command == "apply":
        count = apply_categories(products, state)
        if count > 0:
            print(f"Updated {count} products with categories/tags in STATE.json")

            report = generate_report(get_products(load_state()))
            print(f"\nNew distribution:")
            for cat, cnt in sorted(report["category_distribution"].items(), key=lambda x: -x[1]):
                print(f"  {cat:20s}: {cnt}")
        else:
            print("No products needed updating.")

    elif args.command == "report":
        report = generate_report(products)
        print(f"=== Product Category/Tag Report ===")
        print(f"Total: {report['total']}")
        print(f"Uncategorized: {report['uncategorized']}")
        print(f"No tags: {report['no_tags']}\n")

        print("Category Distribution:")
        for cat, cnt in sorted(report["category_distribution"].items(), key=lambda x: -x[1]):
            pct = cnt / report["total"] * 100
            bar = "#" * int(pct / 2)
            print(f"  {cat:20s}: {cnt:3d} ({pct:5.1f}%) {bar}")

        if report["top_tags"]:
            print("\nTop Tags:")
            for tag, cnt in report["top_tags"].items():
                print(f"  {tag:20s}: {cnt}")

        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        out = ANALYSIS_DIR / "product_tag_report.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nSaved: {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
