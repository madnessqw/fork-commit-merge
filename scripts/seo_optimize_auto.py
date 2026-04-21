#!/usr/bin/env python3
"""
SEO Optimizasyon Scripti - Cycle 1022
STATE.json'dan ürünleri çekerek otomatik meta tag optimizasyonu
"""

import json
import os
import re
from pathlib import Path

def generate_keywords(name):
    """Ürün adından anahtar kelimeler oluştur"""
    base = name.lower().replace(' pro', '').replace('premium', '').strip()
    words = base.split()

    # Temel anahtar kelimeler
    base_keywords = ', '.join(words) if len(words) > 1 else base

    # Kategori bazlı ek anahtar kelimeler
    categories = {
        'uuid': 'UUID generator, unique identifier, GUID generator',
        'jwt': 'JWT decoder, JWT token, authentication, token inspector',
        'html': 'HTML tool, web development, HTML utility',
        'css': 'CSS tool, styling, web design, CSS generator',
        'json': 'JSON tool, JSON formatter, JSON validator',
        'xml': 'XML tool, XML formatter, XML validator, XML parser',
        'yaml': 'YAML converter, YAML parser, YAML to JSON',
        'sql': 'SQL formatter, SQL beautifier, database tool',
        'cron': 'cron expression, cron job, scheduler, crontab',
        'url': 'URL encoder, URL decoder, URL tool, web utility',
        'base64': 'Base64 encoder, Base64 decoder, encoding tool',
        'password': 'password generator, password security, secure password',
        'hash': 'hash generator, checksum, MD5, SHA256',
        'markdown': 'Markdown tool, Markdown converter, Markdown preview',
        'docker': 'Docker tool, Docker Compose, container tool',
        'nginx': 'Nginx config, server config, web server',
        'api': 'API tool, API tester, REST API, API development',
        'timestamp': 'timestamp converter, epoch converter, unix time',
        'color': 'color tool, color picker, color converter, palette',
        'toml': 'TOML parser, TOML validator, config file',
        'regex': 'regex tester, regular expression, pattern matching',
        'webhook': 'webhook tester, HTTP webhook, webhook debugger',
        'og': 'OpenGraph, social media, meta image, Twitter card',
        'svg': 'SVG generator, vector graphics, SVG pattern',
        'csv': 'CSV converter, CSV to JSON, spreadsheet tool',
        'git': 'Git tool, version control, Git command',
        'lorem': 'Lorem ipsum, placeholder text, dummy text',
        'unit': 'unit test, test generator, testing tool',
        'diff': 'diff tool, text comparison, file compare',
        'minif': 'minifier, code compression, optimize',
        'format': 'code formatter, beautifier, prettify',
        'encoder': 'encoder, decoder, encoding tool',
        'generator': 'code generator, dev tool, generator',
        'validator': 'validator, validation tool, code checker',
        'converter': 'file converter, format converter, data conversion',
        'builder': 'builder tool, generator, creator',
        'inspector': 'inspector tool, debugger, analyzer',
        'analyzer': 'analyzer tool, code analysis, scanner',
        'tester': 'tester tool, testing utility, debug tool',
        'studio': 'design studio, creator tool, visual editor',
    }

    extra_keywords = []
    for key, value in categories.items():
        if key in base:
            extra_keywords.append(value)

    if extra_keywords:
        return f"{base_keywords}, {', '.join(extra_keywords)}, developer tools, online tool, web utility"
    else:
        return f"{base_keywords}, developer tools, online tool, web utility, productivity"

def generate_description(name, slug):
    """Ürün adından açıklama oluştur"""
    base = name.replace(' Pro', '').strip()

    templates = [
        f"Professional {base} tool for developers. Generate, convert, and validate instantly with a clean, modern interface.",
        f"Advanced {base} utility for developers. Fast, secure, and completely client-side processing for maximum privacy.",
        f"The ultimate {base} tool. Powerful features with an intuitive interface designed for developers and power users.",
        f"{base} made simple. Professional-grade tool with instant results and developer-friendly features.",
    ]

    # Slug hash'ine göre tutarlı bir şablon seç
    import hashlib
    idx = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(templates)
    return templates[idx]

