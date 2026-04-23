# Unhealthy Live Triage Report
**Generated:** 2026-04-23 23:43 UTC
**Count:** 3

| Slug | HTTP | Label | Suggested Action |
|------|------|-------|-----------------|
| jwt-generator | 500 | server_error | Check Vercel build/runtime logs; redeploy if transient |
| diffmaster | 401 | sso_protection | Check Vercel project settings -> disable Vercel Authentication |
| timestamp-converter | 451 | geo_block | Check Vercel firewall/geo rules; may need region whitelist |
