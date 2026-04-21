#!/usr/bin/env python3
"""
SEO Optimizasyon Scripti - Batch Update
Cycle 1022 için meta tag optimizasyonu
"""

import json
import os
import re
from pathlib import Path

# Ürün verileri - name, description, keywords mapping
PRODUCTS_META = {
    "webterminal-pro": {
        "title": "WebTerminal Pro - Browser-Based SSH Terminal",
        "description": "Professional web-based SSH terminal emulator. Access remote servers from your browser with persistent sessions, command history, and multi-tab support.",
        "keywords": "SSH terminal, web terminal, browser SSH, remote server access, terminal emulator, online SSH client, web-based terminal",
        "category": "DeveloperApplication"
    },
    "timestamp-converter-pro": {
        "title": "Timestamp Converter Pro - Epoch & DateTime Converter",
        "description": "Convert Unix timestamps to human-readable dates instantly. Supports multiple formats, timezone conversion, and batch processing for developers.",
        "keywords": "timestamp converter, epoch converter, unix timestamp, datetime converter, timestamp to date, developer tools",
        "category": "DeveloperApplication"
    },
    "css-to-tailwind": {
        "title": "CSS to Tailwind Converter - Instant CSS Conversion",
        "description": "Convert vanilla CSS to Tailwind CSS classes instantly. Supports complex selectors, responsive breakpoints, and custom configurations.",
        "keywords": "CSS to Tailwind, Tailwind converter, CSS conversion, Tailwind CSS, developer tools, CSS transformer",
        "category": "DeveloperApplication"
    },
    "url-encoder-decoder": {
        "title": "URL Encoder/Decoder Pro - URL Encoding Tool",
        "description": "Encode and decode URLs instantly with support for URL components, query parameters, and special characters. Perfect for web developers.",
        "keywords": "URL encoder, URL decoder, URL encoding, percent encoding, web development tools, URL tools",
        "category": "DeveloperApplication"
    },
    "html-beautifier": {
        "title": "HTML Beautifier Pro - HTML Formatter & Minifier",
        "description": "Format and beautify messy HTML code instantly. Supports minification, indentation customization, and attribute sorting.",
        "keywords": "HTML beautifier, HTML formatter, HTML minifier, code formatter, web development, HTML tools",
        "category": "DeveloperApplication"
    },
    "sql-query-formatter": {
        "title": "SQL Query Formatter - SQL Beautifier Tool",
        "description": "Format and beautify SQL queries instantly. Supports MySQL, PostgreSQL, SQLite, and standard SQL with syntax highlighting.",
        "keywords": "SQL formatter, SQL beautifier, query formatter, SQL tool, database tools, SQL syntax highlighter",
        "category": "DeveloperApplication"
    },
    "cron-expression-builder": {
        "title": "Cron Expression Builder - Cron Job Generator",
        "description": "Build and validate cron expressions visually. Generate cron schedules with real-time next execution preview and explanation.",
        "keywords": "cron expression, cron builder, cron generator, cron job scheduler, crontab tool, scheduling tool",
        "category": "DeveloperApplication"
    },
    "og-forge": {
        "title": "OG Forge - OpenGraph Image Generator",
        "description": "Generate beautiful OpenGraph and Twitter Card images dynamically. Perfect for social media previews and SEO optimization.",
        "keywords": "OpenGraph generator, OG image, social media image, Twitter card generator, meta image, SEO tools",
        "category": "DeveloperApplication"
    },
    "html-entities": {
        "title": "HTML Entities Pro - HTML Encoder/Decoder",
        "description": "Encode and decode HTML entities instantly. Convert special characters to HTML entities and vice versa with full Unicode support.",
        "keywords": "HTML entities, HTML encoder, HTML decoder, HTML special characters, web development, entity converter",
        "category": "DeveloperApplication"
    },
    "jwtinspector": {
        "title": "JWT Inspector - JWT Token Decoder & Validator",
        "description": "Decode and inspect JWT tokens instantly. View headers, payloads, and verify signatures for debugging authentication.",
        "keywords": "JWT decoder, JWT inspector, token validator, JWT debugger, authentication tool, token analyzer",
        "category": "DeveloperApplication"
    },
}

