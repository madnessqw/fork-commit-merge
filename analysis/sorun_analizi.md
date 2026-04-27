# Sorun Analizi — Cycle 231 | 2026-04-27 08:35 UTC

## Ana Darboğaz
- **ready_for_payment_health** — 1 ready_for_payment ürün health-check'te sorunlu; ilk örnek `git-workflow-auto` (HTTP 404, not_found).

## Summary'den Gelen Gerçekler
- Healthy live: 183/183
- Canonical healthy: 169/183
- Health pending: 0
- Fallback healthy: 14
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 14
- Spec-ready backlog: 0

## Canonical Drift Ürünleri
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app health=alternate_healthy code=200 probe=https://croncraft.vercel.app canonical_code=200 canonical_status=redirected_preview_alias
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app health=alternate_healthy code=200 canonical_code=401 canonical_status=unauthorized
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app health=alternate_healthy code=200 canonical_code=402 canonical_status=deployment_disabled
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `chmod-calculator` — current=https://chmod-calculator-5atogp6t7-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app health=alternate_healthy code=200 canonical_code=307 canonical_status=error_307
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app health=alternate_healthy code=200 canonical_code=451 canonical_status=error_451
- `commit-message-generator` — current=https://commit-message-generator-gamma.vercel.app ideal=https://commit-message-generator.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found

## Ready-for-Payment Health Issues
- `git-workflow-auto` — code=404 status=not_found url=https://git-workflow-auto.vercel.app canonical_url=https://git-workflow-auto.vercel.app canonical_code=404 canonical_status=not_found

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
