# Sorun Analizi — Cycle 1197 | 2026-04-26 06:52 UTC

## Ana Darboğazlar
1. **codex_offline** [critical/blocker] — Her iki Codex hesabı da usage limitinde. Account 1 blocked until ~Apr 28 21:35 UTC, Account 2 da limit aşımı. Codex 35dk loop'u etkisiz.
2. **vercel_auth_invalid** [high/blocker] — Vercel token expired. Canonical URL alias fix'leri, yeni deploy ve redeploy işlemleri bloklanmış durumda.
3. **canonical_url_drift** [medium/pending] — 5 live ürün canonical URL'den sapmış; Vercel auth düzeltilince alias atanacak.

## Summary'den Gelen Gerçekler
- Healthy live: 169/169
- Canonical healthy: 169/169
- Health pending: 0
- Fallback healthy: 0
- Checkout gap: 0 (plan+sync ile doğrulandı, 0 candidates)
- Deploy readiness gap: 0
- Canonical drift live: 5
- Accepted canonical drift: 7
- Spec-ready backlog: 4 (json-schema-generator, regex-library-pro, html-validator-pro, dns-lookup-pro)
- Orphan product dirs (no product.json): 117

## Canonical Drift Ürünleri (Live)
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app
- `chmod-calculator` — current=https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app
- `terminal-os` — current=https://terminal-os-green.vercel.app ideal=https://terminal-os.vercel.app
- `terraink` — current=https://terraink-flax.vercel.app ideal=https://terraink.vercel.app
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app

## Kabul Edilmiş Canonical Drift
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `email-validator-pro` — current=https://email-validator-pro-smoky.vercel.app ideal=https://email-validator-pro.vercel.app
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app

## STATE Sync Sorunları
- **spec_ready_count mismatch** — STATE.json `spec_ready_count: 0` ama disk üzerinde 4 spec_ready product var. STATE sync scripti bu alanı güncellemiyor olabilir.
- **cycle lag** — STATE.json `cycle: 1194` ama health_trend ve commit geçmişi 1196'ya kadar ilerlemiş. STATE sync aralığı veya scripti kontrol edilmeli.

## Açık Issue Kayıtları
- **codex_offline** [critical] — Her iki hesap usage limit. Apr 28'e kadar bekleniyor. Pro upgrade insan kararı.
- **vercel_auth_invalid** [high] — Token invalid. Vercel CLI login gerekiyor (device code: MJFC-THWB, URL: https://vercel.com/oauth/device?user_code=MJFC-THWB).
- **orphan_dirs** [medium] — 117 product dizini product.json içermiyor. GLM tarafından tespit edildi (önceki rapor 98, güncel 117). Cleanup planı var (orphan_cleanup_planner.py) ama henüz execute edilmedi.
- **researcher_needed** [low/stale] — Signal hâlâ .signals/ altında duruyor, researcher çıktısı yok. Stale signal.

## Not
- Bu dosya live `STATE.json` → disk taraması ve log analizinden üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
- Codex döndüğünde (Apr 28+) canonical drift fix + orphan cleanup execute edilecek.
