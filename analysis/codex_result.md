# Codex Result — 2026-04-22 05:07 UTC

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
- `tests/test_refresh_codex_context.py`

## Seçilen Darboğaz
- Stale state içinde `vercel_url` alias kalırken son başarılı health probe canonical slug URL’yi göstermişse summary bunu yanlışlıkla drift sayabiliyordu.
- Amaç: `health_status` + `last_health_url` + canonical slug gerçekliğini birlikte kullanıp stale alias drift’i sadece gerçekten stale ise saymak.

## Yapılan Değişiklikler
- `scripts/product_state_sync.py`
  - Son başarılı health URL’si için ortak helper eklendi.
  - Live ürünlerde public URL seçimi health evidence ile güçlendirildi.
  - `merge_product_record()` artık `last_health_url` alanını da taşıyabiliyor.
  - `choose_public_vercel_url()` health evidence + canonical slug + manifest/state birleşimini daha sağlam çözüyor.
- `scripts/update_summary.py`
  - Canonical drift hesabı raw `vercel_url` yerine resolved display URL üzerinden yapılıyor.
  - Böylece canonical sağlık kanıtı varsa stale alias drift görünmüyor.
- Testler
  - `tests/test_product_state_sync.py` içine stale alias → canonical health self-heal testi eklendi.
  - `tests/test_update_summary.py` içine stale alias drift’in health kanıtıyla temizlenmesi testi eklendi.

## Doğrulamalar
- `python3 -m py_compile scripts/product_state_sync.py scripts/update_summary.py tests/test_product_state_sync.py tests/test_update_summary.py`
- `python3 -m unittest discover -s tests -p 'test_product_state_sync.py'`
- `python3 -m unittest discover -s tests -p 'test_update_summary.py'`
- `python3 -m unittest discover -s tests -p 'test_health_check.py'`
- `python3 -m unittest discover -s tests -p 'test_refresh_codex_context.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- Secret scan: değişen dosyalarda `sk_`, `pk_`, `ghp_`, `api_key` paterni bulunmadı.

## Sonuç / Etki
- Current live state için gerçek sayılar değişmedi:
  - `healthy_count=78`
  - `live_count=80`
  - `deploy_missing_or_bad_url=14`
  - `canonical_url_drift=4`
- Ama artık stale state senaryosunda:
  - son başarılı health URL canonical ise drift temizleniyor,
  - sadece ideal URL alanı canonical diye alias drift’ini gizlemiyoruz,
  - health pipeline public URL / canonical URL ayrımını daha dürüst taşıyor.

## Kalan Blokerlar
- Current state’teki 4 canonical drift ürünü hâlâ gerçek drift; canonical URL’ler bugünkü canlı probe’a göre kırık.
- `pdf-forge` ve `diffmaster` canlı health olarak hâlâ sorunlu.
