#!/usr/bin/env python3
"""Build a compact, fresh STATE_SUMMARY.json from STATE.json.

The old version copied stale counter fields from STATE.json. That made the
summary lie whenever products were promoted or spec-ready items were mixed into
the active list. This script recomputes the operational counters from the
product records every time.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_metadata import get_checkout_url


STATE_FILE = ROOT / "STATE.json"
SUMMARY_FILE = ROOT / "STATE_SUMMARY.json"


PRODUCT_IDENTITY_FIELDS = ("name", "slug", "status", "vercel_url", "checkout_url")


def _has_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None


def _pick(product: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = product.get(key)
        if _has_value(value):
            return value
    return None


def normalize_product(product: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(product)
    normalized["name"] = _pick(product, "name", "n")
    normalized["slug"] = _pick(product, "slug", "s")
    normalized["status"] = _pick(product, "status", "st")
    normalized["vercel_url"] = _pick(product, "vercel_url", "v")
    normalized["checkout_url"] = get_checkout_url(product)
    return normalized


def is_placeholder_product(product: dict[str, Any]) -> bool:
    return not any(_has_value(product.get(field)) for field in PRODUCT_IDENTITY_FIELDS)


def product_key(product: dict[str, Any]) -> str | None:
    slug = product.get("slug")
    if _has_value(slug):
        return f"slug:{slug}"
    name = product.get("name")
    if _has_value(name):
        return f"name:{name}"
    return None


def product_quality_score(product: dict[str, Any]) -> int:
    return sum(1 for value in product.values() if _has_value(value))


def dedupe_products(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    anonymous: list[dict[str, Any]] = []

    for product in products:
        key = product_key(product)
        if key is None:
            anonymous.append(product)
            continue
        if key not in deduped:
            deduped[key] = product
            order.append(key)
            continue
        if product_quality_score(product) > product_quality_score(deduped[key]):
            deduped[key] = product

    return [deduped[key] for key in order] + anonymous


def _as_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    normalized_items = [normalize_product(item) for item in value if isinstance(item, dict)]
    meaningful_items = [item for item in normalized_items if not is_placeholder_product(item)]
    return dedupe_products(meaningful_items)


def load_products(state: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    products = state.get("products", {})
    if isinstance(products, dict):
        active = _as_list(products.get("active"))
        spec_ready = _as_list(products.get("spec_ready"))
    elif isinstance(products, list):
        active = _as_list(products)
        spec_ready = []
    else:
        active = []
        spec_ready = []
    return active, spec_ready


def has_checkout(product: dict[str, Any]) -> bool:
    return bool(get_checkout_url(product))


def health_code(product: dict[str, Any]) -> int | None:
    raw = product.get("last_health_code")
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def is_healthy(product: dict[str, Any]) -> bool:
    return product.get("health_status") == "healthy" or health_code(product) == 200


def compact_product(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": product.get("name"),
        "s": product.get("slug"),
        "st": product.get("status"),
        "v": product.get("vercel_url"),
        "c": get_checkout_url(product),
    }


def build_summary(state: dict[str, Any]) -> dict[str, Any]:
    active, external_spec_ready = load_products(state)
    live = [p for p in active if p.get("status") == "live"]
    spec_ready_inside_active = [p for p in active if p.get("status") == "spec_ready"]
    ready_for_payment = [p for p in active if p.get("status") == "ready_for_payment"]

    products_without_url = [p for p in active if p.get("status") in {"live", "ready_for_payment", "spec_ready"} and not p.get("vercel_url")]
    unhealthy_live = [p for p in live if not is_healthy(p)]
    checkout_gap_live = [p for p in live + ready_for_payment if not has_checkout(p)]
    spec_ready_total = len({p.get("slug") for p in [*external_spec_ready, *spec_ready_inside_active] if p.get("slug")})

    return {
        "cycle": state.get("cycle"),
        "mode": state.get("mode"),
        "balance": state.get("balance"),
        "active_count": len(active),
        "live_count": len(live),
        "healthy_count": sum(1 for p in live if is_healthy(p)),
        "unhealthy_count": len(unhealthy_live),
        "checkout_gap_count": len(checkout_gap_live),
        "deploy_missing_or_bad_url": len(products_without_url) + len(unhealthy_live),
        "spec_ready_count": spec_ready_total,
        "next_action": state.get("next_action"),
        "vercel_auth_issue": state.get("vercel_auth_issue"),
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "products": [compact_product(p) for p in active],
        "gaps": {
            "missing_url": [p.get("slug") for p in products_without_url],
            "unhealthy_live": [
                {
                    "slug": p.get("slug"),
                    "url": p.get("vercel_url"),
                    "code": health_code(p),
                    "health_status": p.get("health_status"),
                }
                for p in unhealthy_live
            ],
            "missing_checkout": [p.get("slug") for p in checkout_gap_live],
        },
    }


def main() -> int:
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    summary = build_summary(state)
    SUMMARY_FILE.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        "STATE_SUMMARY.json updated: "
        f"active={summary['active_count']} live={summary['live_count']} "
        f"healthy={summary['healthy_count']} checkout_gaps={summary['checkout_gap_count']} "
        f"deploy_gaps={summary['deploy_missing_or_bad_url']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
