#!/usr/bin/env python3
"""Analyze functional overlap between products in the portfolio.

Detects products that serve similar purposes based on keyword analysis
of names, descriptions, taglines, and features.  Helps identify
consolidation candidates to reduce portfolio bloat and improve clarity.

Usage::

    python3 -m scripts.product_overlap_analyzer
    python3 -m scripts.product_overlap_analyzer --json
    python3 -m scripts.product_overlap_analyzer --threshold 0.4
    python3 -m scripts.product_overlap_analyzer --categories
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "products"
STATE_SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

DEFAULT_THRESHOLD = 0.35

STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "as", "be", "was", "are",
    "been", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "this", "that", "these",
    "those", "not", "no", "so", "if", "than", "too", "very", "just",
    "about", "up", "out", "all", "also", "into", "over", "after",
    "your", "you", "we", "they", "our", "their", "its",
    "pro", "generator", "tool", "converter", "builder", "maker",
    "studio", "checker", "validator", "formatter", "analyzer",
    "online", "free", "instant", "perfect", "easy", "simple",
    "need", "needs", "help", "helps", "using", "use", "used",
})


def _tokenize(text: str) -> list[str]:
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]


def _extract_keywords(product: dict[str, Any]) -> list[str]:
    tokens: list[str] = []
    for field in ("name", "tagline", "description"):
        val = product.get(field, "")
        if val:
            tokens.extend(_tokenize(str(val)))
    for feat in product.get("features", []):
        if feat:
            tokens.extend(_tokenize(str(feat)))
    return tokens


def _jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def load_products(products_dir: Path = PRODUCTS_DIR) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    if not products_dir.is_dir():
        return products
    for entry in sorted(products_dir.iterdir()):
        if not entry.is_dir():
            continue
        pj = entry / "product.json"
        if not pj.exists():
            continue
        try:
            data = json.loads(pj.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        data["_dir"] = entry.name
        products.append(data)
    return products


def compute_overlap_matrix(
    products: list[dict[str, Any]],
    *,
    threshold: float = DEFAULT_THRESHOLD,
) -> list[dict[str, Any]]:
    keyword_sets: list[tuple[dict[str, Any], set[str]]] = []
    for p in products:
        kw = set(_extract_keywords(p))
        if kw:
            keyword_sets.append((p, kw))

    overlaps: list[dict[str, Any]] = []
    for i in range(len(keyword_sets)):
        for j in range(i + 1, len(keyword_sets)):
            p_a, kw_a = keyword_sets[i]
            p_b, kw_b = keyword_sets[j]
            sim = _jaccard_similarity(kw_a, kw_b)
            if sim >= threshold:
                shared = sorted(kw_a & kw_b)
                overlaps.append({
                    "slug_a": p_a.get("slug", p_a.get("_dir", "?")),
                    "name_a": p_a.get("name", "?"),
                    "slug_b": p_b.get("slug", p_b.get("_dir", "?")),
                    "name_b": p_b.get("name", "?"),
                    "similarity": round(sim, 3),
                    "shared_keywords": shared,
                    "shared_count": len(shared),
                })

    overlaps.sort(key=lambda o: (-o["similarity"], o["slug_a"]))
    return overlaps


def overlap_summary(
    products: list[dict[str, Any]],
    *,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Any]:
    overlaps = compute_overlap_matrix(products, threshold=threshold)
    affected_slugs: set[str] = set()
    for o in overlaps:
        affected_slugs.add(o["slug_a"])
        affected_slugs.add(o["slug_b"])

    sim_buckets: dict[str, int] = {
        "high_0.6+": 0,
        "medium_0.4-0.6": 0,
        "low_0.35-0.4": 0,
    }
    for o in overlaps:
        s = o["similarity"]
        if s >= 0.6:
            sim_buckets["high_0.6+"] += 1
        elif s >= 0.4:
            sim_buckets["medium_0.4-0.6"] += 1
        else:
            sim_buckets["low_0.35-0.4"] += 1

    keyword_counter: Counter[str] = Counter()
    for o in overlaps:
        keyword_counter.update(o["shared_keywords"])

    return {
        "total_products": len(products),
        "overlap_pairs": len(overlaps),
        "affected_products": len(affected_slugs),
        "affected_slugs": sorted(affected_slugs),
        "similarity_buckets": sim_buckets,
        "top_shared_keywords": keyword_counter.most_common(20),
        "overlaps": overlaps,
    }


def category_clustering(
    products: list[dict[str, Any]],
) -> dict[str, list[str]]:
    clusters: dict[str, list[str]] = {}
    for p in products:
        keywords = _extract_keywords(p)
        if not keywords:
            continue
        primary = keywords[0] if keywords else "other"
        counter = Counter(keywords)
        top = counter.most_common(1)[0][0]
        category = top if top != primary else primary
        clusters.setdefault(category, []).append(
            p.get("slug", p.get("_dir", "?"))
        )
    return {k: v for k, v in sorted(clusters.items(), key=lambda x: -len(x[1]))}


def consolidation_suggestions(
    overlaps: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    for o in overlaps:
        if o["similarity"] < 0.5:
            continue
        slug_a = o["slug_a"]
        slug_b = o["slug_b"]
        keep = slug_a if len(slug_a) >= len(slug_b) else slug_b
        merge = slug_b if keep == slug_a else slug_a
        suggestions.append({
            "keep": keep,
            "merge_into": merge,
            "similarity": o["similarity"],
            "shared_keywords": o["shared_keywords"],
            "reason": f"{o['similarity']:.0%} keyword overlap — likely duplicate or near-duplicate",
        })
    return suggestions


def format_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Product Overlap Analysis",
        "",
        f"**Products analyzed:** {summary['total_products']}",
        f"**Overlap pairs:** {summary['overlap_pairs']}",
        f"**Affected products:** {summary['affected_products']}",
        "",
        "## Similarity Distribution",
    ]
    for bucket, count in summary["similarity_buckets"].items():
        marker = "**" if "high" in bucket else ""
        lines.append(f"- {marker}{bucket}: {count} pairs{marker}")

    lines.append("")
    lines.append("## Top Shared Keywords")
    for kw, count in summary["top_shared_keywords"][:10]:
        lines.append(f"- `{kw}`: {count} pairs")

    lines.append("")
    lines.append("## Overlap Pairs (sorted by similarity)")
    for o in summary["overlaps"]:
        lines.append(
            f"- `{o['slug_a']}` ↔ `{o['slug_b']}` "
            f"({o['similarity']:.0%}) — "
            f"shared: {', '.join(o['shared_keywords'][:5])}"
        )

    suggestions = consolidation_suggestions(summary["overlaps"])
    if suggestions:
        lines.append("")
        lines.append("## Consolidation Candidates (>50% overlap)")
        for s in suggestions:
            lines.append(
                f"- KEEP `{s['keep']}` ← merge `{s['merge_into']}` "
                f"({s['similarity']:.0%})"
            )

    return "\n".join(lines)


def main() -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Product overlap analyzer")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--categories", action="store_true")
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Similarity threshold (default: {DEFAULT_THRESHOLD})",
    )
    args = parser.parse_args()

    products = load_products()
    if not products:
        print("No products found.")
        return {}

    if args.categories:
        clusters = category_clustering(products)
        if args.json:
            print(json.dumps(clusters, indent=2, ensure_ascii=False))
        else:
            for cat, slugs in clusters.items():
                print(f"\n[{cat}] ({len(slugs)} products)")
                for s in slugs:
                    print(f"  - {s}")
        return {"clusters": clusters}

    summary = overlap_summary(products, threshold=args.threshold)

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(format_report(summary))

    return summary


if __name__ == "__main__":
    main()
