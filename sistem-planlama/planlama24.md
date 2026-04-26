# Planlama #24 — Micro-SaaS & API-First Data Products Uygulama Haritası
**Tarih:** 2026-04-21 19:13 +03
**Bağlı Araştırma:** arastirma24.md

## Swarm Agent ile Nasıl Uygulanır?
UniverseCreator için doğru mimari **API Product Foundry v2**: araştırma, veri doğrulama, spec tasarımı, rapor üretimi ve API/MCP paketlemeyi tek lane’e bağlayan bir sistem.

Önerilen roller:
1. **Opportunity Miner**
   - Giriş: önceki `arastirma*.md`, Reddit/HN şikayetleri, `projeler.txt`, 113+ ürün health çıktıları, fiyat/pricing sayfaları, GTIP/HS verileri.
   - Çıkış: API/report adayları: persona, problem, veri kaynağı, risk, fiyat, demo output.
2. **Risk & Source Gate**
   - Green: customer-provided URL, public pricing page, public/open data, kendi ürün health data.
   - Yellow: scraping gerektiren ama public olan sayfalar, rate-limit riski.
   - Red: LinkedIn/Amazon/kapalı hesap/kişisel veri/TOS kırmızı alanlar.
3. **Spec Designer**
   - OpenAPI + JSON schema + typed error + sample response + freshness/evidence fields.
   - Koddan önce ürün sözleşmesi yazılır. Bu “API’nin PRD’si”.
4. **Batch-first Verifier**
   - İlk versiyon live API değil; manuel/batch CSV+PDF+JSON output.
   - Ama output, gelecekte API response olacak formatta üretilir.
5. **MCP Wrapper Curator**
   - OpenAPI’den MCP generate edilebilir ama sadece güvenli/değerli subset expose edilir.
   - Read-only default, düşük tool count, net tool descriptions.
6. **Usage & Cost Ledger**
   - Key/customer bazlı call count, success/fail, provider cost, freshness, latency, manual labor minutes.
   - API para kazandırıyor mu yoksa proxy maliyeti mi yakıyor, erken görülür.
7. **Docs & Distribution Publisher**
   - Docs, curl, Postman collection, n8n/Make örneği, “agent config snippet”, demo report.
8. **Sales/Feedback Loop**
   - İlk satış self-serve subscription değil: paid pilot / one-off report / managed monthly alert.
   - Müşteri feedback’i endpoint scope’unu küçültür, fiyatı keskinleştirir.

## Gerekli Bileşenler
- **Script/Bot:**
  - opportunity scoring sheet/generator
  - OpenAPI/spec template
  - sample JSON/report generator
  - source freshness checker
  - API usage ledger
  - pricing/cost calculator
  - docs and demo artifact generator
  - MCP wrapper checklist
- **MCP/Araç:**
  - Jina/curl: public docs/pricing/data source okuma
  - chrome-devtools-axi / Playwright: browser-required evidence, screenshot, console/network
  - ArXiv/MCPTube: API/MCP/testing pattern takibi
  - OpenAPI/Postman: machine-readable API dokümantasyonu
  - opsiyonel: `openapi-mcp-server`, Azure Data API Builder, Vulcan SQL gibi wrapper/data API örnekleri
- **API:**
  - Başlangıç: static/batch JSON endpoint veya manual key delivery; zorunlu değil.
  - Orta vade: Stripe usage-based billing veya Lago tarzı usage metering.
  - Marketplace: RapidAPI/APILayer sadece discovery/test; RapidAPI fee **%25 + payout fee** hesaba yazılmalı.
- **İnsan Müdahalesi:**
  - İlk ürün adayını seçme
  - risk sınıfı ve veri kaynağı onayı
  - fiyat/positioning kararı
  - ilk müşteri konuşmaları
  - ödeme/provider kısıtları nedeniyle ilk paid pilot teslimi

## Workflow Haritası
Araştırma çıktısı
→ 10 API/report adayı çıkar
→ risk/fırsat skoru ver
→ 3 adayı spec-first yaz
→ 1 adayı batch output ile demo üret
→ 5-10 hedef kişiye göster
→ ödeme/yanıt sinyali al
→ manuel monthly report veya paid pilot sat
→ stable response schema kesinleşirse API endpoint aç
→ usage ledger + docs ekle
→ OpenAPI + Postman collection + MCP wrapper çıkar
→ n8n/Make örneği ve weekly alert ekle
→ traction varsa self-serve pricing ve marketplace draft

### En uygun ilk 3 aday
1. **Checkout / Website Evidence API**
   - Input: URL listesi.
   - Output: HTTP status, screenshot/evidence URL, CTA/checkout var mı, console/network error özeti, freshness.
   - Neden iyi: UniverseCreator zaten portfolio health/audit pratiğine sahip. Legal risk düşük çünkü customer-provided URL.
   - Fiyat: $19 starter, $79 pro, $199 agency/managed.
