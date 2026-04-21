#!/usr/bin/env python3
"""
Vercel'den index.html dosyalarını senkronize eder.
SEO optimizasyonu için eksik kaynak dosyalarını geri getirir.
"""
import json
import subprocess
import os
import time
from pathlib import Path

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")

def sync_html_files(batch_size=10):
    """Vercel'de live olan ancak yerel index.html'i eksik olan ürünlerden çek."""
    with open("STATE.json") as f:
        state = json.load(f)

    products = state.get("products", {}).get("active", [])
    synced = 0
    failed = []

    # Live ancak yerel index.html eksik olan ürünleri bul
    missing_html = []
    for p in products:
        if not isinstance(p, dict):
            continue
        slug = p.get("slug", "")
        vercel_url = p.get("vercel_url", "")

        if vercel_url and not Path(f"products/{slug}/index.html").exists():
            missing_html.append((slug, vercel_url))

    print(f"📦 Senkronizasyon gereken: {len(missing_html)} ürün")
    print(f"🔄 Batch başlıyor: {min(batch_size, len(missing_html))} ürün")

    for i, (slug, url) in enumerate(missing_html[:batch_size], 1):
        try:
            dir_path = Path(f"products/{slug}")
            dir_path.mkdir(parents=True, exist_ok=True)

            # URL'yi normalize et
            clean_url = url.replace("https://", "")
            clean_url = clean_url.split("/")[0]  # domain only

            # index.html'i çek
            result = subprocess.run(
                ["curl", "-sf", "-o", str(dir_path / "index.html"),
                 f"https://{clean_url}/"],
                capture_output=True, text=True
            )

            if result.returncode == 0 and (dir_path / "index.html").stat().st_size > 1000:
                synced += 1
                print(f"  ✅ {i}. {slug}: OK ({(dir_path / 'index.html').stat().st_size} bytes)")
            else:
                failed.append(slug)
                print(f"  ❌ {i}. {slug}: FAILED (status={result.returncode})")

            time.sleep(0.3)  # Rate limit koruması

        except Exception as e:
            failed.append(slug)
            print(f"  ❌ {slug}: ERROR ({e})")

    print(f"\n✅ Senkronizasyon tamamlandı: {synced}/{batch_size}")
    print(f"❌ Hatalar: {len(failed)} ({failed[:5]}...)")

    return synced, failed

if __name__ == "__main__":
    import sys
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    sync_html_files(batch)
