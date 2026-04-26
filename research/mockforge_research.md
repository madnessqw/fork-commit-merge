# MockForge - Derin Pazar Araştırması Raporu

**Tarih:** 2026-04-09
**Araştırmacı:** UniverseCreator - Researcher Agent
**Konu:** Serverless API Mock Generator - Pazar, rakipler, gap analizi

---

## 1. Ürün Tanımı

**MockForge:** Frontend developer'ların backend beklemeden scenario-based mock API oluşturmasını sağlayan serverless servis.

**Hedef Kitle:** Frontend developer'lar, indie hacker'lar, startup ekipleri, freelancer'lar

**Temel Değer Önerisi:** "Backend ekibini bekleme. 30 saniyede gerçekçi mock API'ını kur, frontend'ini geliştir."

---

## 2. Rakip Analizi

### 2.1 Beeceptor (En Yakın Doğrudan Rakip)

| Özellik | Detay |
|---------|-------|
| **Model** | SaaS - HTTP endpoint mocking |
| **Fiyatlandırma** | Free ($0), Individual ($10/ay), Team ($25/ay), Scale ($99/ay), Enterprise |
| **Free Limitler** | 50 req/gün, 3 mock rule, public endpoint |
| **Individual** | 15K req/ay, 50 rule, private endpoint |
| **Team** | 100K req/ay, 250 rule, custom domain |
| **Scale** | 1M+ req/ay, 500 rule, $40/ekstra 1M req |
| **Öne Çıkan Özellikler** | AI mock creation, traffic recording, conditional responses, stateful behavior, CRUD routes, fault/latency injection, SOC 2 + ISO 27001 |
| **Zayıf Noktalar** | Per-endpoint limitler kafa karıştırıcı, free tier çok kısıtlı (50 req/gün), scenario-based logic yok, UI basit, "senaryo" kavramı yok - sadece static/conditional rules |
| **GitHub** | Kapalı kaynak |

### 2.2 WireMock Cloud (En Güçlü Rakip)

| Özellik | Detay |
|---------|-------|
| **Model** | Open-source + Cloud SaaS |
| **Fiyatlandırma** | Free (1K calls/ay), Enterprise (custom) |
| **Free Limitler** | 1,000 calls/ay, 3 running API, 10 req/s, shared hosting |
| **Öne Çıkan Özellikler** | REST/gRPC/GraphQL, stateful mocking, chaos testing, fake data generation, Git Sync (yakında), K8s self-hosted |
| **Zayıf Noktalar** | Free tier sadece 1K calls/ay (çok düşük), Enterprise dışında orta segment yok, öğrenme eğrisi dik, Java-centric geçmiş, UI karmaşık, "scenario-based" değil "rule-based" |
| **GitHub** | ~7K stars (wiremock/wiremock) |
| **Önemli Not** | MockLab WireMock Cloud'a migrate oldu (2023) |

### 2.3 Mockoon (Desktop + Cloud)

