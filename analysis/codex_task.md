# Codex Task — Generated 2026-04-24 15:04 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Ready-for-payment health düzeltmesi**

Live sağlık metriğini şişirmeden ready_for_payment ürünlerin health sorunlarını da görünür tut. Bu ürünleri ayrı takip et; live outage diye sayma ama 404/401 gibi sonuçları context'e kaybetme.

## Canlı State Özeti
- Cycle: 1113
- Live sağlık: 91/91 (%100.0)
- Canonical healthy: 84/91 (%92.3)
- Health pending: 0
- Fallback healthy: 7
- Checkout gap: 0
- Deploy readiness gap: 15
- Deploy/url gap: 2
- Canonical drift: 7
- Canonical drift slugs: `jwt-generator`, `pdf-forge`, `webhook-tester`, `email-validator-pro`, `diffmaster`, `html-entity-encoder`, `timestamp-converter`
- Fallback healthy slugs: `jwt-generator`, `pdf-forge`, `webhook-tester`, `email-validator-pro`, `diffmaster`, `html-entity-encoder`, `timestamp-converter`
- Spec-ready count: 2
- Next action: 7 canonical URL drift'ini düzelt; fallback alias'ı ezme

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/ödeme-provider aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
