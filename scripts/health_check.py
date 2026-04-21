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


HEALTH_CHECKABLE_STATUSES = {"live", "ready_for_payment"}

def check_product_health(product):
    """Check health of a single product"""
    name = product.get('name', product.get('n', 'Unknown'))
    slug = product.get('slug', product.get('s', 'unknown'))
    url = health_check_url(product)

    if not url:
        return {'name': name, 'slug': slug, 'status': 'no_url', 'code': None}

    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '10', url],
            capture_output=True, text=True, timeout=15
        )
        code = result.stdout.strip()

        if code == '200':
            return {'name': name, 'slug': slug, 'status': 'healthy', 'code': 200}
        elif code == '404':
            return {'name': name, 'slug': slug, 'status': 'not_found', 'code': 404}
        elif code == '401':
            return {'name': name, 'slug': slug, 'status': 'unauthorized', 'code': 401}
        elif code == '000':
            return {'name': name, 'slug': slug, 'status': 'timeout', 'code': 0}
        else:
            return {'name': name, 'slug': slug, 'status': f'error_{code}', 'code': code}
    except Exception as e:
        return {'name': name, 'slug': slug, 'status': 'error', 'code': str(e)}

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
    unhealthy = []
    no_url = []

    # Check products in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_product_health, p): p for p in live_products}

        for future in as_completed(futures):
            result = future.result()
            if result['status'] == 'healthy':
                healthy.append(result)
                print(f"✅ {result['name']}: HTTP {result['code']}")
            elif result['status'] == 'no_url':
                no_url.append(result)
                print(f"⚠️  {result['name']}: NO URL")
            else:
                unhealthy.append(result)
                print(f"❌ {result['name']}: {result['status'].upper()} (HTTP {result['code']})")

    print()
    print("=== SUMMARY ===")
    print(f"✅ Healthy: {len(healthy)}")
    print(f"❌ Unhealthy: {len(unhealthy)}")
    print(f"⚠️  No URL: {len(no_url)}")
    success_rate = (len(healthy) / len(live_products) * 100) if live_products else 0.0
    print(f"Success rate: {success_rate:.1f}%")

    # Update state with health status
    for result in healthy + unhealthy + no_url:
        for p in products:
            if p.get('slug') == result['slug'] or p.get('s') == result['slug']:
                if result['status'] == 'healthy':
                    p['health_status'] = 'healthy'
                    p['last_health_code'] = 200
                else:
                    p['health_status'] = result['status']
                    p['last_health_code'] = result['code'] if isinstance(result['code'], int) else 0

    # Save state
    state['healthy_count'] = len(healthy)
    state['unhealthy_count'] = len(unhealthy)
    state['deploy_missing_or_bad_url'] = len(unhealthy) + len(no_url)

    with open('STATE.json', 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print("STATE.json updated with health status")

    # Return summary for further processing
    return {
        'healthy': len(healthy),
        'unhealthy': len(unhealthy),
        'no_url': len(no_url),
        'total': len(live_products)
    }

if __name__ == '__main__':
    result = main()
    sys.exit(0 if result['unhealthy'] == 0 else 1)
