# Araştırma #30 — Ticari İstihbarat & HS Codes (3. tur / 2026 tarife şoku doğrulaması)
**Tarih:** 2026-04-21 22:50
**Konu:** Ticari İstihbarat & HS Codes — GTIP/HTS/HS bazlı pazar fırsatı, tarife şoku, buyer/supplier discovery ve compliance-safe rapor ürünü

**Kaynaklar:**
- Yerel katalog: `/home/gokhan/UniverseCreator/projeler.txt` keyword taraması (`gtip|hs code|tariff|customs|trade data|import|export|buyer|supplier`) — doğrudan trade-intelligence ürünü zayıf; browser/scraping/API kası dolaylı kaldı.
- ddgr web araması: `GTIP HS codes trade intelligence import export buyer data 2025 2026`, `HS code trade data API customs tariff market intelligence 2025`, `ImportGenius Volza Panjiva trade data pricing HS code 2025 case study` — bu ortamda boş sonuç döndürdü; web/Jina fallback kullanıldı.
- UNCTAD — Global trade to hit record $35T in 2025: https://unctad.org/news/global-trade-hit-record-35-trillion-despite-slowing-momentum
- WTO — March 2026 Global Trade Outlook: https://www.wto.org/english/news_e/news26_e/stat_19mar26_329_e.htm
- WTO/ITC/UNCTAD — World Tariff Profiles 2025: https://www.wto.org/english/res_e/publications_e/world_tariff_profiles25_e.htm
- WCO — Harmonized System overview: https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
- UN Comtrade pricing/licensing: https://shop.un.org/databases
- U.S. Census API — Monthly U.S. Imports by HS: https://api.census.gov/data/timeseries/intltrade/imports/hs.html
- USITC — Harmonized Tariff Schedule: https://hts.usitc.gov/
- CBP — Tariff Classification informed-compliance publication: https://www.cbp.gov/document/publications/tariff-classification
- ImportGenius pricing: https://www.importgenius.com/pricing
- ImportGenius HS code enrichment launch: https://www.importgenius.com/press-releases/importgenius-unlocks-ai-powered-hs-code-search-for-global-trade-teams
- Volza pricing/search snippets: https://www.volza.com/pricing/ and https://www.volza.com/global-trade-data/plan/exclusive-to-sme-corporate/
- TariffCenter.AI / TariffAI snapshot via Jina + chrome-devtools-axi + Botasaurus: https://www.tariffcenter.ai/
- DutyDecoder HS finder page: https://dutydecoder.com/hs-code-finder/
- GitHub — datasets/harmonized-system: https://github.com/datasets/harmonized-system
- GitHub — uncomtrade/comtradeapicall: https://github.com/uncomtrade/comtradeapicall
- GitHub — SupplyGraphAI/supplygraph-ai: https://github.com/SupplyGraphAI/supplygraph-ai
- GitHub — gattuzzo0/hscode_predictor: https://github.com/gattuzzo0/hscode_predictor
- GitHub search results: `hscode`, `customs tariff`, `HTS classification`, `trade compliance agent`, `UN Comtrade API`.
- ArXiv: Explainable Product Classification for Customs (`2311.10922`), Multimodal Approach for HS Code Prediction (`2406.04349`), Industrial HS Code Prediction (`2602.17102`), ATLAS HTS benchmark (`2509.18400`), GraphFC customs fraud (`2305.11377`).
- MCPTube/YouTube: Zonos HS AI classification (`AM1X5z2GGn4`), Abu Dhabi Customs Smart HS Classification (`EA25vMFLb-U`), Harmonize HTS Classifier for Shopify (`zjfkyl_SV3U`), HS Code complete guide (`Inr1qOd6-BA`).
- Reddit JSON API: r/CustomsBroker, r/supplychain, r/logistics, r/smallbusiness, r/Entrepreneur, r/ImportYeti, r/AmazonFBATips.

## Özet Bulgular

