# Sorun Analizi — Cycle 1192 | 2026-04-26 04:51 UTC

## Ana Darboğaz
- **vercel_auth_invalid** — Vercel CLI token expired. Alias fix, yeni deploy ve drift düzeltme bloklu.
- **codex_offline** — Codex account Apr 28'e kadar offline. Major build/deploy yok.

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift (live): 5
- Accepted canonical drift: 7
- Spec-ready backlog: 0

## Canonical Drift Ürünleri (Live)
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
- **vercel_auth_invalid** [high/blocked] — Vercel CLI auth expired. Manuel token refresh gerekli. Bloklayıcı.
- **codex_offline** [medium/scheduled] — Codex account Apr 28'e kadar pasif. Build/deploy pipeline daralması.
- **agent_missing** [low/pending] — Toolsmith agent henüz spawn edilmedi. Şu an bloklayıcı değil.

## Not
- `state_drift` (eski cycle 759 kaydı) temizlendi — STATE.json şu an cycle 1192 ile senkron.
- Checkout rollout tamamlandı (0 gap, 165 polar-ok).
- Gelir $0 — 169 canlı ürün satışa hazır ancak trafik/dönüşüm eksik.
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
