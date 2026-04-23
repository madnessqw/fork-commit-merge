# Codex Result — 2026-04-23 02:14 UTC

## Ne okundu
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `CODEBASE_MAP.md`
- `skills/build_checklist.md`
- `scripts/health_check.py`, `scripts/product_state_sync.py`
- İlgili regression testleri: `tests/test_health_check.py`, `tests/test_product_state_sync.py`, `tests/test_update_summary.py`

## Ne değişti
- Health pipeline artık canonical probe kanıtını ayrı `canonical_probe_url` alanında saklıyor.
- Fallback alias başarılı olsa bile canonical probe URL ile fallback probe URL birbirine karışmıyor.
- `product_state_sync` canonical probe kanıtı yoksa eski fallback kaydını canonical başarı gibi yorumlamıyor; kanıt varsa redirected-preview drift görünür kalıyor.
- Regression testleri eklendi/güncellendi.

## Doğrulamalar
- `python3 -m py_compile scripts/health_check.py scripts/product_state_sync.py` ✅
- `python3 -m unittest discover -s tests -p 'test_*.py'` ✅ — 101 test
- `python3 scripts/update_summary.py` ✅ — live=88, healthy=80, fallback_healthy=3, canonical_drift=3
- Secret scan changed files ✅

## Kalan blokajlar
- 8 live ürün hâlâ sağlıksız; 3 ürün fallback alias ile ayakta.
- `html-entity-encoder` canonical URL hâlâ Vercel tarafında manuel kontrol gerektiriyor; kod bunu çözülmüş göstermedi.
