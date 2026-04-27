# Codex Task — Generated 2026-04-27 12:00 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Ready-for-payment health düzeltmesi**

Live sağlık metriğini şişirmeden ready_for_payment ürünlerin health sorunlarını da görünür tut. Bu ürünleri ayrı takip et; live outage diye sayma ama 404/401 gibi sonuçları context'e kaybetme.

## Canlı State Özeti
- Cycle: 237
- Live sağlık: 184/184 (%100.0)
- Canonical healthy: 170/184 (%92.4)
- Health pending: 0
- Fallback healthy: 14
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 14
- Canonical drift slugs: `croncraft`, `diffmaster`, `html-entity-encoder`, `jwt-generator`, `nginx-config`, `pdf-forge`, `webhook-tester`, `chmod-calculator`
- Fallback healthy slugs: `croncraft`, `diffmaster`, `html-entity-encoder`, `jwt-generator`, `nginx-config`, `pdf-forge`, `webhook-tester`, `chmod-calculator`, ...
- Spec-ready count: 0
- Next action: 14 canonical URL drift'ini düzelt; fallback alias'ı ezme

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/ödeme-provider aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