- **2026'da fırsat sadece “GTIP pazar raporu” değil, “tarife şoku + fırsat + buyer map” paketi.** UNCTAD 2025 global trade’in ilk kez **$35T üstüne** çıkacağını, 2025’te yaklaşık **%7 / $2.2T** büyüme beklediğini yazıyor. WTO ise 2025 dünya mal ticareti hacmini **%4.6** artmış gösterip 2026 baz senaryosunu **%1.9**’a indiriyor. Yani hacim büyük, ama belirsizlik de para ediyor.
- **HS/HTS sınıflandırma hâlâ yüksek riskli yarı-otomasyon işi.** WCO HS’nin 200+ ülke/ekonomi tarafından gümrük tarifesi ve ticaret istatistiği temeli olarak kullanıldığını söylüyor. Ama Reddit customs broker topluluğu AI classifier’lara güvenmiyor: örnek bir AI tool “var olmayan”/uyumsuz kod verdiği için eleştiriliyor; broker’lar USITC HTS + CBP ruling/ICP’ye dönüyor.
- **AI doğru yerde kullanılınca güçlü, yanlış yerde hukuki mayın.** ArXiv tarafında top-3/top-5 başarılar yüksek: KCS explainable classifier top-3 **%93.9**, multimodal çalışma top-3 **%93.5 / top-5 %98.2**, industrial serverless çalışma **%98** accuracy iddia ediyor. Ama ATLAS benchmark 10 haneli HTS’de yalnız **%40** full correctness ve 6 haneli **%57.5** veriyor. Sonuç: 6 hane öneri + kaynak + insan QA; 10/12 hane kesinlik iddiası yok.
- **Pazarın ücret çıpası yüksek; düşük bilet rapor hâlâ mantıklı.** ImportGenius self-serve fiyatı **$229/mo** ve **$449/mo**, global enterprise başlangıcı **$1,999/mo**. UN Comtrade premium **$2,000/yıl** individual, özel sektör kurumsal **$12,000/yıl**. KOBİ/ajans için $39-$199 arası kaynaklı snapshot hâlâ boşluk.
- **Yeni wedge: “Tariff Exposure & Refund/Route Watch”**. TariffCenter gibi yeni oyuncular $19/mo ile HS lookup, landed cost, change alerts, refund tracker ve AI chat satıyor. Bu vendor iddiaları bağımsız doğrulama değil; ama ürün yönü net: sadece sınıflandırma değil, **sürekli değişen tarife kararını işletme diline çevirme**.

## Gerçek Başarı Hikayeleri

### 1) ImportGenius — HS kodunu lead/sourcing zekâsına çeviren ücretli platform
- Güncel pricing sayfası: **USA Essentials Flex $229/mo**, **USA Pro Flex $449/mo**, **Global Enterprise $1,999/mo** starting price.
- Essentials: 25 search/day, 1,000 row/month download, son 12 ay U.S. import data.
- USA Pro: 50 search/day, 1,000 row/month, U.S. import 2006-present, AI-powered Genius Company Profiler + HS code search.
- Enterprise: 25+ ülke shipment data, unlimited encrypted searches, custom limits, research/data-science team ve API delivery.
- 2025 press release: 2024-2025 U.S. import kayıtlarının yaklaşık **%70**’i HS kodla zenginleştirilmiş; yalnız **%80+ confidence** tahminleri gösteriliyor, düşük confidence’ta HS4/HS2’ye fallback var.
- Ders: Bu pazar “kod bulucu” değil; HS kodu **buyer search, competitor mapping, procurement, market intelligence** gateway’i.

### 2) ImportYeti — public bill-of-lading datasının community validation’ı
- 2020 r/Entrepreneur launch postunda araç **70M bill of lading** üzerinde ücretsiz arama sunuyordu; yorumlar FBA/supplier discovery talebini net gösterdi.
- 2024 r/logistics güncellemesinde kurucu **155+ görüşme** ve **300+ ürün değişikliği** yaptığını yazdı; kullanıcılar consolidation, logistics sales ve India handicraft exporter kullanımını anlattı.
- r/ImportYeti’de bir kullanıcı HS-code-level data için ödeme isteğini açık söyledi: “HS code 2912 için B/L bilgisi alabilir miyim, shipment value nerede, legal mi?”
- Ders: Kullanıcı ürünü dashboard diye değil, “hangi şirket kiminle alıp satıyor?” cevabı için istiyor. Bu cevap pazar fırsatı + lead listesi + outreach paketine dönüşür.

