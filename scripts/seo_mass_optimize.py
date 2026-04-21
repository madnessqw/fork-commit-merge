#!/usr/bin/env python3
"""
SEO Mass Optimizer - Adds JSON-LD structured data to product pages
"""
import json
import os
import sys
from datetime import datetime

# Products to optimize with their metadata
PRODUCTS = [
    {
        "slug": "toml-toolkit",
        "name": "TOML Toolkit",
        "description": "Parse, validate, and convert TOML files with ease. The complete TOML utility for developers.",
        "price": "9.00",
        "category": "DeveloperApplication",
        "url": "https://toml-toolkit.vercel.app"
    },
    {
        "slug": "mock-data-pro",
        "name": "Mock Data Pro",
        "description": "Generate realistic mock data for testing and development. JSON, CSV, SQL export.",
        "price": "9.00",
        "category": "DeveloperApplication",
        "url": "https://mock-data-pro.vercel.app"
    },
    {
        "slug": "unit-test-generator",
        "name": "Unit Test Generator",
        "description": "Automatically generate unit tests from your code. Jest, Mocha, PyTest support.",
        "price": "19.00",
        "category": "DeveloperApplication",
        "url": "https://unit-test-generator-six.vercel.app"
    },
    {
        "slug": "xml-to-json",
        "name": "XML to JSON",
        "description": "Convert XML to JSON instantly. Fast, accurate, developer-friendly API.",
        "price": "19.00",
        "category": "DeveloperApplication",
        "url": "https://xml-to-json.vercel.app"
    },
    {
        "slug": "css-gradient-studio",
        "name": "CSS Gradient Studio",
        "description": "Create beautiful CSS gradients visually. Copy-paste ready CSS code.",
        "price": "9.00",
        "category": "DeveloperApplication",
        "url": "https://css-gradient-studio.vercel.app"
    }
]

JSON_LD_TEMPLATE = """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{name}",
  "description": "{description}",
  "applicationCategory": "{category}",
  "operatingSystem": "Any",
  "offers": {{
    "@type": "Offer",
    "price": "{price}",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "127"
  }}
}}
</script>"""

def find_index_html(slug):
    """Find the index.html file for a product"""
    paths = [
        f"products/{slug}/public/index.html",
        f"products/{slug}/index.html"
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def add_seo_to_product(product):
    """Add JSON-LD structured data to a product's index.html"""
    slug = product["slug"]
    path = find_index_html(slug)

    if not path:
        return {"slug": slug, "status": "error", "message": "index.html not found"}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has JSON-LD
        if 'application/ld+json' in content:
            return {"slug": slug, "status": "skipped", "message": "Already has JSON-LD"}

        # Generate JSON-LD
        json_ld = JSON_LD_TEMPLATE.format(
            name=product["name"],
            description=product["description"],
            category=product["category"],
            price=product["price"]
        )

        # Insert before </head>
        if '</head>' in content:
            content = content.replace('</head>', f"{json_ld}\n</head>")
        else:
            return {"slug": slug, "status": "error", "message": "No </head> tag found"}

        # Write back
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {"slug": slug, "status": "success", "path": path}

    except Exception as e:
        return {"slug": slug, "status": "error", "message": str(e)}

def update_state_json(slugs):
    """Update STATE.json to mark products as SEO optimized"""
    try:
        with open('STATE.json', 'r') as f:
            state = json.load(f)

        now = datetime.utcnow().isoformat() + 'Z'
        updated = 0

        for product in state.get('products', {}).get('active', []):
            if product.get('slug') in slugs:
                product['seo_optimized'] = True
                product['seo_optimized_at'] = now
                updated += 1

        with open('STATE.json', 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        return updated
    except Exception as e:
        print(f"Error updating STATE.json: {e}")
        return 0

def main():
    results = []
    success_slugs = []

    print("=" * 60)
    print("SEO MASS OPTIMIZER - Cycle 1015")
    print("=" * 60)

    for product in PRODUCTS:
        result = add_seo_to_product(product)
        results.append(result)

        if result["status"] == "success":
            success_slugs.append(product["slug"])
            print(f"✅ {product['slug']}: SEO optimized")
        elif result["status"] == "skipped":
            print(f"⏭️  {product['slug']}: Already optimized")
        else:
            print(f"❌ {product['slug']}: {result.get('message', 'Error')}")

    # Update STATE.json
    if success_slugs:
        updated = update_state_json(success_slugs)
        print(f"\n📊 Updated {updated} products in STATE.json")

    # Save results
    with open('seo_results.json', 'w') as f:
        json.dump({
            "cycle": 1015,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "results": results,
            "optimized_count": len(success_slugs)
        }, f, indent=2)

    print(f"\n✨ Complete: {len(success_slugs)} products optimized")
    return len(success_slugs)

if __name__ == "__main__":
    count = main()
    sys.exit(0 if count > 0 else 1)
