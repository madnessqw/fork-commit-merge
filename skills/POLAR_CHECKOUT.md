# POLAR CHECKOUT OPERATIONS — UniverseCreator

Bu dosya Codex/Claude için kısa ama gerçek çalışma rehberidir.
Amaç: UniverseCreator ürün kataloğunu **Polar-first** ödeme rayına taşımak.

## Gerçek Durum
- Polar checkout hattı gerçek `$1` smoke test ile doğrulandı.
- Checkout açıldı, ödeme geçti, dashboard'a düştü.
- Payout bankaya inişi hâlâ ayrıca izleniyor; ama checkout rollout artık deney değil.

## Ana Kural
### 1) Static katalog ürünü
Kullan: **Polar product + Polar checkout link**

Sebep:
- ürün sayfasında kalıcı URL gerekir
- short-lived checkout session katalog checkout'u gibi kullanılamaz

### 2) Ad-hoc custom work
Kullan: **Polar checkout session**

Örnek:
- tek seferlik bug fix
- maintainer'a özel ödeme linki
- custom $20 / $30 / $200 tahsilat

## Truth Source
### Fiyat keşfi sırası
1. `products/<slug>/product.json` → `price`
2. Parse edilemiyorsa ürün dosyaları:
   - `index.html`
   - `public/index.html`
   - `README.md`
   - `product-spec.md`
   - `spec.json`
   - `spec.md`
   - `api/process.js`
3. Elle fiyat uydurma yok

### Checkout truth source
- `product.json` içindeki `checkout_url`
- `payment_provider = polar`
- varsa:
  - `polar_product_id`
  - `polar_product_price_id`
  - `polar_checkout_link_id`

Landing page veya README farklıysa onları buna hizala.

## Ana Tool
### `scripts/polar_checkout_sync.py`

#### Plan
```bash
python3 scripts/polar_checkout_sync.py plan \
  --status live \
  --status ready_for_payment \
  --replace-non-polar \
  --output analysis/polar_checkout_plan.md
```

Ne yapar:
- aday ürünleri listeler
- fiyat kaynağını gösterir
- Polar migration kapsamını çıkarır

#### Gerçek sync
```bash
POLAR_OAT='polar_oat_...' \
python3 scripts/polar_checkout_sync.py sync-links \
  --status live \
  --status ready_for_payment \
  --replace-non-polar \
  --output analysis/polar_checkout_sync_report.md
```

Ne yapar:
- Polar ürünlerini listeler
- yerel slug ile eşler
- ürün yoksa oluşturur
- fiyat drift varsa günceller
- reusable checkout link üretir
- `product.json` alanlarını günceller

## Tool Matrisi
| Tool/Dosya | Ne işe yarar | Ne zaman kullan |
|---|---|---|
| `scripts/polar_checkout_sync.py plan` | rollout adaylarını çıkarır | sync'ten önce |
| `scripts/polar_checkout_sync.py sync-links` | Polar product + checkout link oluşturur/günceller | canlı rollout |
| `scripts/checkout_metadata.py` | `checkout_url` + `payment_provider` normalize eder | manifest/state drift temizliği |
| `scripts/create_product.sh` | yeni ürün scaffold eder, payment varsayılanını Polar yapar | yeni katalog ürünü açarken |
| `scripts/deploy_product.sh` | GitHub + Vercel deploy eder, ürünü payment-ready/live state'e taşır | ürün deploy'u |
| `scripts/deploy_readiness.py` | deploy/payment readiness gap'lerini okur | rollout öncesi boşluk tespiti |
| `scripts/refresh_codex_context.py` | Codex context'ini günceller | büyük değişiklik sonrası |
| `analysis/polar_checkout_plan.md` | aday ürün listesi | plan review |
| `analysis/polar_checkout_sync_report.md` | gerçek sync çıktısı | rollout sonrası audit |
| `analysis/legacy_checkout_refs.md` | eski checkout referanslarını bulur | migration cleanup |

## Polar API Modları
### Checkout Link
- reusable
- katalog ürünü için doğru seçim
- landing page butonuna yazılır

