# Mikro-SaaS Arastirma Raporu - Vercel Serverless Fikirleri

**Tarih:** 2026-04-09
**Arastirmaci:** UniverseCreator Research Agent
**Mevcut Urunler:** 24 (Vercel-deployed)

---

## MEVCUT PORTFOY ANALIZI

### Sahip Oldugumuz Kategoriler

| Kategori | Urunler |
|----------|---------|
| **Veri Formatlama** | json-formatter-pro, json-schema-validator, dataflip, pdf-forge |
| **Developer Utility** | curl2code, regex-tester-pro, codesnap, url-forge |
| **API/Web Araclari** | webhook-tester, mockforge, meta-fetch, function-call-debugger |
| **Guvenlik** | jwtinspector, rateguard |
| **AI/LLM** | llm-token-lens |
| **Medya/Image** | og-forge, qrforge, colormine |
| **Monitoring** | http-pulse, statusbeacon |
| **Diger** | geoip-lite, techstack, carbonlite |

### EKSİK KATEGORİLER (Firsat Alanlari)

- API Security / Header Analysis - **HIC YOK**
- Image Processing / Optimization API - **HIC YOK**
- Prompt Engineering / LLM Cost Tools - **SADECE llm-token-lens (kismi)**
- OpenAPI / API Contract Testing - **HIC YOK** (mockforge var ama OpenAPI degil)
- Web Performance / Core Web Vitals - **HIC YOK**
- Email Validation / Deliverability - **HIC YOK**
- Screenshot / Visual Testing API - **HIC YOK**
- SSL/TLS Monitoring - **HIC YOK**

---

## PAZAR ARAŞTIRMASI BULGULARI

### 1. AI/LLM Developer Tools Pazarı
- **Cursor IDE** $20-40/ay ile en populer AI code editor oldu
- **LLM Cost Calculator** araclari trending (llm-prices.com, MorphLLM %70-90 tasarruf iddia ediyor)
- Reddit'te B2B SaaS olarak prompt + cost optimization araclari cok talep goruyor
- **Trend:** Developer'lar LLM API harcamalarini kontrol etmek istiyor

### 2. API Security Pazarı
- **AquilaX** $19/ay'dan basliyor, 70+ guvenlik araci sunuyor
- **42Crunch**, **APIsec** enterprise seviyede $200+/ay
- **CORS Tester**, **Security Headers Checker** ucretsiz olarak mevcut ama profesyonel arac yok
- **Trend:** "Vibe coding" artisi ile AI-uretilen kod guvenlik aciklari yaratıyor, audit ihtiyaclari artıyor

### 3. Image Processing API Pazarı
- **Cloudimage** $69/ay'dan basliyor (pahali)
- **APYHub** "pennies per thousand" ile ucuz alternatif
- **Assets.so** on-the-fly image transformation + OG images
- Shopify apps $10-40/ay arasi
- **Trend:** Developer'lar basit, uygun fiyatli image API'si ariyor

### 4. OpenAPI / API Documentation
- **SwaggerHub** ucretsiz + ucretli planlar
- **Beeceptor** OpenAPI'den mock server olusturuyor
- **Apidog**, **Postman** $14-29/ay
- **Trend:** API-first development artiyor, sozlesme tabanli test onemli

---

## 5 URUN FIKRI

### 1. ScanGuard - API Guvenlik Tarayicisi

**Tagline:** "Scan your API for vulnerabilities in seconds"

**Problem:** Developer'lar API'larini test ederken CORS, security headers, SSL, exposed endpoints gibi guvenlik sorunlarini manuel kontrol ediyor. Mevcut cozumler ya cok pahali (AquilaX $19/ay, 42Crunch $200+/ay) ya da cok basit (ucretsiz CORS tester'lar).

**Cozum:** Tek tiklamada API endpoint'ini tara, guvenlik raporu uret.

**Teknik Detay (Vercel Serverless):**
```
POST /api/scan          → URL al, guvenlik taramasi yap
GET  /api/scan/:id      → Tarama sonucunu getir
POST /api/scan/schedule → Periyodik tarama planla (cron)
GET  /api/reports       → Tum raporlari listele
```

**Tarama Modulleri:**
- CORS misconfiguration detection
- Security headers analizi (CSP, HSTS, X-Frame-Options, etc.)
- SSL/TLS certificate check
- Exposed environment variables (.env, .git)
- Rate limiting testi
- Common vulnerability scan (SQLi, XSS probing - basic)

**Fiyat:** $29 (one-time) veya $9/ay (subscription - periyodik tarama icin)

**Neden Satar:** "Vibe coding" trendi ile AI-uretilen kod guvenlik sorunlari iceriyor. Developer'lar hizli, uygun fiyatli guvenlik araci istiyor. Pazar bozuk - ortasi yok (ucretsiz basit araclardan enterprise $200+/ay'a atliyor).