### 3) TariffCenter.AI / TariffAI — yeni nesil düşük fiyatlı tarife intelligence sinyali
- Browser + Botasaurus snapshot: sayfa kendini “tariff command center” olarak konumluyor; başlangıç **$19/mo**, 7 günlük trial.
- Sayfada görünen ürün modülleri: photo/text HS classification, confidence score, official-source cited AI chat, tariff change alerts, refund tracker, landed cost, supplier switch ROI, API access.
- Snapshot iddiaları: **29,794 HTS codes**, **1,946 tariff actions**, **2,846 policy documents**, live rate updates; misclassification penalty vendor iddiası **$20K-$50K**.
- Ders: Pazar artık “tek seferlik HS lookup”tan “tarife değişim işletim sistemi”ne kayıyor. Bizim rapor ürünü buna aylık watchlist upsell eklemeli.

### 4) SupplyGraph AI — agentic trade compliance mimarisi yön sinyali
- GitHub repo düşük yıldızlı ama konu çok doğru: customs classification, tariff calculation, trade compliance, multi-tier supply chain risk intelligence.
- Agent library içinde **Customs Classification Agent**, **U.S. Tariff Calculation Agent**, **Due Diligence Agent**, **Corporate Exception Agent** gibi roller var.
- Repo A2A/MCP dokümantasyonu ve SDK örneği veriyor; bu, UniverseCreator swarm için doğru mimariyi doğruluyor: tek model değil, specialized agent chain + source-linked evidence.

### 5) Shopify/commerce mini-app sinyali
- Harmonize HTS Classifier videosu: Shopify ürünlerini HS/HTS kodla sınıflandırıyor, confidence score gösteriyor, **73,000+ CBP customs rulings** analizine dayandığını söylüyor, bulk classification ve product metafield storage anlatıyor.
- Bu gelir rakamı değil, ama vertical wedge net: Shopify/WooCommerce/FBA satıcıları için “catalog HS audit + landed cost risk” küçük ama satılabilir paket.

## Pazar Büyüklüğü & Fırsat

### Makro hacim
- **UNCTAD:** 2025 global trade ilk kez **$35T+**, yaklaşık **%7** büyüme ve **$2.2T** ek hacim beklentisi. East Asia, Africa ve South-South trade güçlü; manufacturing/electronics ana motor.
- **WTO:** 2025 world merchandise trade volume **%4.6** arttı; 2026’da baseline **%1.9**, 2027’de **%2.6** bekleniyor. AI-enabling goods 2025’te **$4.18T**’a çıktı ve global trade growth’un **%42**’sini oluşturdu.
- **World Tariff Profiles 2025:** 170+ ülke/customs territory için tariff + non-tariff measure profilleri.
- **WCO:** HS, 200+ ülke/ekonomi tarafından gümrük tarifesi ve trade statistics temeli olarak kullanılıyor.

### Veri / lisans ekonomisi
- **UN Comtrade:** Premium Individual **$2,000/yıl**, Institutional Pro 1 **$6,000/yıl**, private-sector Pro 2 **$12,000/yıl**. API/Batch/Bulk individual planda **5,000 query/day**, institutional planda unlimited. Re-dissemination ayrıca kurallı; data extraction için kullanıcıların da premium subscriber olması gerekebilir.
- **ImportGenius:** $229/$449/$1,999 aylık fiyat çıpası. AI HS search self-serve Pro ve Enterprise’da değerli özellik olarak paketleniyor.
- **Volza:** Arama snippet’leri 203 ülke, 3.5B+ shipment database, buyer/supplier/price trend/LinkedIn profile yönünü doğruluyor; Jina fetch Cloudflare 504 verdiği için sayfa içeriği sınırlı doğrulandı.

### Somut ücretsiz veri örneği — U.S. Census API, Turkey → U.S. imports, 2026-02
U.S. Census Monthly Imports by HS API’dan `CTY_CODE=4890` ile çekildi. Bu şirket-level data değil; ama pazar/tarife snapshot için yeterli sinyal. “Yaklaşık efektif duty” burada `CAL_DUT_MO / GEN_VAL_MO`; resmi tarife oranı değil, analiz oranı.

