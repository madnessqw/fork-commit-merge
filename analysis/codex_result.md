# Codex Result — 2026-04-22

## Okunan Kaynaklar
- `skills/codex_skill.md`
- `analysis/codex_task.md`
- `STATE_SUMMARY.json`
- `analysis/oneri.md`
- `analysis/sorun_analizi.md`
- `analysis/kullanici_gereksinim.md`
- `analysis/cozum_planlama.md`
- `scripts/checkout_metadata.py`
- `scripts/standardize_checkout_fields.py`
- `scripts/create_product.sh`
- `scripts/deploy_product.sh`
- `tests/test_checkout_metadata.py`
- `tests/test_update_summary.py`
- Örnek metadata: `products/html-entities/product.json`, `products/cron-expression-parser/product.json`

## Seçilen Darboğaz
- Spec doğruydu: checkout metadata hâlâ tek yazma sözleşmesine sahip değildi.
- Okuma tarafı legacy alias'ları tolere ediyordu ama yazma tarafı aynı pisliği üretmeye devam ediyordu.
- Sonuç: yeni `product.json` ve deploy sonrası `STATE.json` kayıtları sürekli `checkout_url` + legacy alias çoğaltıyordu; migration helper da bunları gerçekten temizlemiyordu.

## Yapılan Değişiklikler
- `scripts/checkout_metadata.py`
  - `prune_legacy` eklendi.
  - Canonical okuma korunurken yazma tarafı isterse `lemon_checkout_url` ve `lemonsqueezy_checkout_url` alanlarını tamamen silebiliyor.
  - `merge_checkout_metadata()` bu modu destekleyecek şekilde güncellendi; mevcut checkout korunurken legacy alias'lar da temizlenebiliyor.
- `scripts/standardize_checkout_fields.py`
  - Migration helper artık default olarak legacy checkout alias'larını prune ediyor.
  - Gerekirse eski davranış için `--keep-legacy` bayrağı eklendi.
- `scripts/create_product.sh`
  - Yeni ürün metadata şablonu artık canonical sözleşmeyle başlıyor: `checkout_url` + `payment_provider`.
- `scripts/deploy_product.sh`
  - Deploy sonrası hem `product.json` hem `STATE.json` kayıtları canonical write moduna geçirildi.
  - Redeploy merge fix'i korunuyor; checkout kaybı olmadan legacy alanlar da temizleniyor.
- `tests/test_checkout_metadata.py`
  - Legacy prune davranışı ve merge sonrası canonical-only sonuç için regresyon testleri eklendi.
- `tests/test_standardize_checkout_fields.py`
  - Migration helper'ın write modunda alias'ları gerçekten sildiğini doğrulayan test eklendi.

## Geçen Doğrulamalar
- `python3 -m py_compile scripts/checkout_metadata.py scripts/standardize_checkout_fields.py tests/test_checkout_metadata.py tests/test_standardize_checkout_fields.py` ✅
- `bash -n scripts/create_product.sh` ✅
- `bash -n scripts/deploy_product.sh` ✅
- `python3 -m unittest discover -s tests -p 'test_checkout_metadata.py'` ✅
- `python3 -m unittest discover -s tests -p 'test_standardize_checkout_fields.py'` ✅
- `python3 -m unittest discover -s tests -p 'test_update_summary.py'` ✅
- `python3 scripts/standardize_checkout_fields.py` ✅
  - Dry-run: `would_update=142 scanned=148`

## Kalan Blokajlar
- Repo genelinde 142 `product.json` kaydı hâlâ canonical migration bekliyor; bu turda bilerek toplu rewrite yapmadım.
- Manual LemonSqueezy/Vercel aksiyonları hâlâ manual; kodla çözülmüş gibi davranılmadı.
- Workspace kirli; commit sadece bu turda gerçekten dokunduğum dosyalarla sınırlandırılmalı.
