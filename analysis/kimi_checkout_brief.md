# KİMİ CHECKOUT BRIEF — Polar Checkout URL Oluşturma + Sorun Çözme

## ÖNCELİK SIRASI (KRİTİK!)
1. **ÖNCE** Checkout URL ayarla — `sync-links` çalıştır, gap varsa kapat
2. **SONRA** Sorunları çöz — tespit edilen sorunları düzelt, test et, kaydet

ASLA önce sorun çözme ile başlama. Checkout öncelik.

---

## Kimin Görevi
Checkout URL'leri eksik olan ürünlere Polar checkout link eklemek.
Ardından: tespit edilen sorunları çözmek (script hataları, sağlık sorunları, vb.)

## Referans Dosyalar (Oku!)
1. `skills/POLAR_CHECKOUT.md` — **ANA REFERANS** — Polar API kuralları, komutlar, bilinen sorunlar
2. `lessons/checkout-url-lessons.md` — Aktif ürün tablosu, fiyatlar, başarılı workflow adımları
3. `SYSTEM_ARCHITECTURE.md` Section 9 — Polar checkout akışı açıklaması

## Checkout Komutları

### Plan (ne yapılacak görmek için)
```bash
cd /home/gokhan/UniverseCreator
POLAR_OAT='polar_oat_46i4TTg7tq2yuxa8ebTUo84fiDa5OiY2a5xXB19aJXB' \
python3 scripts/polar_checkout_sync.py plan \
  --status live \
  --status ready_for_payment \
  --replace-non-polar \
  --output analysis/polar_checkout_plan.md
```

### Sync (gerçek iş — checkout URL oluştur)
```bash
POLAR_OAT='polar_oat_46i4TTg7tq2yuxa8ebTUo84fiDa5OiY2a5xXB19aJXB' \
python3 scripts/polar_checkout_sync.py sync-links \
  --status live \
  --status ready_for_payment \
  --replace-non-polar \
  --output analysis/polar_checkout_sync_report.md
```

## Kritik Kurallar (POLAR_CHECKOUT.md'den)

| Kural | Detay |
|---|---|
| **Minimum fiyat** | $0.50 — $0.10 reddedilir |
| **Price payload** | `"amount_type": "fixed"` kullan — `"type": "fixed"` çalışmaz (422 hatası) |
| **OAT ile org_id YASAK** | Checkout/product create çağrılarında organization_id gönderme (422 hatası) |
| **Kütüphane** | `requests` kullan — `urllib` 307 redirect'i POST→GET'e çevirir |
| **Checkout link tipi** | Reusable (uzun ömürlü) — session değil |

## Polar API Key
```
POLAR_OAT= polar_oat_46i4TTg7tq2yuxa8ebTUo84fiDa5OiY2a5xXB19aJXB
```

Token'ı doğrudan komut içinde kullanıyorsun — başka yere kaydetme.

## Fiyat Kaynağı Önceliği
1. `spec.json["price"]` — en yetkili (= website fiyatı)
2. `product.json["price"]`
3. Dosya text arama ($XX kalıpları)

## State Kontrol Et
```bash
cat /home/gokhan/UniverseCreator/STATE_SUMMARY.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Live: {d[\"live_count\"]}, Healthy: {d[\"healthy_count\"]}, Checkout gap: {d[\"checkout_gap_count\"]}')"
```

## Output (Çıktı Kuralları)
- `analysis/polar_checkout_sync_report.md` — sync sonucu
- product.json güncellenmeli (checkout_url, payment_provider: "polar", polar_product_id, polar_checkout_link_id)
- Lessons güncellenmeli (`lessons/checkout-url-lessons.md`)
- **Commit ZORUNLU** — her döngü minimum 1 commit

## Sorun Çözme (Secondary Görev)
Checkout tamamlandıktan SONRA çözülcek sorunlar:

### Sağlık Sorunları
- unhealthy ürünler → health check yap, nedenini bul, düzelt
- canonical drift → URL'leri düzelt

### Script Hataları
- Bash/python hataları → debug et, düzelt, test et
- Deployment hataları → loglardan analiz et

### Önerileri Uygula
- `analysis/oneri.md` veya raporlardaki öneriler → uygula
- Lessons'a kaydet

### Sorun Çözme Workflow
1. Sorunu tespit et (log, error mesajı, vb.)
2. Kök nedeni bul
3. Düzelt (edit/write)
4. Test et (test script veya manuel curl)
5. Lessons'a kaydet (ne çözüldü, nasıl)
6. Commit at

## Bilinen Sorunlar + Çözümler

| Sorun | Çözüm |
|---|---|
| 422 "type" hatası | `"amount_type": "fixed"` kullan |
| $0.10 reddedildi | Minimum $0.50 kullan |
| urllib 307 redirect POST→GET | `requests` kütüphanesi kullan |
| OAT + org_id = 422 | org_id çıkar payload'dan |
| vercel_url yok ama checkout_url var | `--replace-non-polar` ile yakala |

## Workflow (Adım Adım)
### Önce (Öncelik 1)
1. Plan çalıştır → adayları gör
2. Scope doğru mu kontrol et
3. Sync-links çalıştır
4. product.json güncellendi mi kontrol et
5. Lessons güncelle (yeni checkout'lar için tabloyu güncelle)
6. Commit at

### Sonra (Öncelik 2)
7. Sorunları tespit et (loglar, STATE, health check)
8. Tespit edilen sorunları çöz
9. Test et
10. Lessons güncelle
11. Commit at

### Her Zaman
12. Telegram raporu gönder
