# Codex Result — 2026-04-22 09:11 +03

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE_SUMMARY.json`
- `STATE.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `CODEBASE_MAP.md`
- `scripts/product_state_sync.py`
- `scripts/update_summary.py`
- `scripts/health_check.py`
- `tests/test_product_state_sync.py`
- `tests/test_update_summary.py`
- `tests/test_health_check.py`

## Seçilen Darboğaz
- Canlı health snapshot’lar stale kalıyordu: non-200 probe sonuçlarında `health_status` bazen hâlâ `healthy` görünüyordu.
- Unhealthy gap çıktıları da public/resolved URL yerine raw alias alanını basıyordu.

## Yapılan Değişiklikler
- `scripts/product_state_sync.py`
  - `normalize_health_snapshot()` eklendi.
  - Live / ready-for-payment ürünlerde `last_health_code` int’e çevriliyor.
  - `401 / 404 / 0` gibi failure kodları sırasıyla `unauthorized / not_found / timeout` olarak normalize ediliyor.
  - Manifest yokken de health normalizasyonu ve public URL çözümü çalışıyor; eski healthy label artık failure code üstüne yazamıyor.
- `scripts/update_summary.py`
  - `gaps.unhealthy_live[].url` artık `display_vercel_url()` kullanıyor.
  - Böylece gap listesi raw alias değil, public/resolved URL ile hizalanıyor.
- `tests/test_product_state_sync.py`
  - Stale healthy health_status’ın failure code ile normalize edildiğini doğrulayan test eklendi.
- `tests/test_update_summary.py`
  - Unhealthy gap satırının resolved URL + normalize health_status ile çıktığını doğrulayan test eklendi.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_update_summary.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/update_summary.py`
- Secret scan: değişen kod dosyalarında gizli anahtar izi yok.

## Sonuç / Etki
- Live health state artık non-200 probe’larda sahte `healthy` etiketi taşımıyor.
- Summary ve gap raporu public URL gerçeğiyle hizalandı.
- `STATE_SUMMARY.json` yerelde yeniden üretildi; güncel snapshot `80 live / 78 healthy / 2 unhealthy` gösteriyor.

## Kalan Blokerler
- `pdf-forge` timeout ve `diffmaster` 401 gerçek canlı problemler; otomasyon artık bunları doğru raporluyor ama çözmüyor.
- Manuel Vercel/deploy müdahalesi hâlâ insan gerektiriyor.
