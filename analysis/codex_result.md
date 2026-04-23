# Codex Result — 2026-04-23 15:05 +03

## 2026-04-23 15:05 +03 — Health/canonical duplicate-snapshot dedupe

### Okunanlar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
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

### Ne Değişti
- `scripts/product_state_sync.py` artık duplicate slug kaydında kör kalite skoruyla seçmiyor; önce en yeni health snapshot'ı, sonra görünür fallback alias'ı tercih ediyor.
- `merge_preferred_record()` eklendi: daha yeni fallback snapshot seçilince checkout gibi stabil metadata kaybolmasın diye eksik alanları eski kayıttan backfill ediyor.
- `scripts/update_summary.py` aynı preference key'i kullanıyor; summary dedupe artık daha yeni fallback snapshot'ı canonical çöpüne ezdirmiyor.
- Regression testler eklendi: duplicate canonical + newer fallback snapshot senaryosunda public URL alias kalıyor ve checkout metadata korunuyor.

### Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_update_summary.py scripts/health_check.py scripts/refresh_codex_context.py`
- `PYTHONPATH=. python3 -m pytest tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py -q`
- Sonuç: **94 passed**
- Secret scan temiz: değişen dosyalarda `sk_` / `pk_` / `ghp_` / `api_key` izi yok.

### Kalan Blokajlar
- Canlı portföyde hâlâ 3 gerçek health outage var: `jwt-generator`, `diffmaster`, `timestamp-converter`.
- 4 fallback alias canlı; bu değişiklik onların daha yeni snapshot varken canonical duplicate tarafından ezilmesini önlüyor.

## Okunanlar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
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

## Ne Değişti
- `scripts/product_state_sync.py` güçlendirildi: health snapshot artık explicit canonical URL ile preview alias çakıştığında canonical probe başarısızsa fallback alias'ı görünür tutuyor.
- `_successful_snapshot_url()` ve `successful_health_url()` artık canonical snapshot eskimişse preview alias'ı tercih ediyor; bu, `STATE.json` içindeki health alanlarının canonical gerçeği ezmesini engelliyor.
- `normalize_health_snapshot()` artık canonical başarı yoksa ama fallback alias 200 veriyorsa ürünü `alternate_healthy` olarak koruyor; canonical failure detaylarını da kaybetmiyor.
- `tests/test_product_state_sync.py` ve `tests/test_update_summary.py` içine regression eklendi/güncellendi: canonical health URL eskiyken fallback alias görünür kalıyor ve summary drift bunu doğru sayıyor.

## Doğrulamalar
- `PYTHONPATH=. python3 -m py_compile scripts/product_state_sync.py tests/test_product_state_sync.py tests/test_update_summary.py`
- `PYTHONPATH=. python3 -m pytest tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py -q`
- Sonuç: **92 passed**
- Secret scan temiz: değişen dosyalarda gizli anahtar izi yok.

## Kalan Blokajlar
- 3 canlı ürün hâlâ gerçekten sağlıksız: `jwt-generator`, `diffmaster`, `timestamp-converter`.
- 4 fallback alias canlı ve görünür kalmalı; bu kod artık onları canonical cache artığından ezmiyor.
