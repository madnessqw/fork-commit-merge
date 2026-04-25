# Sorun Analizi — Cycle 1170 | 2026-04-25 15:00 UTC

## Ana Darboğaz
- **canonical_url_drift** — 5 live ürün canonical URL'den sapmış; ilk örnek `croncraft` (https://quickcron.vercel.app → https://croncraft.vercel.app).

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 163/169
- Health pending: 0
- Fallback healthy: 6
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 5
- Spec-ready backlog: 0
- Accepted canonical drift: 1

## Canonical Drift Ürünleri
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app health=alternate_healthy code=200 probe=https://croncraft.vercel.app canonical_code=200 canonical_status=redirected_preview_alias
- `chmod-calculator` — current=https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app health=alternate_healthy code=200 canonical_code=307 canonical_status=error_307
- `terminal-os` — current=https://terminal-os-green.vercel.app ideal=https://terminal-os.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `terraink` — current=https://terraink-flax.vercel.app ideal=https://terraink.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found

## Kabul Edilmiş Canonical Drift
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app health=alternate_healthy code=200 canonical_code=402 canonical_status=deployment_disabled

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
