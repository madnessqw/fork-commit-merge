# Codex Result — 2026-04-22 08:39 +03

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
- `scripts/audit_portfolio_health.py`
- `tests/test_product_state_sync.py`
- `tests/test_update_summary.py`
- `tests/test_health_check.py`

## Seçilen Darboğaz
- Health pipeline'da `alternate_healthy` sonuçları pratikte sağlıklı sayılması gerekirken console/özet tarafında hâlâ sert sağlık dışı gibi görünüyordu.
- Ayrıca eski doküman ve otomasyonların referans verdiği `scripts/audit_portfolio_health.py` entrypoint'i repo içinde yoktu.

## Yapılan Değişiklikler
- `scripts/health_check.py`
  - Ortak yardımcı `is_synced_health_result()` eklendi.
  - `alternate_healthy` sonuçları artık healthy bucket'a giriyor.
  - Canonical drift fallback'leri ayrı uyarı olarak gösteriliyor; sağlık yüzdesi ve özet sayılar artık bununla tutarlı.
- `scripts/audit_portfolio_health.py`
  - Geriye dönük uyumluluk için yeni wrapper eklendi.
  - Eski isim artık gerçek health pipeline'a delege ediyor.
- `tests/test_health_check.py`
  - `alternate_healthy`'nin sağlıklı bucket'a dahil olduğunu doğrulayan test eklendi.

## Doğrulamalar
- `python3 -m py_compile scripts/health_check.py scripts/audit_portfolio_health.py tests/test_health_check.py`
- `python3 -m unittest discover -s tests -p 'test_health_check.py'`
- `python3 -m unittest discover -s tests -p 'test_update_summary.py'`
- `python3 -m unittest discover -s tests -p 'test_product_state_sync.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- Secret scan: değişen dosyalarda `sk_`, `pk_`, `ghp_`, `api_key` paterni bulunmadı.

## Sonuç / Etki
- Health check artık fallback URL ile canlı kalan ürünü gereksiz yere "unhealthy" gibi göstermiyor.
- Canonical drift hâlâ ayrı uyarı olarak görünür kalıyor; yani sorun gizlenmiyor, sadece yanlış sınıflandırma düzeltiliyor.
- Eski `audit_portfolio_health.py` yolu artık boşa düşmüyor.

## Kalan Blokerlar
- Live state'teki canonical drift ürünleri hâlâ gerçek drift olabilir; bu run yalnızca sınıflandırma ve giriş noktası uyumluluğunu düzeltti.
- `pdf-forge` ve `diffmaster` gibi gerçek broken canlılar ayrı problem olarak kalıyor.
