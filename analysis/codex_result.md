# Codex Result — 2026-04-22 11:13 +0300

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE.json`
- `STATE_SUMMARY.json`
- `scripts/product_state_sync.py`
- `scripts/health_check.py`
- `scripts/update_summary.py`
- `tests/test_product_state_sync.py`
- `tests/test_update_summary.py`
- `tests/test_health_check.py`

## Seçilen Darboğaz
- Health probe sonrası bazı live ürünlerde compact `v` alanı ve üst seviye sayaçlar state içinde stale kalıyordu.
- `STATE_SUMMARY.json` doğruydu ama `STATE.json` eski canonical drift/counter snapshot’ını taşıdığı için state-summary senkronu bozuluyordu.

## Yapılan Değişiklikler
- `scripts/product_state_sync.py`
  - `sync_state_snapshot()` eklendi; state içindeki active/spec_ready ürünleri tek adımda normalize edip canonical/public URL snapshot’ını geri üretiyor.
- `scripts/update_summary.py`
  - `STATE.json` artık summary üretimi sırasında normalize ediliyor ve derived sayaçlar geri yazılıyor.
  - `persist_summary()` varsayılan yolunu çağrı anında çözecek şekilde düzelttim; test patch’leri boşa düşmüyor.
- `scripts/health_check.py`
  - Health sonuçlarından sonra state snapshot yeniden senkronize ediliyor; sonra summary yazılıyor.
- `tests/test_product_state_sync.py`
  - Stale compact URL snapshot’ını canonical’a geri çeviren regression testi eklendi.
- `tests/test_update_summary.py`
  - `update_summary.main()` için state+summary persistence regression testi eklendi.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py scripts/health_check.py tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py`
- `python3 -m pytest tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py -q`
- `python3 scripts/update_summary.py`

## Sonuç / Etki
- `STATE.json` ve `STATE_SUMMARY.json` artık aynı canonical snapshot’ı taşıyor.
- Örnek state sayıları senkron: `live_count=82`, `healthy_count=79`, `canonical_url_drift=0`.
- Health pipeline artık alternate health URL’ye düşse bile public canonical state’i kirletmiyor.

## Kalan Blokerler
- Canlı backlog hâlâ aynı: `pdf-forge` timeout, `diffmaster` 401, `git-diff-visualizer` checkout eksikliği.
