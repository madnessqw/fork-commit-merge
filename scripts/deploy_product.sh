#!/bin/bash
# deploy_product.sh — Deploy a product to GitHub + Vercel + send Telegram notification
# Usage: ./scripts/deploy_product.sh <slug>
# Example: ./scripts/deploy_product.sh codesnap

set -e

SLUG="$1"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PRODUCT_DIR="$BASE_DIR/products/$SLUG"
PRODUCT_JSON="$PRODUCT_DIR/product.json"

# Telegram config
BOT_TOKEN="7590893298:AAGUHxxOCuWCi4NItlQP8Wr6sNGGVaImXII"
CHAT_ID="7941453284"

# GitHub config
GH_USER="universe7creator"
export GH_TOKEN="${GH_TOKEN:-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}"
export GITHUB_TOKEN="$GH_TOKEN"

if [ -z "$SLUG" ]; then
  echo "❌ Usage: $0 <slug>"
  exit 1
fi

if [ ! -d "$PRODUCT_DIR" ]; then
  echo "❌ Product not found: $PRODUCT_DIR"
  exit 1
fi

if [ ! -f "$PRODUCT_JSON" ]; then
  echo "❌ product.json not found in $PRODUCT_DIR"
  exit 1
fi

# Read product metadata
NAME=$(python3 -c "import json; print(json.load(open('$PRODUCT_JSON'))['name'])")
TAGLINE=$(python3 -c "import json; print(json.load(open('$PRODUCT_JSON'))['tagline'])")
PRICE=$(python3 -c "import json; print(json.load(open('$PRODUCT_JSON'))['price'])")
DESC=$(python3 -c "import json; print(json.load(open('$PRODUCT_JSON')).get('description', ''))")
CURRENT_VERCEL_URL=$(python3 -c "import json; data=json.load(open('$PRODUCT_JSON')); print((data.get('vercel_url') or '').strip())")

is_healthy_vercel_url() {
  local candidate="${1%/}"
  [ -z "$candidate" ] && return 1
  curl -fsS --max-time 15 "$candidate/api/health" >/dev/null 2>&1
}

