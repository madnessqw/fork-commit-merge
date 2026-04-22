#!/usr/bin/env python3
"""Reconcile STATE active records with product.json manifests.

STATE.json is operational cache, not the durable source of truth. Product
manifests often carry the latest status while STATE keeps stale live URLs or
health data. These helpers merge both views without pretending manual deploy /
payment steps are already solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_metadata import get_checkout_url, has_value, normalize_checkout_metadata


PRODUCTS_DIR = ROOT / "products"

PRE_DEPLOY_STATUSES = {"building", "spec_ready", "ready_to_deploy"}
HEALTH_CHECKABLE_STATUSES = {"live", "ready_for_payment"}


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _pick(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if has_value(value):
            return value
    return None


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    normalized["name"] = _clean_text(_pick(record, "name", "n"))
    normalized["slug"] = _clean_text(_pick(record, "slug", "s"))
    normalized["status"] = _clean_text(_pick(record, "status", "st"))
    normalized["vercel_url"] = normalize_url(_pick(record, "vercel_url", "v"))
    normalized["deployment_url"] = normalize_url(_pick(record, "deployment_url"))
    normalized["checkout_url"] = get_checkout_url(record)
    return normalized


def normalize_url(value: Any) -> str | None:
    url = _clean_text(value)
    if url is None:
        return None
    return url.rstrip("/")


def canonical_vercel_url(slug: str | None) -> str | None:
    clean_slug = _clean_text(slug)
    if clean_slug is None:
        return None
    return f"https://{clean_slug}.vercel.app"


def load_product_catalog(products_dir: Path = PRODUCTS_DIR) -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}

    if not products_dir.exists():
        return catalog

    for path in sorted(products_dir.glob("*/product.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        slug = _clean_text(record.get("slug")) or path.parent.name
        catalog[slug] = record

    return catalog


def choose_public_vercel_url(
    *,
    slug: str | None,
    state_url: Any,
    manifest_url: Any,
    deployment_url: Any = None,
    status: str | None = None,
) -> str | None:
    normalized_state_url = normalize_url(state_url)
    normalized_manifest_url = normalize_url(manifest_url)
    normalized_deployment_url = normalize_url(deployment_url)
    normalized_status = _clean_text(status)

    if normalized_status in PRE_DEPLOY_STATUSES and normalized_manifest_url is None:
        return None

    if normalized_status in HEALTH_CHECKABLE_STATUSES:
        return normalized_state_url or normalized_deployment_url or normalized_manifest_url

    return normalized_state_url or normalized_deployment_url or normalized_manifest_url


def merge_product_record(
    state_record: dict[str, Any],
    manifest_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    merged = normalize_checkout_metadata(
        normalize_record(state_record),
        force_canonical_key=True,
        prune_legacy=True,
    )

    manifest = (
        normalize_checkout_metadata(
            normalize_record(manifest_record),
            force_canonical_key=True,
            prune_legacy=True,
        )
        if manifest_record is not None
        else None
    )

    if manifest is None:
        return merged

    for field in ("name", "slug", "status", "category", "price", "github_url"):
        manifest_value = manifest.get(field)
        if has_value(manifest_value):
            merged[field] = manifest_value

    effective_status = merged.get("status")
    merged["deployment_url"] = normalize_url(manifest.get("deployment_url")) or normalize_url(merged.get("deployment_url"))
    merged["vercel_url"] = choose_public_vercel_url(
        slug=merged.get("slug"),
        state_url=merged.get("vercel_url"),
        manifest_url=manifest.get("vercel_url"),
        deployment_url=merged.get("deployment_url"),
        status=effective_status,
    )

    manifest_checkout_url = get_checkout_url(manifest)
    if effective_status in PRE_DEPLOY_STATUSES and manifest_checkout_url is None:
        merged["checkout_url"] = None
        merged.pop("payment_provider", None)
    elif manifest_checkout_url is not None:
        merged["checkout_url"] = manifest_checkout_url
        payment_provider = manifest.get("payment_provider")
        if has_value(payment_provider):
            merged["payment_provider"] = payment_provider

    manifest_health_status = manifest.get("health_status")
    manifest_health_code = manifest.get("last_health_code")
    if merged.get("health_status") is None and has_value(manifest_health_status):
        merged["health_status"] = manifest_health_status
    if merged.get("last_health_code") is None and has_value(manifest_health_code):
        merged["last_health_code"] = manifest_health_code

    return normalize_checkout_metadata(
        merged,
        force_canonical_key=True,
        prune_legacy=True,
    )


def sync_state_products(
    products: list[dict[str, Any]],
    product_catalog: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    catalog = product_catalog or {}
    synced: list[dict[str, Any]] = []

    for product in products:
        normalized = normalize_record(product)
        slug = normalized.get("slug")
        manifest = catalog.get(slug) if slug else None
        synced.append(merge_product_record(product, manifest))

    return synced


def health_check_url(product: dict[str, Any]) -> str | None:
    return normalize_url(_pick(product, "vercel_url", "v", "deployment_url"))
