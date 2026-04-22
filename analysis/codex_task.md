# Codex Task — Generated 2026-04-22 12:42 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Health/canonical drift düzeltmesi**

Canlı ürünlerin health alanları ile canonical/vercel URL gerçekliğini senkron tutan scripti güçlendir. Şu an 2 ürün fallback alias ile canlı; manuel Vercel korumasını çözüldü gibi gösterme. Önce mevcut health pipeline'ını oku, sonra yalnız otomasyon tarafını düzelt.

## Canlı State Özeti
- Cycle: 1094
- Live sağlık: 79/91 (%86.8)
- Checkout gap: 0
- Deploy/url gap: 14
- Canonical drift: 2
- Spec-ready count: 11
- Next action: wait_for_vercel_limit_reset

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/LemonSqueezy aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
