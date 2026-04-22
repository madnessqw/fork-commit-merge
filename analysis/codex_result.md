# Codex Result — 2026-04-22 01:09 UTC

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE.json`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `scripts/health_check.py`
- `scripts/update_summary.py`
- `scripts/refresh_codex_context.py`
- `tests/test_health_check.py`
- `tests/test_update_summary.py`
- `tests/test_product_state_sync.py`
- `tests/test_refresh_codex_context.py`

## Seçilen Darboğaz
- Asıl bug, health check’in fallback URL 200 verdiğinde ürünü `healthy` sayıp public canonical URL drift’ini maskelemesiydi.
- Bu, canonical/public URL kırıkken alias çalışıyorsa sistemi “iyiymiş” gibi gösteriyordu. Aptalca ama düzeltildi.

## Yapılan Değişiklikler
- `scripts/health_check.py`
  - Primary URL 200 ise `healthy`, fallback URL 200 ise `alternate_healthy` döndürüyor.
  - Healthy branch public `vercel_url`’ı koruyor; fallback probe artık public URL’yi overwrite etmiyor.
  - `last_health_url` kaydediliyor.
  - Konsol çıktısı fallback başarılarını warning olarak işaretliyor.
- `scripts/update_summary.py`
  - Health sayımı artık `health_status == healthy` **ve** `last_health_code == 200` istiyor.
  - Unhealthy gap satırları `probe_url` ile zenginleştirildi.
- `scripts/refresh_codex_context.py`
  - `probe_url` varsa `analysis/sorun_analizi.md` içinde görünür oldu.
- Testler
  - Yeni `tests/test_health_check.py` eklendi.
  - `tests/test_update_summary.py`’e fallback-healthy drift testi eklendi.

## Sonuç / Etki
- Public URL ile health probe URL’sini birbirine karıştıran maskeleme kapandı.
- Current live state’te fallback-healthy örneği çıkmadı; halen sadece `pdf-forge` (HTTP 500) ve `diffmaster` (HTTP 401) unhealthy.
- `STATE_SUMMARY.json` güncellendi ve live özet yine `75/77` healthy kaldı.
- `STATE.json` artık health probe provenance için `last_health_url` taşıyor.

## Doğrulamalar
- `python3 -m py_compile scripts/health_check.py scripts/update_summary.py scripts/refresh_codex_context.py tests/test_health_check.py tests/test_update_summary.py`
- `PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_health_check.py'`
- `PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_update_summary.py'`
- `PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_product_state_sync.py'`
- `PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_refresh_codex_context.py'`
- `python3 scripts/health_check.py` → 86 healthy / 2 unhealthy probeable item, exit 1 beklenen
- `python3 scripts/update_summary.py`
- `python3 scripts/refresh_codex_context.py`

## Kalan Blokajlar
- `pdf-forge` canonical URL `https://pdf-forge.vercel.app` HTTP 500 dönüyor.
- `diffmaster` canonical URL `https://diffmaster.vercel.app` HTTP 401 dönüyor.
- Bunlar kodla “çözüldü” diye yazılmadı; manuel Vercel müdahalesi hâlâ gerekli.
