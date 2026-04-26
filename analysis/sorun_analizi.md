# Sorun Analizi — Cycle 1218 | 2026-04-26 16:55 UTC

## Ana Darboğaz
- **canonical_url_drift** — 6 live ürün canonical URL'den sapmış (toplam 13: 6 live + 7 accepted). Vercel auth invalid olduğu için alias/redirect düzeltilemiyor.
- **STATE.json inconsistency** — canonical_url_drift alanı 0 gösteriyordu, gerçek değer 13. Kimi tarafından düzeltildi.

## Summary'den Gelen Gerçekler
- Healthy live: 177/177
- Canonical healthy: 177/177
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 13 (6 live + 7 accepted)
- Spec-ready backlog: 0
- Accepted canonical drift: 7

## Canonical Drift Ürünleri
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app
- `chmod-calculator` — current=https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app
- `terminal-os` — current=https://terminal-os-green.vercel.app ideal=https://terminal-os.vercel.app
- `terraink` — current=https://terraink-flax.vercel.app ideal=https://terraink.vercel.app
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app
- `commit-message-generator` — current=https://commit-message-generator-gamma.vercel.app ideal=https://commit-message-generator.vercel.app

## Kabul Edilmiş Canonical Drift
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `email-validator-pro` — current=https://email-validator-pro-smoky.vercel.app ideal=https://email-validator-pro.vercel.app
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