| HS | Ürün kısa açıklaması | 2026-02 General Import Value | 2026 YTD Value | 2026-02 Calculated Duty | Yaklaşık duty/value |
|---|---|---:|---:|---:|---:|
| 570242 | MMF pile carpets | $56,535,522 | $107,415,249 | $7,167,911 | %12.7 |
| 870899 | Motor vehicle parts/accessories | $4,873,406 | $12,876,674 | $900,757 | %18.5 |
| 610910 | Cotton knit T-shirts | $3,062,808 | $6,650,531 | $927,123 | %30.3 |
| 940360 | Wooden furniture, nesoi | $2,226,099 | $4,768,631 | $361,645 | %16.2 |
| 392410 | Plastic table/kitchenware | $1,875,505 | $3,578,813 | $330,633 | %17.6 |
| 080222 | Shelled hazelnuts | $587,297 | $931,273 | $54,150 | %9.2 |
| 850440 | Static converters / power supplies | $608,906 | $765,741 | $90,760 | %14.9 |
| 732393 | Stainless steel table/kitchen articles | $51,806 | $93,645 | $24,579 | %47.4 |

**Fırsat yorumu:** Halı hâlâ en güçlü demo lane. Ama 2026 turunda yeni sinyal şu: T-shirt, stainless kitchenware, plastic tableware ve furniture gibi HS’ler “opportunity” kadar **tariff pain** satıyor. Bu raporun adı sadece Opportunity Snapshot değil, **GTIP Tariff Exposure Snapshot** olmalı.

## Rakipler & Boşluklar

### Rakip kümeleri

1. **Enterprise shipment intelligence:** ImportGenius, Volza, Panjiva/S&P, Datamyne, PIERS.
   - Güçlü: company-level shipment records, buyer/supplier, trend, export, alerts.
   - Zayıf: pahalı, onboarding ağır, KOBİ için fazla geniş; lisans ve data interpretation yükü kullanıcıya kalıyor.

2. **Resmi veri araçları:** WCO, WTO Tariff Profiles, U.S. Census API, USITC HTS, CBP rulings/ICP, UN Comtrade, WITS/Trade Map.
   - Güçlü: authoritative ve ücretsiz/ucuz.
   - Zayıf: dağınık, teknik, karar çıktısı üretmiyor; küçük ihracatçı “kime ne satayım?” cevabını alamıyor.

3. **AI HS finder / landed-cost araçları:** DutyDecoder, TariffCenter, hscodefinder.ai, Shopify HTS apps, Zonos tarzı classifier’lar.
   - Güçlü: hızlı first-pass, confidence, e-commerce entegrasyonu.
   - Zayıf: customs broker topluluğu güvenmiyor; bazı araçlar hatalı/ülkeye uyumsuz kod verebiliyor. Kaynak + human QA olmadan tehlikeli.

4. **Open-source / developer layer:** datasets/harmonized-system, uncomtrade/comtradeapicall, hscode_predictor, UK trade-tariff-backend, SupplyGraph AI.
   - Güçlü: başlangıç veri sözlüğü ve agent pattern’i var.
   - Zayıf: production-grade data coverage, legal updates ve usability hâlâ boş.

### Açık boşluklar

- **Türkçe/GTIP karar paketi boşluğu:** Türkiye KOBİ’si için “ürün → GTIP/HS adayları → ABD/EU/Gulf fırsat → duty/risk → buyer arama sorguları → outreach metni” şeklinde tek sayfalık net ürün yok.
- **Tariff shock watch boşluğu:** 2025-2026 tarife oynaklığı small business Reddit’te doğrudan panik yaratıyor. İnsanlar dashboard değil, “bu karar benim HS’imi vuruyor mu?” cevabı istiyor.
- **AI güven boşluğu:** Customs broker’lar “AI ile classify etme” diye bağırıyor; bu bizim avantajımız. Ürünü “AI customs broker” diye satmak aptallık olur. Doğru pozisyon: **source-linked analyst assist + broker-ready evidence pack**.
- **Low-ticket entry boşluğu:** $229-$1,999/mo platforma giremeyen KOBİ için $39-$199 arası “first pass + watchlist + next actions” paketi daha kolay satılır.
- **Buyer discovery translation gap:** Public/paid shipment data var ama kullanıcı bunu CRM/outreach planına çeviremiyor.

