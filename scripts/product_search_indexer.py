#!/usr/bin/env python3
"""Build a searchable index of all products for dedup and discovery.

Reads STATE.json products, extracts searchable tokens from name/slug/category/tags,
builds an inverted index for fast keyword lookup, and detects potential duplicates
via slug similarity scoring.

Usage:
    python3 scripts/product_search_indexer.py search "uuid generator"
    python3 scripts/product_search_indexer.py search --category developer-tools
    python3 scripts/product_search_indexer.py duplicates --threshold 0.6
    python3 scripts/product_search_indexer.py stats
    python3 scripts/product_search_indexer.py --json
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "STATE.json"

STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "for", "in", "on", "to", "of", "with",
    "by", "is", "it", "at", "as", "be", "this", "that", "from", "but", "not",
    "pro", "tool", "tools", "app", "maker", "creator", "generator", "builder",
    "manager", "helper", "simple", "easy", "fast", "free", "online", "web",
})


def _tokenize(text: str) -> list[str]:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    tokens = []
    for part in text.split():
        for sub in part.split("-"):
            sub = sub.strip()
            if sub and sub not in STOP_WORDS and len(sub) > 1:
                tokens.append(sub)
    return tokens


def load_products() -> list[dict[str, Any]]:
    if not STATE_FILE.exists():
        return []
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return state.get("products", {}).get("active", [])


def build_index(products: list[dict]) -> dict[str, Any]:
    inverted: dict[str, list[str]] = defaultdict(list)
    token_map: dict[str, list[str]] = {}
    categories: dict[str, list[str]] = defaultdict(list)

    for p in products:
        slug = p.get("slug", "")
        name = p.get("name", "")
        category = p.get("category", "")
        tags = p.get("tags", [])

        all_text = " ".join([name, slug, " ".join(tags)])
        tokens = _tokenize(all_text)
        unique_tokens = list(set(tokens))

        token_map[slug] = unique_tokens

        for t in unique_tokens:
            inverted[t].append(slug)

        if category:
            categories[category].append(slug)

    return {
        "inverted": dict(inverted),
        "token_map": token_map,
        "categories": dict(categories),
        "product_count": len(products),
    }


def search(
    index: dict[str, Any],
    products: list[dict],
    query: str,
    category: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    query_tokens = set(_tokenize(query))
    if not query_tokens:
        return []

    slug_scores: dict[str, float] = defaultdict(float)
    inverted = index["inverted"]
    token_map = index["token_map"]

    for qt in query_tokens:
        for idx_token, slugs in inverted.items():
            if qt == idx_token:
                for s in slugs:
                    slug_scores[s] += 2.0
            elif qt in idx_token or idx_token in qt:
                for s in slugs:
                    slug_scores[s] += 1.0

    if category:
        cat_slugs = set(index["categories"].get(category, []))
        slug_scores = {s: sc for s, sc in slug_scores.items() if s in cat_slugs}

    results = sorted(slug_scores.items(), key=lambda x: -x[1])[:limit]

    slug_to_product = {p.get("slug", ""): p for p in products}

    output = []
    for slug, score in results:
        p = slug_to_product.get(slug, {})
        output.append({
            "slug": slug,
            "name": p.get("name", ""),
            "category": p.get("category", ""),
            "status": p.get("status", ""),
            "score": round(score, 2),
            "tags": p.get("tags", []),
        })

    return output


def find_duplicates(
    products: list[dict],
    threshold: float = 0.6,
    limit: int = 30,
) -> list[dict[str, Any]]:
    slugs = [p.get("slug", "") for p in products]
    names = [p.get("name", "") for p in products]
    n = len(slugs)
    pairs = []

    for i in range(n):
        for j in range(i + 1, min(i + 50, n)):
            slug_sim = SequenceMatcher(None, slugs[i], slugs[j]).ratio()
            name_sim = SequenceMatcher(None, names[i].lower(), names[j].lower()).ratio()
            combined = max(slug_sim, name_sim)
            if combined >= threshold:
                pairs.append({
                    "product_a": slugs[i],
                    "product_b": slugs[j],
                    "name_a": names[i],
                    "name_b": names[j],
                    "similarity": round(combined, 3),
                })

    pairs.sort(key=lambda x: -x["similarity"])
    return pairs[:limit]


def compute_stats(products: list[dict], index: dict) -> dict[str, Any]:
    categories: dict[str, int] = Counter()
    statuses: dict[str, int] = Counter()
    tag_counter: Counter = Counter()
    price_counter: Counter = Counter()

    for p in products:
        categories[p.get("category", "uncategorized")] += 1
        statuses[p.get("status", "unknown")] += 1
        for t in p.get("tags", []):
            tag_counter[t] += 1
        price_counter[str(p.get("price", "none"))] += 1

    vocab_size = len(index["inverted"])

    return {
        "total_products": len(products),
        "vocabulary_size": vocab_size,
        "categories": dict(categories.most_common()),
        "statuses": dict(statuses),
        "top_tags": dict(tag_counter.most_common(15)),
        "top_prices": dict(price_counter.most_common(10)),
    }


def format_results(results: list[dict], title: str) -> str:
    lines = [f"# {title}", ""]
    for r in results:
        name = r.get("name") or r.get("name_a") or r.get("product_a", "")
        slug = r.get("slug") or r.get("product_a", "")
        lines.append(
            f"- **{name}** "
            f"(`{slug}`) "
            f"[{r.get('category', '')}] "
            f"score={r.get('score', r.get('similarity', 0))}"
        )
        if r.get("name_b"):
            lines.append(f"  ↔ **{r['name_b']}** (`{r['product_b']}`) sim={r['similarity']}")
    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Product search indexer")
    sub = parser.add_subparsers(dest="command")

    s_search = sub.add_parser("search", help="Search products by keywords")
    s_search.add_argument("query", nargs="*", default=[])
    s_search.add_argument("--category", "-c", default=None)
    s_search.add_argument("--limit", "-n", type=int, default=20)

    s_dup = sub.add_parser("duplicates", help="Find potential duplicate products")
    s_dup.add_argument("--threshold", "-t", type=float, default=0.6)
    s_dup.add_argument("--limit", "-n", type=int, default=30)

    sub.add_parser("stats", help="Show portfolio statistics")

    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    products = load_products()
    index = build_index(products)

    if args.command == "search":
        query = " ".join(args.query)
        results = search(index, products, query, category=args.category, limit=args.limit)
        if args.json:
            print(json.dumps({"query": query, "results": results}, indent=2, ensure_ascii=False))
        else:
            print(format_results(results, f"Search: '{query}'"))
        return {"results": results}

    if args.command == "duplicates":
        pairs = find_duplicates(products, threshold=args.threshold, limit=args.limit)
        if args.json:
            print(json.dumps(pairs, indent=2, ensure_ascii=False))
        else:
            print(format_results(pairs, f"Duplicates (threshold={args.threshold})"))
        return {"duplicates": pairs}

    if args.command == "stats":
        stats = compute_stats(products, index)
        if args.json:
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            lines = ["# Portfolio Statistics", ""]
            lines.append(f"Total products: {stats['total_products']}")
            lines.append(f"Vocabulary size: {stats['vocabulary_size']}")
            lines.append("")
            lines.append("## Categories")
            for cat, n in stats["categories"].items():
                lines.append(f"- {cat}: {n}")
            lines.append("")
            lines.append("## Top Tags")
            for tag, n in stats["top_tags"].items():
                lines.append(f"- {tag}: {n}")
            print("\n".join(lines))
        return stats

    if args.json:
        print(json.dumps({"index_size": index["product_count"]}, indent=2))
    else:
        print(f"Index built: {index['product_count']} products, {len(index['inverted'])} tokens")
    return index


if __name__ == "__main__":
    main()
