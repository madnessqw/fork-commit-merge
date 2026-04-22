# Çözüm Planlama — Cycle 948 | 2026-04-20 09:50 UTC

## Öncelikli Eylemler (Toolsmith için)

### 1. [ÇÖZÜMSÜZ — P0] STATE.json healthy_count=0 BUG
- **Sorun:** `scripts/audit_portfolio_health.py` çalışmıyor, STATE healthy_count=0 raporluyor
- **Kök neden:** Script dependency veya path sorunu; cache invalidation düzgün yapılmıyor
- **Çözüm:**
  1. `audit_portfolio_health.py`'yi debug et — import hataları, path sorunları kontrol et
  2. `healthy_count` hesaplamasını product.json'ları direkt okuyarak yap
  3. STATE.json'ı her cycle'da product.json'lardan yeniden oluştur
- **Kalıcı fix:** STATE.json'ı "cached snapshot" yap, her cycle'da force-refresh

### 2. [ÇÖZÜMSÜZ — P1] 65 Building Ürün Deploy Pipeline Tıkalı
- **Sorun:** 65 ürün "building" statüsünde, kodları hazır ama deploy edilmemiş
- **Kök neden:** Vercel token invalid + toplu deploy mekanizması yok
- **Çözüm:**
  1. Vercel token'ı yenile (kullanıcı gerekli)
  2. `scripts/batch_deploy.sh` yaz — tüm building ürünleri sırayla deploy et
  3. Deploy sonrası product.json'da status → "live" güncelle
- **Kalıcı fix:** Yeni ürün oluşturulduğunda otomatik deploy pipeline (GitHub push → Vercel auto-deploy)

### 3. [ÇÖZÜMSÜZ — P2] LemonSqueezy Checkout Gap (GELİR BLOKERI)
- **Sorun:** 65/113 ürün checkout URL eksik
- **Kök neden:** LemonSqueezy identity verification pending
- **Çözüm:** Gökhan'ın manuel müdahalesi gerekli — kimlik doğrulaması tamamlanmalı
- **Otomasyon:** Verification sonrası `scripts/create_checkout_urls.py` ile toplu URL oluşturma

### 4. [TEKRARLAYAN — P3] Codex Usage Limit Geçişleri
- **Sorun:** 02:40-03:21 UTC arası sık hesap değiştirme
- **Kök neden:** İki hesap arası usage limit'e yakın olma
- **Çözüm:** Geçiş eşiğini %80'den %90'a çek, bekleme süresi ekle
- **Kalıcı fix:** Üçüncü hesap ekle veya usage monitoring alert'i kur

## Sistem Evrim Adımları (Codex görevi olabilir)
1. **STATE.json refactoring** — product.json'ları source of truth yap, STATE'i cached snapshot yap
2. **Otomatik kategori atama scripti** — ürün adı + README analizinden kategori çıkarımı
3. **Log rotation scripti** — 10MB üstü log'ları gzip'le, son 3 dosyayı tut
4. **Checkout URL field standardizasyonu** — tüm product.json'larda tek `checkout_url` + `payment_provider`
5. **Boş klasör temizleme pipeline'ı** — product.json olmayan 86 klasörü `_archived/` altına taşı
6. **Fiyat atama otomasyonu** — kategori/benzer ürünlere göre otomatik fiyat önerisi
7. **Deploy pipeline otomasyonu** — building → deploy → live akışını otomatikleştir

## Düşük Öncelik
- [YENİ] 104/113 kategorisiz ürün — otomatik kategori scripti yazılınca çözülür
- [YENİ] 86 boş klasör — gürültü kaynağı ama acil değil, arşivleme yeterli
- [YENİ] webhook-tester canonical drift false positive — HTTP 200 dönüyor, STATE güncellenmeli
- Codex usage limit geçişleri — şu an otomatik çalışıyor, üçüncü hesap long-term çözüm

## Genel Sistem Notu
Sistem 948 cycle'a ulaşmış ve stabil çalışıyor. Ana sorunlar:
1. **Veri bütünlüğü:** STATE.json gerçeği yansıtmıyor — product.json'lar source of truth olmalı
2. **Deploy pipeline:** Vercel token sorunları + toplu deploy eksikliği 65 ürünü engelliyor
3. **Gelir akışı:** LemonSqueezy verification olmadan checkout URL oluşturulamıyor — bu tek bloker
4. **Veri kalitesi:** Kategori, fiyat ve field standardizasyonu eksik — ürün sayısı arttıkça büyüyen borç

Sistem "çalışıyor ama potansiyelinin çok altında" durumunda. 43 live ürün var ama sadece 5'i fiyatlı, 65'i deploy bekliyor, 64'ü checkout eksikli. Öncelik: deploy pipeline → LemonSqueezy → veri kalitesi.
