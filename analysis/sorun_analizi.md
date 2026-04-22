# Sorun Analizi — Cycle 1100 | 2026-04-22 14:08 UTC

## Ana Darboğaz
- **live_health** — 2 canlı ürün gerçekten sağlıksız. İlk örnek `email-validator-pro` (HTTP 404).

## Summary'den Gelen Gerçekler
- Healthy live: 89/91
- Health pending: 0
- Checkout gap: 0
- Deploy/url gap: 4
- Canonical drift: 0
- Spec-ready backlog: 11

## Canlı Sağlıksız Ürünler
- `email-validator-pro` — code=404 status=not_found url=https://email-validator-pro.vercel.app
- `html-entity-encoder` — code=402 status=error_402 url=https://html-entity-encoder.vercel.app

## URL/Deploy Eksikleri
- browser-use-studio, agent-prompt-engineer

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
