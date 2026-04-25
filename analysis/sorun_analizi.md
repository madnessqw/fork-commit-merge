# Sorun Analizi — Cycle 1184 | 2026-04-25 20:52 UTC

## Summary
- Healthy live: 169/169
- Canonical healthy: 169/169 (canonical_url_override ile)
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Canonical drift: 5 (kabul edilmiş 7)
- Spec-ready backlog: 0

## Canonical Drift Ürünleri (Aktif — Fix Bekleyen)
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app
- `chmod-calculator` — current=https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app
- `terminal-os` — current=https://terminal-os-green.vercel.app ideal=https://terminal-os.vercel.app
- `terraink` — current=https://terraink-flax.vercel.app ideal=https://terraink.vercel.app
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app

## Kabul Edilmiş Canonical Drift
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `email-validator-pro` — current=https://email-validator-pro-smoky.vercel.app ideal=https://email-validator-pro.vercel.app
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app

## Açık Issue Kayıtları
- **codex_offline** [high/blocker] — Codex both accounts blocked until Apr 28. No new builds/deploys possible. GLM and Kimi maintaining system.
- **vercel_auth_invalid** [high/blocker] — Vercel auth token invalid. Deployments blocked. Device code auth pending (MJFC-THWB).
- **canonical_drift_5** [medium/pending] — 5 products on hash URLs, canonical URLs not aliased. Requires Vercel auth to fix.
- **zero_revenue** [high/ongoing] — $0 revenue. 169 live products with Polar checkout but no sales. Marketing/discovery gap.

## Çözülmüş (Resolved)
- state_drift — fixed in cycle 1177 (12 missing live products added, 1 duplicate removed)
- price_mismatch — 4/4 resolved in cycle 1162
- checkout_gap — 0 gaps verified since cycle 1164
- deploy_gap — corrected to 0 in cycle 1178

## Not
- Bu dosya live STATE.json → STATE_SUMMARY.json ve unresolved issue kayıtlarından üretildi.
- Codex Apr 28'e kadar offline — yeni ürün geliştirme ve deploy durdu.
