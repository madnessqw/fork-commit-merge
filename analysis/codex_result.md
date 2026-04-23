# Codex Result — 2026-04-23 22:40 UTC

## Mod
- EXECUTION
- Slug: `health-canonical-drift`

## Okunan Dosyalar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `CODEBASE_MAP.md`
- `skills/build_checklist.md`
- `scripts/health_check.py`
- `scripts/product_state_sync.py`
- `scripts/update_summary.py`
- `tests/test_health_check.py`
- `tests/test_product_state_sync.py`
- `tests/test_update_summary.py`

## Seçilen Darboğaz
`health_check.py`, sadece `health_probe_url` içinde kalan fallback alias'ı tekrar aday listesine almıyordu. Böyle bir snapshot'ta canonical probe patlarsa canlı fallback alias yanlışlıkla ölü sayılıyordu.

## Yapılan Değişiklik
- `scripts/health_check.py`: probe aday listesine `health_probe_url` eklendi.
- `tests/test_health_check.py`: sadece `health_probe_url` üzerinden bilinen fallback alias'ın canonical probe sonrası tekrar denendiğini doğrulayan regresyon testi eklendi.

## Doğrulama
- `python3 -m py_compile scripts/health_check.py tests/test_health_check.py`
- `pytest tests/test_health_check.py` → 20/20 geçti
- `pytest tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py` → 110/110 geçti
- Secret scan: kaba grep `mask_the_alias` içindeki `sk_` yüzünden false-positive verdi; manuel inceleme + token-şekilli regex ile doğrulandı → temiz
- `sync_state_snapshot()` karşılaştırması: mevcut live snapshot'ta ek drift üretmedi (`changed products = 0`)

## Kalan Blokajlar
- 3 canlı ürün hâlâ gerçekten sağlıksız: `jwt-generator` (500), `diffmaster` (401), `timestamp-converter` (451)
- 4 ürün fallback alias ile canlı: `pdf-forge`, `webhook-tester`, `email-validator-pro`, `html-entity-encoder`
- Bunlar kodla “çözülmüş” gibi işaretlenmedi; manual/canonical taraf hâlâ ayrı iş
