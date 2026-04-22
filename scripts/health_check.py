#!/usr/bin/env python3
"""
Health check script for all live products
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.product_state_sync import health_check_url, load_product_catalog, sync_state_products
from scripts.product_state_sync import sync_state_snapshot
from scripts.update_summary import apply_summary_fields, build_summary, persist_summary


HEALTH_CHECKABLE_STATUSES = {"live", "ready_for_payment"}
SYNCED_HEALTH_STATUSES = {"healthy", "alternate_healthy"}


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


def _normalize_url(value):
    if value is None:
        return None
    text = str(value).strip().rstrip("/")
    return text or None


def _status_for_http_code(code):
    http_code = _coerce_http_code(code)
    if http_code == 200:
        return "healthy"
    if http_code == 401:
        return "unauthorized"
    if http_code == 404:
        return "not_found"
    if http_code == 0:
        return "timeout"
    if http_code is not None:
        return f"error_{http_code}"
    return f"error_{code}"


def _build_probe_result(name, slug, url, code, checked_at):
    return {
        "name": name,
        "slug": slug,
        "url": url,
        "status": _status_for_http_code(code),
        "code": _coerce_http_code(code) or 0,
        "checked_at": checked_at,
    }


def is_synced_health_result(result):
    return result.get("status") in SYNCED_HEALTH_STATUSES


def apply_health_result(product, result):
    """Write a probe result back to a product record."""
    checked_at = result.get("checked_at") or _utc_now_iso()
    slug = product.get("slug", product.get("s"))
    canonical_url = result.get("canonical_url")
    if canonical_url is None and slug:
        canonical_url = f"https://{slug}.vercel.app"

    if result.get("url"):
        product["last_health_url"] = result["url"]

    if slug:
        product["ideal_vercel_url"] = canonical_url or f"https://{slug}.vercel.app"

    product["canonical_health_url"] = canonical_url

    product["canonical_health_status"] = result.get("canonical_status") or (
        result["status"] if result["status"] != "alternate_healthy" else None
    )
    product["canonical_health_code"] = _coerce_http_code(
        result.get("canonical_code") if result.get("canonical_code") is not None else (
            result.get("code") if result["status"] != "alternate_healthy" else None
        )
    )
    product["canonical_health_checked_at"] = checked_at

    if result["status"] in SYNCED_HEALTH_STATUSES and result.get("url"):
        product["vercel_url"] = result["url"]
        product["v"] = result["url"]

    product["health_status"] = result["status"]
    product["last_health_code"] = _coerce_http_code(result.get("code")) or 0
    product["last_health_check"] = checked_at
    product["health_checked_at"] = checked_at


def check_product_health(product):
    """Check health of a single product"""
    name = product.get('name', product.get('n', 'Unknown'))
    slug = product.get('slug', product.get('s', 'unknown'))
    checked_at = _utc_now_iso()
    candidates = []
    primary_url = _normalize_url(health_check_url(product))
    if primary_url:
        candidates.append(primary_url)
    for key in ("deployment_url", "vercel_url", "v"):
        candidate = _normalize_url(product.get(key))
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    if not candidates:
        return {'name': name, 'slug': slug, 'status': 'no_url', 'code': None, 'checked_at': checked_at}

    canonical_failure = None
    try:
        for idx, url in enumerate(candidates):
            result = subprocess.run(
                ['curl', '-4', '-L', '-sS', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '10', url],
                capture_output=True, text=True, timeout=15
            )
            code = result.stdout.strip()
            http_code = _coerce_http_code(code)

            if http_code == 200:
                if idx == 0:
                    return {
                        'name': name,
                        'slug': slug,
                        'status': 'healthy',
                        'code': 200,
                        'url': url,
                        'canonical_url': url,
                        'canonical_status': 'healthy',
                        'canonical_code': 200,
                        'checked_at': checked_at,
                    }

                canonical_probe = canonical_failure or _build_probe_result(
                    name,
                    slug,
                    candidates[0],
                    code,
                    checked_at,
                )
                return {
                    'name': name,
                    'slug': slug,
                    'status': 'alternate_healthy',
                    'code': 200,
                    'url': url,
                    'canonical_url': candidates[0],
                    'canonical_status': canonical_probe['status'],
                    'canonical_code': canonical_probe['code'],
                    'checked_at': checked_at,
                }

            failure = _build_probe_result(name, slug, url, code, checked_at)
            if idx == 0:
                canonical_failure = failure

        return canonical_failure or _build_probe_result(name, slug, candidates[0], 'unknown', checked_at)
    except Exception as e:
        return {'name': name, 'slug': slug, 'status': 'error', 'code': str(e), 'url': candidates[0] if candidates else None, 'checked_at': checked_at}

def main():
    # Load state
    with open('STATE.json', encoding='utf-8') as f:
        state = json.load(f)

    products = state.get('products', {}).get('active', [])
    synced_products = sync_state_products(products, load_product_catalog())
    synced_by_slug = {
        (item.get('slug') or item.get('s')): item
        for item in synced_products
        if (item.get('slug') or item.get('s'))
    }

    for product in products:
        slug = product.get('slug') or product.get('s')
        synced = synced_by_slug.get(slug)
        if not synced:
            continue
        product.update(synced)

    live_products = [p for p in synced_products if p.get('status') in HEALTH_CHECKABLE_STATUSES]

    print(f"=== HEALTH CHECK ===")
    print(f"Total products: {len(products)}")
    print(f"Live products to check: {len(live_products)}")
    print()

    healthy = []
    fallback_healthy = []
    unhealthy = []
    no_url = []

    # Check products in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_product_health, p): p for p in live_products}

        for future in as_completed(futures):
            result = future.result()
            if is_synced_health_result(result):
                healthy.append(result)
                if result['status'] == 'alternate_healthy':
                    fallback_healthy.append(result)
                    print(f"⚠️  {result['name']}: ALTERNATE HEALTHY (HTTP {result['code']})")
                else:
                    print(f"✅ {result['name']}: HTTP {result['code']}")
            elif result['status'] == 'no_url':
                no_url.append(result)
                print(f"⚠️  {result['name']}: NO URL")
            else:
                unhealthy.append(result)
                icon = "⚠️" if result['status'] == 'alternate_healthy' else "❌"
                print(f"{icon} {result['name']}: {result['status'].upper()} (HTTP {result['code']})")

    print()
    print("=== SUMMARY ===")
    print(f"✅ Healthy: {len(healthy)}")
    print(f"❌ Unhealthy: {len(unhealthy)}")
    print(f"⚠️  No URL: {len(no_url)}")
    if fallback_healthy:
        print(f"⚠️  Canonical drift but healthy via fallback: {len(fallback_healthy)}")
    success_rate = (len(healthy) / len(live_products) * 100) if live_products else 0.0
    print(f"Success rate: {success_rate:.1f}%")

    # Update state with health status
    for result in healthy + unhealthy + no_url:
        for p in products:
            if p.get('slug') == result['slug'] or p.get('s') == result['slug']:
                apply_health_result(p, result)

    product_catalog = load_product_catalog()
    state = sync_state_snapshot(state, product_catalog=product_catalog)
    summary = build_summary(state, product_catalog=product_catalog)

    # Save state
    state = apply_summary_fields(state, summary)

    with open('STATE.json', 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    persist_summary(summary)

    print(
        "STATE.json updated with health status "
        f"(healthy={summary['healthy_count']} live={summary['live_count']} "
        f"canonical_drift={summary['canonical_url_drift']})"
    )

    # Return summary for further processing
    return {
        'healthy': summary['healthy_count'],
        'unhealthy': summary['unhealthy_count'],
        'no_url': len(no_url),
        'fallback_healthy': len(fallback_healthy),
        'total': summary['live_count']
    }

if __name__ == '__main__':
    result = main()
    sys.exit(0 if result['unhealthy'] == 0 else 1)
