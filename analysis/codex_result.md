# Codex Result — 2026-04-23 17:15 +0300

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
- Live ürünlerin canonical URL'ye yanlış erken normalize edilmesini engelleyen dar bir fallback-koruma dalı eklendi.
- Bu dal sadece live kayıt public URL'si zaten canonical olduğunda, visible bir preview/fallback alias varken ve canonical probe snapshot henüz yokken çalışıyor.
- Böylece fallback alias 200 ile ayakta olan kayıtlar canonical drift olarak görünür kalıyor; canonical promotion senaryoları ve predeploy canonicalizasyonu bozulmuyor.
- `tests/test_product_state_sync.py` ve `tests/test_update_summary.py` içine bu davranış için regresyon testleri eklendi.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_update_summary.py`
- `python3 -m pytest -q tests/test_product_state_sync.py tests/test_update_summary.py`
- Secret scan: değişen dosyalarda `sk_`, `pk_`, `ghp_`, `api_key` kalıbı bulunmadı.

## Kalan Blokajlar
- 3 canlı ürün hâlâ gerçekten sağlıksız: `jwt-generator`, `diffmaster`, `timestamp-converter`.
- 4 fallback alias canlı kalmaya devam ediyor; summary onları canonical drift olarak ayrı gösteriyor.
