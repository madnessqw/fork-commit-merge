# Codex Result — 2026-04-22 23:04 UTC

## Okunan Dosyalar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `CODEBASE_MAP.md`
- `scripts/product_state_sync.py`
- `scripts/update_summary.py`
- `tests/test_product_state_sync.py`
- `tests/test_update_summary.py`
- `tests/test_refresh_codex_context.py`

## Yapılan Değişiklik
- `scripts/product_state_sync.py` içinde manifest-backed kayıtlar için health normalizasyonundan **sonra** `vercel_url` tekrar çözümleniyor.
- Böylece canonical probe patlakken fallback alias 200 dönüyorsa kayıt `alternate_healthy` kalırken public `vercel_url` da gerçekten çalışan alias'a dönüyor.
- Önceki davranış dümdüz yalandı: manifest canonical URL'yi geri basıyor, state ise `alternate_healthy` yazıp ölü canonical adresi göstermeye devam ediyordu.
- Regression testi eklendi: `tests/test_product_state_sync.py::test_manifest_backed_fallback_keeps_reachable_alias_as_public_url`.

## Doğrulama
- `python3 -m py_compile scripts/product_state_sync.py tests/test_product_state_sync.py tests/test_update_summary.py tests/test_refresh_codex_context.py`
- `python3 -m unittest discover -s tests -p 'test_product_state_sync.py'`
- `python3 -m unittest discover -s tests -p 'test_update_summary.py'`
- `python3 -m unittest discover -s tests -p 'test_refresh_codex_context.py'`
- `python3 scripts/update_summary.py`
- `python3 scripts/refresh_codex_context.py`
- Secret scan: değişen dosyalarda token-shaped regex taraması geçti.

## Sonuç
- Fallback alias ile yaşayan canlı ürünlerde state artık health alanı ile public URL konusunda birbiriyle çelişmiyor.
- Refresh sonrası özet hâlâ dürüst: live sağlık `84/88`, fallback healthy `3`, canonical drift `3`, needs fix `7`.

## Kalan Blokajlar
- `pdf-forge`, `webhook-tester`, `email-validator-pro` hâlâ gerçek canonical drift; kod bunları çözülmüş gibi göstermiyor.
- `jwt-generator` (500), `diffmaster` (401), `html-entity-encoder` (402), `timestamp-converter` (451) hâlâ canlı sorun.
- `html-entity-encoder` için manuel Vercel dashboard kontrolü hâlâ sıradaki aksiyon.