2. **AI Tool & API Pricing Change Watch**
   - Input: provider/model/tool listesi.
   - Output: price delta, plan changes, context/limit, source evidence, weekly alert.
   - Neden iyi: Postman agent-ready API boşluğu + AI cost dashboard çizgisine yakın.
   - Risk: pricing page scraping kırılabilir; tazelik ve kaynak kanıtı şart.
3. **HS/GTIP Trade Snapshot API + Report**
   - Input: HS/GTIP code + country pair.
   - Output: import/export trend, tariff/risk note, buyer/supplier clues, evidence sources.
   - Neden iyi: yüksek B2B değer; fakat veri pipeline daha ağır. Önce report-first.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen uygulanacak şey:** Kod yazmadan önce **Checkout / Website Evidence API için spec + demo report** çıkar. Bu, mevcut portfolio health/audit hafızasına en yakın ve ödeme gelmeden altyapı yakmayan wedge.
- **En düşük çaba / en yüksek çıktı adımı:** 10 URL’lik demo veri setiyle tek sayfa “evidence report” üret: status, screenshot, checkout CTA, broken link, console/network clue, recommended fix. Aynı JSON gelecekte API response olur.
- **Hangi mevcut araç/script kısmen yapar?**
  - mevcut product health/audit deneyimi
  - Jina/curl
  - chrome-devtools-axi / Playwright screenshot
  - sistem-planlama araştırma hafızası
  - Vercel/product health çıktıları
- **Proof-of-concept minimum gereksinimler:**
  - 1 OpenAPI taslak dosyası
  - 3 sample JSON response
  - 1 PDF/Markdown demo report
  - fiyat hipotezi: $19/$79/$199
  - 20 hedef persona listesi: indie SaaS, Shopify ajansı, white-label otomasyon ajansı, küçük e-commerce seller
  - ödeme/provider hazır değilse “manual paid audit” olarak teslim planı
- **Tahmini kurulum süresi ve ilk gelir beklentisi:**
  - Spec + demo: **1-2 gün**
  - İlk 20 outreach: **2-3 gün**
  - Paid pilot realist hedef: **$29-$99 one-off** veya 1 managed müşteri adayı
  - MRR beklentisi: 1-2 haftada **$0-$200 MRR**; daha gerçekçi ilk hedef “ödeme niyeti ve canlı feedback”.
- **Bu hafta yapılacak karar:** API altyapısına atlamadan önce satış formatı seçilmeli: `one-off evidence audit` mi, `monthly monitoring` mi? İlk satış için one-off daha az sürtünmeli.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda:**
  - 1 productized report canlı: Checkout/Website Evidence Audit.
  - 1 machine-readable response schema + docs sayfası.
  - 10-30 potansiyel müşteriye gösterilmiş demo.
  - 1-3 paid pilot veya net pivot kararı.
- **2. ay sonunda:**
  - manual key/usage ledger
  - simple endpoint veya protected JSON delivery
  - OpenAPI spec + Postman collection
  - weekly alert/report template
  - ilk n8n/Make workflow örneği
- **3. ay sonunda:**
  - 2 API/report ürünü: Evidence API + AI Pricing Watch veya HS/GTIP Snapshot
  - MCP wrapper beta: sadece read-only, 3-5 tool
  - usage/cost dashboard
  - marketplace draft: APILayer/RapidAPI sadece test kanalı
- **Başarı metrikleri:**
  - demo-to-reply rate
  - paid pilot sayısı
  - report delivery time
  - cost per URL / cost per 1,000 checks
  - false positive rate
  - customer-visible freshness
  - API calls per active key
  - support minutes per customer
  - churn/cancel reason
- **Paralel çalışabilecek adımlar:**
  - spec yazımı
  - target list/outreach
  - demo report design
  - source/risk kontrol
  - pricing hypothesis
  - docs skeleton
  - sample MCP wrapper research
- **Ölçeklendirme gereksinimleri:**
  - reliable scheduler/queue
  - screenshot storage/evidence retention
  - customer key/plan registry
  - basic abuse/rate limit
  - status monitor
  - payment provider netleşmesi
  - TOS/legal risk checklist

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator bir **agent-ready data/API studio** olur. Research swarm fırsatı bulur, Spec Designer endpoint sözleşmesi çıkarır, Batch Verifier veri kalitesini doğrular, Sales Loop paid pilot satar, sonra API/MCP wrapper açılır.
- **Yan ürünler / yeni gelir kolları:**
  - Checkout/Website Evidence monthly monitoring: $19-$199/ay
  - AI Pricing Watch API/report: $19-$149/ay
  - HS/GTIP Snapshot report: $39-$499/report veya $199+/ay managed
  - n8n/Make templates: one-off $19-$99
  - white-label agency API: $300-$1,500/ay
  - MCP server bundle: API’lerin agent-tool versiyonu
  - data freshness/SLA upsell
