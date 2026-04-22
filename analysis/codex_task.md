# Codex Task — Generated 2026-04-22 22:39 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Health/canonical drift düzeltmesi**

Canlı ürünlerin health alanları ile canonical/vercel URL gerçekliğini senkron tutan scripti güçlendir. Şu an 3 ürün fallback alias ile canlı; manuel Vercel korumasını çözüldü gibi gösterme. Önce mevcut health pipeline'ını oku, sonra yalnız otomasyon tarafını düzelt.

## Canlı State Özeti
- Cycle: 1108
- Live sağlık: 84/88 (%95.5)
- Health pending: 0
- Fallback healthy: 3
- Checkout gap: 0
- Deploy readiness gap: 20
- Deploy/url gap: 21
- Canonical drift: 3
- Spec-ready count: 26
- Next action: html-entity-encoder Vercel Dashboard manuel kontrol

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/LemonSqueezy aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
