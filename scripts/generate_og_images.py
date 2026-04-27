#!/usr/bin/env python3
"""Generate OG images for products based on product.json metadata.

Usage:
    python3 scripts/generate_og_images.py <slug> [slug2 slug3 ...]
    python3 scripts/generate_og_images.py --top N   # top N by price
    python3 scripts/generate_og_images.py --all      # all products
"""

import json
import os
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = REPO_ROOT / "products"
STATE_FILE = REPO_ROOT / "STATE.json"

# OG image dimensions
WIDTH = 1200
HEIGHT = 630

GRADIENTS = [
    ("#667eea", "#764ba2"),   # purple-blue
    ("#f093fb", "#f5576c"),   # pink-red
    ("#4facfe", "#00f2fe"),   # blue-cyan
    ("#43e97b", "#38f9d7"),   # green-teal
    ("#fa709a", "#fee140"),   # pink-yellow
    ("#a18cd1", "#fbc2eb"),   # lavender-pink
    ("#ff9a9e", "#fecfef"),   # salmon-rose
    ("#6a11cb", "#2575fc"),   # deepblue-blue
    ("#f12711", "#f5af19"),   # red-orange
    ("#c471f5", "#fa71cd"),   # violet-pink
]

def load_state():
    with open(STATE_FILE) as f:
        return json.load(f)

def get_top_products(n):
    state = load_state()
    active = state['products']['active']
    
    def get_price(p):
        price = p.get('price', 0)
        if isinstance(price, str):
            price = price.replace('$', '').strip()
            try:
                price = int(price)
            except:
                price = 0
        return int(price)
    
    return [p['s'] for p in sorted(active, key=get_price, reverse=True)[:n]]

def load_product(slug):
    pj = PRODUCTS_DIR / slug / "product.json"
    if not pj.exists():
        return None
    with open(pj) as f:
        return json.load(f)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def blend_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return f"#{int(r1+(r2-r1)*t):02x}{int(g1+(g2-g1)*t):02x}{int(b1+(b2-b1)*t):02x}"

def generate_svg(name, tagline, price, gradient_idx):
    g1, g2 = GRADIENTS[gradient_idx % len(GRADIENTS)]
    bg1 = blend_color(g1, g2, 0)
    bg2 = blend_color(g1, g2, 1)
    
    name_escaped = name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    tagline_escaped = tagline.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>
  <!-- Grid pattern -->
  <g opacity="0.08">
    <line x1="0" y1="0" x2="{WIDTH}" y2="{HEIGHT}" stroke="white" stroke-width="1"/>
    <line x1="{WIDTH}" y1="0" x2="0" y2="{HEIGHT}" stroke="white" stroke-width="1"/>
    <line x1="{WIDTH//2}" y1="0" x2="{WIDTH//2}" y2="{HEIGHT}" stroke="white" stroke-width="0.5"/>
    <line x1="0" y1="{HEIGHT//2}" x2="{WIDTH}" y2="{HEIGHT//2}" stroke="white" stroke-width="0.5"/>
  </g>
  <!-- Product name -->
  <text x="{WIDTH//2}" y="{HEIGHT//2 - 40}" 
        font-family="Arial, Helvetica, sans-serif" font-size="72" font-weight="bold" 
        fill="white" text-anchor="middle" filter="url(#glow)">{name_escaped}</text>
  <!-- Tagline -->
  <text x="{WIDTH//2}" y="{HEIGHT//2 + 30}" 
        font-family="Arial, Helvetica, sans-serif" font-size="28" 
        fill="rgba(255,255,255,0.85)" text-anchor="middle">{tagline_escaped}</text>
  <!-- Price badge -->
  <rect x="{WIDTH//2 - 80}" y="{HEIGHT//2 + 70}" width="160" height="50" rx="25" fill="rgba(255,255,255,0.2)"/>
  <text x="{WIDTH//2}" y="{HEIGHT//2 + 105}" 
        font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold"
        fill="white" text-anchor="middle">${price}</text>
  <!-- Footer -->
  <text x="{WIDTH//2}" y="{HEIGHT - 40}" 
        font-family="Arial, Helvetica, sans-serif" font-size="20" 
        fill="rgba(255,255,255,0.5)" text-anchor="middle">UniverseCreator — Developer Tools</text>
</svg>'''
    return svg

def ensure_dir(path):
    path.parent.mkdir(parents=True, exist_ok=True)

def generate_og_image(slug, dry_run=False):
    product = load_product(slug)
    if not product:
        print(f"  [SKIP] {slug}: no product.json")
        return False
    
    name = product.get('name', slug)
    tagline = product.get('tagline', product.get('description', '')[:80])
    
    price = product.get('price', 0)
    if isinstance(price, str):
        price = price.replace('$', '').strip()
        try:
            price = int(price)
        except:
            price = 0
    
    # Check if og_image already exists
    if product.get('og_image'):
        print(f"  [SKIP] {slug}: og_image already set ({product['og_image'][:50]})")
        return False
    
    gradient_idx = sum(ord(c) for c in slug) % len(GRADIENTS)
    svg = generate_svg(name, tagline, price, gradient_idx)
    
    out_dir = PRODUCTS_DIR / slug / "public"
    ensure_dir(out_dir)
    out_path = out_dir / "og-image.png"
    
    if dry_run:
        print(f"  [DRY] {slug}: would write {out_path} (name={name}, price=${price})")
        return True
    
    # Write SVG temp file
    svg_path = out_path.with_suffix('.svg')
    svg_path.write_text(svg)
    
    # Convert to PNG with ImageMagick
    try:
        result = subprocess.run(
            ['convert', '-background', 'none', '-density', '150', str(svg_path), 
             '-resize', f'{WIDTH}x{HEIGHT}', str(out_path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and out_path.exists():
            # Update product.json
            product['og_image'] = f"/og-image.png"
            with open(PRODUCTS_DIR / slug / "product.json", 'w') as f:
                json.dump(product, f, indent=2)
            svg_path.unlink()
            print(f"  [OK] {slug}: generated {out_path} (${price})")
            return True
        else:
            print(f"  [FAIL] {slug}: convert failed: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"  [ERROR] {slug}: {e}")
        return False

def main():
    dry_run = '--dry' in sys.argv
    if dry_run:
        sys.argv.remove('--dry')
    
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    
    if args[0] == '--top':
        slugs = get_top_products(int(args[1]))
    elif args[0] == '--all':
        state = load_state()
        slugs = [p['s'] for p in state['products']['active']]
    else:
        slugs = args
    
    print(f"Generating OG images for {len(slugs)} products...")
    results = []
    for slug in slugs:
        ok = generate_og_image(slug, dry_run=dry_run)
        results.append((slug, ok))
    
    ok_count = sum(1 for _, ok in results if ok)
    print(f"\nDone: {ok_count}/{len(results)} generated")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
