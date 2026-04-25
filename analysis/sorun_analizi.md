# Sorun Analizi — Cycle 1179 | 2026-04-25 21:00 UTC

## Durum Özeti
- **Sistem stabil.** 169/169 ürün sağlıklı. Checkout gap: 0. Canonical drift: 0. Deploy gap: 0.
- Önceki cycle'da (1178) tespit edilen 5 canonical drift ürünü çözüldü (GLM cycle 1172'de override uygulandı).

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0
- Deploy readiness gap: 0
- Deploy/url gap: 0
- Canonical drift: 0
- Spec-ready backlog: 0
- Accepted canonical drift: 7 (jwt-generator, pdf-forge, webhook-tester, email-validator-pro, diffmaster, html-entity-encoder, timestamp-converter)

## Çözülen Sorunlar (Bu Cycle / Son Cycles)
- ✅ canonical_url_drift: 5 → 0 (croncraft, chmod-calculator, terminal-os, terraink, nginx-config — canonical_url_override ile çözüldü)
- ✅ STATE.json inconsistency: 12 eksik live ürün eklendi, 1 duplicate (terraink) temizlendi
- ✅ price mismatch: 4/4 çözüldü (chmod-calculator, hash-generator-pro, http-pulse, og-forge)
- ✅ deploy_gap: 9 → 0 (düzeltildi)

## Açık Issue Kayıtları
- **codex_offline** [medium/known] — Codex her iki hesap da Apr 28'e kadar bloklu. Builder kapasitesi düşük.
- **vercel_auth_invalid** [medium/known] — Vercel auth token geçersiz. Yeni deploy gerektiğinde manuel müdahale gerekir.
- **state_drift** [low/resolved] — Önceki cycle'larda kritikti; STATE.json cycle 1179'da senkronize.

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
