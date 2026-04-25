# GLM Code Result
**Tarih:** 2026-04-25 14:47 | **Cycle:** 1170

## Ne Yapıldı
drift_severity_breakdown() fonksiyonu summary_visibility.py'ye eklendi. Health dashboard'da canonical drift ürünlerinin severity'leri (not_found, error_500, deployment_disabled, vs.) artık görünür. Compact, full ve JSON çıktılarında severity breakdown mevcut.

## Değişen Dosyalar
- `scripts/summary_visibility.py` — drift_severity_breakdown() fonksiyonu eklendi
- `scripts/health_dashboard.py` — severity breakdown compact/full/JSON render'larda gösteriliyor
- `tests/test_summary_visibility.py` — 5 yeni test (drift severity)
- `tests/test_health_dashboard.py` — 4 yeni test (dashboard severity display)

## Test Sonucu
84 passed (tüm testler geçti)

## Commit
ae16ab6 — glm: 20260425-1447 — drift_severity_breakdown() in summary_visibility, health dashboard severity display, 9 new tests
