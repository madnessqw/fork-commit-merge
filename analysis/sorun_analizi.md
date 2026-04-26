# Sorun Analizi — Cycle 1191 | 2026-04-26 01:05 UTC

## Ana Bulgular
- **checkout_gap**: 0 — Polar plan 0 candidates, tüm ürünler checkout'a sahip
- **canonical_drift**: 12 accepted (Vercel alias düzeltilemiyor — auth invalid)
- **codex_offline**: Apr 28'e kadar devre dışı
- **vercel_auth_invalid**: Alias fix için auth gerekiyor
- **$0 revenue**: Satış henüz başlamadı

## Canonical Drift Durumu (12 Ürün — Tümü Accepted)
Vercel auth invalid olduğu için ideal URL'ye alias atanamıyor.
Bu ürünler canlı çalışıyor, sadece URL ideal formda değil.

| # | Slug | Mevcut URL | İdeal URL | Durum |
|---|------|-----------|-----------|-------|
| 1 | jwt-generator | jwt-generator-rho.vercel.app | jwt-generator.vercel.app | accepted |
| 2 | pdf-forge | pdf-forge-five.vercel.app | pdf-forge.vercel.app | accepted |
| 3 | croncraft | quickcron.vercel.app | croncraft.vercel.app | accepted |
| 4 | webhook-tester | webhook-tester-beryl.vercel.app | webhook-tester.vercel.app | accepted |
| 5 | email-validator-pro | email-validator-pro-smoky.vercel.app | email-validator-pro.vercel.app | accepted |
| 6 | diffmaster | diffmaster-coral.vercel.app | diffmaster.vercel.app | accepted |
| 7 | html-entity-encoder | html-entity-encoder-1p2e2xs77...vercel.app | html-entity-encoder.vercel.app | accepted |
| 8 | timestamp-converter | timestamp-converter-pro.vercel.app | timestamp-converter.vercel.app | accepted |
| 9 | chmod-calculator | chmod-calculator-azjwwgvl6...vercel.app | chmod-calculator.vercel.app | accepted |
| 10 | terminal-os | terminal-os-green.vercel.app | terminal-os.vercel.app | accepted |
| 11 | terraink | terraink-flax.vercel.app | terraink.vercel.app | accepted |
| 12 | nginx-config | nginx-config-egj3ho5tp...vercel.app | nginx-config.vercel.app | accepted |

## Açık Issue Kayıtları
- **vercel_auth_invalid** [high/pending] — Alias fix için Vercel CLI auth yenileme gerekiyor
- **codex_offline** [medium/known] — Apr 28'e kadar devre dışı, GLM/Kimi build modunda
- **$0_revenue** [high/ongoing] — Checkout tamam, satış/pazarlama stratejisi eksik

## Not
- STATE.json cycle 1191'e güncellendi.
- Canonical drift önceki raporda 5+7 olarak ayrılmıştı; gerçek durum 12 accepted drift.
- Drift'lerin tümü `v == ideal_vercel_url` ama `canonical_probe_url != v` şeklinde — probe ideal URL'yi hedefliyor, Vercel deploy farklı URL üretmiş.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
