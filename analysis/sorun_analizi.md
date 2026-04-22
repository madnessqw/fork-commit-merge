# Sorun Analizi — Cycle 1090 | 2026-04-22 10:07 UTC

## Ana Darboğaz
- **live_health** — 4 canlı ürün sağlıksız; ilk örnek `jwt-generator` (HTTP 0).

## Summary'den Gelen Gerçekler
- Healthy live: 78/82
- Checkout gap: 0
- Deploy/url gap: 8
- Canonical drift: 0
- Spec-ready backlog: 13

## Canlı Sağlıksız Ürünler
- `jwt-generator` — code=0 status=timeout url=https://jwt-generator.vercel.app
- `pdf-forge` — code=0 status=timeout url=https://pdf-forge.vercel.app
- `diffmaster` — code=401 status=unauthorized url=https://diffmaster.vercel.app
- `html-entity-encoder` — code=0 status=timeout url=https://html-entity-encoder.vercel.app

## URL/Deploy Eksikleri
- json-schema-to-ts, mcp-server-scaffolder, browser-use-studio, agent-prompt-engineer

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
