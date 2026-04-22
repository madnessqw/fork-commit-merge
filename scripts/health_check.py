#!/usr/bin/env python3
"""
Health check script for all live products
"""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_metadata import get_checkout_url
from scripts.product_state_sync import health_check_url, load_product_catalog, sync_state_products
from scripts.update_summary import build_summary, persist_summary


HEALTH_CHECKABLE_STATUSES = {"live", "ready_for_payment"}
SYNCED_HEALTH_STATUSES = {"healthy", "alternate_healthy"}


def _normalize_url(value):
    if value is None:
        return None
    text = str(value).strip().rstrip("/")
    return text or None


def is_synced_health_result(result):
    return result.get("status") in SYNCED_HEALTH_STATUSES


def apply_health_result(product, result):
    """Write a probe result back to a product record."""
    if result.get("url"):
        product["last_health_url"] = result["url"]

    slug = product.get("slug", product.get("s"))
    if slug:
        product["ideal_vercel_url"] = f"https://{slug}.vercel.app"

    if result["status"] in SYNCED_HEALTH_STATUSES and result.get("url"):
        product["vercel_url"] = result["url"]
        product["v"] = result["url"]

    product["health_status"] = result["status"]
    product["last_health_code"] = result["code"] if isinstance(result["code"], int) else 0


def check_product_health(product):
    """Check health of a single product"""
    name = product.get('name', product.get('n', 'Unknown'))
    slug = product.get('slug', product.get('s', 'unknown'))
    candidates = []
    primary_url = _normalize_url(health_check_url(product))
    if primary_url:
        candidates.append(primary_url)
    for key in ("deployment_url", "vercel_url", "v"):
        candidate = _normalize_url(product.get(key))
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    if not candidates:
        return {'name': name, 'slug': slug, 'status': 'no_url', 'code': None}

    first_failure = None
    try:
        for url in candidates:
            result = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '10', url],
                capture_output=True, text=True, timeout=15
            )
            code = result.stdout.strip()

            if code == '200':
                status = 'healthy' if url == candidates[0] else 'alternate_healthy'
                return {'name': name, 'slug': slug, 'status': status, 'code': 200, 'url': url}

            if first_failure is None:
                if code == '404':
                    first_failure = {'name': name, 'slug': slug, 'status': 'not_found', 'code': 404, 'url': url}
                elif code == '401':
                    first_failure = {'name': name, 'slug': slug, 'status': 'unauthorized', 'code': 401, 'url': url}
                elif code == '000':
                    first_failure = {'name': name, 'slug': slug, 'status': 'timeout', 'code': 0, 'url': url}
                else:
                    first_failure = {'name': name, 'slug': slug, 'status': f'error_{code}', 'code': code, 'url': url}

        return first_failure or {'name': name, 'slug': slug, 'status': 'error', 'code': 'unknown', 'url': candidates[0]}
    except Exception as e:
        return {'name': name, 'slug': slug, 'status': 'error', 'code': str(e), 'url': candidates[0] if candidates else None}

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
        product['status'] = synced.get('status')
        product['st'] = synced.get('status')
        product['vercel_url'] = synced.get('vercel_url')
        product['v'] = synced.get('vercel_url')
        if synced.get('deployment_url') is not None or 'deployment_url' in product:
            product['deployment_url'] = synced.get('deployment_url')
        checkout_url = get_checkout_url(synced)
        if checkout_url is not None or 'checkout_url' in product or 'c' in product:
            product['checkout_url'] = checkout_url
            product['c'] = checkout_url

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

    summary = build_summary(state, product_catalog=load_product_catalog())

    # Save state
    state['active_count'] = summary['active_count']
    state['live_count'] = summary['live_count']
    state['healthy_count'] = summary['healthy_count']
    state['unhealthy_count'] = summary['unhealthy_count']
    state['checkout_gap_count'] = summary['checkout_gap_count']
    state['missing_checkout'] = summary['checkout_gap_count']
    state['deploy_missing_or_bad_url'] = summary['deploy_missing_or_bad_url']
    state['canonical_url_drift'] = summary['canonical_url_drift']
    state['canonical_url_drift_products'] = summary['canonical_url_drift_products']
    state['spec_ready_count'] = summary['spec_ready_count']
    # `build_summary()` now treats canonical drift as part of live health, so the
    # fix count is the unhealthy live set. No double-counting the same drift twice.
    state['needs_fix_count'] = summary['unhealthy_count']
    state['last_updated'] = summary['last_updated']

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