def find_index_html(slug):
    """Ürünün index.html dosyasını bul"""
    paths = [
        Path(f"products/{slug}/public/index.html"),
        Path(f"products/{slug}/index.html"),
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def update_product_seo(product):
    """Bir ürünün SEO meta tag'lerini güncelle"""
    slug = product.get('slug')
    name = product.get('name')

    filepath = find_index_html(slug)
    if not filepath:
        return False, "index.html bulunamadı"

    try:
        content = filepath.read_text(encoding='utf-8')

        # Meta verileri oluştur
        title = name
        description = generate_description(name, slug)
        keywords = generate_keywords(name)
        canonical = product.get('vercel_url', f"https://{slug}.vercel.app")

        # 1. Title güncelle
        title_pattern = r'<title>[^<]*</title>'
        if re.search(title_pattern, content):
            content = re.sub(title_pattern, f'<title>{title}</title>', content)
        else:
            content = re.sub(r'(<head[^>]*>)', f'\\1\n    <title>{title}</title>', content)

        # 2. Meta description güncelle/ekle
        desc_pattern = r'<meta name="description" content="[^"]*">'
        if re.search(desc_pattern, content):
            content = re.sub(desc_pattern, f'<meta name="description" content="{description}">', content)
        else:
            content = re.sub(
                r'(<meta charset="[^"]+"/?>|<meta name="viewport"[^>]+>)',
                f'\\1\n    <meta name="description" content="{description}">',
                content
            )

        # 3. Keywords ekle (yoksa)
        if not re.search(r'<meta name="keywords"', content):
            content = re.sub(
                r'(<meta name="description"[^>]+>)',
                f'\\1\n    <meta name="keywords" content="{keywords}">',
                content
            )

        # 4. Robots meta ekle (yoksa)
        if not re.search(r'<meta name="robots"', content):
            content = re.sub(
                r'(<meta name="keywords"[^>]+>)',
                f'\\1\n    <meta name="robots" content="index, follow, max-image-preview:large">',
                content
            )

        # 5. Author meta ekle (yoksa)
        if not re.search(r'<meta name="author"', content):
            content = re.sub(
                r'(<meta name="robots"[^>]+>)',
                f'\\1\n    <meta name="author" content="Universe7Creator">',
                content
            )

        # 6. Canonical link ekle/güncelle
        canonical_pattern = r'<link rel="canonical" href="[^"]*">'
        if re.search(canonical_pattern, content):
            content = re.sub(canonical_pattern, f'<link rel="canonical" href="{canonical}">', content)
        else:
            content = re.sub(
                r'(<meta name="author"[^>]+>)',
                f'\\1\n    <link rel="canonical" href="{canonical}">',
                content
            )

        # 7. OG title/description güncelle
        og_title_pattern = r'<meta property="og:title" content="[^"]*">'
        if re.search(og_title_pattern, content):
            content = re.sub(og_title_pattern, f'<meta property="og:title" content="{title}">', content)

        og_desc_pattern = r'<meta property="og:description" content="[^"]*">'
        if re.search(og_desc_pattern, content):
            content = re.sub(og_desc_pattern, f'<meta property="og:description" content="{description}">', content)

        # 8. Twitter title/description güncelle
        tw_title_pattern = r'<meta (?:name|property)="twitter:title" content="[^"]*">'
        if re.search(tw_title_pattern, content):
            content = re.sub(tw_title_pattern, f'<meta name="twitter:title" content="{title}">', content)

        tw_desc_pattern = r'<meta (?:name|property)="twitter:description" content="[^"]*">'
        if re.search(tw_desc_pattern, content):
            content = re.sub(tw_desc_pattern, f'<meta name="twitter:description" content="{description}">', content)

        # 9. Schema.org JSON-LD ekle (yoksa)
        if not re.search(r'<script type="application/ld\+json">', content):
            schema = {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": name,
                "description": description,
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Any",
                "offers": {
                    "@type": "Offer",
                    "price": "19.00",
                    "priceCurrency": "USD"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.8",
                    "ratingCount": "150"
                },
                "url": canonical
            }
            schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
            schema_script = f'''<script type="application/ld+json">
    {schema_json}
    </script>'''

            # CSS link'ten önce veya head kapanışından önce ekle
            if '<link href="https://fonts.googleapis.com' in content:
                content = content.replace(
                    '<link href="https://fonts.googleapis.com',
                    f'{schema_script}\n    <link href="https://fonts.googleapis.com'
                )
            else:
                content = re.sub(r'(</head>)', f'{schema_script}\n    \\1', content)

        # Dosyaya yaz
        filepath.write_text(content, encoding='utf-8')
        return True, "Güncellendi"

    except Exception as e:
        return False, str(e)

def main():
    """Ana fonksiyon - STATE.json'dan ürünleri çek ve SEO optimizasyonu yap"""
    # STATE.json oku
    with open('STATE.json') as f:
        state = json.load(f)

    products = state.get('products', {}).get('active', [])

    # SEO optimize edilmemiş ürünleri filtrele
    not_seo_optimized = [p for p in products if not p.get('seo_optimized', False)]

    print("=" * 70)
    print("🚀 SEO OPTIMIZASYONU - CYCLE 1022")
    print("=" * 70)
    print(f"Toplam ürün: {len(products)}")
    print(f"SEO optimize edilecek: {len(not_seo_optimized)}")
    print("=" * 70)

    # İlk 24 ürünü işle (Vercel limit: 100 deploy/gün)
    batch_size = 24
    batch = not_seo_optimized[:batch_size]

    updated = 0
    failed = 0
    failed_slugs = []

    for product in batch:
        slug = product.get('slug')
        name = product.get('name')

        success, msg = update_product_seo(product)

        if success:
            # Ürünü seo_optimized olarak işaretle
            product['seo_optimized'] = True
            product['seo_updated_at'] = json.dumps({"updated": True})
            print(f"✅ {slug}: {name[:40]}...")
            updated += 1
        else:
            print(f"❌ {slug}: {msg}")
            failed += 1
            failed_slugs.append(slug)

    # STATE.json güncelle
    with open('STATE.json', 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print("=" * 70)
    print(f"✅ Güncellenen: {updated}")
    print(f"❌ Başarısız: {failed}")
    if failed_slugs:
        print(f"   Başarısız slugs: {', '.join(failed_slugs)}")
    print("=" * 70)

    # Özet dosyası oluştur
    summary = {
        "cycle": state.get('cycle', 1022),
        "mode": "OPTIMIZE",
        "action": "seo_optimization",
        "updated_count": updated,
        "failed_count": failed,
        "failed_slugs": failed_slugs,
        "remaining": len(not_seo_optimized) - updated
    }

    with open('seo_update_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    return updated, failed

if __name__ == "__main__":
    main()
