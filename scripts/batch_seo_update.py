#!/usr/bin/env python3
"""
Batch SEO Meta Tag Updater for UniverseCreator Products
Updates meta tags, structured data, and SEO elements for multiple products
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# SEO-optimized meta descriptions for each product type
SEO_DESCRIPTIONS = {
    "api-request-builder": "Build and test API requests with our powerful HTTP client. Supports REST, GraphQL with authentication, custom headers, and request history.",
    "number-base-converter": "Convert numbers between binary, decimal, hexadecimal, octal and 30+ bases instantly. Essential tool for programmers and developers.",
    "xml-master-pro": "Advanced XML editor with validation, formatting, XPath queries, and XSLT transformation. The ultimate XML toolkit for developers.",
    "table-to-csv": "Convert HTML tables to CSV format instantly. Extract data from web pages and export to Excel-compatible format with one click.",
    "dataflip": "Transform and convert data between JSON, CSV, XML, and YAML formats. Clean, validate, and format your data with ease.",
    "jwt-generator": "Generate secure JWT tokens with custom claims and algorithms. Test and debug JWTs with our developer-friendly tool.",
    "hash-generator-pro": "Generate MD5, SHA-1, SHA-256, SHA-512 and 15+ hash algorithms instantly. Verify file integrity and create secure checksums.",
    "pdf-forge": "Create, merge, split, and convert PDF documents online. Professional PDF toolkit for developers and businesses.",
    "text-transformer-pro": "Transform text with 50+ converters: case changes, encoding, slug generation, and more. Essential text processing toolkit.",
    "xml-formatter": "Format and validate XML documents with syntax highlighting. Beautiful XML editor with tree view and error detection.",
    "markdown-previewer": "Live Markdown editor with GitHub-flavored preview. Write documentation, README files, and formatted text with instant preview.",
    "croncraft": "Build cron expressions with visual scheduler. Generate and validate cron jobs for Linux, Unix, and cloud scheduling.",
    "envguard-pro": "Secure environment variable manager for development teams. Encrypt, share, and manage .env files safely.",
    "base64-pro": "Encode and decode Base64 strings and files. Supports data URLs, image encoding, and batch processing for developers.",
    "llm-token-lens": "Analyze and count tokens for OpenAI, Claude, and LLaMA models. Optimize your prompts and reduce API costs.",
    "css-grid-gen": "Generate CSS Grid layouts visually. Create responsive grid templates with custom gaps, areas, and auto-placement.",
    "http-pulse": "Monitor HTTP endpoints with uptime checks, response time tracking, and status code monitoring. Free website monitoring tool.",
    "dockerfile-generator": "Generate optimized Dockerfiles for Node.js, Python, Go, Ruby, and 15+ frameworks. Best practices built-in.",
    "timestamp-master": "Convert between Unix timestamps and human-readable dates. Support for multiple formats and timezones for developers.",
    "html-to-markdown-pro": "Convert HTML to clean Markdown format. Preserve formatting while transforming web content to MD files.",
    "api-spec-validator": "Validate OpenAPI/Swagger specifications. Check for errors, test endpoints, and ensure API documentation quality.",
    "markdown-previewer-pro": "Professional Markdown editor with themes, export options, and collaborative features. Write beautiful documentation.",
    "http-load-tester-pro": "Load test your APIs with concurrent requests. Measure response times, throughput, and identify performance bottlenecks.",
    "carbonlite": "Create beautiful code screenshots with Carbon styling. Share syntax-highlighted code snippets on social media."
}

KEYWORDS = {
    "api-request-builder": "API client, HTTP request builder, REST API tester, GraphQL client, API development tools",
    "number-base-converter": "binary converter, hex to decimal, base calculator, programmer tools, number systems",
    "xml-master-pro": "XML editor, XML validator, XPath tool, XSLT transformer, XML formatter",
    "table-to-csv": "HTML table to CSV, data extraction, web scraping tool, CSV export, Excel conversion",
    "dataflip": "data converter, JSON to CSV, XML to JSON, data transformation, file format converter",
    "jwt-generator": "JWT token generator, JSON Web Token, token debugger, JWT encoder, authentication tool",
    "hash-generator-pro": "hash calculator, MD5 generator, SHA-256, checksum tool, file integrity",
    "pdf-forge": "PDF creator, merge PDF, split PDF, PDF converter, document toolkit",
    "text-transformer-pro": "text converter, case changer, slug generator, text formatter, string manipulation",
    "xml-formatter": "XML beautifier, XML validator, XML pretty print, XML editor online, XML checker",
    "markdown-previewer": "Markdown editor, MD preview, GitHub markdown, README editor, documentation tool",
    "croncraft": "cron expression generator, cron builder, schedule maker, cron tester, Linux cron",
    "envguard-pro": "environment variables, .env manager, secrets manager, config encryption, devops tools",
    "base64-pro": "Base64 encoder, Base64 decoder, data URL generator, image to Base64, file encoding",
    "llm-token-lens": "token counter, OpenAI tokens, Claude tokens, LLM pricing, AI cost calculator",
    "css-grid-gen": "CSS Grid generator, grid layout tool, responsive design, CSS template maker",
    "http-pulse": "website monitor, uptime checker, HTTP status monitor, site availability, endpoint monitoring",
    "dockerfile-generator": "Dockerfile creator, container generator, Docker best practices, containerization tool",
    "timestamp-master": "Unix timestamp converter, epoch converter, date formatter, developer tools, timestamp calculator",
    "html-to-markdown-pro": "HTML to Markdown, web to MD, content converter, documentation generator",
    "api-spec-validator": "OpenAPI validator, Swagger checker, API documentation validator, REST API testing",
    "markdown-previewer-pro": "professional markdown, collaborative editing, document export, themed markdown",
    "http-load-tester-pro": "load testing, API performance, stress test, concurrent requests, benchmark tool",
    "carbonlite": "code screenshot, syntax highlighting, code sharing, developer social media, carbon alternative"
}

def update_product_seo(slug):
    """Update SEO meta tags for a single product"""
    product_dir = Path(f"products/{slug}")
    index_file = product_dir / "index.html"

    if not index_file.exists():
        print(f"❌ {slug}: index.html not found")
        return False

    try:
        content = index_file.read_text(encoding='utf-8')

        # Get product info
        name_match = re.search(r'<title>(.*?)</title>', content)
        product_name = name_match.group(1) if name_match else slug.replace('-', ' ').title()

        description = SEO_DESCRIPTIONS.get(slug, f"Professional {product_name} tool for developers. Fast, secure, and easy to use.")
        keywords = KEYWORDS.get(slug, f"{product_name}, developer tools, online utility")

        # Check if already has SEO tags
        if '<meta name="description"' in content and 'seo_optimized' in content:
            print(f"⏭️  {slug}: Already optimized")
            return True

        # Find head section
        head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL)
        if not head_match:
            print(f"❌ {slug}: No head section found")
            return False

        head_content = head_match.group(1)
        original_head = head_content

        # Build new meta tags
        new_meta_tags = f"""<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="UniverseCreator">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://{slug}.vercel.app/">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://{slug}.vercel.app/">
    <meta property="og:title" content="{product_name}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://{slug}.vercel.app/api/og">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://{slug}.vercel.app/">
    <meta name="twitter:title" content="{product_name}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://{slug}.vercel.app/api/og">

    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "{product_name}",
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
    </script>
    <meta name="seo_optimized" content="true">"""

        # Replace the head content
        new_content = content.replace(original_head, new_meta_tags)

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
    # Read products from command line or use default batch
    import sys
    if len(sys.argv) > 1:
        slugs = sys.argv[1:]
    else:
        # Default first batch
        slugs = [
            "api-request-builder", "number-base-converter", "xml-master-pro",
            "table-to-csv", "dataflip", "jwt-generator", "hash-generator-pro",
            "pdf-forge", "text-transformer-pro", "xml-formatter", "markdown-previewer",
            "croncraft", "envguard-pro", "base64-pro", "llm-token-lens",
            "css-grid-gen", "http-pulse", "dockerfile-generator", "timestamp-master",
            "html-to-markdown-pro", "api-spec-validator", "markdown-previewer-pro",
            "http-load-tester-pro", "carbonlite"
        ]

    print(f"🔍 Processing {len(slugs)} products for SEO optimization...\n")

    success_count = 0
    for slug in slugs:
        if update_product_seo(slug):
            success_count += 1

    print(f"\n✅ Successfully optimized: {success_count}/{len(slugs)}")

    # Update STATE.json
    if success_count > 0:
        update_state_json(slugs[:success_count])

    return success_count

if __name__ == "__main__":
    main()
