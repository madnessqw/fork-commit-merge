# Unhealthy Live Triage Report
**Generated:** 2026-04-24 13:07 UTC
**Count:** 7

| Slug | HTTP | Label | Severity | Quick Fix |
|------|------|-------|----------|----------|
| jwt-generator | 500 | canonical_drift/server_error | medium | `cd products/jwt-generator && vercel logs --output json 2>/dev/null | tail -50 || echo 'Check Vercel dashboard → Deployments → Function Logs'` |
| pdf-forge | 500 | canonical_drift/server_error | medium | `cd products/pdf-forge && vercel logs --output json 2>/dev/null | tail -50 || echo 'Check Vercel dashboard → Deployments → Function Logs'` |
| webhook-tester | 404 | canonical_drift/not_found | medium | `cd products/webhook-tester && vercel --prod --yes 2>&1` |
| email-validator-pro | 404 | canonical_drift/not_found | medium | `cd products/email-validator-pro && vercel --prod --yes 2>&1` |
| diffmaster | 401 | canonical_drift/sso_protection | medium | `vercel project ls --yes 2>/dev/null && vercel inspect diffmaster 2>/dev/null || echo 'Check Vercel dashboard → Settings → Authentication → Disable Vercel Authentication'` |
| html-entity-encoder | 402 | canonical_drift/deployment_disabled | medium | `vercel inspect html-entity-encoder 2>/dev/null || echo 'Check billing/deployment status in Vercel dashboard'` |
| timestamp-converter | 451 | canonical_drift/geo_block | medium | `echo 'Geo-block: check Vercel Firewall rules → vercel.com/dashboard → project → Settings → Firewall'` |

**Severity breakdown:** 0 high / 7 medium / 0 low
