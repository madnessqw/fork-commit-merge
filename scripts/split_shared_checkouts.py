#!/usr/bin/env python3
"""
Split shared Polar checkout URLs for duplicate product pairs.

Problem: 4 product pairs share the SAME Polar checkout URL and polar_product_id.
When a customer clicks "Buy" on either product, they hit the same checkout.
Each pair also has a price inversion (Pro cheaper than Base).

Solution:
  1. Create a NEW Polar product for the -pro version with correct price
  2. Generate a NEW checkout link for that product
  3. Update product.json with new polar_product_id + checkout_url
  4. Keep base product checkout unchanged

Usage:
    python3 scripts/split_shared_checkouts.py --dry-run
    python3 scripts/split_shared_checkouts.py --execute

Author: UniverseCreator Cycle 1201
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

POLAR_API = "https://api.polar.sh/v1"


def get_token() -> str:
    token = os.environ.get("POLAR_OAT", "")
    if not token:
        token = json.load(open(ROOT / "config" / "polar.json")).get("polar_oat", "")
    if not token:
        raise RuntimeError("POLAR_OAT not set")
    return token


def polar_request(token: str, method: str, path: str, **kwargs) -> dict:
    url = f"{POLAR_API}{path}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    r = requests.request(method, url, headers=headers, timeout=60, **kwargs)
    if r.status_code >= 400:
        raise RuntimeError(f"Polar API error {r.status_code}: {r.text[:200]}")
    return r.json() if r.content else {}


def main():
    parser = argparse.ArgumentParser(description="Split shared Polar checkout URLs")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--execute", action="store_true", help="Actually make changes")
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        parser.print_help()
        return

    token = get_token()

    # 4 shared checkout pairs: (base_slug, pro_slug)
    PAIRS = [
        ("uuid-generator", "uuid-generator-pro"),
        ("timestamp-converter", "timestamp-converter-pro"),
        ("toml-parser", "toml-parser-pro"),
        ("markdown-previewer", "markdown-previewer-pro"),
    ]

    results = []

    for base_slug, pro_slug in PAIRS:
        print(f"\n{'='*60}")
        print(f"SPLITTING: {base_slug} + {pro_slug}")

        base_path = ROOT / "products" / base_slug / "product.json"
        pro_path = ROOT / "products" / pro_slug / "product.json"

        base_pj = json.load(open(base_path))
        pro_pj = json.load(open(pro_path))

        base_price = base_pj.get("price", "?")
        pro_price = pro_pj.get("price", "?")
        base_name = base_pj.get("name", pro_pj.get("name", "?"))
        pro_name = pro_pj.get("name", base_name)

        print(f"  BASE  {base_slug}: price={base_price}, name={base_name}")
        print(f"  PRO   {pro_slug}: price={pro_price}, name={pro_name}")

        # Check price inversion
        def parse_price(p: str) -> float:
            p = p.replace("$", "").strip()
            try:
                return float(p)
            except ValueError:
                return 0.0

        base_val = parse_price(base_price)
        pro_val = parse_price(pro_price)

        if pro_val < base_val:
            print(f"  ⚠️  PRICE INVERSION: Pro({pro_price}) < Base({base_price})")

        # Get existing polar_product_id for pro version
        pro_ppid = pro_pj.get("polar_product_id", "")
        base_ppid = base_pj.get("polar_product_id", "")

        print(f"  BASE polar_product_id: {base_ppid}")
        print(f"  PRO  polar_product_id: {pro_ppid}")
        print(f"  BASE checkout_url: {base_pj.get('checkout_url','')[:50]}...")
        print(f"  PRO  checkout_url:  {pro_pj.get('checkout_url','')[:50]}...")

        # If they share the same polar_product_id, we need to fix it
        if base_ppid == pro_ppid and base_ppid:
            print(f"  ❌ SHARED polar_product_id — need to create new product for PRO")

            if args.execute:
                # Create new Polar product for pro version with correct price
                price_cents = int(pro_val * 100)
                if price_cents < 50:
                    price_cents = 500  # minimum $5

                create_payload = {
                    "name": f"{pro_name} (Pro Version)",
                    "description": pro_pj.get("description", f"Professional version of {pro_name}"),
                    "visibility": "public",
                    "metadata": {
                        "source": "universecreator",
                        "local_slug": pro_slug,
                    },
                    "prices": [{
                        "amount_type": "fixed",
                        "price_amount": price_cents,
                        "price_currency": "usd",
                    }],
                }

                print(f"  → Creating new Polar product: {create_payload}")
                resp = polar_request(token, "POST", "/products", json=create_payload)
                new_ppid = resp.get("id", "")
                print(f"  → New polar_product_id: {new_ppid}")

                if new_ppid:
                    # Fetch the new product to get its price ID
                    prod_resp = polar_request(token, "GET", f"/products/{new_ppid}")
                    prices = prod_resp.get("prices", [])
                    active_price = next((p for p in prices if p.get("currency") == "usd" and p.get("active") and p.get("type") == "fixed"), None)
                    if not active_price:
                        active_price = prices[0] if prices else {}
                    price_id = active_price.get("id", "")
                    print(f"  → New product price_id: {price_id}")

                    # Create checkout link using price ID
                    cl_payload = {
                        "product_price_id": price_id,
                        "payment_processor": "stripe",
                        "label": f"universecreator:{pro_slug}",
                        "metadata": {"source": "universecreator", "local_slug": pro_slug},
                        "allow_discount_codes": True,
                    }
                    cl_resp = polar_request(token, "POST", "/checkout-links", json=cl_payload)
                    new_checkout_id = cl_resp.get("id", "")
                    new_checkout_url = cl_resp.get("url", "")
                    print(f"  → New checkout_url: {new_checkout_url}")

                    # Update pro product.json
                    pro_pj["polar_product_id"] = new_ppid
                    pro_pj["checkout_url"] = new_checkout_url
                    pro_pj["payment_provider"] = "polar"
                    pro_path.write_text(json.dumps(pro_pj, indent=2))
                    print(f"  → Updated {pro_slug}/product.json")

                    results.append({
                        "slug": pro_slug,
                        "old_ppid": pro_ppid,
                        "new_ppid": new_ppid,
                        "new_checkout_url": new_checkout_url,
                    })
                else:
                    print(f"  ✗ Failed to create new Polar product")
            else:
                print(f"  💡 Would: POST /products → new product → POST /checkout_links")
        else:
            print(f"  ✓ Different polar_product_ids — already split")

    print(f"\n{'='*60}")
    if args.dry_run:
        print("DRY RUN — no changes made")
    elif args.execute:
        print("EXECUTE COMPLETE")
        if results:
            print("\nUpdated products:")
            for r in results:
                print(f"  {r['slug']}: {r['old_ppid']} → {r['new_ppid']}")
                print(f"    checkout: {r['new_checkout_url']}")


if __name__ == "__main__":
    main()
