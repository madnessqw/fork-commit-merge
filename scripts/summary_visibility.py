#!/usr/bin/env python3
"""Helpers for surfacing canonical drift and fallback alias truth.

Several summary/report consumers only see the compact STATE_SUMMARY snapshot.
These helpers reconstruct the visible alias truth from either the detailed
gap lists, the compact product list, or the top-level count fields so compact
snapshots do not hide fallback-healthy products.
"""

from __future__ import annotations

from typing import Any


def _has_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None


def _normalize_url(value: Any) -> str | None:
    if not _has_value(value):
        return None
    return str(value).strip().rstrip("/") or None


def _ideal_url(slug: str | None) -> str | None:
    clean_slug = str(slug or "").strip()
    if not clean_slug:
        return None
    return f"https://{clean_slug}.vercel.app"


def _summary_products_by_slug(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    products = summary.get("products", [])
    if not isinstance(products, list):
        return {}

    indexed: dict[str, dict[str, Any]] = {}
    for item in products:
        if not isinstance(item, dict):
            continue
        slug = str(item.get("s") or item.get("slug") or "").strip()
        if slug:
            indexed[slug] = item
    return indexed


def _visible_public_url(product: dict[str, Any] | None) -> str | None:
    if not isinstance(product, dict):
        return None

    for key in (
        "v",
        "vercel_url",
        "deployment_url",
        "effective_health_url",
        "last_health_url",
        "health_probe_url",
    ):
        value = _normalize_url(product.get(key))
        if value is not None:
            return value
    return None


def _entry_from_product(
    slug: str,
    product: dict[str, Any] | None,
    *,
    allow_equal_url: bool,
) -> dict[str, Any] | None:
    ideal_url = _ideal_url(slug)
    current_url = _visible_public_url(product)

    if current_url is None:
        return {"slug": slug, "ideal_url": ideal_url} if ideal_url is not None else {"slug": slug}

    if ideal_url is not None and current_url == ideal_url and not allow_equal_url:
        return None

    entry: dict[str, Any] = {"slug": slug, "url": current_url}
    if ideal_url is not None:
        entry["ideal_url"] = ideal_url
    return entry


def canonical_drift_entries(summary: dict[str, Any]) -> list[dict[str, Any]]:
    gaps = summary.get("gaps", {})
    if isinstance(gaps, dict):
        raw_entries = gaps.get("canonical_url_drift")
        if isinstance(raw_entries, list):
            entries = [item for item in raw_entries if isinstance(item, dict)]
            if entries:
                return entries

    product_map = _summary_products_by_slug(summary)
    raw_slugs = summary.get("canonical_url_drift_products")
    if isinstance(raw_slugs, list):
        entries: list[dict[str, Any]] = []
        for raw_slug in raw_slugs:
            slug = str(raw_slug).strip()
            if not slug:
                continue
            entry = _entry_from_product(
                slug,
                product_map.get(slug),
                allow_equal_url=True,
            )
            if entry is not None:
                entries.append(entry)
        if entries:
            return entries

    entries = []
    for slug, product in product_map.items():
        entry = _entry_from_product(slug, product, allow_equal_url=False)
        if entry is not None:
            entries.append(entry)
    return entries


def fallback_healthy_entries(summary: dict[str, Any]) -> list[dict[str, Any]]:
    gaps = summary.get("gaps", {})
    if isinstance(gaps, dict):
        raw_entries = gaps.get("fallback_healthy")
        if isinstance(raw_entries, list):
            entries = [item for item in raw_entries if isinstance(item, dict)]
            if entries:
                return entries

    canonical_drift = canonical_drift_entries(summary)
    if canonical_drift:
        return canonical_drift

    product_map = _summary_products_by_slug(summary)
    raw_slugs = summary.get("fallback_healthy_products")
    if isinstance(raw_slugs, list):
        entries: list[dict[str, Any]] = []
        for raw_slug in raw_slugs:
            slug = str(raw_slug).strip()
            if not slug:
                continue
            entry = _entry_from_product(
                slug,
                product_map.get(slug),
                allow_equal_url=True,
            )
            if entry is not None:
                entries.append(entry)
        if entries:
            return entries

    return []


def canonical_drift_count(summary: dict[str, Any]) -> int:
    raw = summary.get("canonical_url_drift")
    if raw is not None:
        if isinstance(raw, list):
            return len(raw)
        try:
            return int(raw)
        except (TypeError, ValueError):
            pass

    entries = canonical_drift_entries(summary)
    return len(entries)


def fallback_healthy_count(summary: dict[str, Any]) -> int:
    raw = summary.get("fallback_healthy_count")
    if raw is not None:
        if isinstance(raw, list):
            return len(raw)
        try:
            return int(raw)
        except (TypeError, ValueError):
            pass

    entries = fallback_healthy_entries(summary)
    return len(entries)
