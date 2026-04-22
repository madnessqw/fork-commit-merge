# Sorun Analizi — Cycle 1073 | 2026-04-22 01:08 UTC

## Ana Darboğaz
- **live_health** — 2 canlı ürün sağlıksız; ilk örnek `pdf-forge` (HTTP 0).

## Summary'den Gelen Gerçekler
- Healthy live: 75/77
- Checkout gap: 0
- Deploy/url gap: 20
- Canonical drift: 0
- Spec-ready backlog: 27

## Canlı Sağlıksız Ürünler
- `pdf-forge` — code=0 status=error_500 url=https://pdf-forge.vercel.app
- `diffmaster` — code=401 status=unauthorized url=https://diffmaster.vercel.app

## URL/Deploy Eksikleri
- sql-to-nosql, chmod-calculator, binary-inspector, ssl-config-generator, browser-mock-studio, docker-compose-builder, env-file-manager, git-diff-visualizer, code-screenshot-beautifier, json-schema-to-ts, mcp-inspector-pro, api-security-scanner, ...

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