## Teknik Gereksinimler

### Veri katmanı
- WCO HS + açık HS sözlüğü (`datasets/harmonized-system`) — 2/4/6 digit taxonomy.
- Türkiye GTIP / Ticaret Bakanlığı / BTI uyarı katmanı — 12 haneli yerel yapı ve “final authority” notu.
- U.S. Census HS imports API — ücretsiz demo ve U.S. market snapshot.
- USITC HTS + CBP rulings/ICP — ABD duty/classification evidence.
- WTO Tariff Profiles / UNCTAD / UN Comtrade / WITS — macro ve ülke karşılaştırma.
- Opsiyonel paid: ImportGenius/Volza/Panjiva — yalnız satış doğrulanınca company-level list için.

### Agent pipeline
1. **Intake Agent** — ürün açıklaması, mevcut GTIP, hedef pazar, müşteri tipi ve amaç (`opportunity`, `tariff shock`, `buyer map`, `catalog audit`) alır.
2. **HS Hypothesis Agent** — 2/4/6 digit adayları + confidence + alternatifler üretir; kesin hüküm vermez.
3. **Official Evidence Agent** — WCO/USITC/CBP/Census/WTO/UN kaynaklarını toplar, tarih ve URL bağlar.
4. **Tariff Exposure Agent** — calculated duty/value, MFN/additional duty, policy-change ve refund/watch riskini özetler.
5. **Market Opportunity Agent** — hacim, YTD trend, ülke/ürün yoğunluğu ve rekabet/route sinyali çıkarır.
6. **Buyer/Supplier Map Agent** — paid data yoksa query pack; varsa company list + CSV + outreach segmentation.
7. **Compliance QA Agent** — “legal/tariff advice değil”, customs broker/authority final, lisans/redistribution sınırı, hallucination check.
8. **Composer Agent** — PDF/Markdown/CSV teslim paketi, 3 aksiyon, 3 outreach mesajı ve upsell önerisi.

### Araç / maliyet notu
- Ücretsiz POC: Census API + USITC/CBP + WCO/WTO + Jina + browser + manuel QA.
- Düşük maliyet: token + browser/runtime; rapor başı dış API maliyeti sıfıra yakın.
- Paid data eşiği: en az **3-5 ücretli rapor** veya 1 agency paketi satılmadan ImportGenius/Volza alınmamalı. Aksi hâlde $229/mo bile boşuna yanar.

## Ham Notlar

- ddgr bu tur da boş döndü; web.run + Jina + Reddit JSON + GitHub daha verimliydi.
- `projeler.txt` doğrudan GTIP/HS ürünü vermedi; bu kötü değil. İçerideki kaldıraç veri/scraping/browser automation kası.
- Reddit r/CustomsBroker 2026-03-19 postu CBP 5106/OCR/AI classification’ın “Customs Business” sayılabileceği tartışmasını taşıyor. Bu hukuki çizgi önemli: ürün dışarıya classification filing yapmamalı; sadece analyst pack üretmeli.
- r/supplychain 2025-09-06 postu “10,000 ton çelik kimin aldığı neden bu kadar zor?” diye soruyor; yorumlar veri duvarı/paywall gerçeğini söylüyor. Bu bizim buyer-map ürününü doğruluyor.
- r/smallbusiness 2025-08-24 ve 2025-10-26 tariff postları tarife riskini soyut compliance probleminden günlük işletme krizine çevirmiş.
- Zonos videosu kritik mimari prensip verdi: universal 6 digit daha sabit; ülke-specific uzantılar çok daha dinamik. Sistemde `HS-6 core` ile `country extension / tariff layer` ayrı tutulmalı.
- MCPTube HS guide: HS kodu vergi, clearance, agreement eligibility, restricted goods ve statistics için tek omurga. Hata; fines, holds, overpayment ve delays demek.
- Chrome/Botasaurus TariffCenter snapshot’ı product direction açısından değerli ama vendor iddiaları bağımsız gerçek gibi yazılmamalı. Kullanım: feature benchmarking.
