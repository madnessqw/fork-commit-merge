# Sorun Analizi — Cycle 1072 | 2026-04-22 00:14 UTC

## Ana Darboğaz
- **live_health** — 1 canlı ürün sağlıksız; ilk örnek `jwt-generator` (HTTP 0).

## Summary'den Gelen Gerçekler
- Healthy live: 76/77
- Checkout gap: 0
- Deploy/url gap: 25
- Canonical drift: 2
- Spec-ready backlog: 33

## Canlı Sağlıksız Ürünler
- `jwt-generator` — code=0 status=error_500 url=https://jwt-generator.vercel.app

## URL/Deploy Eksikleri
- security-headers-checker, subdomain-finder, nginx-config-tester, ssl-cipher-analyzer, htpasswd-generator, docker-run-generator, sql-to-nosql, chmod-calculator, binary-inspector, ssl-config-generator, browser-mock-studio, docker-compose-builder, ...

## Canonical Drift Ürünleri
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app
- `diffmaster` — current=https://diffmaster-rose.vercel.app ideal=https://diffmaster.vercel.app

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
