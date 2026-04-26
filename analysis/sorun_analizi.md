# Sorun Analizi — Cycle 1193 | 2026-04-26 02:29 UTC

## Ana Darboğaz
- **vercel_auth_invalid** — Vercel CLI authentication expired. Alias fixes, canonical drift resolution, and new deploys blocked.
- **codex_offline** — Both Codex accounts usage limited until Apr 28.

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 12 (5 live + 7 accepted)
- Spec-ready backlog: 0

## Canonical Drift Ürünleri (Live — 5)
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app
- `chmod-calculator` — current=https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app
- `terminal-os` — current=https://terminal-os-green.vercel.app ideal=https://terminal-os.vercel.app
- `terraink` — current=https://terraink-flax.vercel.app ideal=https://terraink.vercel.app
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app

## Kabul Edilmiş Canonical Drift (7)
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `email-validator-pro` — current=https://email-validator-pro-smoky.vercel.app ideal=https://email-validator-pro.vercel.app
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app

## Yeni Bulgular (Cycle 1193)
- **98 Orphan Product Directories** — `products/` klasöründe 98 dizin STATE.json active listesinde yok. GLM `portfolio_orphan_scanner.py` ile tespit etti.
- **Researcher Signal Stale** — `.signals/researcher_needed` (reason=research_stale) mevcut ancak işlenme durumu belirsiz.

## Açık Issue Kayıtları
- Vercel auth invalid → manual token refresh gerekli
- Codex offline until Apr 28
- 98 orphan directories → arşiv/kurtarma analizi bekleniyor

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Canonical drift 12 ürün (5 live + 7 accepted) Vercel alias fix ile çözülecek — auth invalid nedeniyle bloklu.
- Checkout coverage %100 — 0 gap.
