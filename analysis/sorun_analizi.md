# Sorun Analizi — Cycle 1189 | 2026-04-26 02:27 UTC

## Ana Darboğaz
- **Codex offline** — Both accounts usage limit hit, Apr 28'e kadar offline.
- **Vercel auth invalid** — Yeni deploy ve alias fix yapılamıyor.

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 0
- Spec-ready backlog: 0

## Canonical Drift Ürünleri
- Yok (0 drift — önceki cycle'larda düzeltilmiş veya kabul edilmiş).

## Kabul Edilmiş Canonical Drift
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `email-validator-pro` — current=https://email-validator-pro-smoky.vercel.app ideal=https://email-validator-pro.vercel.app
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app

## Açık Issue Kayıtları
- **codex_offline** [high/in_progress] — Both accounts usage limit, Apr 28'e kadar bekleniyor.
- **vercel_auth_invalid** [high/blocked] — Manuel token refresh gerekli.
- **zero_revenue** [medium/ongoing] — 169 live ürün, aktif checkout, ama satış yok.

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
