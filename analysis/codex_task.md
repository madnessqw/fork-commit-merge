# Codex Task — Generated 2026-04-24 09:06 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Health/canonical drift düzeltmesi**

Canlı ürünlerin health alanları ile canonical/vercel URL gerçekliğini senkron tutan scripti güçlendir. Şu an 4 ürün fallback alias ile canlı; manuel Vercel korumasını çözüldü gibi gösterme. Önce mevcut health pipeline'ını oku, sonra yalnız otomasyon tarafını düzelt.

## Canlı State Özeti
- Cycle: 1110
- Live sağlık: 88/91 (%96.7)
- Canonical healthy: 84/91 (%92.3)
- Health pending: 0
- Fallback healthy: 4
- Checkout gap: 0
- Deploy readiness gap: 15
- Deploy/url gap: 5
- Canonical drift: 4
- Canonical drift slugs: `pdf-forge`, `webhook-tester`, `email-validator-pro`, `html-entity-encoder`
- Fallback healthy slugs: `pdf-forge`, `webhook-tester`, `email-validator-pro`, `html-entity-encoder`
- Spec-ready count: 2
- Next action: 3 canlı ürünü düzelt; 4 fallback alias'ı görünür tut

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/ödeme-provider aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
