#!/usr/bin/env python3
"""
Health check script for all live products
"""

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.product_state_sync import (
    health_check_url,
    load_product_catalog,
    sync_state_products,
)
from scripts.product_state_sync import sync_state_snapshot
from scripts.update_summary import apply_summary_fields, build_summary, persist_summary


HEALTH_CHECKABLE_STATUSES = {"live", "ready_for_payment"}
SYNCED_HEALTH_STATUSES = {"healthy", "alternate_healthy"}
CANONICAL_REDIRECTED_PREVIEW_STATUS = "redirected_preview_alias"
HEALTH_AUDIT_BUCKETS = ("live", "ready_for_payment")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_http_code(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.isdigit():
            return int(text)
    return None


def _parse_probe_stdout(stdout):
    text = (stdout or "").strip()
    if not text:
        return None, None

    code_text, _, effective_text = text.partition(" ")
    code = _coerce_http_code(code_text)
    effective_url = _normalize_url(effective_text) if effective_text else None
    return code, effective_url


def _normalize_url(value):
    if value is None:
        return None
    text = str(value).strip().rstrip("/")
    return text or None


def _is_preview_alias_url(url, slug):
    normalized_url = _normalize_url(url)
    clean_slug = str(slug).strip() if slug is not None else ""
    if normalized_url is None or not clean_slug:
        return False
    canonical_url = f"https://{clean_slug}.vercel.app"
    return normalized_url.endswith(".vercel.app") and normalized_url != canonical_url


def _status_for_http_code(code):
    http_code = _coerce_http_code(code)
    if http_code == 200:
        return "healthy"
    if http_code == 401:
        return "unauthorized"
    if http_code == 402:
        return "deployment_disabled"
    if http_code == 403:
        return "forbidden"
    if http_code == 404:
        return "not_found"
    if http_code == 429:
        return "rate_limited"
    if http_code == 451:
        return "geo_blocked"
    if http_code == 500:
        return "server_error"
    if http_code == 0:
        return "timeout"
    if http_code is not None:
        return f"error_{http_code}"
    return f"error_{code}"


def _build_probe_result(name, slug, url, code, checked_at, effective_url=None):
    return {
        "name": name,
        "slug": slug,
        "url": url,
        "effective_url": effective_url or url,
        "status": _status_for_http_code(code),
        "code": _coerce_http_code(code) or 0,
        "checked_at": checked_at,
    }


def _preferred_public_url(result, slug):
    """Keep the probed fallback alias visible when alternate health exists."""
    probe_url = _normalize_url(result.get("url"))
    effective_url = _normalize_url(result.get("effective_url")) or probe_url

    if result.get("status") == "alternate_healthy":
        for candidate in (probe_url, effective_url):
            if candidate and _is_preview_alias_url(candidate, slug):
                return candidate

    return effective_url or probe_url


def is_synced_health_result(result):
    return result.get("status") in SYNCED_HEALTH_STATUSES


def _empty_health_bucket():
    return {
        "healthy": [],
        "fallback_healthy": [],
        "unhealthy": [],
        "no_url": [],
    }


def summarize_health_audit_results(results, status_by_slug):
    """Group audit results so live metrics stay separate from ready-for-payment issues."""
    buckets = {bucket: _empty_health_bucket() for bucket in HEALTH_AUDIT_BUCKETS}

    for result in results:
        bucket_name = status_by_slug.get(result.get("slug"), "live")
        if bucket_name not in buckets:
            bucket_name = "live"

        bucket = buckets[bucket_name]
        if is_synced_health_result(result):
            bucket["healthy"].append(result)
            if result.get("status") == "alternate_healthy":
                bucket["fallback_healthy"].append(result)
        elif result.get("status") == "no_url":
            bucket["no_url"].append(result)
        else:
            bucket["unhealthy"].append(result)

    return buckets


def apply_health_result(product, result):
    """Write a probe result back to a product record."""
    if not isinstance(result, dict):
        return
    checked_at = result.get("checked_at") or _utc_now_iso()
    slug = product.get("slug", product.get("s"))
    canonical_url = result.get("canonical_url")
    canonical_probe_url = _normalize_url(result.get("canonical_probe_url"))
    probe_url = result.get("url")
    effective_url = _normalize_url(result.get("effective_url")) or _normalize_url(
        probe_url
    )
    public_url = _preferred_public_url(result, slug)
    canonical_target = f"https://{slug}.vercel.app" if slug else canonical_url
    if canonical_url is None and slug:
        canonical_url = f"https://{slug}.vercel.app"

    if probe_url:
        product["health_probe_url"] = probe_url
    if effective_url:
        product["effective_health_url"] = effective_url
        product["last_health_url"] = effective_url

    if slug:
        product["ideal_vercel_url"] = canonical_url or f"https://{slug}.vercel.app"

    product["canonical_health_url"] = canonical_url
    product["canonical_probe_url"] = canonical_probe_url or canonical_url

    status = result.get("status", "unknown")
    product["canonical_health_status"] = result.get("canonical_status") or (
        status if status != "alternate_healthy" else None
    )
    product["canonical_health_code"] = _coerce_http_code(
        result.get("canonical_code")
        if result.get("canonical_code") is not None
        else (result.get("code") if status != "alternate_healthy" else None)
    )
    product["canonical_health_checked_at"] = checked_at

    if status in SYNCED_HEALTH_STATUSES and public_url:
        product["deployment_url"] = public_url
        product["vercel_url"] = public_url
        product["v"] = public_url

    product["health_status"] = status
    product["last_health_code"] = _coerce_http_code(result.get("code")) or 0
    product["last_health_check"] = checked_at
    product["health_checked_at"] = checked_at

    if status == "healthy" and _is_preview_alias_url(effective_url or probe_url, slug):
        product["health_status"] = "alternate_healthy"
        product["ideal_vercel_url"] = canonical_target
        product["canonical_health_url"] = canonical_target
        product["canonical_probe_url"] = canonical_target
        product["canonical_health_status"] = "pending"
        product["canonical_health_code"] = None


def check_product_health(product):
    """Check health of a single product"""
    name = product.get("name", product.get("n", "Unknown"))
    slug = product.get("slug", product.get("s", "unknown"))
    checked_at = _utc_now_iso()
    candidates = []
    primary_url = _normalize_url(health_check_url(product))
    if primary_url:
        candidates.append(primary_url)
    for key in (
        "effective_health_url",
        "last_health_url",
        "health_probe_url",
        "deployment_url",
        "vercel_url",
        "v",
    ):
        candidate = _normalize_url(product.get(key))
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    if not candidates:
        return {
            "name": name,
            "slug": slug,
            "status": "no_url",
            "code": None,
            "checked_at": checked_at,
        }

    canonical_failure = None
    try:
        for idx, url in enumerate(candidates):
            result = subprocess.run(
                [
                    "curl",
                    "-4",
                    "-L",
                    "-sS",
                    "-o",
                    "/dev/null",
                    "-w",
                    "%{http_code} %{url_effective}",
                    "--max-time",
                    "10",
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            code, effective_url = _parse_probe_stdout(result.stdout)
            http_code = _coerce_http_code(code)

            if http_code == 200:
                if idx == 0 and _is_preview_alias_url(url, slug):
                    canonical_url = f"https://{slug}.vercel.app"
                    return {
                        "name": name,
                        "slug": slug,
                        "status": "alternate_healthy",
                        "code": 200,
                        "url": url,
                        # The probed public URL is the fallback alias itself.
                        # Keep it visible even if curl reports a redirected
                        # canonical effective URL; otherwise the state sync
                        # layer can accidentally "heal" the alias away.
                        "effective_url": url,
                        "canonical_url": canonical_url,
                        "canonical_probe_url": canonical_url,
                        "canonical_status": "pending",
                        "canonical_code": None,
                        "checked_at": checked_at,
                    }
                visible_effective_url = effective_url or url
                if (
                    _is_preview_alias_url(url, slug)
                    and effective_url is not None
                    and effective_url != url
                ):
                    # Later preview-alias candidates can also redirect to the
                    # canonical slug. Keep the alias itself visible so the
                    # fallback URL does not get "healed" away just because the
                    # redirect target happened to answer 200.
                    visible_effective_url = url
                redirected_preview_alias = (
                    idx == 0
                    and effective_url is not None
                    and effective_url != url
                    and slug
                    and effective_url.endswith(".vercel.app")
                    and effective_url != f"https://{slug}.vercel.app"
                )
                if redirected_preview_alias:
                    return {
                        "name": name,
                        "slug": slug,
                        "status": "alternate_healthy",
                        "code": 200,
                        "url": url,
                        "effective_url": effective_url,
                        "canonical_url": url,
                        "canonical_probe_url": candidates[0],
                        "canonical_status": CANONICAL_REDIRECTED_PREVIEW_STATUS,
                        "canonical_code": 200,
                        "checked_at": checked_at,
                    }
                if idx == 0:
                    return {
                        "name": name,
                        "slug": slug,
                        "status": "healthy",
                        "code": 200,
                        "url": url,
                        "effective_url": effective_url or url,
                        # For a direct success, the final effective URL is the
                        # truthful canonical record. This avoids freezing a
                        # redirected preview alias into canonical metadata.
                        "canonical_url": effective_url or url,
                        "canonical_probe_url": candidates[0],
                        "canonical_status": "healthy",
                        "canonical_code": 200,
                        "checked_at": checked_at,
                    }

                canonical_probe = canonical_failure or _build_probe_result(
                    name,
                    slug,
                    candidates[0],
                    code,
                    checked_at,
                )
                return {
                    "name": name,
                    "slug": slug,
                    "status": "alternate_healthy",
                    "code": 200,
                    "url": url,
                    "effective_url": visible_effective_url,
                    "canonical_url": candidates[0],
                    "canonical_probe_url": candidates[0],
                    "canonical_status": canonical_probe["status"],
                    "canonical_code": canonical_probe["code"],
                    "checked_at": checked_at,
                }

            failure = _build_probe_result(
                name, slug, url, code, checked_at, effective_url=effective_url
            )
            if idx == 0:
                canonical_failure = failure

        if canonical_failure is None:
            canonical_failure = _build_probe_result(
                name, slug, candidates[0], "unknown", checked_at
            )
        final_failure = canonical_failure
        final_failure["canonical_probe_url"] = candidates[0]
        return final_failure
    except Exception as e:
        return {
            "name": name,
            "slug": slug,
            "status": "error",
            "code": str(e),
            "url": candidates[0] if candidates else None,
            "effective_url": candidates[0] if candidates else None,
            "canonical_probe_url": candidates[0] if candidates else None,
            "checked_at": checked_at,
        }


def main():
    # Load state
    with open("STATE.json", encoding="utf-8") as f:
        raw_state = json.load(f)

    # Keep the file-backed snapshot pristine; the working copy is what we mutate
    # while health results are applied. Otherwise the "raw" state fed into
    # summary/readiness checks gets polluted by sync side effects.
    state = deepcopy(raw_state)
    products = state.get("products", {}).get("active", [])
    synced_products = sync_state_products(products, load_product_catalog())
    synced_by_slug = {
        (item.get("slug") or item.get("s")): item
        for item in synced_products
        if (item.get("slug") or item.get("s"))
    }

    for product in products:
        slug = product.get("slug") or product.get("s")
        synced = synced_by_slug.get(slug)
        if not synced:
            continue
        product.update(synced)

    checkable_products = [
        p for p in synced_products if p.get("status") in HEALTH_CHECKABLE_STATUSES
    ]
    live_products = [p for p in checkable_products if p.get("status") == "live"]
    ready_for_payment_products = [
        p for p in checkable_products if p.get("status") == "ready_for_payment"
    ]
    status_by_slug = {
        (item.get("slug") or item.get("s")): item.get("status")
        for item in checkable_products
        if (item.get("slug") or item.get("s"))
    }

    print(f"=== HEALTH CHECK ===")
    print(f"Total products: {len(products)}")
    print(f"Live products to check: {len(live_products)}")
    if ready_for_payment_products:
        print(f"Ready-for-payment products to check: {len(ready_for_payment_products)}")
    print()

    all_results = []

    # Check products in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_product_health, p): p for p in checkable_products}

        for future in as_completed(futures):
            result = future.result()
            all_results.append(result)

            bucket_name = status_by_slug.get(result.get("slug"), "live")
            if bucket_name not in HEALTH_AUDIT_BUCKETS:
                bucket_name = "live"
            bucket_label = "Live" if bucket_name == "live" else "Ready-for-payment"

            if is_synced_health_result(result):
                if result["status"] == "alternate_healthy":
                    print(
                        f"⚠️  [{bucket_label}] {result['name']}: ALTERNATE HEALTHY (HTTP {result['code']})"
                    )
                else:
                    print(f"✅ [{bucket_label}] {result['name']}: HTTP {result['code']}")
            elif result["status"] == "no_url":
                print(f"⚠️  [{bucket_label}] {result['name']}: NO URL")
            else:
                icon = "⚠️" if result["status"] == "alternate_healthy" else "❌"
                print(
                    f"{icon} [{bucket_label}] {result['name']}: {result['status'].upper()} (HTTP {result['code']})"
                )

    print()
    print("=== SUMMARY ===")
    audit_buckets = summarize_health_audit_results(all_results, status_by_slug)
    live_bucket = audit_buckets["live"]
    ready_bucket = audit_buckets["ready_for_payment"]

    print(f"✅ Live healthy: {len(live_bucket['healthy'])}")
    print(f"❌ Live unhealthy: {len(live_bucket['unhealthy'])}")
    print(f"⚠️  Live no URL: {len(live_bucket['no_url'])}")
    if live_bucket["fallback_healthy"]:
        print(
            f"⚠️  Live canonical drift but healthy via fallback: {len(live_bucket['fallback_healthy'])}"
        )
    success_rate = (
        (len(live_bucket["healthy"]) / len(live_products) * 100)
        if live_products
        else 0.0
    )
    print(f"Live success rate: {success_rate:.1f}%")

    if ready_for_payment_products:
        print()
        print("=== READY FOR PAYMENT ===")
        print(f"✅ Ready-for-payment healthy: {len(ready_bucket['healthy'])}")
        print(f"❌ Ready-for-payment issues: {len(ready_bucket['unhealthy'])}")
        print(f"⚠️  Ready-for-payment no URL: {len(ready_bucket['no_url'])}")
        if ready_bucket["fallback_healthy"]:
            print(
                "⚠️  Ready-for-payment canonical drift but healthy via fallback: "
                f"{len(ready_bucket['fallback_healthy'])}"
            )

    # Update state with health status
    for result in all_results:
        for p in products:
            if p.get("slug") == result["slug"] or p.get("s") == result["slug"]:
                apply_health_result(p, result)

    product_catalog = load_product_catalog()
    state = sync_state_snapshot(state, product_catalog=product_catalog)
    summary = build_summary(state, product_catalog=product_catalog, raw_state=raw_state)

    # Save state
    state = apply_summary_fields(state, summary)

    with open("STATE.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    persist_summary(summary)

    print(
        "STATE.json updated with health status "
        f"(healthy={summary['healthy_count']} live={summary['live_count']} "
        f"canonical_drift={summary['canonical_url_drift']})"
    )

    # Return summary for further processing
    return {
        "healthy": len(live_bucket["healthy"]),
        "unhealthy": len(live_bucket["unhealthy"]),
        "no_url": len(live_bucket["no_url"]),
        "fallback_healthy": len(live_bucket["fallback_healthy"]),
        "total": len(live_products),
        "ready_for_payment_healthy": len(ready_bucket["healthy"]),
        "ready_for_payment_unhealthy": len(ready_bucket["unhealthy"]),
        "ready_for_payment_no_url": len(ready_bucket["no_url"]),
        "ready_for_payment_fallback_healthy": len(ready_bucket["fallback_healthy"]),
        "ready_for_payment_total": len(ready_for_payment_products),
    }


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result["unhealthy"] == 0 else 1)