---

### 2. PixelForge - Image Processing API

**Tagline:** "Resize, convert, optimize images via simple API"

**Problem:** Developer'lar image isleme icin ya pahali servisler (Cloudimage $69/ay) kullanmak zorunda ya da kendi infrastructure'larini kurmak zorunda (Sharp + Lambda).

**Cozum:** RESTful API ile image resize, format conversion (WebP, AVIF, PNG, JPG), optimizasyon.

**Teknik Detay (Vercel Serverless):**
```
POST /api/resize        → Resmi boyutlandir (width, height, fit)
POST /api/convert       → Format degistir (WebP, AVIF, PNG, JPG)
POST /api/optimize      → Sikistir (quality seviyesi)
POST /api/og            → Open Graph image uret (text overlay + template)
GET  /api/transform/:id → Onceden islenmis resmi getir
POST /api/batch         → Toplu islem (max 10 resim)
```

**Fiyat:** $19 (one-time) + kullanim bazli ek paketler

**Neden Satar:** Her web projesi image isleme ihtiyaci duyar. Mevcut cozumler ya pahali ya da karmasik. Vercel'de Sharp + serverless function ile rahat calisir.

---

### 3. PromptOps - LLM Prompt & Cost Optimizer

**Tagline:** "Optimize your prompts, minimize your LLM costs"

**Problem:** Developer'lar LLM API harcamalarini takip etmekte, prompt'larini optimize etmekte ve model karsilastirmasi yapmakta zorlaniyor. llm-token-lens sadece token sayiyor, daha fazlasi gerekli.

**Cozum:** Prompt test, karsilastirma, maliyet hesaplama ve optimizasyon araci.

**Teknik Detay (Vercel Serverless):**
```
POST /api/prompt/test     → Prompt'u test et, sonuc don
POST /api/prompt/compare  → 2+ prompt'u karsilastir
POST /api/prompt/optimize → Prompt'u kucult/optimizasyon oner
GET  /api/cost/calculate  → Token maliyetini hesapla (tum modeller)
GET  /api/cost/track      → API harcama takibi
GET  /api/models          → Model karsilastirma tablosu
POST /api/prompt/template → Prompt sablonu kaydet/paylas
```

**Fiyat:** $19 (one-time)

**Neden Satar:** LLM kullanimi patlama yasiyor. Her developer cost optimization ihtiyaci hissediyor. llm-token-lens'den daha kapsamli.

---

### 4. SchemaForge - OpenAPI Spec Validator & Mock Tester

**Tagline:** "Validate your OpenAPI specs, test against real responses"

**Problem:** Developer'lar OpenAPI spec yaziyor ama gercek API response'larinin spec'e uygun olup olmadigini test edecek uygun fiyatli arac bulamiyor. Mockforge var ama OpenAPI validation yok.

**Cozum:** OpenAPI spec validasyonu, gercek API response karsilastirmasi, mock generation.

**Teknik Detay (Vercel Serverless):**
```
POST /api/validate        → OpenAPI spec validasyonu (3.0/3.1)
POST /api/compare         → Spec vs gercek API response karsilastir
POST /api/mock/generate   → Spec'den mock endpoint uret
POST /api/mock/test       → Mock endpoint'i test et
GET  /api/docs/generate   → Spec'den dokumantasyon uret
POST /api/import          → Postman collection / Swagger import
```

**Fiyat:** $29 (one-time)

**Neden Satar:** API-first development standart oluyor. Mockforge'a ek deger. Postman/Swagger alternatifi olarak konumlanabilir.

---

### 5. PulseCheck - Web Performance Monitor

**Tagline:** "Monitor Core Web Vitals and performance from multiple locations"

**Problem:** Developer'lar websitelerinin performansini izlemek icin Google PageSpeed Insights API'sini manuel kullanmak zorunda. Surekli izleme, alerting ve tarihsel karsilastirma yapan uygun fiyatli arac yok.

**Cozum:** Otomatik Core Web Vitals izleme, multi-location test, performans raporlari.

**Teknik Detay (Vercel Serverless):**
```
POST /api/test/url        → URL test et (LCP, CLS, INP, FCP, TTFB)
GET  /api/test/:id        → Test sonucunu getir
POST /api/monitor         → Periyodik monitoring ayarla (cron)
GET  /api/monitor/:id     → Monitoring gecmisi
GET  /api/reports         → Performans raporlari
POST /api/alert           → Alert threshold ayarla
GET  /api/compare         → 2 URL karsilastir
```

**Fiyat:** $19 (one-time)

**Neden Satar:** Core Web Vitals SEO icin kritik. Google surekli threshold'lari guncelliyor. Her website sahibinin ihtiyaci var.