### Checkout Session
- kısa ömürlü
- custom iş / özel tahsilat için doğru seçim
- katalog checkout'u gibi yapıştırılmaz

## `--replace-non-polar` ne yapar?
- mevcut checkout'u başka provider olan ürünleri de migration adayına alır
- yani legacy provider checkout'ları Polar'a taşıyabilirsin

## İlgili Yardımcı Dosyalar
- `analysis/polar_checkout_rollout.md` → migration kararı ve geçmiş
- `analysis/polar_checkout_plan.md` → aday listesi
- `analysis/legacy_checkout_refs.md` → repo içindeki legacy checkout referansları
- `scripts/checkout_metadata.py` → checkout/provider normalize eder
- `scripts/create_product.sh` → yeni ürün scaffold
- `scripts/deploy_product.sh` → deploy sonrası payment-ready state üretir

## Operasyon Sırası
1. Plan çıkar
2. Scope doğru mu kontrol et
3. Sync çalıştır
4. `product.json` güncellendi mi kontrol et
5. Gerekirse landing page/README hardcoded checkout URL'lerini düzelt
6. Summary/report yenile

## Güvenlik
- Token'ı repo dosyasına yazma
- Token'ı prompt dosyasına yazma
- Token'ı `POLAR_OAT` env var ile ver
- Scope'ları gereksiz admin seviyesine çıkarma

## OAT Scope Seti — Geniş ama Makul
Açık olmalı:
- `products:read`
- `products:write`
- `checkout_links:read`
- `checkout_links:write`
- `checkouts:read`
- `checkouts:write`
- `orders:read`
- `payments:read`
- `transactions:read`
- `customers:read`
- `customers:write`
- `discounts:read`
- `discounts:write`
- `custom_fields:read`
- `custom_fields:write`
- `files:read`
- `benefits:read`
- `benefits:write`
- `notifications:read`
- `events:read`
- `metrics:read`

İyi ekler (otonom katalog + abonelik/lisans büyürse):
- `files:write`
- `notifications:write`
- `events:write`
- `license_keys:read`
- `license_keys:write`
- `subscriptions:read`
- `subscriptions:write`
- `customer_portal:read`
- `customer_portal:write`
- `customer_sessions:write`
- `customer_meters:read`
- `customer_seats:read`
- `customer_seats:write`
- `meters:read`
- `meters:write`
- `notification_recipients:read`
- `notification_recipients:write`

Okunabilir ama şimdilik operasyon dışı:
- `payouts:read`
- `refunds:read`
- `wallets:read`
- `members:read`
- `organizations:read`
- `organization_access_tokens:read`
- `profile`
- `user:read`
- `openid`
- `email`

Şimdilik kapalı kalsın:
- `refunds:write`
- `payouts:write`
- `organization_access_tokens:write`
- `organizations:write`
- `members:write`
- `wallets:write`
- `webhooks:write`
- `user:write`

## ⚠️ Polar API Quirks (canlı testten öğrenildi)
- **Minimum fiyat: $0.50** — $0.10 rejected, $1 = güvenli alt sınır
- **price create payload:** `amount_type: "fixed"` kullan — `type: "fixed"` çalışmıyor (422)
- **OAT ile organization_id gönderme** — checkout/product create çağrılarında yasak (422)
- **Checkout session** için sadece `{"products": ["product_id"]}` yeterli
- **requests kütüphanesi kullan** — `urllib` 307 redirect'i POST ile takip etmiyor (POST → GET'e döner)
- **`deneme-test` product ID:** `63d64f8b-2acc-4326-b9d9-467df790f9dd` (smoke test, $1, smoke_test kind)

## Swarm Davranış Kuralı
- Önce checkout gap'i kapat
- Sonra legacy checkout drift temizle
- Sonra landing page hardcode URL'lerini hizala
- Session URL ile katalog checkout karıştırma
- Checkout üretildi diye payout çözüldü yalanı yazma

## Kısa Başlangıç Komutu
```bash
cd /home/gokhan/UniverseCreator
cat skills/POLAR_CHECKOUT.md
python3 scripts/polar_checkout_sync.py plan --status live --status ready_for_payment --replace-non-polar --output analysis/polar_checkout_plan.md
```
