# Vercel AutoFix Report
**Generated:** 2026-04-24T09:42:59.339688Z
**Diagnosed:** 7

**Recovered:** 0 | **Auto-fixable:** 4 | **Applied:** 0

## diffmaster — HTTP 401
- **Root cause:** Vercel Authentication / SSO Protection enabled
- **URL:** `https://diffmaster.vercel.app`
- **Prior code:** 401 → **Current:** 401
- **Config issues:** uses_deprecated_routes
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://diffmaster.vercel.app/api/health → HTTP 401
- **Fix steps:**
  1. Open Vercel dashboard → project Settings → Deployment Protection
  1. Disable 'Vercel Authentication'
  1. Redeploy: cd products/diffmaster && vercel --prod --yes

## email-validator-pro — HTTP 404
- **Root cause:** Project not deployed or wrong slug
- **URL:** `https://email-validator-pro.vercel.app`
- **Prior code:** 404 → **Current:** 404
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://email-validator-pro.vercel.app/api/health → HTTP 404
- **Fix steps:**
  1. Verify project files exist locally
  1. Deploy: cd products/email-validator-pro && vercel --prod --yes

## html-entity-encoder — HTTP 402
- **Root cause:** Deployment disabled (billing or plan limit)
- **URL:** `https://html-entity-encoder.vercel.app`
- **Prior code:** 402 → **Current:** 402
- **Config issues:** uses_deprecated_routes
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://html-entity-encoder.vercel.app/api/health → HTTP 402
- **Fix steps:**
  1. Check Vercel billing status
  1. Verify project is not paused
  1. Redeploy if needed

## jwt-generator — HTTP 500
- **Root cause:** Server error — build or runtime failure
- **URL:** `https://jwt-generator.vercel.app`
- **Prior code:** 500 → **Current:** 500
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://jwt-generator.vercel.app/api/health → HTTP 404
- **Fix steps:**
  1. Check Vercel deployment logs
  1. Inspect api/ directory for runtime errors
  1. Fix code and redeploy

## pdf-forge — HTTP 500
- **Root cause:** Server error — build or runtime failure
- **URL:** `https://pdf-forge.vercel.app`
- **Prior code:** 500 → **Current:** 500
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://pdf-forge.vercel.app/api/health → HTTP 500
- **Fix steps:**
  1. Check Vercel deployment logs
  1. Inspect api/ directory for runtime errors
  1. Fix code and redeploy

## timestamp-converter — HTTP 451
- **Root cause:** Geo-blocked by Vercel Firewall
- **URL:** `https://timestamp-converter.vercel.app`
- **Prior code:** 451 → **Current:** 451
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://timestamp-converter.vercel.app/api/health → HTTP 451
- **Fix steps:**
  1. Check Vercel Firewall rules → project Settings → Firewall
  1. Remove or modify geo-blocking rules
  1. Whitelist necessary regions

## webhook-tester — HTTP 404
- **Root cause:** Project not deployed or wrong slug
- **URL:** `https://webhook-tester.vercel.app`
- **Prior code:** 404 → **Current:** 404
- **API files:** health.js, process.js, webhook.js
- **Health endpoint:** https://webhook-tester.vercel.app/api/health → HTTP 404
- **Fix steps:**
  1. Verify project files exist locally
  1. Deploy: cd products/webhook-tester && vercel --prod --yes
