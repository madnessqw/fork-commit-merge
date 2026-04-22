# Sorun Analizi — Cycle 1108 | 2026-04-22 17:49 UTC

## Ana Darboğaz
- **live_health** — 7 canlı ürün gerçekten sağlıksız. İlk örnek `jwt-generator` (HTTP 500).

## Summary'den Gelen Gerçekler
- Healthy live: 84/91
- Health pending: 0
- Checkout gap: 0
- Deploy readiness gap: 5
- Deploy/url gap: 9
- Canonical drift: 0
- Spec-ready backlog: 11

## Canlı Sağlıksız Ürünler
- `jwt-generator` — code=500 status=error_500 url=https://jwt-generator.vercel.app
- `pdf-forge` — code=500 status=error_500 url=https://pdf-forge.vercel.app
- `webhook-tester` — code=404 status=not_found url=https://webhook-tester.vercel.app
- `email-validator-pro` — code=404 status=not_found url=https://email-validator-pro.vercel.app
- `diffmaster` — code=401 status=unauthorized url=https://diffmaster.vercel.app
- `html-entity-encoder` — code=402 status=deployment_disabled url=https://html-entity-encoder.vercel.app
- `timestamp-converter` — code=451 status=error_451 url=https://timestamp-converter.vercel.app

## URL/Deploy Eksikleri
- browser-use-studio, agent-prompt-engineer

## Deploy Readiness Issues
- Count: 5 | Manifest gaps: 3 | URL gaps: 5 | State gaps: 5
- `csv-to-sql-pro` — manifest=spec_version; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle, lemonsqueezy_product_id
- `json-to-csv-pro` — manifest=spec_version; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle, lemonsqueezy_product_id
- `url-parser-pro` — manifest=spec_version; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle, lemonsqueezy_product_id
- `agent-prompt-engineer` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle, lemonsqueezy_product_id
- `browser-use-studio` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle, lemonsqueezy_product_id

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
