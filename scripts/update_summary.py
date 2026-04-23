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
from scripts.deploy_readiness import collect_spec_ready_deploy_readiness
from scripts.product_state_sync import (
    canonical_target_vercel_url,
    display_vercel_url,
    load_product_catalog,
    merge_preferred_record,
    record_preference_key,
    sync_state_snapshot,
    sync_state_products,
    successful_health_url,
)


STATE_FILE = ROOT / "STATE.json"
SUMMARY_FILE = ROOT / "STATE_SUMMARY.json"


PRODUCT_IDENTITY_FIELDS = ("name", "slug", "status", "vercel_url", "checkout_url")
SUMMARY_STATE_FIELDS = (
    "active_count",
    "live_count",
    "healthy_count",
    "canonical_healthy_count",
    "fallback_healthy_count",
    "unhealthy_count",
    "pending_health_count",
    "checkout_gap_count",
    "missing_checkout",
    "deploy_missing_or_bad_url",
    "canonical_url_drift",
    "canonical_url_drift_products",
    "fallback_healthy_products",
    "spec_ready_count",
    "deploy_readiness_count",
    "deploy_readiness_manifest_gap_count",
    "deploy_readiness_url_gap_count",
    "deploy_readiness_state_gap_count",
    "needs_fix_count",
    "next_action",
    "last_updated",
)


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


def _normalize_url(value: Any) -> str | None:
    if not _has_value(value):
        return None
    return str(value).strip().rstrip("/")


def _looks_like_manual_dashboard_action(value: Any) -> bool:
    text = str(value or "").strip().lower()
    if not text:
        return False
    return "vercel dashboard" in text or "manuel" in text or "manual" in text


def _effective_next_action(state: dict[str, Any], unhealthy_live: list[dict[str, Any]], canonical_drift_live: list[dict[str, Any]]) -> str | None:
    raw = state.get("next_action")
    raw_text = str(raw).strip() if raw is not None else ""
    if raw_text and not _looks_like_manual_dashboard_action(raw_text):
        return raw_text

    if unhealthy_live:
        if canonical_drift_live:
            return f"{len(unhealthy_live)} canlı ürünü düzelt; {len(canonical_drift_live)} fallback alias'ı görünür tut"
        return f"{len(unhealthy_live)} canlı ürünü düzelt"

    if canonical_drift_live:
        return f"{len(canonical_drift_live)} canonical URL drift'ini düzelt; fallback alias'ı ezme"

    return raw_text or None


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
        if record_preference_key(product) > record_preference_key(deduped[key]):
            deduped[key] = merge_preferred_record(product, deduped[key])

    return [deduped[key] for key in order] + anonymous


