# Codex Result — 2026-04-23 07:05 UTC

## Okunanlar
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

## Ne Değişti
- `scripts/product_state_sync.py` içinde `alternate_healthy` kayıtların başarılı URL seçimi sertleştirildi.
  - Stale canonical URL, fallback alias daha yeni/gerçek görünür URL iken onu artık shadow edemiyor.
  - `_successful_snapshot_url()` alternate healthy durumunda önce görünür fallback URL’yi seçiyor.
- `scripts/update_summary.py` artık sağlıkta başarılı public URL seçimini aynı mantıktan alıyor; summary drift hesabı raw stale canonical değere saplanmıyor.
- Regresyon testleri eklendi:
  - stale `effective_health_url` canonical olsa bile fallback alias görünür kalıyor,
  - summary canonical drift entry fallback alias + effective canonical durumunu doğru sayıyor.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_update_summary.py`
- `python3 -m unittest discover -s tests -p 'test_product_state_sync.py'`
- `python3 -m unittest discover -s tests -p 'test_update_summary.py'`
- Secret scan: değişen dosyalarda `sk_`, `pk_`, `ghp_`, `api_key` bulunmadı.

## Kalan Blokajlar
- Canlı portföyde hâlâ 3 gerçek outage var:
  - `jwt-generator` → HTTP 500
  - `diffmaster` → HTTP 401
  - `timestamp-converter` → HTTP 451
- 4 ürün fallback alias ile canlı; bu durum artık canonical healthy diye maskelenmiyor.
