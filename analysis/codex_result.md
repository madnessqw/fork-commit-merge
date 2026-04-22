# Codex Result — 2026-04-22 18:39 +03

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
- `scripts/product_state_sync.py`
  - Stale bir failure kaydı, canlı 200 fallback ile eşleştiğinde artık `alternate_healthy` durumu ezilmiyor.
  - Final 200 branch’i raw kaydı tekrar okuyup fallback durumunu bozmak yerine normalize edilmiş durumu koruyor.
  - Bu yüzden gerçek reachable fallback URL artık canonical alias’ın arkasına gizlenmiyor.
- `tests/test_product_state_sync.py`
  - `error_404 + 200 fallback` senaryosu için regresyon testi eklendi.
  - Beklenti: `health_status=alternate_healthy`, `vercel_url=v=last_health_url=fallback URL`.
- `tests/test_update_summary.py`
  - Aynı stale failure + başarılı fallback senaryosu summary seviyesinde kilitlendi.
  - Beklenti: `healthy_count=1`, `canonical_url_drift=1`, public `v` fallback URL.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_update_summary.py tests/test_health_check.py`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Secret scan: değişen dosyalarda `sk_`, `pk_`, `ghp_`, `api_key` eşleşmesi yok
- `git diff --check`

## Kalan Blokerler
- `html-entity-encoder` için gerçek canlı outage hâlâ var: HTTP `402`.
- Kod artık bu tür reachable fallback kayıtlarını yanlışlıkla `healthy` diye gizlemiyor; ama 402’yi çözmek için hâlâ manuel Vercel tarafı işi gerekiyor.
