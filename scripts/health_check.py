#!/usr/bin/env python3
"""
Health check script for all live products
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_product_health(product):
    """Check health of a single product"""
    name = product.get('name', product.get('n', 'Unknown'))
    slug = product.get('slug', product.get('s', 'unknown'))
    url = product.get('vercel_url', product.get('v', None))

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
    with open('STATE.json') as f:
        state = json.load(f)

    products = state.get('products', {}).get('active', [])
    live_products = [p for p in products if p.get('status', p.get('st', '')) in ('live', 'ready_for_payment')]

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
    print(f"Success rate: {len(healthy)/len(live_products)*100:.1f}%")

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

    with open('STATE.json', 'w') as f:
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
