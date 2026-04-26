# Sorun Analizi — Cycle 1203 | 2026-04-26 09:03 UTC

## Ana Darboğaz
- **canonical_url_drift** — 5 live ürün canonical URL'den sapmış; Vercel auth invalid olduğu için alias fix yapılamıyor.

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 5
- Spec-ready backlog: 0
- Accepted canonical drift: 7

## Canonical Drift Ürünleri
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
- **vercel_auth_invalid** [high/blocked] — Token geçersiz, yeni deployment ve alias düzeltme yapılamıyor. Device code: MJFC-THWB
- **codex_offline** [high/blocked] — Her iki hesap usage limit doldu, Apr 28'e kadar bekleniyor.

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Stale issue'lar (state_drift, agent_missing) temizlendi — eski cycle'lardan kalmıştı.