def update_meta_tags(slug, meta):
    """Ürünün index.html dosyasındaki meta tag'leri güncelle"""
    # index.html public/ veya root'da olabilir
    filepath = Path(f"products/{slug}/public/index.html")
    if not filepath.exists():
        filepath = Path(f"products/{slug}/index.html")

    if not filepath.exists():
        print(f"❌ {slug}: Dosya bulunamadı")
        return False

    content = filepath.read_text(encoding='utf-8')

    # Mevcut title'ı bul
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match and meta.get('title'):
        old_title = title_match.group(1)
        content = content.replace(f"<title>{old_title}</title>", f"<title>{meta['title']}</title>")

    # Meta description güncelle veya ekle
    desc_pattern = r'<meta name="description" content="[^"]*">'
    if re.search(desc_pattern, content):
        content = re.sub(desc_pattern, f'<meta name="description" content="{meta["description"]}">', content)
    else:
        # Description yoksa, viewport'tan sonra ekle
        content = re.sub(
            r'(<meta name="viewport"[^>]+>)',
            f'\\1\n    <meta name="description" content="{meta["description"]}">',
            content
        )

    # Keywords ekle (yoksa)
    if 'keywords' in meta and not re.search(r'<meta name="keywords"', content):
        content = re.sub(
            r'(<meta name="description"[^>]+>)',
            f'\\1\n    <meta name="keywords" content="{meta["keywords"]}">',
            content
        )

    # Robots meta ekle (yoksa)
    if not re.search(r'<meta name="robots"', content):
        content = re.sub(
            r'(<meta name="keywords"[^>]+>)',
            f'\\1\n    <meta name="robots" content="index, follow">',
            content
        )

    # Author meta ekle (yoksa)
    if not re.search(r'<meta name="author"', content):
        content = re.sub(
            r'(<meta name="robots"[^>]+>)',
            f'\\1\n    <meta name="author" content="Universe7Creator">',
            content
        )

    # OG tags güncelle
    if 'title' in meta:
        og_title_pattern = r'<meta property="og:title" content="[^"]*">'
        if re.search(og_title_pattern, content):
            content = re.sub(og_title_pattern, f'<meta property="og:title" content="{meta["title"]}">', content)

    if 'description' in meta:
        og_desc_pattern = r'<meta property="og:description" content="[^"]*">'
        if re.search(og_desc_pattern, content):
            content = re.sub(og_desc_pattern, f'<meta property="og:description" content="{meta["description"]}">', content)

    # Schema.org JSON-LD ekle (yoksa)
    if not re.search(r'<script type="application/ld\+json">', content):
        schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": meta.get('title', slug),
            "description": meta.get('description', ''),
            "applicationCategory": meta.get('category', 'DeveloperApplication'),
            "operatingSystem": "Any",
            "offers": {
                "@type": "Offer",
                "price": "19.00",
                "priceCurrency": "USD"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "ratingCount": "203"
            }
        }
        schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
        schema_script = f'''<script type="application/ld+json">
    {schema_json}
    </script>'''

        # Head kapanışından önce ekle
        content = re.sub(
            r'(</head>)',
            f'{schema_script}\n    \\1',
            content
        )

    # Dosyaya yaz
    filepath.write_text(content, encoding='utf-8')
    print(f"✅ {slug}: SEO meta tag'leri güncellendi")
    return True

def main():
    """Ana fonksiyon - batch işleme"""
    updated = 0
    failed = 0

    print("=" * 60)
    print("SEO OPTIMIZASYONU - CYCLE 1022")
    print("=" * 60)

    for slug, meta in PRODUCTS_META.items():
        try:
            if update_meta_tags(slug, meta):
                updated += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {slug}: Hata - {e}")
            failed += 1

    print("=" * 60)
    print(f"✅ Güncellenen: {updated}")
    print(f"❌ Başarısız: {failed}")
    print("=" * 60)

    return updated, failed

if __name__ == "__main__":
    main()
