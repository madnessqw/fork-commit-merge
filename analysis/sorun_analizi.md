# Sorun Analizi — Cycle 1178 | 2026-04-25 20:30 UTC

## Durum Özeti
- **Healthy live:** 169/169 (100%)
- **Canonical healthy:** 169/169
- **Health pending:** 0
- **Fallback healthy:** 0
- **Checkout gap:** 0
- **Deploy readiness gap:** 0
- **Deploy/url gap:** 0
- **Canonical drift:** 0 (TÜMÜ ÇÖZÜLDÜ)
- **Spec-ready backlog:** 0
- **Accepted canonical drift:** 12 (alternate_healthy — fallback URL'ler çalışıyor)

## Çözülen Sorunlar (Önceki Cycle'larda)
- ~~**canonical_url_drift** — 12 üründen sapmıştı; tümü çözüldü~~
  - `croncraft`, `chmod-calculator`, `terminal-os`, `terraink`, `nginx-config` — cycle 1172'de fix
  - `jwt-generator`, `pdf-forge`, `webhook-tester`, `email-validator-pro`, `diffmaster`, `html-entity-encoder`, `timestamp-converter` — alternate_healthy olarak kabul edildi
- ~~**state_drift** [high/çözüldü] — STATE.json cycle 1173'te 12 eksik ürün vardı; cycle 1177'de eklendi, 1 duplicate terraink kaldırıldı~~

## Aktif Darboğazlar
- **vercel_auth_invalid** [medium/beklemede] — Vercel auth token geçersiz; yeni deploy yapılamıyor. Codex offline Apr 28'e kadar. GLM/Kimi build moduna geçebilir.
- **agent_missing** [low/beklemede] — Toolsmith agent henüz spawn edilmedi; capability gap var ancak acil değil

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
