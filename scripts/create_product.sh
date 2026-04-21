#!/bin/bash
# create_product.sh — Create a new product from template
# Usage: ./scripts/create_product.sh <slug> "<Product Name>" "<Description>" "<Price>"
# Example: ./scripts/create_product.sh pdf-extract "PDF Table Extractor" "Extract tables from PDFs" "\$9"

set -e

SLUG="$1"
NAME="$2"
DESC="$3"
PRICE="${4:-\$19}"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PRODUCT_DIR="$BASE_DIR/products/$SLUG"

if [ -z "$SLUG" ] || [ -z "$NAME" ]; then
  echo "❌ Usage: $0 <slug> \"<Product Name>\" \"<Description>\" \"<Price>\""
  echo "   Example: $0 pdf-extract \"PDF Table Extractor\" \"Extract tables\" \"\\\$9\""
  exit 1
fi

if [ -d "$PRODUCT_DIR" ]; then
  echo "❌ Product directory already exists: $PRODUCT_DIR"
  exit 1
fi

echo "🚀 Creating product: $NAME ($SLUG)"
mkdir -p "$PRODUCT_DIR"/{api,public}

# product.json metadata
cat > "$PRODUCT_DIR/product.json" << EOJSON
{
  "name": "$NAME",
  "slug": "$SLUG",
  "tagline": "$DESC",
  "description": "$DESC",
  "price": "$PRICE",
  "features": [],
  "tech_stack": "Vercel + Node.js",
  "status": "building",
  "vercel_url": null,
  "github_url": null,
  "lemonsqueezy_checkout_url": null,
  "lemonsqueezy_product_id": null,
  "webhook_url": null,
  "created_cycle": null,
  "deployed_cycle": null
}
EOJSON

# package.json
cat > "$PRODUCT_DIR/package.json" << EOJSON
{
  "name": "$SLUG",
  "version": "1.0.0",
  "description": "$DESC",
  "main": "api/process.js",
  "scripts": {
    "dev": "node dev-server.js",
    "vercel-build": "echo 'Build complete'"
  },
  "dependencies": {},
  "engines": {
    "node": ">=18.0.0"
  }
}
EOJSON

# vercel.json
cat > "$PRODUCT_DIR/vercel.json" << 'EOJSON'
{
  "version": 2,
  "builds": [
    { "src": "api/**/*.js", "use": "@vercel/node" },
    { "src": "public/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/api/health", "dest": "/api/health.js" },
    { "src": "/api/process", "dest": "/api/process.js" },
    { "src": "/api/webhook", "dest": "/api/webhook.js" },
    { "src": "/(.*)", "dest": "/public/$1" }
  ]
}
EOJSON

# Health endpoint
cat > "$PRODUCT_DIR/api/health.js" << EOJS
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');
  return res.status(200).json({
    status: 'ok',
    product: '$SLUG',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
};
EOJS

# Placeholder process endpoint
cat > "$PRODUCT_DIR/api/process.js" << 'EOJS'
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // TODO: Implement product-specific logic here
  return res.status(200).json({ message: 'Process endpoint ready. Implement your logic.' });
};
EOJS

# Webhook endpoint (LemonSqueezy compatible)
cat > "$PRODUCT_DIR/api/webhook.js" << 'EOJS'
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  if (!secret) return true;
  const computed = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(signature));
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const rawBody = JSON.stringify(req.body);
    const signature = req.headers['x-signature'];
    const secret = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;

    if (secret && signature && !verifySignature(rawBody, signature, secret)) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    const eventName = req.body?.meta?.event_name;
    console.log(`[WEBHOOK] Event: ${eventName}`);
    return res.status(200).json({ message: `Event ${eventName} received` });
  } catch (error) {
    console.error('[ERROR] Webhook:', error);
    return res.status(200).json({ message: 'Processed with errors' });
  }
};
EOJS

# Landing page placeholder
cat > "$PRODUCT_DIR/public/index.html" << EOHTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$NAME</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; color: #333; }
    .container { max-width: 800px; margin: 0 auto; padding: 60px 20px; text-align: center; color: white; }
    h1 { font-size: 3rem; margin-bottom: 20px; }
    p { font-size: 1.2rem; opacity: 0.9; margin-bottom: 40px; }
    .cta { display: inline-block; background: white; color: #667eea; padding: 15px 40px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 1.1rem; }
    .cta:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
  </style>
</head>
<body>
  <div class="container">
    <h1>$NAME</h1>
    <p>$DESC</p>
    <a href="#" class="cta" id="buyBtn">Get Started — $PRICE</a>
  </div>
  <script>
    const CHECKOUT_URL = window.__CHECKOUT_URL || null;
    document.getElementById('buyBtn').addEventListener('click', (e) => {
      e.preventDefault();
      if (CHECKOUT_URL) window.open(CHECKOUT_URL, '_blank');
      else alert('Store coming soon! Contact @OtonomUniverseCreator on Telegram.');
    });
  </script>
</body>
</html>
EOHTML

echo "✅ Product '$NAME' created at: $PRODUCT_DIR"
echo ""
echo "Next steps:"
echo "  1. Implement api/process.js with your product logic"
echo "  2. Customize public/index.html landing page"
echo "  3. Run: ./scripts/deploy_product.sh $SLUG"
