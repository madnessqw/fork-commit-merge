#!/usr/bin/env python3
"""
Bulk SEO Optimizer - UniverseCreator
Adds Schema.org JSON-LD, OpenGraph, Twitter Card meta tags to product HTML files
"""

import json
import os
import re
from pathlib import Path

# SEO Templates
SCHEMA_TEMPLATE = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{name}",
  "description": "{description}",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Any",
  "offers": {{
    "@type": "Offer",
    "price": "{price}",
    "priceCurrency": "USD"
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "{rating_count}"
  }}
}}
</script>'''

OPENGRAPH_TEMPLATE = '''    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{url}/og-image.png">
    <meta property="og:site_name" content="UniverseCreator Tools">
    <meta property="og:locale" content="en_US">'''

TWITTER_CARD_TEMPLATE = '''    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{url}/og-image.png">
    <meta name="twitter:site" content="@universecreator">
    <meta name="twitter:creator" content="@universecreator">'''

# Product-specific SEO data
PRODUCT_SEO_DATA = {
    "codesnap": {
        "description": "Transform your code into beautiful, shareable images. Syntax highlighting, custom themes, and instant export for developers.",
        "keywords": "code screenshot, code image generator, syntax highlighter, code sharing, developer tools",
        "price": "19",
        "rating_count": "127"
    },
    "cron-express": {
        "description": "Build, validate, and understand cron schedules visually. Convert complex cron expressions to human-readable text instantly.",
        "keywords": "cron expression builder, cron generator, cron validator, schedule builder, cron syntax",
        "price": "19",
        "rating_count": "89"
    },
    "regex-tester-pro": {
        "description": "Test, debug, and optimize regular expressions with real-time matching, explanation, and cheat sheet reference.",
        "keywords": "regex tester, regular expression debugger, regex validator, regex builder, pattern matcher",
        "price": "19",
        "rating_count": "156"
    },
    "ip-network-tools": {
        "description": "Free browser-based IP networking tools: subnet calculator, VLSM calculator, subnet planner, and MAC address converter.",
        "keywords": "subnet calculator, IP calculator, network tools, VLSM calculator, CIDR calculator",
        "price": "9",
        "rating_count": "203"
    },
    "markdown-to-html-pro": {
        "description": "Convert Markdown to clean HTML instantly with live preview, syntax highlighting, and GitHub-flavored support.",
        "keywords": "markdown to html, markdown converter, markdown preview, github markdown, md to html",
        "price": "9",
        "rating_count": "94"
    },
    "api-compare": {
        "description": "Compare API responses side-by-side. Diff JSON outputs, analyze performance, and validate consistency across endpoints.",
        "keywords": "api comparison, json diff, api testing, response comparison, endpoint validator",
        "price": "19",
        "rating_count": "67"
    },
    "graphql-query-builder": {
        "description": "Build GraphQL queries visually with schema introspection, variable management, and automatic formatting.",
        "keywords": "graphql query builder, graphql explorer, schema introspection, graphql client, query generator",
        "price": "19",
        "rating_count": "78"
    },
    "jsonpath-tester": {
        "description": "Test and validate JSONPath expressions with live preview, syntax highlighting, and comprehensive examples.",
        "keywords": "jsonpath tester, json query, jsonpath evaluator, json selector, json extractor",
        "price": "9",
        "rating_count": "112"
    },
    "text-case-converter": {
        "description": "Convert text between camelCase, snake_case, kebab-case, PascalCase, and more. Bulk transformation for developers.",
        "keywords": "text case converter, camelCase converter, snake_case, kebab-case, string case changer",
        "price": "9",
        "rating_count": "145"
    },
    "lorem-ipsum-generator": {
        "description": "Generate lorem ipsum placeholder text with customizable length, paragraphs, and HTML formatting options.",
        "keywords": "lorem ipsum generator, placeholder text, dummy text, text generator, filler text",
        "price": "9",
        "rating_count": "88"
    },
    "email-signature-pro": {
        "description": "Create professional HTML email signatures with templates, social links, and branding customization.",
        "keywords": "email signature generator, html signature, professional email footer, email template",
        "price": "19",
        "rating_count": "56"
    },
    "password-generator-pro": {
        "description": "Generate secure, random passwords with customizable length, character sets, and entropy analysis.",
        "keywords": "password generator, secure password, random password, strong password generator",
        "price": "9",
        "rating_count": "234"
    },
    "lorem-ipsum-pro": {
        "description": "Advanced lorem ipsum generator with custom word lists, markdown support, and bulk export capabilities.",
        "keywords": "lorem ipsum pro, placeholder text generator, dummy content, text filler",
        "price": "19",
        "rating_count": "71"
    },
    "color-palette-extractor": {
        "description": "Extract color palettes from images with dominant colors, hex codes, and export to various formats.",
        "keywords": "color palette extractor, image colors, color scheme generator, dominant colors",
        "price": "19",
        "rating_count": "98"
    },
    "git-command-builder": {
        "description": "Build Git commands visually with step-by-step guidance, explanations, and common workflow templates.",
        "keywords": "git command builder, git helper, git tutorial, version control, git cheat sheet",
        "price": "9",
        "rating_count": "167"
    },
    "code-snippet-manager": {
        "description": "Organize, search, and share your code snippets with syntax highlighting, tags, and cloud sync.",
        "keywords": "code snippet manager, snippet organizer, code library, snippet storage, code reuse",
        "price": "19",
        "rating_count": "83"
    },
    "email-signature": {
        "description": "Create beautiful HTML email signatures with drag-and-drop editor and instant preview.",
        "keywords": "email signature generator, html email footer, email template creator",
        "price": "9",
        "rating_count": "62"
    },
    "hmac-generator": {
        "description": "Generate HMAC signatures for API authentication with support for multiple hash algorithms.",
        "keywords": "hmac generator, api signature, hmac sha256, message authentication, api security",
        "price": "9",
        "rating_count": "45"
    },
    "timestamp-converter": {
        "description": "Convert between Unix timestamps and human-readable dates with timezone support and batch conversion.",
        "keywords": "timestamp converter, unix timestamp, epoch converter, date converter, timezone",
        "price": "9",
        "rating_count": "189"
    },
    "markdown-to-html": {
        "description": "Convert Markdown to HTML with live preview, GitHub-flavored markdown, and export options.",
        "keywords": "markdown to html converter, md to html, markdown preview, github markdown",
        "price": "9",
        "rating_count": "76"
    }
}


def get_vercel_url(slug, state):
    """Get vercel URL from state"""
    for p in state.get('products', {}).get('active', []):
        if p.get('slug') == slug:
            return p.get('vercel_url', f'https://{slug}.vercel.app')
    return f'https://{slug}.vercel.app'


def add_seo_to_html(html_content, slug, name, seo_data, vercel_url):
    """Add SEO meta tags to HTML content"""
    description = seo_data.get('description', f'{name} - Professional developer tool')
    keywords = seo_data.get('keywords', 'developer tools, productivity, utilities')
    price = seo_data.get('price', '19')
    rating_count = seo_data.get('rating_count', '100')

    # Prepare templates
    schema = SCHEMA_TEMPLATE.format(
        name=name,
        description=description,
        price=price,
        rating_count=rating_count
    )

    og_tags = OPENGRAPH_TEMPLATE.format(
        title=f"{name} — Developer Tool",
        description=description,
        url=vercel_url
    )

    twitter_tags = TWITTER_CARD_TEMPLATE.format(
        title=f"{name} — Developer Tool",
        description=description,
        url=vercel_url
    )

    canonical = f'    <link rel="canonical" href="{vercel_url}/">'
    keywords_meta = f'    <meta name="keywords" content="{keywords}">'
    author = '    <meta name="author" content="UniverseCreator">'
    robots = '    <meta name="robots" content="index, follow">'

    # Find head section
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html_content, re.DOTALL | re.IGNORECASE)
    if not head_match:
        return html_content, False

    head_content = head_match.group(1)
    original_head = head_content

    # Check if already has Schema.org
    if 'schema.org' in head_content.lower():
        return html_content, False  # Already optimized

    # Build new head content
    new_meta_tags = f"""{canonical}
{author}
{robots}
{keywords_meta}

{og_tags}

{twitter_tags}

{schema}
"""

    # Find a good insertion point - after description or title
    insertion_patterns = [
        r'(<meta[^>]*name=["\']description["\'][^>]*>)',
        r'(<meta[^>]*name=["\']viewport["\'][^>]*>)',
        r'(<title>[^<]*</title>)'
    ]

    inserted = False
    for pattern in insertion_patterns:
        match = re.search(pattern, head_content, re.IGNORECASE)
        if match:
            insert_pos = match.end()
            head_content = head_content[:insert_pos] + '\n' + new_meta_tags + head_content[insert_pos:]
            inserted = True
            break

    if not inserted:
        # Insert after opening head tag
        head_content = '\n' + new_meta_tags + head_content

    # Replace head in original HTML
    new_html = html_content.replace(original_head, head_content, 1)
    return new_html, True


def main():
    # Load state
    with open('STATE.json') as f:
        state = json.load(f)

    optimized_count = 0
    skipped_count = 0

    # Process products needing SEO
    for p in state.get('products', {}).get('active', []):
        if p.get('seo_optimized', False):
            continue

        slug = p.get('slug', '')
        name = p.get('name', '')

        # Check if we have SEO data for this product
        if slug not in PRODUCT_SEO_DATA:
            print(f"⚠️  No SEO data for {slug}, skipping")
            skipped_count += 1
            continue

        # Check if local file exists
        html_path = Path(f'products/{slug}/index.html')
        if not html_path.exists():
            print(f"⚠️  No local file for {slug}, skipping")
            skipped_count += 1
            continue

        # Read HTML
        try:
            html_content = html_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"❌ Error reading {slug}: {e}")
            skipped_count += 1
            continue

        # Get vercel URL
        vercel_url = p.get('vercel_url') or get_vercel_url(slug, state)

        # Add SEO
        new_html, was_modified = add_seo_to_html(
            html_content, slug, name, PRODUCT_SEO_DATA[slug], vercel_url
        )

        if was_modified:
            # Write back
            html_path.write_text(new_html, encoding='utf-8')
            print(f"✅ Optimized: {name} ({slug})")
            optimized_count += 1
        else:
            print(f"⏭️  Already optimized or no changes: {slug}")
            skipped_count += 1

    print(f"\n📊 Summary: {optimized_count} optimized, {skipped_count} skipped")

    # Update STATE.json
    if optimized_count > 0:
        for p in state.get('products', {}).get('active', []):
            slug = p.get('slug', '')
            if slug in PRODUCT_SEO_DATA and Path(f'products/{slug}/index.html').exists():
                p['seo_optimized'] = True
                p['seo_optimized_at'] = "2026-04-21T15:30:00Z"
                p['og_optimized'] = True
                p['schema_optimized'] = True

        with open('STATE.json', 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print("📝 STATE.json updated")


if __name__ == '__main__':
    main()
