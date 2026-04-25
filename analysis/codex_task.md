# Codex Task — Generated 2026-04-25 07:35 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Canonical URL drift düzeltmesi**

Live ürünlerin public URL'si ile ideal canonical URL'sini aynı tut. Önce health pipeline'ını ve summary sync'ini doğrula; alias/redirect farkını manuel Vercel fix gibi saklamaya çalışma.

## Canlı State Özeti
- Cycle: 1156
- Live sağlık: 168/168 (%100.0)
- Canonical healthy: 168/168 (%100.0)
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 4
- Canonical drift slugs: `croncraft`, `chmod-calculator`, `terminal-os`, `terraink`
- Accepted canonical drift: 7
- Accepted canonical drift slugs: `jwt-generator`, `pdf-forge`, `webhook-tester`, `email-validator-pro`, `diffmaster`, `html-entity-encoder`, `timestamp-converter`
- Fallback healthy slugs: `croncraft`, `chmod-calculator`, `terminal-os`, `terraink`
- Spec-ready count: 0
- Next action: 4 canonical URL drift'ini düzelt; fallback alias'ı ezme

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/ödeme-provider aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
