# Codex Result — 2026-04-22 04:40 UTC

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE_SUMMARY.json`
- `STATE.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `CODEBASE_MAP.md`
- `scripts/update_summary.py`
- `scripts/health_check.py`
- `scripts/product_state_sync.py`
- `tests/test_update_summary.py`
- `tests/test_health_check.py`
- `tests/test_product_state_sync.py`
- `tests/test_refresh_codex_context.py`

## Seçilen Darboğaz
- `deploy_missing_or_bad_url` canonical drift’i de saydığı için deploy backlog şişiyordu.
- Bu, alias-only ama sağlıklı ürünleri “deploy/güncelleme bekliyor” gibi gösteriyordu.
- Gerçek kırıklar ile canonical drift aynı sepette olmamalıydı.

## Yapılan Değişiklikler
- `scripts/update_summary.py`
  - `deploy_missing_or_bad_url` hesabı canonical drift’i dışarıda bırakacak şekilde daraltıldı.
  - Canonical drift ayrı gap olarak korunuyor.
- `tests/test_update_summary.py`
  - Canonical drift örneklerinde deploy gap beklentileri `1 -> 0` olarak güncellendi.
- Üretilen artefaktlar yeniden yazıldı:
  - `STATE_SUMMARY.json`
  - `analysis/oneri.md`
  - `analysis/sorun_analizi.md`
  - `analysis/codex_task.md`

## Doğrulamalar
- `python3 -m py_compile scripts/update_summary.py tests/test_update_summary.py`
- `python3 -m unittest discover -s tests -p 'test_update_summary.py'`
- `python3 -m unittest discover -s tests -p 'test_health_check.py'`
- `python3 -m unittest discover -s tests -p 'test_product_state_sync.py'`
- `python3 -m unittest discover -s tests -p 'test_refresh_codex_context.py'`
- `python3 scripts/update_summary.py`
- `python3 scripts/refresh_codex_context.py`
- Secret scan: değişen dosyalarda bariz credential paterni bulunmadı.

## Sonuç / Etki
- `STATE_SUMMARY.json` artık daha dürüst:
  - `live_count=80`
  - `healthy_count=78`
  - `unhealthy_count=2`
  - `deploy_missing_or_bad_url=14`
  - `canonical_url_drift=4`
- Canonical drift ayrı kaldı:
  - `jwt-generator`
  - `webhook-tester`
  - `html-entity-encoder`
  - `timestamp-converter`
- Canlı sağlık açığı hâlâ gerçek iki bozuk ürünle sınırlı:
  - `pdf-forge` — HTTP 500/0
  - `diffmaster` — HTTP 401

## Kalan Blokerlar
- `pdf-forge` hâlâ bozuk.
- `diffmaster` hâlâ Vercel korumasına takılıyor.
- 4 ürün canonical drift durumda; bu kodla raporlandı, manuel Vercel/alias düzeltmesi ayrı iş.
