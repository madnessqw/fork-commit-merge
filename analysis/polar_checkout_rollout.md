# Polar Checkout Rollout — UniverseCreator

## Neden
- UniverseCreator ürün kataloğunda yaklaşık 160 `product.json` var.
- Bunların 86 tanesinde `checkout_url` boş.
- Polar checkout hattı canlı test ile doğrulandı: gerçek checkout açıldı, ödeme dashboard'a düştü.
- Banka payout hâlâ pending olsa da checkout üretim hattı artık kurumsal aday değil, çalışır durumda.

## Bugün tam olarak ne yaptık
1. Polar OAT ile canlı `$1` smoke test checkout session oluşturuldu.
   - Test başarılı geçti; checkout açıldı ve ödeme dashboard'a düştü.
2. Aktif prompt zinciri bulundu:
   - `prompts/codex_prompt.txt` → Codex loop
   - `PROMPT.txt` → Claude loop
   - `skills/FACTORY.md` → Claude'un ana operational skill'i
   - `skills/POLAR_CHECKOUT.md` → Polar checkout tool/source-of-truth rehberi
3. Claude/Codex prompt'ları Polar checkout rollout önceliğine çekildi.
4. Eski provider'a bağlı prompt metinleri operasyonel akıştan çıkarıldı.
5. `scripts/polar_checkout_sync.py` eklendi.
6. `scripts/create_product.sh` ve `scripts/deploy_product.sh` artık Polar-first düşünmeye başladı.
7. `scripts/checkout_metadata.py` Polar URL'lerinden provider inference yapacak şekilde güncellendi.
8. Codex ilk mesajda uzun tool dump almak yerine `skills/POLAR_CHECKOUT.md` okuyacak şekilde promptlar kısaltıldı.

## Çok önemli ayrım
### 1) Static katalog ürünleri
Bunlar için **Polar product + Polar checkout link** kullan.

Sebep:
- ürün sayfasında kalıcı checkout URL gerekir
- checkout session kısa ömürlüdür, katalog checkout'u gibi kullanmak aptallık olur

### 2) Ad-hoc custom work
Bunlar için **Polar checkout session** kullan.

Örnek:
- bir maintainer'a özel bug fix linki
- tek seferlik `$20`, `$30`, `$200` tahsilat

## `$1` smoke test nasıl oluşturuldu
Kullanılan scope'lar:
- `checkouts:write`
- `products:read`
- `checkouts:read`

Kullanılan mevcut Polar ürün:
- `API Spec Validator — Quick Check`
- fiyat: `$1`

Canlı session URL oluşturma mantığı:
- mevcut product ID seçildi
- `POST /v1/checkouts/` ile session açıldı
- kullanıcıya session URL verildi

Not:
- Bu model sadece smoke test ve ad-hoc custom work içindir
- 140+ katalog ürünü için **doğru model değildir**

## Katalog rollout için gereken token scope'ları
### Minimum mantıklı OAT
- `products:read`
- `products:write`
- `checkout_links:read`
- `checkout_links:write`

### Geniş ama makul OAT
- `checkouts:read`
- `checkouts:write`  # smoke test / ad-hoc work için
- `orders:read`
- `payments:read`
- `transactions:read`
- `customers:read`
- `customers:write`
- `discounts:read`
- `discounts:write`
- `custom_fields:read`
- `custom_fields:write`  # ileride checkout form alanları için

### Bilerek verilmemesi gerekenler
- `refunds:*`
- `payouts:*`
- `organization_access_tokens:*`
- `members:*`
- `organizations:write`
- `webhooks:*`  # webhook otomasyonu gerçekten kurulmadan verme

## Yeni script
### Plan modu
```bash
python3 scripts/polar_checkout_sync.py plan --status live --status ready_for_payment --replace-non-polar \
  --output analysis/polar_checkout_plan.md
```

Bu komut:
- yerel `product.json` dosyalarını tarar
- `vercel_url` + `price` olan ürünleri aday sayar
- checkout gap listesini markdown olarak üretir

### Sync modu
```bash
POLAR_OAT='polar_oat_...' \
python3 scripts/polar_checkout_sync.py sync-links --status live --status ready_for_payment --replace-non-polar \
  --output analysis/polar_checkout_sync_report.md
```

Bu komut:
- Polar'daki ürünleri okur
- `metadata.local_slug` ile yerel ürünü eşler
- ürün yoksa oluşturur
- fiyat drift varsa günceller
- reusable checkout link üretir
- `products/<slug>/product.json` içine şunları yazar:
  - `checkout_url`
  - `payment_provider=polar`
  - `polar_product_id`
  - `polar_product_price_id`
  - `polar_checkout_link_id`

## Fiyat kaynağı kuralı
1. Önce `products/<slug>/product.json` içindeki `price`
2. Parse edilemiyorsa ürün dosyalarından fiyat keşfi (`index.html`, `public/index.html`, README, spec`)
3. Elle uydurma fiyat yok

## Codex'e verilen yeni öncelik
- Birinci iş: Polar checkout rollout
- `live` ve `ready_for_payment` checkout gap'leri önce kapatılacak
- Session vs checkout link ayrımı korunacak
- Eski checkout listeleri tekrar prompt'a sokulmayacak

## Hâlâ açık kalan şey
- Polar payout'un Enpara'ya fiilen düşmesi

Bu pending olsa da checkout rollout altyapısı artık beklemeye alınmamalı.
En doğru rota:
- **build now**
- **bank payout trust later**

## Sonraki somut adım
Geniş OAT scope seti hazırlandı ve prompt/tool rehberi `skills/POLAR_CHECKOUT.md` içine taşındı.

Bir sonraki gerçek operasyon:
```bash
POLAR_OAT='...' \
python3 scripts/polar_checkout_sync.py sync-links \
  --status live \
  --status ready_for_payment \
  --replace-non-polar \
  --output analysis/polar_checkout_sync_report.md
```

Bu komut gerçek ürün rollout'unu başlatır.