---

## KARSILASTIRMA TABLOSU

| Urun | Pazar | Rekabet | Teknik Zorluk | Gelir Potansiyeli | Portfoy Uyumu |
|------|-------|---------|---------------|-------------------|---------------|
| **ScanGuard** | Guvenlik | Orta | Orta | YUKSEK | EKSİK kategori |
| **PixelForge** | Image/Media | Yuksek | Yuksek | ORTA-YUKSEK | EKSİK kategori |
| **PromptOps** | AI/LLM | Dusuk | Orta | YUKSEK | llm-token-lens tamamlayici |
| **SchemaForge** | API Tools | Dusuk | Orta | ORTA | mockforge tamamlayici |
| **PulseCheck** | Monitoring | Orta | Dusuk | ORTA | http-pulse tamamlayici |

---

## BUILD ONERISI: ScanGuard

### Neden ScanGuard?

1. **HIC RAKIP YOK** mevcut urunlerimizde - guvenlik kategorisi tamamen bos
2. **Pazar zamani** - "Vibe coding" trendi ile AI-uretilen kod guvenlik aciklari yaratıyor, developer'lar guvenlik araci ariyor
3. **Teknik olarak uygun** - Vercel serverless function'lar HTTP istekleri yapabilir, CORS check, header analizi, SSL check hepsi serverless ile yapilabilir
4. **Yuksek fiyatlandirma potansiyeli** - Guvenlik araclari her zaman premium fiyatlandirilir ($29 one-time veya $9/ay)
5. **Cross-sell** - Mevcut urunlerle bundle edilebilir (rateguard + jwtinspector + ScanGuard = Guven Paketi)
6. **Product Hunt'da ilgi** - Developer security tools her zaman ilgi goruyor
7. **Tekrarlayan gelir** - Periyodik tarama feature'ı ile subscription'a donusebilir

### Minimum Viable Product (MVP):

```
/api/scan          → POST: URL al, 5 modulu tara, rapor don
/api/scan/:id      → GET: Onceki tarama sonucunu getir
/api/reports       → GET: Tum raporlari listele
```

**5 Tarama Modulu:**
1. CORS Analysis (misconfig detection)
2. Security Headers (CSP, HSTS, X-Frame, X-Content-Type, Referrer-Policy)
3. SSL/TLS Check (cert expiry, protocol version)
4. Exposed Files (.env, .git, .DS_Store, backup files)
5. Info Disclosure (server headers, technology fingerprinting)

### UI Sayfalari:
- Ana sayfa: URL gir + tek tiklamada tarama
- Sonuc sayfası: Detayli guvenlik raporu (skor + detaylar)
- Gecmis sayfası: Onceki taramalar

### Teknoloji Stack:
- Frontend: Next.js (zaten Vercel'de)
- Backend: Vercel Serverless Functions (Node.js)
- HTTP requests: `node-fetch` veya `undici`
- SSL check: `tls` module (built-in)
- Cron: Vercel Cron Jobs (periyodik tarama icin)

### Tahmini Gelir:
- 100 satis/ay x $29 = $2,900/ay
- %5 conversion ile subscription: 50 kullanici x $9/ay = $450/ay
- **Toplam potansiyel: $3,350/ay**

---

## IKINCIL ONERI: PromptOps

Ekipteki AI/LLM uzmanligi ile PromptOps hizli gelistirilebilir. llm-token-lens ile sinerji yaratir.

**Fark:** llm-token-lens token sayar, PromptOps prompt test + cost optimization + model karsilastirma yapar.

---

## KAYNAKLAR

- [ProductHunt Engineering Tools 2026](https://www.producthunt.com/categories/engineering-development)
- [Top 12 Developer Tools 2026](https://medium.com/@writertripathi/top-12-developer-tools-you-should-be-using-in-2026-e39503b81bf9)
- [GitHub Trending - Security AI Feb 2026](https://medium.com/@lssmj2014/github-trending-february-10-2026-security-ai-financial-agents-explode-35b4d5c5d91b)
- [AquilaX API Security Pricing](https://aquilax.ai/pricing)
- [LLM Cost Optimization - MorphLLM](https://morphllm.com/llm-cost-optimization)
- [LLM Pricing Calculator](https://www.llm-prices.com/)
- [Image Optimization APIs 2026](https://onesimpleapi.com/best/image-optimization-apis)
- [Solo Dev SaaS Stack $10K/month](https://dev.to/dev_tips/the-solo-dev-saas-stack-powering-10kmonth-micro-saas-tools-in-2025-pl7)
- [50 Micro SaaS Ideas 2026](https://bigideasdb.com/micro-saas-ideas-2026)
- [OpenAPI Tools](https://openapi.tools/)
