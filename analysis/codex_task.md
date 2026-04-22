# Codex Task — Generated 2026-04-22 14:44 UTC

## MOD: PRODUCTION SAFE INFRA

Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı
stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.

## Aktif Görev
**Canlı sağlık açığını düzelt**

Canlı ürünlerin health alanları ile canonical/vercel URL gerçekliğini senkron tutan scripti güçlendir. Canonical drift yok; gerçek HTTP 404/402 outage'larını doğrula. Önce mevcut health pipeline'ını oku, sonra yalnız otomasyon tarafını düzelt.

## Canlı State Özeti
- Cycle: 1102
- Live sağlık: 89/91 (%97.8)
- Health pending: 0
- Checkout gap: 0
- Deploy/url gap: 4
- Canonical drift: 0
- Spec-ready count: 11
- Next action: Vercel limit reseti bekle (~12 saat) veya manuel dashboard kontrolü yap

## Guardrails
- Dosyaları okumadan edit yapma.
- Production canlı ürün davranışını bozma.
- Manual Vercel/LemonSqueezy aksiyonlarını çözüldü gibi gösterme.
- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.
