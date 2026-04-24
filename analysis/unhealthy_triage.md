# Unhealthy Live Triage Report
**Generated:** 2026-04-24 09:16 UTC
**Count:** 3

| Slug | HTTP | Label | Severity | Quick Fix |
|------|------|-------|----------|----------|
| jwt-generator | 500 | server_error | high | `cd products/jwt-generator && vercel logs --output json 2>/dev/null | tail -50 || echo 'Check Vercel dashboard → Deployments → Function Logs'` |
| diffmaster | 401 | sso_protection | high | `vercel project ls --yes 2>/dev/null && vercel inspect diffmaster 2>/dev/null || echo 'Check Vercel dashboard → Settings → Authentication → Disable Vercel Authentication'` |
| timestamp-converter | 451 | geo_block | low | `echo 'Geo-block: check Vercel Firewall rules → vercel.com/dashboard → project → Settings → Firewall'` |

**Severity breakdown:** 2 high / 0 medium / 1 low
