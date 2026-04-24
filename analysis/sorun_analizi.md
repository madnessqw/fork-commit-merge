# Sorun Analizi — Cycle 1109 | 2026-04-24 05:00 UTC

## Ana Darboğaz
- **live_health** — 3 canlı ürün gerçekten sağlıksız. Ayrıca 4 canlı ürün fallback alias ile ayakta. İlk örnek `jwt-generator` (HTTP 500).

## Summary'den Gelen Gerçekler
- Healthy live: 86/89
- Canonical healthy: 82/89
- Health pending: 0
- Fallback healthy: 4
- Checkout gap: 1
- Deploy readiness gap: 27
- Deploy/url gap: 16
- Canonical drift: 4
- Spec-ready backlog: 22

## Canlı Sağlıksız Ürünler
- `jwt-generator` — code=500 status=error_500 url=https://jwt-generator.vercel.app
- `diffmaster` — code=401 status=unauthorized url=https://diffmaster.vercel.app
- `timestamp-converter` — code=451 status=error_451 url=https://timestamp-converter.vercel.app

## Checkout Eksikleri
- sql-to-nosql

## URL/Deploy Eksikleri
- browser-mock-studio, docker-compose-builder, env-file-manager, git-diff-visualizer, code-screenshot-beautifier, json-schema-to-ts, mcp-inspector-pro, api-security-scanner, docker-command-builder, mcp-server-scaffolder, browser-use-studio, agent-prompt-engineer, ...

## Canonical Drift Ürünleri
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `email-validator-pro` — current=https://email-validator-pro-smoky.vercel.app ideal=https://email-validator-pro.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app health=alternate_healthy code=200 canonical_code=402 canonical_status=deployment_disabled

## Deploy Readiness Issues
- Count: 27 | Manifest gaps: 0 | URL gaps: 27 | State gaps: 24
- `agent-prompt-engineer` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `api-mock-server` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `browser-mock-studio` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `browser-use-studio` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `docker-command-builder` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `docker-compose-builder` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `env-file-manager` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `htpasswd-generator` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `api-security-scanner` — manifest=none; url=vercel_url, deployment_url, webhook_url, checkout_url; state=payment_provider, created_cycle, deployed_cycle
- `case-converter-pro` — manifest=none; url=vercel_url, deployment_url, github_url, webhook_url, checkout_url; state=payment_provider, deployed_cycle

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
