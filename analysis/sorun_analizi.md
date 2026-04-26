# Sorun Analizi — Cycle 1208 | 2026-04-26 08:02 UTC

## Ana Darboğaz
- **vercel_auth_invalid** — 10+ cycle'dır tekrarlanıyor. Deploy yapılamıyor, canonical drift düzeltilemiyor.
- **codex_offline** — Her iki account da limit aşımında. Apr 28'e kadar offline.

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 5 live + 7 accepted
- Spec-ready backlog: 0
- Orphan dirs: 0
- Revenue: $0

## Canonical Drift Ürünleri (Live — Düzeltilmesi Gereken)
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
- **vercel_auth_invalid** [critical/open] — Vercel token expired/invalid. Deploy ve alias fix engelleniyor. Manuel token refresh gerekiyor.
- **codex_offline** [high/open] — Both accounts rate limited until Apr 28. No builder available.
- **zero_revenue** [medium/open] — Checkout infrastructure complete (169/169 Polar) but $0 sales. Traffic/conversion issue suspected.

## Çözülen Issue'lar (Eski Kayıtlar Temizlendi)
- ~~state_drift~~ — STATE.json cycle 1208'e sync edildi. Eski cycle 759 kaydı artık geçerli değil.
- ~~agent_missing~~ — Toolsmith agent kaydı eski, mevcut sistemde bu agent rolü Claude subagent'ları tarafından karşılanıyor.

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
