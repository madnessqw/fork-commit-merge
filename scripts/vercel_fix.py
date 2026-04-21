#!/usr/bin/env python3
"""
Vercel Hash URL Fix Script
Hash içeren Vercel URL'lerini düzgün alias'lara çevirir
"""

import json
import re
import subprocess
import sys
import os

HASH_PAT = re.compile(r"-[a-z0-9]+-madnessqws-projects\.vercel\.app")

def fix_hash_urls():
    with open('STATE.json') as f:
        state = json.load(f)

    active = state.get("products", {}).get("active", [])
    fixed = []
    token = os.environ.get('VERCEL_TOKEN', '')

    for product in active:
        if not isinstance(product, dict):
            continue

        vercel_url = product.get("vercel_url") or ""
        slug = product.get("slug", "")

        # Hash URL mi kontrol et (None kontrolü)
        if vercel_url and HASH_PAT.search(vercel_url):
            print(f"Hash URL found: {slug} -> {vercel_url}")

            # Yeni alias URL oluştur
            new_alias = f"{slug}.vercel.app"

            # Vercel alias set komutu çalıştır
            try:
                if token:
                    cmd = ["vercel", "alias", "set", vercel_url, new_alias, "--token", token]
                else:
                    cmd = ["vercel", "alias", "set", vercel_url, new_alias]
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"  ✅ Alias set: {new_alias}")
                    product["vercel_url"] = f"https://{new_alias}"
                    product["note"] = "Alias fixed"
                    fixed.append(slug)
                else:
                    print(f"  ❌ Alias failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Error: {e}")

    if fixed:
        with open('STATE.json', 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"\nFixed {len(fixed)} products: {fixed}")
    else:
        print("\nNo hash URLs to fix")

if __name__ == "__main__":
    fix_hash_urls()
