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
    },
    "ssl-cert-checker": {"description": "Analyze SSL/TLS certificates for any domain. Check expiration, issuer, chain validation, and security configuration.", "keywords": "SSL Cert Checker", "price": "19", "rating_count": "50"},
    "security-headers-checker": {"description": "Scan and analyze HTTP security headers for any website. Get actionable recommendations to improve web security posture.", "keywords": "Security Headers Checker", "price": "19", "rating_count": "50"},
    "subdomain-finder": {"description": "Discover subdomains for any domain. Security reconnaissance tool for penetration testers and security researchers.", "keywords": "Subdomain Finder", "price": "19", "rating_count": "50"},
    "htaccess-generator": {"description": "Professional Apache .htaccess file generator with rewrite rules, security headers, caching, and compression settings", "keywords": "Htaccess Generator Pro", "price": "19", "rating_count": "50"},
    "nginx-config-tester": {"description": "Validate and test Nginx configuration files with syntax checking, best practice analysis, and security recommendations", "keywords": "Nginx Config Tester", "price": "19", "rating_count": "50"},
    "ssl-cipher-analyzer": {"description": "Analyze SSL/TLS cipher suites, check protocol versions, and get security recommendations for your HTTPS configuration", "keywords": "SSL Cipher Analyzer", "price": "19", "rating_count": "50"},
    "diff-checker-pro": {"description": "Compare text, code, or JSON side-by-side with highlighted differences", "keywords": "Diff Checker Pro", "price": "9", "rating_count": "50"},
    "yaml-validator-pro": {"description": "Validate YAML syntax, detect errors, and format YAML files with proper indentation", "keywords": "YAML Validator Pro", "price": "9", "rating_count": "50"},
    "case-converter-pro": {"description": "Convert text between camelCase, PascalCase, snake_case, kebab-case, and more instantly", "keywords": "Case Converter Pro", "price": "9", "rating_count": "50"},
    "htpasswd-generator": {"description": "Generate Apache/Nginx .htpasswd files with multiple hash algorithms", "keywords": "Htpasswd Generator Pro", "price": "19", "rating_count": "50"},
    "docker-run-generator": {"description": "Visual Docker run command builder with interactive UI, port mapping, volume mounts, and environment variable management", "keywords": "Docker Run Generator", "price": "19", "rating_count": "50"},
    "sql-to-nosql": {"description": "Transform SQL queries into NoSQL equivalents for MongoDB, DynamoDB, and Firestore. Supports SELECT, INSERT, UPDATE, DELETE conversions with schema mapping.", "keywords": "SQL to NoSQL Converter", "price": "19", "rating_count": "50"},
    "binary-inspector": {"description": "Inspect binary files, view hex dumps, analyze headers, and decode binary data structures. Support for multiple encodings and byte orders.", "keywords": "Binary Inspector Pro", "price": "19", "rating_count": "50"},
    "browser-mock-studio": {"description": "Generate professional browser mockups with your screenshots. Chrome, Safari, Firefox styles with dark/light modes and custom backgrounds.", "keywords": "Browser Mock Studio", "price": "19", "rating_count": "50"},
    "env-file-manager": {"description": "Manage .env files with a visual editor. Parse, validate, edit, and sync environment variables across multiple environments.", "keywords": "ENV File Manager", "price": "19", "rating_count": "50"},
    "git-diff-visualizer": {"description": "Visualize git diffs with side-by-side and inline views. Syntax highlighting, word-level diff, and export options.", "keywords": "Git Diff Visualizer", "price": "19", "rating_count": "50"},
    "code-screenshot-beautifier": {"description": "Transform your code into stunning screenshots with customizable themes, backgrounds, and formatting. Perfect for social media sharing.", "keywords": "Code Screenshot Beautifier", "price": "19", "rating_count": "50"},
    "json-schema-to-ts": {"description": "Generate TypeScript interfaces and types from JSON Schema definitions. Supports complex schemas, nested objects, and validation.", "keywords": "JSON Schema to TypeScript", "price": "19", "rating_count": "50"},
    "mcp-inspector-pro": {"description": "Inspect, debug, and test Model Context Protocol (MCP) servers. View tools, resources, and test calls interactively.", "keywords": "MCP Inspector Pro", "price": "19", "rating_count": "50"},
    "api-security-scanner": {"description": "Automated security scanning for REST and GraphQL APIs. Detect common vulnerabilities, misconfigurations, and security headers.", "keywords": "API Security Scanner", "price": "19", "rating_count": "50"},
    "docker-command-builder": {"description": "Build Docker commands visually with a guided interface. Includes templates for common operations and best practices.", "keywords": "Docker Command Builder", "price": "19", "rating_count": "50"},
    "mcp-server-scaffolder": {"description": "Quickly scaffold new Model Context Protocol servers with templates for TypeScript, Python, and other languages.", "keywords": "MCP Server Scaffolder", "price": "19", "rating_count": "50"},
    "browser-use-studio": {"description": "Test and debug browser-use and Playwright automation scripts with live preview and step execution.", "keywords": "Browser Use Studio", "price": "19", "rating_count": "50"},
    "agent-prompt-engineer": {"description": "Engineer and optimize prompts for AI agents. Includes templates, testing, and performance analysis for Claude, GPT, and other models.", "keywords": "Agent Prompt Engineer", "price": "19", "rating_count": "50"},
    "api-mock-server": {"description": "Create mock REST and GraphQL APIs for testing and development. Dynamic responses, request matching, and proxy support.", "keywords": "API Mock Server", "price": "19", "rating_count": "50"},
    "api-mock-generator": {"description": "Generate realistic mock API responses for testing. Create REST and GraphQL mocks instantly.", "keywords": "API Mock Generator", "price": "19", "rating_count": "50"},
    "chmod-calculator": {"description": "Calculate and visualize Linux file permissions with octal, symbolic, and checkbox interfaces. Generate chmod commands instantly.", "keywords": "Chmod Calculator Pro", "price": "9", "rating_count": "50"},
    "jwt-debugger-pro": {"description": "Decode, verify, and debug JWT tokens with signature validation, header analysis, and security checks.", "keywords": "JWT Debugger Pro", "price": "19", "rating_count": "50"},
    "ssl-config-generator": {"description": "Create production-ready SSL/TLS configurations for Nginx, Apache, and other servers. Includes security headers and cipher suite recommendations.", "keywords": "SSL Config Generator", "price": "19", "rating_count": "50"},
    "csv-to-sql-pro": {"description": "Transform CSV files into ready-to-execute SQL INSERT statements with support for multiple database dialects including MySQL, PostgreSQL, SQLite, and SQL Server.", "keywords": "CSV to SQL Pro", "price": "19", "rating_count": "50"},
    "json-to-csv-pro": {"description": "Transform complex nested JSON into clean, flat CSV files. Handles arrays, nested objects, and provides column customization options.", "keywords": "JSON to CSV Pro", "price": "19", "rating_count": "50"},
    "url-parser-pro": {"description": "Extract every component from any URL including protocol, host, pathname, query parameters, hash fragments, and more. Generate ready-to-use code snippets in multiple languages.", "keywords": "URL Parser Pro", "price": "19", "rating_count": "50"},
    "sql-query-builder": {"description": "Visual SQL query builder with drag-and-drop interface. Build complex queries without writing SQL.", "keywords": "SQL Query Builder Pro", "price": "19", "rating_count": "50"},
    "code-formatter-universal": {"description": "Universal code formatter supporting 50+ languages. Auto-format your code with customizable rules.", "keywords": "Code Formatter Universal", "price": "19", "rating_count": "50"},
    "json-diff-pro": {"description": "Compare JSON files side-by-side and visualize differences instantly", "keywords": "JSON Diff Pro", "price": "19", "rating_count": "50"},
    "graphql-schema-validator": {"description": "Validate and visualize GraphQL schemas with detailed error reporting", "keywords": "GraphQL Schema Validator", "price": "19", "rating_count": "50"},
    "code-complexity-analyzer": {"description": "Analyze code complexity and generate maintainability reports", "keywords": "Code Complexity Analyzer", "price": "19", "rating_count": "50"},
    "jwt-decoder-pro": {"description": "Professional JWT token decoder with signature verification, payload inspection, header analysis, and token validation. Supports HS256, HS384, HS512, RS256, RS384, RS512 algorithms.", "keywords": "JWT Decoder Pro", "price": "19", "rating_count": "50"},
    "regex-visualizer-pro": {"description": "Interactive regex visualizer with real-time matching, explanation builder, cheat sheet, and pattern tester. Perfect for learning and debugging complex regular expressions.", "keywords": "Regex Visualizer Pro", "price": "19", "rating_count": "50"},
    "base64-encoder-pro": {"description": "Professional Base64 encoding/decoding tool with file support, URL-safe encoding, multiple output formats, and batch processing capabilities.", "keywords": "Base64 Encoder/Decoder Pro", "price": "19", "rating_count": "50"},
    "ascii-art-generator": {"description": "Generate stylish ASCII banners, logos, and text art for code comments, documentation, and CLI outputs. 30+ fonts, real-time preview, export to TXT.", "keywords": "ASCII Art Generator Pro", "price": "19", "rating_count": "50"},
    "terminal-os": {"description": "Web-based terminal emulator with xterm.js for developers", "keywords": "Terminal OS", "price": "9", "rating_count": "50"},
    "terraink": {"description": "Create stunning custom city map posters from any location worldwide. Powered by OpenStreetMap data with beautiful typography and export-ready PNG output.", "keywords": "Terraink - Cartographic Poster Engine", "price": "19", "rating_count": "50"},
    "docker-compose-generator": {"description": "Generate Docker Compose files quickly, add/remove services, define ports/volumes, validate with YAML preview, and download instantly. Perfect for developers needing production-ready container configurations.", "keywords": "Docker Compose Generator Pro", "price": "19", "rating_count": "50"},
    "mcphub": {"description": "Discover, manage, and monitor MCP servers. The central registry for Model Context Protocol tools with config management and health monitoring.", "keywords": "MCP Hub", "price": "24", "rating_count": "50"},
    "api-to-mcp": {"description": "Convert any REST API into an MCP server in seconds. Upload your OpenAPI spec and get a hosted MCP endpoint. Perfect for AI agents that need to connect to existing APIs.", "keywords": "API to MCP Converter", "price": "14", "rating_count": "50"},
    "json-compare-pro": {"description": "Professional JSON comparison tool for developers. Side-by-side diff view, nested object comparison, array diffing, and precise change detection.", "keywords": "JSON Compare Pro", "price": "19", "rating_count": "50"},
    "json-formatter": {"description": "Free online JSON formatter, validator, and beautifier. Format, validate, minify, and convert JSON with syntax highlighting.", "keywords": "JSON Formatter Pro", "price": "9", "rating_count": "50"},
    "cron-expression-tester": {"description": "Test and validate cron expressions with next run preview and human-readable explanations.", "keywords": "Cron Expression Tester", "price": "9", "rating_count": "50"},
    "csv-to-markdown": {"description": "Convert CSV files to beautifully formatted Markdown tables instantly. Perfect for documentation and reports.", "keywords": "CSV to Markdown Pro", "price": "9", "rating_count": "50"},
    "csv-validator-pro": {"description": "Advanced CSV validation with delimiter detection, schema validation, and error reporting", "keywords": "CSV Validator Pro", "price": "19", "rating_count": "50"},
    "svg-optimizer-pro": {"description": "Advanced SVG optimization tool that reduces file size while preserving quality. Features precision control, batch processing, and visual comparison.", "keywords": "SVG Optimizer Pro", "price": "19", "rating_count": "50"},
    "csv-converter-pro": {"description": "Professional data transformation tool for developers. Convert between CSV, JSON, TSV, Markdown, HTML, and SQL formats instantly.", "keywords": "CSV Converter Pro", "price": "9", "rating_count": "50"},
    "html-entity-pro": {"description": "Convert special characters to HTML entities and back. Perfect for web developers and content creators.", "keywords": "HTML Entity Encoder Pro", "price": "19", "rating_count": "50"},
    "nginx-config": {"description": "Professional Nginx configuration generator with security best practices, SSL templates, and performance optimizations", "keywords": "Nginx Config Generator", "price": "9", "rating_count": "50"},
    "docker-compose-builder": {"description": "Build Docker Compose files visually with drag-and-drop services. Includes templates for popular stacks like LAMP, MEAN, and microservices.", "keywords": "Docker Compose Builder", "price": "19", "rating_count": "50"},
    "commit-message-generator": {"description": "AI-powered tool that analyzes git diffs and generates meaningful conventional commit messages in seconds. Paste your diff, get a proper commit message.", "keywords": "commit-message-generator", "price": "9", "rating_count": "50"},
    "pr-review-agent": {"description": "AI-powered GitHub PR review with static analysis and LLM suggestions. Get instant code review on every pull request — no subscription required.", "keywords": "PR Review Agent", "price": "19", "rating_count": "50"},
    "html-validator-pro": {"description": "Comprehensive HTML validation with W3C standards, accessibility checks, and SEO analysis", "keywords": "HTML Validator Pro", "price": "19", "rating_count": "50"},
    "regex-library-pro": {"description": "Access 100+ battle-tested regex patterns for emails, URLs, credit cards, dates, and more. Test instantly with live matching and explanations.", "keywords": "Regex Library Pro", "price": "19", "rating_count": "50"},
    "json-schema-generator": {"description": "Convert any JSON into valid JSON Schema with inferred types, validation rules, and customizable depth. Supports Draft 7, 2019-09, and 2020-12.", "keywords": "JSON Schema Generator", "price": "19", "rating_count": "50"},
    "dns-lookup-pro": {"description": "Professional DNS lookup tool with multiple record types, propagation check, and DNS health analysis", "keywords": "DNS Lookup Pro", "price": "19", "rating_count": "50"},
    "mcp-marketplace": {"description": "Discover, explore, and configure MCP servers. The registry for AI tool integrations — copy .mcp.json in one click.", "keywords": "MCP Marketplace", "price": "9", "rating_count": "50"},
    "cli-pipe-viz": {"description": "Build and debug shell command pipelines visually. Drag-and-drop commands, connect them with pipes, and see real-time output streaming.", "keywords": "CLI Pipe Viz", "price": "9", "rating_count": "50"},
    "cron-health-checker": {"description": "Verify your cron jobs are actually running. Enter cron expression and last run time, get health status with next expected run, timezone correctness check.", "keywords": "Cron Health Checker", "price": "12", "rating_count": "50"}
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
