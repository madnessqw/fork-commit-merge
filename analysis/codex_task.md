# Codex Task — Generated 2026-04-22 08:35 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Health/canonical drift düzeltmesi**

Canlı ürünlerin health alanları ile canonical/vercel URL gerçekliğini senkron tutan scripti güçlendir. Önce mevcut health pipeline'ını oku, sonra yalnız otomasyon tarafını düzelt; manuel Vercel korumasını çözüldü gibi gösterme.

## Canlı State Özeti
- Cycle: 1088
- Live sağlık: 79/81 (%97.5)
- Checkout gap: 0
- Deploy/url gap: 7
- Canonical drift: 0
- Spec-ready count: 14
- Next action: wait_for_vercel_limit_reset

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/LemonSqueezy aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
