# Codex Result — 2026-04-22 02:44 UTC

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE.json`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `scripts/update_summary.py`
- `scripts/health_check.py`
- `scripts/product_state_sync.py`
- `tests/test_product_state_sync.py`
- `tests/test_health_check.py`
- `tests/test_update_summary.py`

## Seçilen Darboğaz
- Live ürünlerin bir kısmı canonical slug URL yerine preview alias üzerinde sağlıklı görünüyordu.
- Bu, `healthy_count`'ı şişiriyordu; canonical drift ayrı raporlansa da sağlık sayacı gerçeği tam yansıtmıyordu.

## Yapılan Değişiklikler
- `scripts/update_summary.py`
  - `is_healthy()` canonical drift-aware hale getirildi.
  - Live ürün artık sadece `health_status=healthy` ve `200` döndüğü için değil, public URL canonical reality ile de uyumluysa sağlıklı sayılıyor.
- `scripts/health_check.py`
  - `needs_fix_count` çift sayımı kaldırıldı; canonical drift artık health sayısına dahil olduğu için fix sayacı `unhealthy_count` ile uyumlu.
- `tests/test_update_summary.py`
  - Canonical drift'li live ürünlerin sağlıklı sayılmaması için regresyon testleri güncellendi.
- Üretilen dosyalar yenilendi:
  - `STATE_SUMMARY.json`
  - `STATE.json`
  - `analysis/oneri.md`
  - `analysis/sorun_analizi.md`
  - `analysis/codex_task.md`

## Doğrulamalar
- `python3 -m py_compile scripts/update_summary.py scripts/health_check.py tests/test_update_summary.py`
- `PYTHONPATH=. python3 -m pytest -q tests/test_product_state_sync.py tests/test_health_check.py tests/test_update_summary.py`
- `python3 scripts/health_check.py`
- `python3 scripts/update_summary.py`
- `python3 scripts/refresh_codex_context.py`
- Sonuç: `21 passed`

## Sonuç / Etki
- `STATE_SUMMARY.json` artık canonical drift'i sağlık sayısına yediriyor.
- Güncel özet: `72/78` healthy, `6` unhealthy, `4` canonical drift.
- Canonical drift ürünleri şu an: `jwt-generator`, `webhook-tester`, `html-entity-encoder`, `timestamp-converter`.
- `pdf-forge` ve `diffmaster` hâlâ gerçek canlı outage / auth problemi olarak kalıyor.

## Kalan Blokajlar
- `pdf-forge` HTTP 500
- `diffmaster` HTTP 401
- Bunlar kodla “çözüldü” diye yazılmadı; manuel/Vercel tarafı ayrı.
