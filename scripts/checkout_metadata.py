#!/usr/bin/env python3
"""Shared checkout metadata helpers.

Canonical contract:
- `checkout_url`
- `payment_provider`

Legacy keys are still supported on read so older records do not break.
"""

from __future__ import annotations

from typing import Any


CHECKOUT_URL_KEYS = ("checkout_url", "lemon_checkout_url", "lemonsqueezy_checkout_url", "c")
LEGACY_CHECKOUT_URL_KEYS = ("lemon_checkout_url", "lemonsqueezy_checkout_url")
PAYMENT_PROVIDER_KEY = "payment_provider"
LEMONSQUEEZY = "lemonsqueezy"


def has_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None


def pick_first(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if has_value(value):
            return value
    return None


def get_checkout_url(record: dict[str, Any]) -> str | None:
    value = pick_first(record, *CHECKOUT_URL_KEYS)
    if value is None:
        return None
    return str(value).strip()


def infer_payment_provider(record: dict[str, Any], checkout_url: str | None = None) -> str | None:
    provider = pick_first(record, PAYMENT_PROVIDER_KEY)
    if provider is not None:
        return str(provider).strip().lower()

    resolved_checkout_url = checkout_url if has_value(checkout_url) else get_checkout_url(record)
    if resolved_checkout_url is None:
        return None

    if "lemonsqueezy.com" in resolved_checkout_url.lower():
        return LEMONSQUEEZY

    return None


def normalize_checkout_metadata(
    record: dict[str, Any],
    *,
    sync_legacy: bool = True,
    force_canonical_key: bool = False,
    prune_legacy: bool = False,
) -> dict[str, Any]:
    normalized = dict(record)
    checkout_url = get_checkout_url(record)
    payment_provider = infer_payment_provider(record, checkout_url=checkout_url)

    if checkout_url is not None or force_canonical_key or "checkout_url" in normalized:
        normalized["checkout_url"] = checkout_url

    if payment_provider is not None or PAYMENT_PROVIDER_KEY in normalized:
        normalized[PAYMENT_PROVIDER_KEY] = payment_provider

    if prune_legacy:
        for key in LEGACY_CHECKOUT_URL_KEYS:
            normalized.pop(key, None)
    elif sync_legacy and payment_provider == LEMONSQUEEZY:
        for key in LEGACY_CHECKOUT_URL_KEYS:
            normalized[key] = checkout_url

    return normalized


def merge_checkout_metadata(
    record: dict[str, Any],
    fallback_record: dict[str, Any],
    *,
    sync_legacy: bool = True,
    force_canonical_key: bool = False,
    prune_legacy: bool = False,
) -> dict[str, Any]:
    normalized = normalize_checkout_metadata(
        record,
        sync_legacy=sync_legacy,
        force_canonical_key=force_canonical_key,
        prune_legacy=prune_legacy,
    )
    fallback = normalize_checkout_metadata(
        fallback_record,
        sync_legacy=sync_legacy,
        force_canonical_key=force_canonical_key,
        prune_legacy=prune_legacy,
    )

    checkout_url = get_checkout_url(normalized)
    if checkout_url is None:
        fallback_checkout_url = get_checkout_url(fallback)
        if fallback_checkout_url is not None:
            normalized["checkout_url"] = fallback_checkout_url
            checkout_url = fallback_checkout_url

    payment_provider = infer_payment_provider(normalized, checkout_url=checkout_url)
    if payment_provider is None:
        payment_provider = infer_payment_provider(fallback, checkout_url=get_checkout_url(fallback))
        if payment_provider is not None:
            normalized[PAYMENT_PROVIDER_KEY] = payment_provider

    return normalize_checkout_metadata(
        normalized,
        sync_legacy=sync_legacy,
        force_canonical_key=force_canonical_key,
        prune_legacy=prune_legacy,
    )
