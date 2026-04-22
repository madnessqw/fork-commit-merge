# Sorun Analizi — Cycle 1077 | 2026-04-22 03:42 UTC

## Ana Darboğaz
- **live_health** — 6 canlı ürün sağlıksız; ilk örnek `jwt-generator` (HTTP 200).

## Summary'den Gelen Gerçekler
- Healthy live: 73/79
- Checkout gap: 1
- Deploy/url gap: 20
- Canonical drift: 4
- Spec-ready backlog: 23

## Canlı Sağlıksız Ürünler
- `jwt-generator` — code=200 status=alternate_healthy url=https://jwt-generator-8wfm19h9w-madnessqws-projects.vercel.app
- `pdf-forge` — code=0 status=error_500 url=https://pdf-forge.vercel.app
- `webhook-tester` — code=200 status=alternate_healthy url=https://webhook-tester-beryl.vercel.app
- `diffmaster` — code=401 status=unauthorized url=https://diffmaster.vercel.app
- `html-entity-encoder` — code=200 status=alternate_healthy url=https://html-entity-encoder-rigo3b8oy-madnessqws-projects.vercel.app
- `timestamp-converter` — code=200 status=alternate_healthy url=https://timestamp-converter-oql54ya5f-madnessqws-projects.vercel.app

## Checkout Eksikleri
- binary-inspector

## URL/Deploy Eksikleri
- sql-to-nosql, browser-mock-studio, docker-compose-builder, git-diff-visualizer, code-screenshot-beautifier, json-schema-to-ts, mcp-inspector-pro, api-security-scanner, docker-command-builder, mcp-server-scaffolder, browser-use-studio, agent-prompt-engineer, ...

## Canonical Drift Ürünleri
- `jwt-generator` — current=https://jwt-generator-8wfm19h9w-madnessqws-projects.vercel.app ideal=https://jwt-generator.vercel.app
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `html-entity-encoder` — current=https://html-entity-encoder-rigo3b8oy-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-oql54ya5f-madnessqws-projects.vercel.app ideal=https://timestamp-converter.vercel.app

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