| Özellik | Detay |
|---------|-------|
| **Model** | Open-source Desktop + Cloud SaaS |
| **Fiyatlandırma** | Desktop (Free), Cloud Solo ($10/ay), Cloud Team ($24/kullanıcı/ay), Enterprise |
| **Solo Limitler** | 1 API mock, 10K calls/ay, 100 AI endpoint/ay, 5 req/s, 10MB max |
| **Team Limitler** | 3 API mock, 100K calls/ay, 200 AI endpoint/kullanıcı/ay |
| **Öne Çıkan Özellikler** | Desktop app (Electron), AI assistant, data sync, GitHub Accelerator program üyesi |
| **Zayıf Noktalar** | Cloud çok yeni ve sınırlı (Solo'da sadece 1 API!), free desktop'ta cloud yok, 7 gün trial, kredi kartı şart |
| **GitHub** | ~8K stars (mockoon/mockoon) |

### 2.4 Postman Mock Server (Dolaylı ama Büyük Rakip)

| Özellik | Detay |
|---------|-------|
| **Model** | API Platform içinde mock server |
| **Fiyatlandırma** | Free (tek kullanıcı, Mart 2026'dan sonra), Basic ($19/kullanıcı/ay), Enterprise ($5K-$30K/yıl) |
| **Mart 2026 Değişikliği** | **Free plan artık single-user only** - takım işbirliği kaldırıldı! |
| **Mock Server** | Tüm planlarda unlimited mock server calls |
| **Öne Çıkan Özellikler** | Postman ekosistemi ile entegre, collection'dan mock generation, unlimited calls |
| **Zayıf Noktalar** | Free plan artık takım için kullanılamaz (BÜYÜK FIRSAT), mock server sadece Postman collection'ından çalışır, standalone ürün değil, ağır bir araç, frontend developer için fazla kompleks |
| **Fırsat** | Postman'in free takım planını kaldırması, küçük ekipler ve freelancer'lar için alternatif ihtiyacı yarattı |

### 2.5 MSW - Mock Service Worker (Developer Tool)

| Özellik | Detay |
|---------|-------|
| **Model** | Open-source library (JavaScript) |
| **Fiyatlandırma** | Tamamen ücretsiz |
| **Öne Çıkan Özellikler** | Service Worker tabanlı, browser + Node.js, runtime request interception, TypeScript desteği |
| **Zayıf Noktalar** | Kod yazmayı gerektirir (no-code değil), serverless/deploy edilebilir değil, her projede setup gerekir, non-JS ekipleri için uygun değil |
| **GitHub** | ~20K stars (en popüler) |

### 2.6 Stoplight Prism (OpenAPI-based)

| Özellik | Detay |
|---------|-------|
| **Model** | Open-source CLI + Cloud |
| **Fiyatlandırma** | Open-source free, Stoplight Cloud Basic ($44/ay) |
| **Öne Çıkan Özellikler** | OpenAPI spec'den otomatik mock generation, validation, transformation |
| **Zayıf Noktalar** | OpenAPI bilgisi gerektirir, frontend developer için fazla teknik, standalone mock deneyimi zayıf, cloud pahalı |
| **GitHub** | ~4.9K stars |

### 2.7 Diğer Rakipler

| Araç | Model | Not |
|------|-------|-----|
| **MockAPI.io** | SaaS | CRUD mock, basit UI, fiyatlandırma belirsiz |
| **MockAPI Dog** | Free SaaS | Product Hunt 2026, no signup, REST + LLM streaming mock |
| **Mocknica** | AI-Powered | Product Hunt Ara 2025, AI mock generation |
| **JSON Server** | Open-source | Basit JSON file -> REST API, ~62K stars ama çok temel |
| **MockServer** | Open-source | ~4.9K stars, Java-centric, enterprise testing odaklı |
| **Mountebank** | Open-source | Multi-protocol (HTTP, TCP, SMTP), niche kullanım |
| **Microcks** | Open-source | Kubernetes-native, contract-driven, DevOps odaklı |
| **Mockly.me** | AI-Powered | Product Hunt Nis 2025, prompt-to-mock |
| **MockNest Serverless** | AWS Native | Product Hunt Mar 2026, cloud-native teams için |
| **Fake API for Devs** | Vercel | Serverless, free, basit |
| **JSONing Mock API** | SaaS | Product Hunt Kas 2025 |

---

## 3. Fiyat Analizi

### Pazar Fiyat Haritası

| Segment | Araçlar | Fiyat Aralığı |
|---------|---------|---------------|
| **Free / Open-source** | MSW, JSON Server, Mockoon Desktop, WireMock OSS, Prism | $0 |
| **Bireysel (Micro-SaaS)** | Beeceptor Individual, Mockoon Solo, MockAPI.io | $10-$15/ay |
| **Küçük Takım** | Beeceptor Team, Mockoon Team | $24-$25/ay |
| **Orta Ölçek** | Beeceptor Scale | $99/ay |
| **Enterprise** | WireMock Enterprise, Postman Enterprise, Mockoon Enterprise | $5K+/yıl |

### Fiyatlandırma Pattern'leri

1. **Request-based:** Beeceptor (50 req/gün free, 15K-1M+ aylık), WireMock (1K free)
2. **Rule/Endpoint-based:** Beeceptor (3-500 rule), Mockoon (1-3 API mock)
3. **AI-usage based:** Mockoon (100-200 AI endpoint/ay)
4. **Kullanıcı-based:** Mockoon Team ($24/kullanıcı), Postman ($19/kullanıcı)

### Bizim İçin Fiyat Önerisi

Mevcut UniverseCreator ürünlerimizle uyumlu: **$19 one-time** veya **$9/ay**

- $19 one-time: Diğer ürünlerimizle aynı fiyat stratejisi
- $9/ay: Bireysel segment için rekabetçi (Beeceptor $10, Mockoon $10)
- **Öneri: $19 one-time** (UniverseCreator standardı)

---

## 4. Gap Analizi (Pazarda Ne Eksik)

### 4.1 En Büyük Gap: Scenario-Based Mocking

**Hiçbir araç "scenario-based" mocking'i birincil özellik olarak sunmuyor.**

Mevcut araçlar:
- **Rule-based:** Beeceptor, WireMock (if-this-then-that kuralları)
- **Static:** JSON Server, MockAPI.io (sabit response)
- **Spec-based:** Prism, Stoplight (OpenAPI'den üretim)
- **Code-based:** MSW (JavaScript kodu ile)

**Senaryo:** "Kullanıcı login olduğunda, eğer premium ise X response, değilse Y response, eğer token expired ise 401 dön"

Bu senaryoyu kurmak şu an ya kod yazmayı (MSW) ya da karmaşık rule chain'lerini (Beeceptor/WireMock) gerektiriyor. Frontend developer için çok karmaşık.

### 4.2 İkinci Gap: Postman Boşluğu

**Postman Mart 2026'da free takım planını kaldırdı.** Bu, küçük ekipler ve startup'lar için büyük bir boşluk yarattı. Alternatif arayan binlerce developer var.

### 4.3 Üçüncü Gap: Frontend-First Deneyim

Mevcut araçların çoğu QA/Backend developer'lar için tasarlanmış. Frontend developer'lar için:
- Görsel senaryo editörü YOK
- "Senaryoyu çiz" arayüzü YOK (flowchart gibi)
- Real-time preview YOK
- Frontend framework integration (React hooks, Vue composables) ZAYIF

### 4.4 Dördüncü Gap: AI-Powered Prompt-to-Mock

AI ile mock generation yeni emerging bir alan:
- Mocknica (Ara 2025) - AI-powered
- Mockly.me (Nis 2025) - prompt-to-mock
- MockNest (Mar 2026) - AI-powered
- Beeceptor ve Mockoon AI özellikleri ekliyor

**Henüz kimse dominant değil.** Bu alan yeni ve açık.

### 4.5 Beşinci Gap: Serverless + Custom Domain + Unlimited

- Beeceptor'da custom domain sadece Team planında ($25/ay)
- Mockoon Cloud'da Solo planında sadece 1 API
- WireMock free'de sadece 1K calls/ay
- **Serverless + sınırsız (veya çok yüksek limit) + custom domain + uygun fiyat kombinasyonu YOK**

---

## 5. Teknik Feasibility (Vercel Serverless)

### 5.1 Mimari Öneri

```
Frontend (Next.js) ──┬── Vercel Hosting (UI)
                      │
                      └── Vercel Edge Functions (Mock Router)
                             │
                             ├── KV Storage (senaryo tanımları)
                             ├── Postgres (kullanıcı, proje metadata)
                             └── Edge Cache (hot mock response'ları)
```

### 5.2 Vercel Serverless ile Yapılabilir Mi?

**EVET, yapılabilir.** Detaylar:

| Komponent | Vercel Karşılığı | Limit | Uygunluk |
|-----------|------------------|-------|----------|
| **Mock Router** | Edge Functions | 50ms cold start, 1024MB | MUKEMMEL - Edge'de routing çok hızlı |
| **Senaryo Storage** | Vercel KV (Upstash Redis) | 100MB, 40K op/s | MUKEMMEL - Düşük latency |
| **User/Project Data** | Vercel Postgres (Neon) | 500MB free | İYİ - Metadata için yeterli |
| **Static Mock Data** | Edge Config | 100KB | SINIRLI - Büyük mock datalar için yetersiz |
| **Custom Domain** | Vercel Domains | Unlimited | MUKEMMEL |
| **Rate Limiting** | Edge middleware | MUKEMMEL | İYİ |
| **AI Generation** | OpenAI API call | Token bazlı | İYİ - Serverless function'dan çağrılabilir |

### 5.3 Maliyet Analizi (Vercel Pro - $20/ay)

| Hizmet | Free Tier | Pro Kullanım | Aylık Maliyet |
|--------|-----------|--------------|---------------|
| Vercel Hosting | 100GB bandwidth | Paylaşılır | $20 (platform) |
| Vercel KV | 256MB | Paylaşılır | Dahil |
| Vercel Postgres | 500MB | Paylaşılır | Dahil |
| Edge Functions | 1M invocation/ay | Paylaşılır | Dahil |
| OpenAI API | - | ~$5-10 (AI generation) | $5-10 |

**Toplam aylık altyapı maliyeti: ~$25-30** (100 kullanıcıya kadar)

**$19 one-time x 100 kullanıcı = $1,900 gelir vs $30 maliyet = çok yüksek marj**

### 5.4 Teknik Riskler

| Risk | Seviye | Çözüm |
|------|--------|-------|
| Edge function cold start | Düşük | Vercel Edge = ~50ms, kabul edilebilir |
| Mock response latency | Düşük | Edge caching ile <100ms |
| Rate limit abuse | Orta | Edge middleware + KV ile rate limiting |
| Büyük mock data setleri | Orta | Postgres + pagination |
| Custom domain DNS | Düşük | Vercel otomatik yönetiyor |

---

## 6. Önerilen MVP Özellikleri

### 6.1 Core (MVP - İlk 2 Hafta)

1. **Senaryo Editörü (Visual)**
   - Flowchart-benzeri arayüz: "Durum -> Koşul -> Response"
   - Sürükle-bırak senaryo ağacı
   - JSON import/export

2. **Mock Endpoint Yönetimi**
   - GET/POST/PUT/DELETE/PATCH
   - Custom status code, headers, body
   - Path parametreleri ve query string matching

3. **Scenario Engine**
   - Conditional routing (if/else)
   - State machine (senaryo durumları)
   - Delay simulation (latency injection)
   - Error simulation (5xx, timeout)

4. **Fake Data Generation**
   - Faker.js entegrasyonu
   - Template-based response ({{firstName}}, {{email}})
   - AI prompt-to-mock (OpenAI API)

5. **Deployment**
   - Anında canlı endpoint (xxx.mockforge.dev/users)
   - CORS otomatik
   - Request log (son 100 request)

### 6.2 v2 Özellikleri (Sonraki 2 Hafta)

6. **Custom Domain**
   - api.myapp.com -> MockForge'a yönlendirme

7. **Team Collaboration**
   - Shared scenarios
   - Comment/annotation

8. **OpenAPI Import**
   - Swagger/OpenAPI spec'den mock generation
   - Postman collection import

9. **Webhooks & Events**
   - Request geldiğinde webhook trigger
   - Scenario state değiştirme via API

### 6.3 v3 Özellikleri (Gelecek)

10. **Recording Mode**
    - Gerçek API'yi kaydet -> mock'a çevir
    - Traffic inspection

11. **Contract Testing**
    - Mock vs gerçek API drift detection
    - Schema validation

12. **SDK/Integrations**
    - React hook: `useMockForge('scenario-name')`
    - VS Code extension
    - CLI tool

---

## 7. Pazar Büyüklüğü ve Talep

### 7.1 Talep Göstergeleri

| Gösterge | Değer | Kaynak |
|----------|-------|--------|
| MSW GitHub stars | ~20K | mswjs/msw |
| JSON Server GitHub stars | ~62K | typicode/json-server |
| WireMock GitHub stars | ~7K | wiremock/wiremock |
| Mockoon GitHub stars | ~8K | mockoon/mockoon |
| MockAPI Dog Product Hunt | 2026 launch | producthunt.com |
| Mocknica Product Hunt | Ara 2025 launch | producthunt.com |
| Mockly.me Product Hunt | Nis 2025 launch | producthunt.com |
| MockNest Product Hunt | Mar 2026 launch | producthunt.com |

### 7.2 Trend Analizi

- **2025-2026'da 5+ yeni mock API aracı** ProductHunt'a launch edildi
- **Postman free team plan'ı kaldırması** (Mart 2026) büyük bir pazar boşluğu yarattı
- **AI-powered mock generation** emerging bir trend (3 yeni araç 2025-2026)
- **Serverless yaklaşımı** henüz dominant değil - ilk mover avantajı var

### 7.3 Hedef Pazar

| Segment | Büyüklük | Ödeme İhtimali |
|---------|----------|----------------|
| Frontend developer'lar | ~20M worldwide | Orta |
| Indie hacker'lar | ~2M | Yüksek |
| Startup ekipleri (2-10 kişi) | ~500K | Yüksek |
| Freelancer'lar | ~5M | Orta |
| Agency'ler | ~100K | Yüksek |

---

## 8. Rekabet Avantajı (MockForge'un Farkı)

| Özellik | MockForge | Beeceptor | WireMock | Mockoon | MSW |
|---------|-----------|-----------|----------|---------|-----|
| Scenario-based | **EVET** | Hayır | Hayır | Hayır | Kod ile |
| Visual editor | **EVET** | Basit | Karmaşık | Desktop | Yok |
| AI prompt-to-mock | **EVET** | EVET | EVET | EVET | Hayır |
| Serverless | **EVET** | EVET | EVET | Hayır | Hayır |
| Free tier | **EVET** | EVET (50/gün) | EVET (1K/ay) | Desktop | Açık kaynak |
| Fiyat | **$19 one-time** | $10/ay | Custom | $10/ay | Free |
| Flowchart senaryo | **EVET (unique)** | Hayır | Hayır | Hayır | Hayır |
| Frontend-first | **EVET** | Hayır | Hayır | Hayır | Hayır |
| Postman alternatifi | **EVET** | Kısmen | Kısmen | Hayır | Hayır |

---

## 9. Riskler

| Risk | Seviye | Açıklama |
|------|--------|----------|
| **Beeceptor dominansı** | Orta | Beeceptor bu alanda en olgun SaaS, iyi bir product-market fit'i var |
| **Düşük fiyat beklentisi** | Yüksek | Birçok free alternatif var, ödeme yaptırmak zor |
| **Open-source alternatifler** | Orta | JSON Server (62K stars) temel ihtiyaçları bedavaya karşılıyor |
| **AI commodityleşmesi** | Düşük | AI mock generation hızla yaygınlaşıyor, unique feature kalmayabilir |
| **Teknik: Edge function limitleri** | Düşük | Vercel limitleri küçük ekipler için yeterli |
| **Pazar doymuşluğu** | Düşük | 5+ yeni araç 2025-2026'da launch etti ama kimse dominant değil |

---

## 10. Sonuç: BUILD edilmeli mi?

### KARAR: **EVET - BUILD edilmeli**

### Nedenleri:

1. **Gerçek Pazar Boşluğu Var:** Scenario-based mocking, visual editor ve frontend-first deneyim sunan bir ürün YOK. Beeceptor rule-based, WireMock enterprise-focused, Mockoon desktop-centric, MSW code-based.

2. **Postman Fırsatı:** Mart 2026'da Postman'in free takım planını kaldırması, alternatif arayan binlerce developer yarattı. Bu momentumu kaçırmamak lazım.

3. **Düşük Altyapı Maliyeti:** Vercel serverless ile ~$25-30/ay altyapı maliyeti. $19 one-time fiyatla 2 satışta bile break-even.

4. **UniverseCreator Ekosistemine Uygun:** Mevcut 19 ürün $19 one-time fiyat stratejisiyle uyumlu. Frontend developer'lar hedef kitlemizle örtüşüyor.

5. **AI Trend'i Yakalama:** AI prompt-to-mock emerging bir alan. Henüz dominant oyuncu yok. İlk mover avantajı var.

6. **Teknik Risk Düşük:** Vercel Edge Functions + KV + Postgres kombinasyonu bu kullanım için ideal. Cold start <50ms, edge routing <100ms latency.

### Dikkat Edilmesi Gerekenler:

1. **Free tier çok önemli:** JSON Server (62K stars) ve MSW (20K stars) tamamen free. Free tier olmadan adoption olmaz. Öneri: 500 req/ay free, limitsiz senaryo.

2. **Differentiation şart:** Sadece "bir mock API aracı daha" olmaz. **Scenario-based visual editor** ana farklılaştırıcı olmalı.

3. **Hızlı launch:** Bu alan hızlı hareket ediyor (5+ launch 2025-2026). 1 ay içinde MVP launch edilmeli.

4. **Postman alternatifi olarak pozisyonlama:** Marketing'de "Postman free plan bitti, işte alternatifi" mesajı güçlü olabilir.

### Önerilen Yol Haritası:

```
Hafta 1-2: MVP (Senaryo editörü + Mock router + Deploy)
Hafta 3: AI prompt-to-mock + Fake data
Hafta 4: Landing page + Launch
```

---

**Rapor Sonu**

### Kaynaklar

- [Beeceptor Pricing](https://beeceptor.com/pricing/)
- [Mockoon Pricing](https://mockoon.com/pricing/)
- [WireMock Cloud Pricing](https://www.wiremock.io/get-pricing)
- [Postman Pricing Changes 2026](https://dev.to/auden/postman-ends-free-team-plans-in-march-2026-here-is-the-free-alternative-i-switched-to-118p)
- [Top 9 API Mocking Tools 2025 - DEV](https://dev.to/moonlit1151/api-mocking-9-tools-compared-4e1a)
- [MockAPI Dog - Product Hunt](https://www.producthunt.com/products/mockapi-dog)
- [API Simulation Tools Comparison - BrowserStack](https://www.browserstack.com/guide/api-simulation-tools-comparison)
- [Top API Mocking Tools - Zuplo](https://zuplo.com/learning-center/top-api-mocking-tools/)
- [WireMock GitHub](https://github.com/wiremock/wiremock)
- [Mockoon GitHub](https://github.com/mockoon/mockoon)
- [MSW GitHub](https://github.com/mswjs/msw)
- [Prism GitHub](https://github.com/stoplightio/prism)
- [MockServer GitHub](https://github.com/mock-server/mockserver)
