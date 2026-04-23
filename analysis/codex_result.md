# Codex Result — 2026-04-23

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
- `scripts/product_state_sync.py` içinde sağlık/public URL seçimi sıkılaştırıldı.
- Pre-deploy kaynaklardan gelen manifest preview alias’ları, gerçek canonical kanıt yoksa canonical sluga geri çekiliyor.
- Canlı ürünlerde fallback alias görünürlüğü korunuyor; ama explicit canonical sağlık URL’si varsa canonical promotu ezilmiyor.
- `choose_public_vercel_url()` için healthy/no-explicit-health case’inde state/deployment alias görünürlüğü korundu.
- Regresyon testi eklendi: healthy state alias, explicit health URL olmadan fallback display olarak kalıyor.

## Doğrulamalar
- `PYTHONPATH=. pytest -q tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py`
- `python3 -m py_compile scripts/product_state_sync.py tests/test_product_state_sync.py`
- Secret scan: değişen dosyalarda `sk_`, `pk_`, `ghp_`, `api_key` bulunmadı.

## Kalan Blokajlar
- Canlı state tarafında hâlâ güncel outage’lar var:
  - `jwt-generator` → HTTP 500
  - `diffmaster` → HTTP 401
  - `timestamp-converter` → HTTP 451
- Bu task kod tarafında kapandı; canlı prod düzeltmeleri ayrı iş.
