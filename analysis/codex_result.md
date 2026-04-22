# Codex Result — 2026-04-22 05:06 Europe/Istanbul

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE.json`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `scripts/product_state_sync.py`
- `scripts/health_check.py`
- `scripts/update_summary.py`
- `tests/test_product_state_sync.py`
- `tests/test_health_check.py`
- `tests/test_update_summary.py`

## Seçilen Darboğaz
- Health check ve summary, sadece `ideal_vercel_url` olan ürünlerde değil, slug’dan türeyen canonical URL’si preview alias’ın arkasına saklanan canlı ürünlerde de drift’i görmeli.
- Mevcut akış preview alias’ı “iyiymiş” gibi gösterebiliyordu; bu yüzden canonical gerçeklik ile state kaydı ayrı düşüyordu.

## Yapılan Değişiklikler
- `scripts/product_state_sync.py`
  - `canonical_target_vercel_url()` eklendi: canlı / ready_for_payment ürünlerde canonical hedefi slug’dan türetiyor, ideal URL’yi sadece slug yoksa fallback olarak kullanıyor.
  - `display_vercel_url()` eklendi: canlı ürünlerde URL boşsa canonical hedefi gösteriyor.
  - `health_check_url()` artık canonical hedefi önce probe ediyor.
- `scripts/update_summary.py`
  - `canonical_url_drift_entry()` slug-tabanlı canonical hedefi kullanacak şekilde güncellendi.
  - `compact_product()` canlı ürünlerde boş URL yerine canonical display URL gösterecek şekilde güncellendi.
  - `products_without_url` hesabı canonical hedefi olan canlı ürünleri yanlışlıkla missing saymayacak şekilde düzeltildi.
- Testler
  - `tests/test_product_state_sync.py`: canonical-first health probe ve live URL’siz canonical fallback regresyonları eklendi.
  - `tests/test_update_summary.py`: slug bazlı canonical drift ve live URL’siz display regression’ları eklendi.
- `STATE_SUMMARY.json`
  - Yeni kurala göre yeniden üretildi; artık slug canonical drift’i görünür durumda.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/health_check.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_health_check.py tests/test_update_summary.py`
- `PYTHONPATH=. python3 -m pytest -q tests/test_product_state_sync.py tests/test_health_check.py tests/test_update_summary.py`
- `python3 scripts/update_summary.py`
- Sonuç: `21 passed`

## Sonuç / Etki
- Canlı ürünlerde canonical URL, preview alias’ın arkasına saklanmıyor.
- Summary artık live preview alias’ları canonical drift olarak işaretliyor.
- Güncel `STATE_SUMMARY.json` canonical drift sayısı: 8.

## Kalan Blokajlar
- `pdf-forge` ve `diffmaster` hâlâ unhealthy.
- Bu ikisi kodla “çözüldü” diye yazılmadı; manuel/Vercel tarafı hâlâ ayrı mesele.