def _as_list(
    value: Any,
    *,
    product_catalog: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    normalized_items = [normalize_product(item) for item in value if isinstance(item, dict)]
    meaningful_items = [item for item in normalized_items if not is_placeholder_product(item)]
    deduped = dedupe_products(meaningful_items)
    return sync_state_products(deduped, product_catalog or {})


def load_products(
    state: dict[str, Any],
    *,
    product_catalog: dict[str, dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    products = state.get("products", {})
    if isinstance(products, dict):
        active = _as_list(products.get("active"), product_catalog=product_catalog)
        spec_ready = _as_list(products.get("spec_ready"), product_catalog=product_catalog)
    elif isinstance(products, list):
        active = _as_list(products, product_catalog=product_catalog)
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


def public_health_url(product: dict[str, Any]) -> str | None:
    selected = successful_health_url(product)
    if selected is not None:
        return selected

    for key in (
        "effective_health_url",
        "last_health_url",
        "health_probe_url",
        "vercel_url",
        "v",
        "deployment_url",
    ):
        value = _normalize_url(_pick(product, key))
        if value is not None:
            return value
    return None


def canonical_health_code(product: dict[str, Any]) -> int | None:
    raw = product.get("canonical_health_code")
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def is_healthy(product: dict[str, Any]) -> bool:
    # Healthy means the last HTTP probe returned 200. Canonical drift is still tracked
    # separately so URL misalignment does not get smuggled into the outage count.
    status = _pick(product, "health_status")
    return health_code(product) == 200 and (
        status is None or status in {"healthy", "alternate_healthy"}
    )


def is_fallback_healthy(product: dict[str, Any]) -> bool:
    return fallback_public_health_url(product) is not None


def fallback_public_health_url(product: dict[str, Any]) -> str | None:
    if health_code(product) != 200:
        return None

    ideal_url = canonical_target_vercel_url(product)
    current_url = public_health_url(product)
    # Only count fallback health when the visible public URL is still the
    # alias; canonical drift is a separate signal and should stay visible.
    if ideal_url is None or current_url is None or current_url == ideal_url:
        return None

    return current_url


def is_pending_health(product: dict[str, Any]) -> bool:
    """Return True when a live record has no health snapshot yet."""
    if health_code(product) is not None:
        return False

    status = _pick(product, "health_status")
    if isinstance(status, str):
        status = status.strip() or None
    return status is None or status == "pending"


def canonical_url_drift_entry(product: dict[str, Any]) -> dict[str, Any] | None:
    ideal_url = canonical_target_vercel_url(product)
    current_url = public_health_url(product)
    if ideal_url is None or current_url is None or ideal_url == current_url:
        return None
    entry = {
        "slug": product.get("slug"),
        "url": current_url,
        "ideal_url": ideal_url,
    }

    health_code_value = health_code(product)
    if health_code_value is not None:
        entry["health_code"] = health_code_value

    health_status = _pick(product, "health_status")
    if health_code_value == 200 and current_url != ideal_url:
        entry["health_status"] = "alternate_healthy"
    elif health_status is not None:
        entry["health_status"] = health_status

    probe_url = _pick(product, "health_probe_url", "last_health_url")
    if probe_url is not None:
        entry["probe_url"] = probe_url

    effective_url = _pick(product, "effective_health_url", "last_health_url")
    if effective_url is not None and effective_url != probe_url:
        entry["effective_url"] = effective_url

    canonical_url = _pick(product, "canonical_health_url") or ideal_url
    if canonical_url is not None:
        entry["canonical_url"] = canonical_url

    canonical_code = canonical_health_code(product)
    if canonical_code is not None:
        entry["canonical_code"] = canonical_code

    canonical_status = _pick(product, "canonical_health_status")
    if canonical_status is not None:
        entry["canonical_status"] = canonical_status

    return entry


def fallback_healthy_entry(product: dict[str, Any]) -> dict[str, Any] | None:
    if not is_fallback_healthy(product):
        return None
    return canonical_url_drift_entry(product)


def compact_product(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": product.get("name"),
        "s": product.get("slug"),
        "st": product.get("status"),
        "v": display_vercel_url(product),
        "c": get_checkout_url(product),
    }


def apply_summary_fields(state: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    for field in SUMMARY_STATE_FIELDS:
        if field == "missing_checkout":
            state[field] = summary["checkout_gap_count"]
        elif field == "needs_fix_count":
            state[field] = summary["needs_fix_count"]
        else:
            state[field] = summary[field]
    return state


def build_summary(
    state: dict[str, Any],
    *,
    product_catalog: dict[str, dict[str, Any]] | None = None,
    raw_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active, external_spec_ready = load_products(state, product_catalog=product_catalog)
    live = [p for p in active if p.get("status") == "live"]
    spec_ready_inside_active = [p for p in active if p.get("status") == "spec_ready"]
    ready_for_payment = [p for p in active if p.get("status") == "ready_for_payment"]
    canonical_drift_live = [
        drift
        for p in live
        if (drift := canonical_url_drift_entry(p)) is not None
    ]
    canonical_healthy_live = [p for p in live if is_healthy(p) and canonical_url_drift_entry(p) is None]
    fallback_healthy_live = [p for p in live if is_fallback_healthy(p)]
    fallback_healthy_detail = [
        detail
        for p in fallback_healthy_live
        if (detail := fallback_healthy_entry(p)) is not None
    ]
    pending_health_live = [p for p in live if is_pending_health(p)]
    readiness_source = raw_state or state
    readiness = collect_spec_ready_deploy_readiness(readiness_source)

    products_without_url = [
        p
        for p in active
        if p.get("status") in {"live", "ready_for_payment", "spec_ready"}
        and not display_vercel_url(p)
    ]
    unhealthy_live = [p for p in live if not is_healthy(p) and not is_pending_health(p)]
    checkout_gap_live = [p for p in live + ready_for_payment if not has_checkout(p)]
    spec_ready_total = len({p.get("slug") for p in [*external_spec_ready, *spec_ready_inside_active] if p.get("slug")})

    def build_unhealthy_entry(product: dict[str, Any]) -> dict[str, Any]:
        entry = {
            "slug": product.get("slug"),
            "url": display_vercel_url(product),
            "code": health_code(product),
            "health_status": product.get("health_status"),
        }

        canonical_url = _pick(product, "canonical_health_url") or canonical_target_vercel_url(product)
        if canonical_url is not None:
            entry["canonical_url"] = canonical_url

        canonical_code = canonical_health_code(product)
        if canonical_code is None:
            canonical_code = health_code(product)
        if canonical_code is not None:
            entry["canonical_code"] = canonical_code

        canonical_status = _pick(product, "canonical_health_status") or product.get("health_status")
        if canonical_status is not None:
            entry["canonical_status"] = canonical_status

        if (
            probe_url := _pick(product, "health_probe_url", "last_health_url", "effective_health_url")
        ) is not None:
            entry["probe_url"] = probe_url

        if (
            effective_url := _pick(product, "effective_health_url", "last_health_url")
        ) is not None and effective_url != _pick(product, "health_probe_url", "last_health_url"):
            entry["effective_url"] = effective_url

        return entry

    return {
        "cycle": state.get("cycle"),
        "mode": state.get("mode"),
        "balance": state.get("balance"),
        "active_count": len(active),
        "live_count": len(live),
        "healthy_count": sum(1 for p in live if is_healthy(p)),
        "canonical_healthy_count": len(canonical_healthy_live),
        # Fallback health only counts records that still have a concrete drift
        # snapshot. A stale alternate_healthy label on its own is not proof that
        # the fallback alias is actually the live truth.
        "fallback_healthy_count": len(fallback_healthy_detail),
        "unhealthy_count": len(unhealthy_live),
        "pending_health_count": len(pending_health_live),
        "checkout_gap_count": len(checkout_gap_live),
        # Deploy/URL gaps cover missing URLs plus broken live records. Canonical
        # drift stays separate so alias-only products do not inflate the deploy
        # backlog. Pending health snapshots are also counted here so stale live
        # records do not disappear from the operational attention score.
        "deploy_missing_or_bad_url": len(products_without_url) + len(unhealthy_live) + len(pending_health_live),
        "canonical_url_drift": len(canonical_drift_live),
        "spec_ready_count": spec_ready_total,
        "deploy_readiness_count": readiness["count"],
        "deploy_readiness_manifest_gap_count": readiness["manifest_gap_count"],
        "deploy_readiness_url_gap_count": readiness["url_gap_count"],
        "deploy_readiness_state_gap_count": readiness["state_gap_count"],
        # Canonical drift is not an outage, but it is still unresolved work:
        # fallback aliases should stay visible until the canonical URL itself
        # probes cleanly.
        "needs_fix_count": len(unhealthy_live) + len(pending_health_live) + len(canonical_drift_live),
        "next_action": _effective_next_action(state, unhealthy_live, canonical_drift_live),
        "vercel_auth_issue": state.get("vercel_auth_issue"),
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "products": [compact_product(p) for p in active],
        "gaps": {
            "missing_url": [p.get("slug") for p in products_without_url],
            "unhealthy_live": [
                build_unhealthy_entry(p)
                for p in unhealthy_live
            ],
            "pending_health": [
                {
                    "slug": p.get("slug"),
                    "url": display_vercel_url(p),
                    "code": health_code(p),
                    "health_status": "pending",
                }
                for p in pending_health_live
            ],
            "missing_checkout": [p.get("slug") for p in checkout_gap_live],
            "canonical_url_drift": canonical_drift_live,
            "fallback_healthy": fallback_healthy_detail,
            "deploy_readiness": readiness["issues"],
        },
        "canonical_url_drift_products": [item.get("slug") for item in canonical_drift_live if item.get("slug")],
        "fallback_healthy_products": [item.get("slug") for item in fallback_healthy_detail if item.get("slug")],
    }


def persist_summary(summary: dict[str, Any], *, summary_file: Path | None = None) -> None:
    if summary_file is None:
        summary_file = SUMMARY_FILE
    summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    product_catalog = load_product_catalog()
    raw_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    state = sync_state_snapshot(raw_state, product_catalog=product_catalog)
    summary = build_summary(state, product_catalog=product_catalog, raw_state=raw_state)
    state = apply_summary_fields(state, summary)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    persist_summary(summary)
    print(
        "STATE_SUMMARY.json updated: "
        f"active={summary['active_count']} live={summary['live_count']} "
        f"healthy={summary['healthy_count']} checkout_gaps={summary['checkout_gap_count']} "
        f"deploy_gaps={summary['deploy_missing_or_bad_url']} canonical_drift={summary['canonical_url_drift']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
