#!/usr/bin/env python3
"""
Batch SEO Fixer - Adds missing SEO meta tags to products
"""

import re
import json
from pathlib import Path
from datetime import datetime

# SEO metadata for each product
SEO_DATA = {
    "ai-cost-dashboard": {
        "description": "Calculate costs, analyze usage patterns, and get optimization recommendations for OpenAI, Anthropic, Google, and Groq.",
        "keywords": "AI cost calculator, LLM pricing, OpenAI costs, Anthropic Claude pricing, API cost tracker, token cost estimator"
    },
    "chart-studio": {
        "description": "Create beautiful, interactive charts and data visualizations instantly. Export as PNG, SVG, or embed in your projects.",
        "keywords": "chart maker, data visualization, graph generator, pie chart, bar chart, line chart, SVG charts"
    },
    "cronmaster": {
        "description": "Build, validate and debug cron expressions with an intuitive visual scheduler. Perfect for Linux, Unix and cloud scheduling.",
        "keywords": "cron expression generator, cron builder, schedule maker, Linux cron, Unix cron job, crontab generator"
    },
    "css-shadow-studio": {
        "description": "Design beautiful CSS box shadows with an interactive visual editor. Copy-ready CSS code for your web projects.",
        "keywords": "CSS shadow generator, box shadow tool, CSS effects, web design, shadow editor, CSS3 shadows"
    },
    "favicon-generator-pro": {
        "description": "Generate professional favicons for all devices and platforms. Create ICO, PNG, SVG favicons with one click.",
        "keywords": "favicon generator, ICO converter, website icon maker, browser icons, PWA icons, app icons"
    },
    "geoip-lite": {
        "description": "Fast IP geolocation lookup tool. Get location data including country, city, timezone, and coordinates from any IP address.",
        "keywords": "IP lookup, geolocation, IP tracker, location finder, IP to location, geo IP, IP address lookup"
    },
    "html-entity-encoder": {
        "description": "Encode and decode HTML entities instantly. Convert special characters to HTML codes and back with this developer tool.",
        "keywords": "HTML entity encoder, HTML decoder, special characters, HTML codes, web development, character entities"
    },
    "html-entity": {
        "description": "Encode and decode HTML entities instantly. Convert special characters to HTML codes and back with this developer tool.",
        "keywords": "HTML entity encoder, HTML decoder, special characters, HTML codes, web development, character entities"
    },
    "http-api-client": {
        "description": "Test HTTP APIs with a powerful online REST client. Send GET, POST, PUT, DELETE requests with custom headers and authentication.",
        "keywords": "API tester, REST client, HTTP request tool, API debugger, Postman alternative, HTTP testing"
    },
    "openapi-validator": {
        "description": "Validate OpenAPI 3.0 and Swagger 2.0 specifications. Check for errors, lint your API docs, and ensure spec compliance.",
        "keywords": "OpenAPI validator, Swagger linter, API spec validation, OpenAPI 3.0, Swagger 2.0, API documentation"
    },
    "webhook-tester": {
        "description": "Test webhooks and HTTP callbacks instantly. Inspect incoming requests, debug integrations, and verify payload data.",
        "keywords": "webhook tester, HTTP callback debugger, API webhook testing, request inspector, webhook verification"
    },
    "xml-formatter-pro": {
        "description": "Format and beautify XML documents with syntax highlighting. Validate XML, prettify minified XML, and view tree structure.",
        "keywords": "XML formatter, XML beautifier, XML validator, XML pretty print, XML editor, syntax highlighting"
    },
    "yaml-converter-pro": {
        "description": "Convert YAML to JSON and vice versa instantly. Validate YAML syntax, format documents, and transform data formats.",
        "keywords": "YAML converter, YAML to JSON, JSON to YAML, YAML validator, YAML formatter, data conversion"
    }
}