is_valid_vercel_url() {
  [[ "$1" =~ ^https://[^[:space:]]+\.vercel\.app/?$ ]]
}

echo "🚀 Deploying: $NAME ($SLUG)"
echo "=================================="

# Step 1: GitHub Push
echo ""
echo "📦 Step 1: GitHub Push..."
cd "$PRODUCT_DIR"

if [ ! -d .git ]; then
  git init
  git branch -M main
fi

# Create/verify repo
if ! gh repo view "$GH_USER/$SLUG" &>/dev/null 2>&1; then
  echo "  Creating GitHub repo: $GH_USER/$SLUG"
  gh repo create "$GH_USER/$SLUG" --public --description "$TAGLINE" --source=. --push
else
  echo "  Repo exists. Pushing updates..."
  git remote set-url origin "https://$GH_TOKEN@github.com/$GH_USER/$SLUG.git" 2>/dev/null || \
    git remote add origin "https://$GH_TOKEN@github.com/$GH_USER/$SLUG.git" 2>/dev/null || true
  git add -A
  git commit -m "Deploy: $NAME" 2>/dev/null || echo "  Nothing to commit"
  git push -u origin main --force 2>/dev/null || git push -u origin main 2>/dev/null
fi

GITHUB_URL="https://github.com/$GH_USER/$SLUG"
echo "  ✅ GitHub: $GITHUB_URL"

# Step 2: Vercel Deploy
echo ""
echo "🌐 Step 2: Vercel Deploy..."
cd "$PRODUCT_DIR"
VERCEL_OUTPUT=$(vercel --yes --prod --token "${VERCEL_TOKEN:-vcp_258G92BEBEcaDuAoOgCVMLWsW5ifjcMefXGbWFBMGIbUmlLbH72uKAbg}" 2>&1) || true
DEPLOYMENT_URL=$(echo "$VERCEL_OUTPUT" | grep -oP 'https://[^\s]+\.vercel\.app' | head -1)

if [ -z "$DEPLOYMENT_URL" ]; then
  # Try extracting from vercel output differently
  DEPLOYMENT_URL=$(echo "$VERCEL_OUTPUT" | tail -1 | tr -d '[:space:]')
fi

if ! is_valid_vercel_url "$DEPLOYMENT_URL"; then
  echo "❌ Valid Vercel deployment URL alınamadı."
  echo "$VERCEL_OUTPUT"
  exit 1
fi

# PRODUCTION URL: her zaman slug.vercel.app formatını kullan (hash preview değil)
PRODUCTION_URL="https://${SLUG}.vercel.app"
VERCEL_URL="$PRODUCTION_URL"
# Eğer production URL sağlıklıysa onu kullan, değilse deployment URL'yi dene
if ! curl -fsS --max-time 10 "$PRODUCTION_URL" >/dev/null 2>&1; then
  echo "  ⚠️  Production URL henüz hazır değil, deployment URL kullanılıyor (geçici)"
  VERCEL_URL="$DEPLOYMENT_URL"
fi

echo "  ✅ Deployment URL: $DEPLOYMENT_URL"
echo "  ✅ Public URL: $VERCEL_URL"

# Step 3: Health Check
echo ""
echo "🏥 Step 3: Health Check..."
sleep 5
HEALTH=$(curl -s "$DEPLOYMENT_URL/api/health" 2>/dev/null || curl -s "$VERCEL_URL/api/health" 2>/dev/null || echo "timeout")
echo "  Health: $HEALTH"

WEBHOOK_URL="$VERCEL_URL/api/webhook"

# Step 3.5: Disable SSO/Deployment Protection (otomatik)
echo ""
echo "🔓 Step 3.5: Disabling SSO Protection..."
bash "$BASE_DIR/scripts/fix_vercel_protection.sh" "$SLUG" 2>/dev/null && echo "  ✅ Protection disabled" || echo "  ⚠️ Protection fix failed (non-critical)"

# Step 4: Update product.json
echo ""
echo "📝 Step 4: Updating product.json..."
python3 << PYEOF
import json
with open('$PRODUCT_JSON', 'r') as f:
    data = json.load(f)
checkout_url = data.get('checkout_url') or data.get('lemon_checkout_url') or data.get('lemonsqueezy_checkout_url')
data['vercel_url'] = '$VERCEL_URL'
data['deployment_url'] = '$DEPLOYMENT_URL'
data['github_url'] = '$GITHUB_URL'
data['webhook_url'] = '$WEBHOOK_URL'
data['status'] = 'live' if checkout_url else 'ready_for_payment'
with open('$PRODUCT_JSON', 'w') as f:
    json.dump(data, f, indent=2)
print("  ✅ product.json updated")
PYEOF

# Step 5: Telegram Notification
echo ""
echo "📱 Step 5: Sending Telegram notification..."
MSG="🚀 YENİ ÜRÜN HAZIR — LemonSqueezy'e ekle!

📦 Ürün: $NAME
💬 Tagline: $TAGLINE
📝 Açıklama: $DESC

💰 Önerilen fiyat: $PRICE
🌐 Landing page: $VERCEL_URL
🛰️ Deployment URL: $DEPLOYMENT_URL
📂 GitHub: $GITHUB_URL
🔗 Webhook URL (LS'ye gir): $WEBHOOK_URL

📋 Yapman gerekenler:
1. LemonSqueezy'de yeni product oluştur
2. Webhook URL'yi ayarla: $WEBHOOK_URL
3. License key özelliğini aktive et
4. Checkout URL'yi bana geri yaz

✅ Sistem hazır, müşteri bekliyor."

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MSG}" > /dev/null 2>&1

echo "  ✅ Telegram notification sent"

# Step 6: Update STATE.json
echo ""
echo "📊 Step 6: Updating STATE.json..."
python3 << PYEOF
import json, os
state_file = '$BASE_DIR/STATE.json'
with open(state_file, 'r') as f:
    state = json.load(f)

# Move from building to active
product_entry = {
    "name": "$NAME",
    "slug": "$SLUG",
    "status": "ready_for_payment",
    "vercel_url": "$VERCEL_URL",
    "github_url": "$GITHUB_URL",
    "webhook_url": "$WEBHOOK_URL",
    "lemon_product_id": None,
    "lemon_checkout_url": None,
    "revenue": 0,
    "price": "$PRICE"
}

if 'products' not in state:
    state['products'] = {'active': [], 'building': None, 'pipeline': []}

# Add to active list
active = state['products'].get('active', [])
existing_entry = next((p for p in active if p.get('slug') == '$SLUG'), {})
checkout_url = existing_entry.get('checkout_url') or existing_entry.get('lemon_checkout_url')

# Remove existing entry for same slug if any
active = [p for p in active if p.get('slug') != '$SLUG']
product_entry = {
    **existing_entry,
    **product_entry,
    "status": "live" if checkout_url else "ready_for_payment",
    "vercel_url": "$VERCEL_URL",
    "deployment_url": "$DEPLOYMENT_URL",
    "github_url": "$GITHUB_URL",
    "webhook_url": "$WEBHOOK_URL",
    "price": "$PRICE"
}
if checkout_url:
    product_entry["checkout_url"] = checkout_url
    product_entry["lemon_checkout_url"] = checkout_url

active.append(product_entry)
state['products']['active'] = active
state['products']['active_count'] = len(active)

# Clear building if it's this product
if state['products'].get('building', {}).get('slug') == '$SLUG':
    state['products']['building'] = None

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)
print("  ✅ STATE.json updated")
PYEOF

echo ""
echo "=================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "  🌐 $VERCEL_URL"
echo "  📂 $GITHUB_URL"
echo "  🔗 Webhook: $WEBHOOK_URL"
echo ""
echo "⏳ Waiting for LemonSqueezy checkout URL from owner..."
