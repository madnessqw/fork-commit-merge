#!/usr/bin/env python3
"""
SEO optimizasyonu - OG meta tag'lerini ürünlere ekler.
Senkronize edilen yeni ürünler için OG tag'lerini düzenler.
"""
import json
import re
from pathlib import Path

def optimize_seo(batch_size=15):
    """index.html'i senkronize edilen ürünlere OG meta tag'lerini ekle."""
    with open("STATE.json") as f:
        state = json.load(f)

    products = state.get("products", {}).get("active", [])
    optimized = 0
    failed = []

    # Senkronize edilmiş ama OG tag'i olmayan ürünleri bul
    for p in products[:batch_size]:
        if not isinstance(p, dict):
            continue

        slug = p.get("slug", "")
        name = p.get("name", slug.replace("-", " ").title())
        desc = p.get("description", name)
        vercel_url = p.get("vercel_url", f"https://{slug}.vercel.app")

        html_path = Path(f"products/{slug}/index.html")
        if not html_path.exists():
            continue

        content = html_path.read_text(encoding="utf-8")

        # Zaten OG tag'i var mı?
        if '<meta property="og:title"' in content:
            continue

        # OG tag'leri oluştur
        og_title = name
        og_desc = desc if desc else f"{name} - Professional developer tool"
        og_image = f"{vercel_url}/og.png"  # Fallback

        # OG block oluştur
        og_block = f'''<meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{vercel_url}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:site_name" content="{og_title}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{og_title}">
    <meta name="twitter:description" content="{og_desc}">
    <meta name="twitter:image" content="{og_image}">'''

        # OG tag'lerini title'dan sonra ekle
        if "<title>" in content:
            content = re.sub(
                r"(</title>\s*)",
                r"\1\n    " + og_block.replace("\n", "\n    ") + "\n",
                content
            )

            html_path.write_text(content, encoding="utf-8")
            optimized += 1
            print(f"  ✅ {slug}: OG tags added")
        else:
            failed.append(slug)
            print(f"  ⚠️ {slug}: No title tag found")

    print(f"\n✅ OG optimizasyon tamamlandı: {optimized} ürün")
    if failed:
        print(f"⚠️ Atlandı: {len(failed)} ürün ({failed[:5]}...)")

    return optimized

if __name__ == "__main__":
    import sys
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    optimize_seo(batch)
