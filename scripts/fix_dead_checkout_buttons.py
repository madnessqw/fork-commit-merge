#!/usr/bin/env python3
"""
Fix dead checkout buttons in product index.html files.
For products with price in product.json but no checkout wiring in HTML.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def discover_dead_button_slugs() -> list[str]:
    """Auto-discover products with checkout_url in product.json but no wiring in index.html."""
    products_dir = ROOT / "products"
    if not products_dir.exists():
        return []
    slugs = []
    for product_dir in sorted(products_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        slug = product_dir.name
        product_json = product_dir / "product.json"
        index_html = product_dir / "index.html"
        if not product_json.exists() or not index_html.exists():
            continue
        try:
            data = json.loads(product_json.read_text())
            co = data.get("checkout_url", "")
            if not co or not co.startswith("http"):
                continue
            html = index_html.read_text()
            if "const CHECKOUT_URL" in html or "window.open(CHECKOUT_URL" in html:
                continue
            slugs.append(slug)
        except Exception:
            continue
    return slugs


def get_checkout_url(slug: str) -> str | None:
    """Get checkout URL from product.json"""
    product_json = ROOT / "products" / slug / "product.json"
    if not product_json.exists():
        return None
    try:
        data = json.loads(product_json.read_text())
        return data.get("checkout_url")
    except Exception:
        return None


def fix_dead_buttons(slug: str) -> bool:
    """Fix dead checkout buttons in a product's index.html"""
    index_path = ROOT / "products" / slug / "index.html"
    if not index_path.exists():
        return False

    checkout_url = get_checkout_url(slug)
    if not checkout_url:
        return False

    html = index_path.read_text()

    # Check if already has checkout wiring
    if "const CHECKOUT_URL" in html or "window.open(CHECKOUT_URL" in html:
        return False  # Already fixed

    # Add CHECKOUT_URL constant before </script> tags
    script_fix = f'''
    // Checkout
    const CHECKOUT_URL = "{checkout_url}";
    document.querySelectorAll('.buy-btn, .checkout-btn, [class*="buy"], [class*="checkout"]').forEach(btn => {{
        btn.style.cursor = 'pointer';
        btn.addEventListener('click', () => window.open(CHECKOUT_URL, '_blank'));
    }});
    '''

    # For buttons with "Get Access" text
    # Replace: <button ...>Get Access - $19</button>
    # With: <button ... onclick="window.open(CHECKOUT_URL, '_blank')">Get Access - $19</button>

    # Pattern 1: Button with "Get Access" or "Buy Now" or "Get Pro" that has no onclick
    patterns_to_fix = [
        # Button with price text but no onclick
        (r'(<button[^>]*>[^<]*(?:Get Access|Buy Now|Get Pro)[^<]*\$19[^<]*</button>)',
         lambda m: re.sub(r'<button', f'<button onclick="window.open(CHECKOUT_URL, \'_blank\')"', m.group(1))),
        # Button with price text and no onclick (variation)
        (r'(<button[^>]*>[^<]*(?:\$19|19)[^<]*</button>)',
         lambda m: m.group(1) if 'onclick' in m.group(1) else re.sub(r'<button', f'<button onclick="window.open(CHECKOUT_URL, \'_blank\')"', m.group(1))),
        # <a href="#"> with price text - dead link
        (r'(<a[^>]*href="#()"[^>]*>[^<]*(?:Get Access|Buy Now|Get Pro)[^<]*</a>)',
         lambda m: re.sub(r'href="#"', f'href="{checkout_url}" target="_blank"', m.group(1))),
        # <a href="#pricing"> that's actually dead (no pricing section buy button)
        (r'(<a[^>]*href="#pricing"[^>]*>[^<]*(?:Buy Now|Get Pro)[^<]*</a>)',
         lambda m: re.sub(r'href="#pricing"', f'href="{checkout_url}" target="_blank"', m.group(1))),
    ]

    modified = False
    for pattern, replacement in patterns_to_fix:
        new_html, n = re.subn(pattern, replacement, html, flags=re.IGNORECASE)
        if n > 0:
            html = new_html
            modified = True

    # Add CHECKOUT_URL and event listeners before </body>
    if "CHECKOUT_URL" not in html:
        html = html.replace("</body>", f'''
<script>
// Checkout URL - auto-wired by fix_dead_checkout_buttons.py
const CHECKOUT_URL = "{checkout_url}";
document.querySelectorAll('.buy-btn, [class*="buy"], [class*="checkout"]').forEach(btn => {{
    if (!btn.getAttribute('onclick') && !btn.href) {{
        btn.style.cursor = 'pointer';
        btn.addEventListener('click', () => window.open(CHECKOUT_URL, '_blank'));
    }}
}});
</script>
</body>''')
        modified = True

    if modified:
        index_path.write_text(html)
        return True
    return False


def main():
    slugs = discover_dead_button_slugs()
    if not slugs:
        print("No dead checkout buttons found. All products wired.")
        return

    print(f"Discovered {len(slugs)} products with dead checkout buttons")
    fixed = []
    failed = []

    for slug in slugs:
        try:
            if fix_dead_buttons(slug):
                fixed.append(slug)
                print(f"✅ Fixed: {slug}")
            else:
                print(f"⏭️  Skipped: {slug}")
        except Exception as e:
            failed.append((slug, str(e)))
            print(f"❌ Failed: {slug}: {e}")

    print(f"\n=== Summary ===")
    print(f"Fixed: {len(fixed)}")
    print(f"Failed: {len(failed)}")
    if failed:
        for slug, err in failed:
            print(f"  - {slug}: {err}")


if __name__ == "__main__":
    main()