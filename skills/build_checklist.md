# Build Checklist — Builder Agent İçin Zorunlu Kontrol Listesi
**Version:** 1.5 | **Son Guncelleme:** Cycle 640 | **Guven skoru:** Yuksek

> Bu dosya skill-writer agent tarafından her başarılı/başarısız build sonrası güncellenir.
> Builder her deploy öncesi bu listeyi okumalı ve TÜMÜNÜ tamamlamalıdır.

---

## ⚡ DEPLOY ÖNCESİ ZORUNLU KONTROLLER

### 1. Dosya Yapısı
- [ ] `public/index.html` → 400+ satır, dark tema, gradient, animasyonlar
- [ ] `api/process.js` → gerçek iş mantığı (POST → JSON)
- [ ] `api/webhook.js` → LemonSqueezy webhook handler (OPTIONS + POST)
- [ ] `api/health.js` → `{"status":"ok","service":"<slug>"}` döndürüyor
- [ ] `vercel.json` → rewrites/routes doğru tanımlı
- [ ] `product.json` → tüm alanlar dolu

### 2. vercel.json Kontrol
```json
{
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/$1" },
    { "src": "/(.*)", "dest": "/public/index.html" }
  ]
}
```
- [ ] Routes doğru mu? (api/* → api, /* → index.html)
- [ ] Team ID tanımlı mı? (`--team team_dvJDRExvJITRGWh3cWs5L44m`)

### 3. Landing Page Kalite (ZORUNLU)
- [ ] Dark arka plan: `#0a0a0a` veya `#0f172a`
- [ ] Gradient başlık: `text-transparent bg-clip-text`
- [ ] Animasyonlar: fadeInUp, hover scale, CTA pulse
- [ ] Glassmorphism kartlar: `rgba(255,255,255,0.05) + border + backdrop-blur`
- [ ] DEMO/Preview bölümü var ve çalışıyor (mock data ile)
- [ ] CTA glow efekti var
- [ ] FAQ bölümü (en az 4 soru)
- [ ] Trust badges: `✓ No signup ✓ Instant ✓ API Ready`
- [ ] Open Graph meta tags (`og:title`, `og:description`, `og:image`)
- [ ] Mobile responsive (`@media max-width: 768px`)

### 4. API Kontrolleri
- [ ] `/api/health` → `{"status":"ok"}` döndürüyor
- [ ] `/api/process` → POST ile gerçek sonuç döndürüyor
- [ ] `/api/webhook` → OPTIONS isteklerini 200 ile yanıtlıyor
- [ ] CORS headers tüm endpoint'lerde var

### 5. Deploy Komutu
```bash
cd /home/gokhan/UniverseCreator/products/<slug>
VERCEL_TOKEN="$VERCEL_TOKEN" vercel --yes --prod --token "$VERCEL_TOKEN" --scope "$VERCEL_SCOPE"
```
- [ ] Token env'den geliyor mu? (`VERCEL_TOKEN`; dosyaya token yazma)
- [ ] Scope/team env'den geliyor mu? (`VERCEL_SCOPE` gerekirse)
- [ ] `--prod` flag'i var mı?

### 6. Deploy Sonrası Doğrulama
```bash
curl -sf <URL>/api/health | jq .
curl -sf -o /dev/null -w '%{http_code}' <URL>/
```
- [ ] Health check 200 → `{"status":"ok"}`
- [ ] Ana sayfa 200 dönüyor
- [ ] VERCEL URL product.json'a kaydedildi

---

## 🔴 BİLİNEN HATALAR (Tekrar Etme!)

*(Bu bölüm skill-writer tarafından doldurulur)*

### v1.5 - Cycle 640 Guncellemeler
- **24/24 urun healthy:** Tum urunler health check'ten geciyor. Checkout coverage %91.6 (22/24).
- **Checkout bekleyenler:** universe-hub (portfolio hub) ve llm-token-lens (LLM araci) — 49+ cycle'dir checkout URL olusturulmadi. Revenue kaybı devam ediyor.
- **Balance: $0.0:** Hic satis yok. Distribution bottleneck — urun kalitesi yeterli, satis kanali yok.
- **Category gaps:** Security, Database, Image Processing, Email, Testing alanlarinda urun yok.
- **OPTIMIZE mode devam:** Yeni build yok, mevcut 24 urun iyilestiriliyor.
- **Builder standby:** Yeni spec bekliyor, mevcut pattern'leri calisiyor.
- **Standart fiyat $19:** 24/24 urun ayni fiyatta, pricing complexity sifir.

---

## ✅ BAŞARILI BUILD PATTERN'LERİ

*(Bu bölüm skill-writer tarafından doldurulur)*

### v1.5 - Cycle 640 Guncellemeler
- **24/24 urun healthy:** 49+ cycle'dir tum urunler stabil. %91.6 checkout coverage.
- **Distribution > Product:** Urun kalitesi kanitlandi, artik satis/pazarlama oncelikli. Product Hunt, HN, Twitter oneriliyor.
- **Builder standby pattern:** Builder agent mevcut pattern'leri ogreniyor, yeni spec bekliyor.
- **Category gap firsati:** Security (ScanGuard), Database, Image Processing, Email, Testing alanlarinda yeni urun firsati var.
- **$19 standart fiyat:** 24 urun ayni fiyatta, pricing strategy stable.
