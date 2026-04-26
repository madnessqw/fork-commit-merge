#!/usr/bin/env python3
"""Score each product's sales readiness based on key conversion signals.

Evaluates products across 7 dimensions to produce a readiness score (0-100)
and identifies which products need attention before they can effectively sell.

Dimensions:
    1. Healthy (20 pts) — HTTP 200, health_status=healthy
    2. Canonical URL match (15 pts) — vercel_url matches ideal
    3. Valid price (15 pts) — numeric price > 0
    4. Valid checkout (15 pts) — Polar checkout URL present
    5. SEO optimized (10 pts) — seo_optimized=True
    6. OG optimized (10 pts) — og_optimized=True
    7. Schema markup (10 pts) — schema_optimized=True
    8. Checkout active (5 pts) — checkout_status=active

Usage:
    python3 scripts/product_readiness_scorer.py
    python3 scripts/product_readiness_scorer.py --json
    python3 scripts/product_readiness_scorer.py --threshold 80
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"


def _is_healthy(p: dict[str, Any]) -> bool:
    return (
        p.get("health_status") == "healthy"
        and p.get("last_health_code") == 200
    )


def _has_canonical_url(p: dict[str, Any]) -> bool:
    vercel = p.get("vercel_url") or p.get("v") or ""
    ideal = p.get("ideal_vercel_url") or ""
    return bool(vercel and ideal and vercel == ideal)


def _has_valid_price(p: dict[str, Any]) -> bool:
    raw = p.get("price")
    if raw is None:
        return False
    try:
        return float(str(raw).strip().lstrip("$")) > 0
    except (ValueError, TypeError):
        return False


def _has_valid_checkout(p: dict[str, Any]) -> bool:
    co = p.get("checkout_url") or p.get("c") or ""
    return co.startswith("https://buy.polar.sh/")


def _is_seo_optimized(p: dict[str, Any]) -> bool:
    return bool(p.get("seo_optimized"))


def _is_og_optimized(p: dict[str, Any]) -> bool:
    return bool(p.get("og_optimized"))


def _is_schema_optimized(p: dict[str, Any]) -> bool:
    return bool(p.get("schema_optimized"))


def _is_checkout_active(p: dict[str, Any]) -> bool:
    return p.get("checkout_status") == "active"


DIMENSIONS = (
    ("healthy", 20, _is_healthy),
    ("canonical_url", 15, _has_canonical_url),
    ("valid_price", 15, _has_valid_price),
    ("valid_checkout", 15, _has_valid_checkout),
    ("seo_optimized", 10, _is_seo_optimized),
    ("og_optimized", 10, _is_og_optimized),
    ("schema_optimized", 10, _is_schema_optimized),
    ("checkout_active", 5, _is_checkout_active),
)


def score_product(product: dict[str, Any]) -> dict[str, Any]:
    slug = product.get("slug") or product.get("s") or "unknown"
    name = product.get("name") or product.get("n") or slug
    points = 0
    max_points = 0
    passed: list[str] = []
    failed: list[str] = []

    for dim_name, weight, check_fn in DIMENSIONS:
        max_points += weight
        if check_fn(product):
            points += weight
            passed.append(dim_name)
        else:
            failed.append(dim_name)

    score_pct = round(points / max_points * 100, 1) if max_points > 0 else 0

    return {
        "slug": slug,
        "name": name,
        "score": score_pct,
        "points": points,
        "max_points": max_points,
        "passed": passed,
        "failed": failed,
        "status": product.get("status") or product.get("st") or "unknown",
    }


def load_products(state_path: Path = STATE_PATH) -> list[dict[str, Any]]:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data.get("products", {}).get("active", [])


def score_portfolio(
    state_path: Path = STATE_PATH,
) -> dict[str, Any]:
    products = load_products(state_path)
    scored = [score_product(p) for p in products]

    total = len(scored)
    if total == 0:
        return {
            "total": 0,
            "avg_score": 0,
            "ready_count": 0,
            "needs_attention": [],
            "scores": [],
        }

    avg_score = round(sum(s["score"] for s in scored) / total, 1)

    tier_counts = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}
    for s in scored:
        sc = s["score"]
        if sc >= 90:
            tier_counts["excellent"] += 1
        elif sc >= 75:
            tier_counts["good"] += 1
        elif sc >= 50:
            tier_counts["fair"] += 1
        else:
            tier_counts["poor"] += 1

    needs_attention = [s for s in scored if s["score"] < 100]
    needs_attention.sort(key=lambda s: s["score"])

    failing_dims: dict[str, int] = {}
    for s in scored:
        for f in s["failed"]:
            failing_dims[f] = failing_dims.get(f, 0) + 1

    return {
        "total": total,
        "avg_score": avg_score,
        "median_score": sorted(s["score"] for s in scored)[total // 2],
        "tier_counts": tier_counts,
        "ready_count": sum(1 for s in scored if s["score"] >= 90),
        "needs_attention_count": len(needs_attention),
        "failing_dimensions": dict(
            sorted(failing_dims.items(), key=lambda x: -x[1])
        ),
        "bottom_5": [s["slug"] for s in needs_attention[:5]],
        "scores": scored,
    }


def format_report(result: dict[str, Any]) -> str:
    lines = [
        "# Product Readiness Report",
        f"**Total:** {result['total']} | **Avg Score:** {result['avg_score']}% | **Ready (90%+):** {result['ready_count']}",
        "",
        "## Score Distribution",
        f"| Tier | Count |",
        f"|------|-------|",
    ]
    for tier in ("excellent", "good", "fair", "poor"):
        lines.append(f"| {tier.capitalize()} | {result['tier_counts'][tier]} |")

    if result.get("failing_dimensions"):
        lines.extend(["", "## Failing Dimensions"])
        for dim, count in result["failing_dimensions"].items():
            lines.append(f"- **{dim}**: {count} products")

    if result.get("bottom_5"):
        lines.extend(["", f"## Bottom 5 ({', '.join(result['bottom_5'])})"])

    return "\n".join(lines)


def main() -> int:
    threshold = 0
    as_json = "--json" in sys.argv
    for i, arg in enumerate(sys.argv):
        if arg == "--threshold" and i + 1 < len(sys.argv):
            try:
                threshold = int(sys.argv[i + 1])
            except ValueError:
                pass

    result = score_portfolio()

    if threshold > 0:
        below = [s for s in result["scores"] if s["score"] < threshold]
        result["below_threshold"] = below
        result["threshold"] = threshold

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_report(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