- **Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek şey:**
  - Araştırma→spec→evidence→report→feedback→API→MCP aynı sistem içinde döner.
  - Çok ürünlü portföyden sürekli test verisi ve QA pratiği gelir.
  - Her response kanıt ve freshness taşır; “LLM dedi” değil, “source + timestamp + evidence” satılır.
  - API’ler agent-ready tasarlanır: typed errors, predictable schema, narrow tools, scoped keys.
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet, ama 3 aşamada:
    1. report-first paid pilot
    2. managed monthly monitoring/API
    3. self-serve portal + marketplace + MCP catalog
- **3-12 ay evrim sırası:**
  1. 1 proof report
  2. 3 paid pilots
  3. 1 endpoint + manual key
  4. usage ledger + docs
  5. MCP wrapper
  6. second data product
  7. API catalog
  8. white-label/agency tier

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:**
  - spec/demo report: **1-3 gün**
  - paid pilot loop: **1-2 hafta**
  - live API POC: **2-4 hafta**
  - API catalog v1: **2-3 ay**
- **Aylık İşletme Maliyeti:**
  - batch/report-first: **$0-$30/ay**
  - screenshot/browser evidence: **$20-$100/ay** küçük kullanımda
  - external data APIs kullanılırsa: SerpApi **$25-$275+**, Firecrawl **$16-$333+**, ScreenshotOne **$17-$259+** bandı
  - marketplace fee: RapidAPI örneğinde **%25 + payout fee**
- **Potansiyel Gelir:**
  - one-off audit: **$29-$99**
  - starter monitoring/API: **$19-$49/ay**
  - pro: **$79-$149/ay**
  - managed/agency: **$299-$1,500/ay**
  - high-value trade/report: **$39-$499/report**
- **ROI Beklentisi:**
  - Report-first modelde 1 satış bile maliyeti kapatır.
  - Live API altyapısı için break-even hedefi: 3-5 paying customers veya $150-$300 MRR.
  - Eğer 30 hedef kişiden 0 paid pilot çıkarsa ürün değil distribution/problem yanlış; endpoint yazmaya devam etmek aptalca olur.

## Mevcut Sistemle Entegrasyon
- UniverseCreator’ın 113+ ürün ve health/audit hafızası **Evidence API** için doğal test yatağı.
- Araştırma döngüleri zaten pazar/kaynak topluyor; bunlar API aday havuzuna çevrilebilir.
- `sistem-planlama` dosyaları ürün discovery veri tabanı gibi kullanılabilir: her araştırmadan 1 API/report adayı çıkar.
- Browser otomasyon stack’i screenshot/evidence/report üretiminde kullanılır; ama operasyon deterministic kalmalı, AI sadece fallback/yorumlayıcı.
- Payment provider hâlâ kısıtlıysa API self-serve yerine manual report/iyzico Link/Lemon unblock sonrası satış daha mantıklı.

## Riskler & Dikkat Edilecekler
- **Commodity API riski:** Generic screenshot/scrape/search API alanı kalabalık. Vertical workflow ve evidence/report farkı yoksa ürün ezilir.
- **Marketplace marjı:** RapidAPI gibi kanallar fee yer; ilk kanal direct satış ve targeted outreach olmalı.
- **Payment blokeri:** Self-serve subscription ödeme altyapısı hazır değilse API portal kurmak zaman israfı. Paid report-first daha iyi.
- **Legal/TOS riski:** Kapalı platform scraping gelir getirse bile sistemi öldürecek risk taşır. Kırmızı kaynaklar yasak.
- **Cost runaway:** Browser/screenshot/LLM çağrıları metering olmadan satılırsa zarar edilir.
- **Agent abuse/security:** AI agent’lar yüksek frekansta çağrı yapabilir. Rate limit, scoped key, alert şart.
- **LLM validation halüsinasyonu:** Reddit/LLM idea scoring kanıt değil; gerçek ödeme sinyali olmadan inşa yok.
- **Tool count şişmesi:** MCP wrapper’da 50 endpoint açmak kötü fikir. 3-5 güvenli tool ile başla.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Checkout / Website Evidence API için 1 sayfalık OpenAPI-style spec ve 3 sample response yaz.** Endpoint, fields, error model, quota ve pricing hipotezi net olsun.
2. **10 URL’lik demo evidence report üret ve satış sayfası copy’si tasarla.** “Broken checkout / missing CTA / evidence screenshot / fix priority” formatı business buyer’a anlatılır olsun.
3. **20 hedef kişilik mikro-outreach listesi çıkar ve paid pilot teklifini yaz.** Tek teklif: “$49 one-off website checkout evidence audit; beğenirsen monthly monitoring.” MRR masalı değil, ilk para sinyali.
