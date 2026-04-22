# Codex Result — 2026-04-22 11:41 +0300

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE.json`
- `STATE_SUMMARY.json`
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
- No-manifest path'te public URL çözümü, başarılı health probe kanıtını yeterince sıkı kullanmıyordu. Bu yüzden canonical health URL geri kazanılırken bile stale alias davranışı riskli kalıyordu.

## Yapılan Değişiklikler
- `scripts/product_state_sync.py`
  - `resolved_public_vercel_url()` artık public URL kararını tek bir yol üzerinden veriyor ve yalnızca başarılı health probe URL'sini canonical geri kazanımı için kullanıyor.
  - `ideal_vercel_url` tek başına public URL'i zorlamıyor; böylece ideal hedef ile fiili public URL drift'i saklanmıyor.
- `tests/test_product_state_sync.py`
  - Manifest olmayan bir kayıtta başarılı canonical health URL'nin public URL'i canonical'a çektiğini doğrulayan regression testi eklendi.
- `tests/test_update_summary.py`
  - `build_summary()` için aynı no-manifest canonical-health regression testi eklendi.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py scripts/health_check.py tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py`
- `python3 -m pytest tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py -q` → `37 passed`

## Sonuç / Etki
- Canonical health kanıtı varsa alias artık public state'i kirletmiyor.
- Sadece ideal hedef URL taşıyan kayıtlar yanlışlıkla düzelmiş sayılmıyor.
- `STATE_SUMMARY.json` current snapshot ile uyumlu kaldı; core counts değişmedi.

## Kalan Blokerler
- Vercel limit reseti bekleniyor.
- `diffmaster` ve `pdf-forge` hâlâ ürün/vercel kaynaklı manuel veya kaynak-düzeyi iş gerektiriyor.
