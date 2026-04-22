# Kullanıcı Gereksinim Analizi — 2026-04-20 09:50 UTC

## Manuel Yapılması Gerekenler (Otomate Edilemeyen)
- **LemonSqueezy identity verification** — Gökhan'ın LemonSqueezy dashboard'da kimlik belgesi yükleyerek identity verification'ı tamamlaması gerekiyor. Bu olmadan:
  - 65 ürün checkout URL alamaz
  - Hiçbir ödeme alınamaz
  - Toplam potansiyel gelir kaybı: 43 live ürün × ortalama $14 = ~$602/ay
- **Vercel token yenileme** — Mevcut token invalid/expire olmuş. Dashboard'dan yeni Personal Access Token oluşturulmalı ve `VERCEL_TOKEN` env variable olarak güncellenmeli. Bu olmadan:
  - CLI deploy yapılamıyor
  - 65 building ürün deploy edilemez
  - Canonical URL drift düzeltilemez

## Acil (Gelir Engelliyor)
1. **LemonSqueezy verification** → Kritik bloker. Kimlik doğrulaması olmadan sıfır gelir.
2. **Vercel token** → 65 ürün deploy edilemiyor. Deploy olmayan ürün = erişilemez = sıfır trafik.

## Düşük Öncelik (Gelir Etkilemiyor)
- Checkout URL field standardizasyonu — teknik borç, fonksiyonelliği etkilemiyor
- 86 boş klasör temizliği — gürültü ama gelir etkisi yok
- Kategori atama — SEO iyileştirmesi, uzun vadeli
- webhook-tester canonical URL — HTTP 200 dönüyor, functional sorun yok

## Otomasyon Planı (Sonraki Adım)

### Hemen Yapılabilir (Script/Codex ile)
| Görev | Sorumlu | Dosya |
|-------|---------|-------|
| STATE.json healthy_count BUG fix | toolsmith | `scripts/audit_portfolio_health.py` |
| Log rotation scripti | toolsmith | `scripts/log_rotation.sh` |
| Kategori atama otomasyonu | codex_task | `scripts/auto_categorize.py` |
| Boş klasör arşivleme | toolsmith | `scripts/archive_empty_products.sh` |
| Checkout URL field standardizasyonu | codex_task | `scripts/standardize_checkout_fields.py` |

### Kullanıcı Bekleyen (Otomate Edilemeyen)
| Görev | Etki | Beklenen Süre |
|-------|------|---------------|
| LemonSqueezy identity verification | 65 ürün checkout aktif | ~5 dk (belge yükleme) |
| Vercel token yenileme | 65 ürün deploy aktif | ~2 dk (token oluşturma) |

### codex_task.md'ye Eklenecekler
1. `auto_categorize.py` — Ürün adı + README'den kategori çıkarımı
2. `standardize_checkout_fields.py` — Tüm product.json'larda checkout_url standardizasyonu
3. `batch_update_prices.py` — Kategori bazlı otomatik fiyat önerisi