def fix_product(slug):
    """Fix SEO for a single product"""
    index_file = Path(f"products/{slug}/index.html")

    if not index_file.exists():
        print(f"❌ {slug}: index.html not found")
        return False

    try:
        content = index_file.read_text(encoding='utf-8')

        # Get product data
        data = SEO_DATA.get(slug, {})
        if not data:
            print(f"⚠️  {slug}: No SEO data defined, skipping")
            return False

        description = data['description']
        keywords = data['keywords']

        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else slug.replace('-', ' ').title()

        # Build complete SEO head
        seo_head = f"""<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="UniverseCreator">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://{slug}.vercel.app/">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://{slug}.vercel.app/">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://og-forge.vercel.app/api/og?title={title.replace(' ', '%20')}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://{slug}.vercel.app/">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://og-forge.vercel.app/api/og?title={title.replace(' ', '%20')}">

    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "{title}",
      "description": "{description}",
      "url": "https://{slug}.vercel.app/",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "Any",
      "offers": {{
        "@type": "Offer",
        "price": "19.00",
        "priceCurrency": "USD"
      }},
      "creator": {{
        "@type": "Organization",
        "name": "UniverseCreator"
      }}
    }}
    </script>"""

        # Find existing head content
        head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL)
        if not head_match:
            print(f"❌ {slug}: No head section found")
            return False

        old_head = head_match.group(1)

        # Keep non-meta elements (styles, scripts, links, etc.)
        kept_elements = []
        for line in old_head.split('\n'):
            line = line.strip()
            # Skip meta tags, title, and OG tags (we'll replace them)
            if line.startswith('<meta') and ('name="description"' in line or 'name="keywords"' in line or 'property="og:' in line or 'name="twitter:' in line):
                continue
            if line.startswith('<title'):
                continue
            if line.startswith('<link') and 'rel="canonical"' in line:
                continue
            if 'application/ld+json' in line:
                continue
            if line.strip():
                kept_elements.append(line)

        # Combine SEO head with kept elements
        full_head = seo_head + '\n' + '\n'.join(kept_elements)

        # Replace head
        new_content = content.replace(old_head, full_head)

        # Write back
        index_file.write_text(new_content, encoding='utf-8')
        print(f"✅ {slug}: SEO optimized")
        return True

    except Exception as e:
        print(f"❌ {slug}: Error - {e}")
        return False

def update_state_json(slugs):
    """Update STATE.json to mark products as SEO optimized"""
    try:
        with open('STATE.json') as f:
            state = json.load(f)

        products = state.get('products', {}).get('active', [])
        updated_count = 0

        for product in products:
            if product.get('slug') in slugs:
                product['seo_optimized'] = True
                product['seo_optimized_at'] = datetime.utcnow().isoformat() + 'Z'
                updated_count += 1

        with open('STATE.json', 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        print(f"\n📊 STATE.json updated: {updated_count} products marked as SEO optimized")
        return updated_count

    except Exception as e:
        print(f"❌ STATE.json update error: {e}")
        return 0

def main():
    # Products that need fixing (13 products)
    slugs = [
        "ai-cost-dashboard", "chart-studio", "cronmaster", "css-shadow-studio",
        "favicon-generator-pro", "geoip-lite", "html-entity-encoder", "html-entity",
        "http-api-client", "openapi-validator", "webhook-tester", "xml-formatter-pro",
        "yaml-converter-pro"
    ]

    print(f"🔧 Fixing SEO for {len(slugs)} products...\n")

    success_count = 0
    for slug in slugs:
        if fix_product(slug):
            success_count += 1

    print(f"\n✅ Successfully optimized: {success_count}/{len(slugs)}")

    # Update STATE.json
    if success_count > 0:
        update_state_json(slugs)

    # Also mark the 3 already-optimized products
    already_optimized = ["base64-pro", "jwt-generator", "timestamp-master"]
    update_state_json(already_optimized)

    return success_count

if __name__ == "__main__":
    main()
