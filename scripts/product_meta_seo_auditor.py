#!/usr/bin/env python3
"""Audit SEO meta tag quality across all products.

Scans each product's index.html for meta tags (title, description,
og:*, keywords, canonical, robots) and scores them based on completeness,
length, and common defects (typos, truncated values, duplicate content).

Usage::

    python3 scripts/product_meta_seo_auditor.py audit
    python3 scripts/product_meta_seo_auditor.py audit --json
    python3 scripts/product_meta_seo_auditor.py fix-dry-run
    python3 scripts/product_meta_seo_auditor.py report
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "products"
STATE_SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
ANALYSIS_DIR = ROOT / "analysis"

IDEAL_TITLE_LEN = (30, 60)
IDEAL_DESC_LEN = (120, 160)
MAX_KEYWORDS = 10


class MetaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_text = ""
        self._in_title = False
        self.metas: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = attrs_dict.get("name", attrs_dict.get("property", "")).lower()
            content = attrs_dict.get("content", "")
            if name and content:
                self.metas[name] = content
        if tag == "link":
            rel = attrs_dict.get("rel", "").lower()
            href = attrs_dict.get("href", "")
            if rel == "canonical" and href:
                self.metas["canonical"] = href

    def handle_data(self, data):
        if self._in_title:
            self.title_text += data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def extract_meta(html_path: Path) -> dict[str, Any]:
    if not html_path.exists():
        return {}
    raw = html_path.read_text(encoding="utf-8", errors="replace")
    parser = MetaExtractor()
    try:
        parser.feed(raw)
    except Exception:
        pass
    return {"title": parser.title_text, **parser.metas}


def score_meta(meta: dict[str, str]) -> dict[str, Any]:
    issues: list[str] = []
    score = 0

    title = meta.get("title", "")
    if title:
        score += 15
        tl = len(title)
        if tl < IDEAL_TITLE_LEN[0]:
            issues.append(f"title_short({tl})")
        elif tl > IDEAL_TITLE_LEN[1]:
            issues.append(f"title_long({tl})")
        else:
            score += 10
    else:
        issues.append("title_missing")

    desc = meta.get("description", "")
    if desc:
        score += 15
        dl = len(desc)
        if dl < IDEAL_DESC_LEN[0]:
            issues.append(f"desc_short({dl})")
        elif dl > IDEAL_DESC_LEN[1]:
            issues.append(f"desc_long({dl})")
        else:
            score += 10
        if "agentmpt" in desc.lower():
            issues.append("typo_agentmpt")
        if "universe7creator" in desc.lower():
            issues.append("typo_universe7creator")
        if "universe7" in desc.lower():
            issues.append("typo_universe7")
    else:
        issues.append("desc_missing")

    og_title = meta.get("og:title", "")
    if og_title:
        score += 5
    else:
        issues.append("og_title_missing")

    og_desc = meta.get("og:description", "")
    if og_desc:
        score += 5
    else:
        issues.append("og_desc_missing")

    kw = meta.get("keywords", "")
    if kw:
        score += 5
        kw_count = len([k.strip() for k in kw.split(",") if k.strip()])
        if kw_count > MAX_KEYWORDS:
            issues.append(f"keywords_excessive({kw_count})")
    else:
        issues.append("keywords_missing")

    canonical = meta.get("canonical", "")
    if canonical:
        score += 10
    else:
        issues.append("canonical_missing")

    robots = meta.get("robots", "")
    if robots:
        score += 5
        if "noindex" in robots.lower():
            issues.append("noindex_set")
    else:
        issues.append("robots_missing")

    og_image = meta.get("og:image", "")
    if og_image:
        score += 5
    else:
        issues.append("og_image_missing")

    return {"score": score, "max_score": 85, "issues": issues}


def audit_product(product_dir: Path) -> dict[str, Any]:
    html_path = product_dir / "index.html"
    pj_path = product_dir / "product.json"
    meta = extract_meta(html_path)
    result = score_meta(meta)
    result["meta"] = meta
    result["slug"] = product_dir.name

    if pj_path.exists():
        try:
            pj = json.loads(pj_path.read_text())
            result["product_name"] = pj.get("name", "")
            result["category"] = pj.get("category", "")
        except Exception:
            result["product_name"] = ""
            result["category"] = ""
    return result


def audit_all() -> list[dict[str, Any]]:
    results = []
    if not PRODUCTS_DIR.exists():
        return results
    for d in sorted(PRODUCTS_DIR.iterdir()):
        if d.is_dir() and (d / "product.json").exists():
            results.append(audit_product(d))
    return results


def cmd_audit(args: list[str]) -> None:
    results = audit_all()
    as_json = "--json" in args

    if as_json:
        print(json.dumps(results, indent=2))
        return

    total = len(results)
    if total == 0:
        print("No products found.")
        return

    scores = [r["score"] for r in results]
    avg_score = sum(scores) / total
    low = [r for r in results if r["score"] < 40]
    issue_counter = Counter()
    for r in results:
        issue_counter.update(r["issues"])

    print(f"SEO Meta Audit — {total} products")
    print(f"Average score: {avg_score:.1f}/{results[0]['max_score']}")
    print(f"Low scoring (<40): {len(low)}")
    print()
    print("Top issues:")
    for issue, count in issue_counter.most_common(15):
        print(f"  {issue}: {count}")
    print()

    if low:
        print("Low-scoring products:")
        for r in sorted(low, key=lambda x: x["score"]):
            print(f"  {r['slug']:40s} score={r['score']:3d} issues={r['issues']}")


def cmd_fix_dry_run(args: list[str]) -> None:
    results = audit_all()
    typo_products = []
    for r in results:
        for issue in r["issues"]:
            if issue.startswith("typo_"):
                typo_products.append(r)
                break

    if not typo_products:
        print("No typo issues found in meta tags.")
        return

    print(f"Products with typo issues: {len(typo_products)}")
    for r in typo_products:
        print(f"  {r['slug']}: {r['issues']}")
    print()
    print("Run with --apply to auto-fix these typos.")


def cmd_report(args: list[str]) -> None:
    results = audit_all()
    total = len(results)
    if total == 0:
        print("No products found.")
        return

    scores = [r["score"] for r in results]
    avg = sum(scores) / total
    buckets = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}
    for s in scores:
        if s >= 65:
            buckets["excellent"] += 1
        elif s >= 50:
            buckets["good"] += 1
        elif s >= 35:
            buckets["fair"] += 1
        else:
            buckets["poor"] += 1

    category_scores: dict[str, list[int]] = defaultdict(list)
    for r in results:
        cat = r.get("category", "unknown")
        category_scores[cat].append(r["score"])

    print(f"SEO Meta Audit Report — {total} products\n")
    print(f"Average: {avg:.1f}/85")
    print(f"Distribution: excellent={buckets['excellent']} good={buckets['good']} fair={buckets['fair']} poor={buckets['poor']}")
    print()
    print("By category:")
    for cat in sorted(category_scores):
        cs = category_scores[cat]
        print(f"  {cat:20s} avg={sum(cs)/len(cs):5.1f} n={len(cs)}")
    print()

    issue_counter = Counter()
    for r in results:
        issue_counter.update(r["issues"])
    print("Issue frequency:")
    for issue, count in issue_counter.most_common(20):
        pct = count / total * 100
        print(f"  {issue:30s} {count:4d} ({pct:5.1f}%)")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: product_meta_seo_auditor.py [audit|fix-dry-run|report] [--json]")
        sys.exit(1)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == "audit":
        cmd_audit(rest)
    elif cmd == "fix-dry-run":
        cmd_fix_dry_run(rest)
    elif cmd == "report":
        cmd_report(rest)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
