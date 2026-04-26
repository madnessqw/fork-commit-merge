# Araştırma #2 — Ticari İstihbarat & HS Codes
**Tarih:** 2026-04-21 03:47
**Konu:** Ticari İstihbarat & HS Codes — trade data scraping, B2B outreach automation, ihracat/ithalat verileri, GTIP/HS rapor ürünü

**Kaynaklar:**
- WCO — Harmonized System overview: https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
- Türkiye Ticaret Bakanlığı — GTIP / Binding Tariff Information FAQ: https://www.trade.gov.tr/customs-formalities/frequently-asked-questions/tariff
- UNCTAD — global trade 2024: https://unctad.org/news/global-trade-hits-record-33-trillion-2024-driven-services-and-developing-economies
- UNCTAD — Key statistics and trends in international trade 2024: https://unctad.org/publication/key-statistics-and-trends-international-trade-2024
- UN Comtrade pricing/licensing: https://shop.un.org/lec/node/55
- ITC Trade Map FAQ: https://www.trademap.org/stFAQ.aspx
- WITS database coverage: https://wits.worldbank.org/wits/witshelp/content/Basics/A4.Database_Content_Coverage.htm
- U.S. Census HS import API: https://api.census.gov/data/timeseries/intltrade/imports/hs.html
- U.S. International Trade Administration FTA Tariff Tool: https://www.trade.gov/fta-tariff-tool-search
- ImportGenius lead-generation page/pricing: https://www.importgenius.com/trade-data-for-lead-generation
- ImportGenius pricing: https://www.importgenius.com/pricing
- Volza pricing/features: https://www.volza.com/pricing/
- Fortune Business Insights — Trade Management Software Market 2026–2034: https://www.fortunebusinessinsights.com/trade-management-software-market-106816
- Reddit / ImportYeti initial launch: https://www.reddit.com/r/Entrepreneur/comments/hvfgm1
- Reddit / ImportYeti V9 logistics post: https://www.reddit.com/r/logistics/comments/1d9lz3p
- IndieHackers / Proxycurl cold email to $100k MRR: https://www.indiehackers.com/post/how-cold-emailing-grew-my-b2b-startup-to-100k-mrr-62393f7911
- IndieHackers / Cyberleads to $50k MRR: https://www.indiehackers.com/post/how-cyberleads-grew-to-50k-mrr-from-building-in-public-137215f230
- ArXiv: Explainable Product Classification for Customs: https://arxiv.org/pdf/2311.10922v1
- ArXiv: Multimodal Approach for Harmonized System Code Prediction: https://arxiv.org/pdf/2406.04349v1
- ArXiv: Classification of Goods Using Text Descriptions: https://arxiv.org/pdf/2111.01663v1
- ArXiv: Customs Import Declaration Datasets: https://arxiv.org/pdf/2208.02484v3
- ArXiv: GraphFC customs fraud detection: https://arxiv.org/pdf/2305.11377v2
- ArXiv: ATLAS HTS classification benchmark: https://arxiv.org/pdf/2509.18400v1
- MCPTube videoları: Volza Search Tutorial (`WQ3__Rlukdw`), ITA Customs Info Database (`oQOb3RfpK9Y`), Murat Ozturker AI Import-Export 2025 (`t7YfIaSyaS0`), ImportGenius app tutorial (`HLvI3nZIlT4`).

## Özet Bulgular

- **HS/GTIP küçük bir kod gibi görünüyor ama para burada.** WCO'ya göre Harmonized System, gümrük tarifeleri ve ticaret istatistikleri için 200+ ülke/ekonomi tarafından kullanılıyor. Türkiye'de GTIP 12 haneli: ilk 6 hane HS, 7-8 AB Combined Nomenclature, 9-10 ulusal alt açılım, 11-12 istatistik kodu.
- **Pazar devasa, kullanıcı problemi basit:** UNCTAD 2024 global ticareti yaklaşık **$33T**, bunun mal ticaretini yaklaşık **$25T** olarak veriyor. Kullanıcının istediği şey dashboard değil: “Bu ürünü kime, hangi ülkede, hangi gümrük riskiyle satabilirim?”
- **Veri var ama dağınık ve lisanslı.** Trade Map / WITS / Census gibi resmi kaynaklar analiz için güçlü; şirket seviyesinde alıcı-satıcı datası çoğu ülkede paywalled veya yasal olarak sınırlı. UN Comtrade premium bireysel planı **$2,000/yıl**, private-sector institutional planı **$12,000/yıl**; re-dissemination ayrıca kurallı.
- **AI sınıflandırma yardımcı olur, tek başına güvenilir “gümrük kararı” değildir.** Akademik modeller HS-6 önerisinde top-3 seviyesinde %93–95 bandına çıkabiliyor; fakat 10 haneli HTS/GTIP tam sınıflandırma hâlâ zor. 2025 ATLAS benchmark'ında fine-tuned 70B model bile 10 haneli tam doğrulukta **%40** veriyor. Bu işte disclaimer + insan kontrolü şart.
- **İlk ticari ürün “dashboard” değil, rapor olmalı.** En hızlı para: HS/GTIP bazlı **Opportunity Snapshot PDF**: pazar büyüklüğü, son trend, potansiyel hedef ülke, tarifeler, riskler, alıcı/satıcı arama stratejisi, outreach mesajları. Paket fiyatı $19/$39/$79/$499 mantıklı; çünkü ImportGenius gibi platformlar $199–$1,999/mo seviyesinde.

## Gerçek Başarı Hikayeleri

### 1) ImportYeti — public bill of lading datasından viral ürün
- Kurucu Reddit'te 2020'de ImportYeti'yi “70,000,000 bill of ladings” üzerinde ücretsiz arama aracı olarak tanıttı.
- İlk postlarda FBA/e-commerce kullanıcıları supplier bulmak için yoğun beta talebi gösterdi; değer önerisi netti: Alibaba'da kör mail atmak yerine gerçek tedarikçi bağlantılarını görmek.
- 2024 logistics postunda ürün **150,000,000 public shipping records** aradığını, 155+ logistics kullanıcısıyla konuşulduğunu ve 300+ değişiklik yapıldığını söylüyor.
- Ders: Gelir rakamı açık değil ama pazar sinyali güçlü. İnsanlar bu veriyi “merak” için değil; supplier discovery, competitor mapping ve logistics sales için istiyor.

### 2) ImportGenius — trade data doğrudan lead generation ürünü
- ImportGenius sayfası value prop'u açık yazıyor: high-value shipper'ları dakikalar içinde bul, shipment activity ile outreach zamanla, verified contacts export et.
- Kendi sayfasındaki sayılar: **10,000+ teams**, **2B+ customs records**, **21/25+ tracked countries** ifadeleri, **7,500+ active users**.
- Açık pricing: USA Essentials Flex **$199–$229/mo**, USA Pro Flex **$399–$449/mo**, Global Enterprise **$1,999/mo** starting price. Global datasets starting price **$199**, annual commit ile %20 tasarruf mesajı var.
- Sayfada logistics sales için güçlü sosyal kanıt var: “70% of our leads come from ImportGenius”, close rate doubled, multiple six-figure clients gibi müşteri ifadeleri.
- Ders: Trade data sadece “istatistik” değil; iyi paketlenirse outbound sales intelligence olur.

### 3) Volza — workflow'un kendisi bizim report formatını gösteriyor
- Volza tutorial'ı üç arama modu anlatıyor: global search, country-specific search, universal search.
- Arama kriterleri: product name, HSN code, consignee name, shipper name; subfilter, save/workspace, last 3 years summary.
- Pricing/features sayfasında free trial + Startup + SME + Corporate ayrımı var; SME/Corporate için **203 countries**, unlimited fair-use search, full shipment view, LinkedIn contact profile gibi alanlar görünüyor.
- Ders: Kullanıcının istediği şey “HS gir → alıcı/satıcı ve shipment summary gör”. Biz ilk aşamada bunu manuel/yarı otomatik rapora çeviririz.

### 4) ITA Customs Info Database — resmi tarifeyi ürüne bağlama akışı
- ITA videosu workflow'u net: ülke seç → HS veya keyword gir → classification hierarchy gör → duties/taxes tabında hesapla → tariff treatment ve incoterm bazını kontrol et.
- Önemli uyarı: ithalatçı ülkenin customs office'i HS kodu ve vergilerde final authority. Bu bizim raporlarda “analyst assist, legal/tariff advice değil” disclaimer'ını zorunlu yapar.

### 5) IndieHackers / B2B data ve outreach paralelleri
- Proxycurl hikayesi: cold email + SEO ile $100k MRR; B2B data ürünleri için founder-led outbound'ın işe yaradığını anlatıyor.
- Cyberleads: lead generation service modelinde $50k MRR anlatısı; 1,000+ lead list ve done-for-you planlar üzerinden satıyor.
- Bu örnekler trade-specific değil; ama bizim modelle aynı para mekaniği var: **özel veri → yüksek niyetli liste → outbound/rapor → B2B satış**.

## Pazar Büyüklüğü & Fırsat

### Makro pazar
- UNCTAD'a göre 2024 global goods+services trade yaklaşık **$33T**; goods trade yaklaşık **$25T**.
- 2024 büyümesi **%3.7 / $1.2T**, services +9%, goods +2%.
- Bu hacimde küçük bir vertical bile yeter: örneğin Türkiye → ABD belirli HS kodları, Körfez ithalatçıları, AB tekstil/tarım buyer'ları.

### Software / compliance pazar sinyali
- Fortune Business Insights: global trade management software market **$1.3688B (2026)** → **$2.6298B (2034)**, CAGR **%8.5**.
- Grand View Research farklı tahminle 2023'te **$1.1947B** ve 2030'da **$1.7176B** veriyor. Tahminler değişiyor ama ortak mesaj aynı: compliance + trade analytics software büyüyor.

### Resmi veri kapsamı
- WCO HS: 200+ ülke/ekonomi temel alıyor.
- ITC Trade Map FAQ: 5,000+ HS ürün, yaklaşık 220 ülke/territory, reported + mirror data ile dünya ticaretinin **%97** kapsaması, HS time-series 1988'den beri.
- WITS: UNSD COMTRADE imports/exports/re-exports since 1962, summary coverage tablosunda **274 countries**, HS 6-digit.
- UN Comtrade: close to 200 countries/areas since 1962, tens of billions of data points, >99% merchandise trade olarak tanımlanıyor.
- U.S. Census API: current month + year-to-date imports by HS, country, value, quantity, shipping weight, duty, district/mode fields.

### Somut API örneği — Turkey → U.S. imports, Census API, 2026-02
Bu sorgular ücretsiz U.S. Census HS import API ile çekildi; şirket ismi yok, ama ürün/ülke fırsat taraması için yeterli.

| HS | Açıklama | 2026-02 Aylık General Import Value | 2026 YTD Value | 2026-02 Calculated Duty | Yaklaşık efektif duty |
|---|---:|---:|---:|---:|---:|
| 080222 | Shelled hazelnuts/filberts | $587,297 | $931,273 | $54,150 | %9.2 |
| 570242 | MMF pile carpets, made-up | $56,535,522 | $107,415,249 | $7,167,911 | %12.7 |
| 610910 | Cotton knit T-shirts/singlets | $3,062,808 | $6,650,531 | $927,123 | %30.3 |
| 870899 | Motor vehicle parts/accessories NESOI | $4,873,406 | $12,876,674 | $900,757 | %18.5 |

**Fırsat yorumu:** Daha ilk ücretsiz veri çağrısında halı HS 570242 için tek ayda $56.5M Türkiye→ABD import görünmesi, “GTIP opportunity report” satış mesajı için yeterli malzeme veriyor. Ama bu aggregate data; importer listesi için US bill-of-lading/commercial platform gerekir.

## Rakipler & Boşluklar

### Rakip/alternatif kümeleri

1. **Enterprise trade intelligence:** ImportGenius, Panjiva/S&P, Descartes Datamyne, PIERS, Trademo, Tendata, Volza.
   - Güçlü: shipment-level data, company names, alerts, CRM export.
   - Zayıf: pahalı, İngilizce/enterprise odaklı, novice exporter için fazla geniş.

2. **Resmi ve yarı-resmi istatistik araçları:** UN Comtrade, ITC Trade Map, WITS, U.S. Census, USITC DataWeb, Access2Markets, ITA tools, Türkiye Ticaret Bakanlığı.
   - Güçlü: güvenilir, ucuz/ücretsiz, makro karar için iyi.
   - Zayıf: dağınık, ürün/ülke/HS eşlemesi acemi için zor, şirket seviyesinde data yok veya sınırlı.

3. **HS/HTS classification araçları:** Zonos, Avalara, Tarifflo, WCO BACUDA, HTS API tarzı ürünler.
   - Güçlü: classification workflow.
   - Zayıf: opportunity/lead/outreach kısmını çözmez.

4. **Lead-gen / enrichment araçları:** Apollo, Clay, Proxycurl, Instantly, Smartlead.
   - Güçlü: outreach ve enrichment.
   - Zayıf: “bu şirket gerçekten bu HS ürünü ithal ediyor mu?” sinyalini tek başına vermez.

### Boşluklar

- **Türkçe/GTIP-yerelleştirme boşluğu:** Türkiye ihracatçısına GTIP → pazar → tarife → buyer/outreach anlatan basit, Türkçe, PDF-first ürün az.
- **SME için “done-for-you insight” boşluğu:** Küçük ihracatçı $399/mo platforma girmek istemez; $39–$79 rapor alır.
- **Action gap:** Platformlar data gösteriyor; kullanıcıya “ilk 20 potansiyel ülke/segment + mesaj metni + risk” veren ürün daha satılabilir.
- **Legal-safe AI gap:** Çoğu AI aracı HS kodunu kendinden emin uyduruyor. Bizim fark: her raporda kaynak, confidence, resmi authority uyarısı ve insan QA.
- **Vertical report gap:** “Halı ABD pazar fırsatı”, “Fındık Körfez alıcı listesi”, “Tekstil duty shock alert” gibi mikro raporlar SEO ve outbound için daha iyi.

## Teknik Gereksinimler

### Veri kaynakları
- **Ücretsiz başlangıç:** ITC Trade Map, WITS, U.S. Census API, trade.gov tools, Türkiye Ticaret Bakanlığı, public tariff databases, official HS nomenclature.
- **Opsiyonel paid:** ImportGenius/Volza/Datamyne/Panjiva gibi shipment-level kaynaklar; sadece ödeme döngüsü doğrulanınca alınmalı.
- **Legal/licensing:** UN Comtrade verisini aynen re-distribute etmek lisanslı; ücretsiz küçük analiz/visualization ile premium/data extraction ayrımı dikkat ister.

### Agent pipeline
1. **Intake Agent:** ürün adı, Türkçe açıklama, mevcut GTIP/HS, hedef ülke, hedef rol (ihracatçı/ithalatçı/lojistikçi) alır.
2. **HS Normalizer:** ürün açıklamasından 2/4/6 digit HS adayları çıkarır; Türkiye 12 haneli GTIP için resmi kaynak/BTI uyarısı ekler.
3. **Trade Data Agent:** Trade Map/WITS/Census gibi kaynaklardan ülke-pazar, trend, import value, duty/tariff sinyali toplar.
4. **Opportunity Scorer:** pazar hacmi, büyüme, duty yükü, rekabet yoğunluğu, veri güveni, erişilebilir buyer sinyali skorlar.
5. **Lead Strategy Agent:** shipment-level data varsa company lead; yoksa trade association, importer directory, LinkedIn/Apollo/Clay query stratejisi üretir.
6. **Outreach Agent:** buyer'a, freight forwarder'a veya ihracatçıya uygun mail/LinkedIn mesajı üretir; göndermez, insan onayı bekler.
7. **Compliance QA Agent:** “legal advice değil”, customs authority final, kaynak tarihleri, data license, spam/KVKK/GDPR uyarılarını kontrol eder.
8. **Report Composer:** PDF/Markdown/CSV olarak paketler.

### Minimum rapor bileşenleri
- Ürün/HS/GTIP özeti ve confidence.
- Hedef pazar hacmi ve trend.
- Top importer/exporter countries.
- Duty/tariff snapshot + source date.
- Rakip/alternatif supplier countries.
- Buyer finding strategy.
- 3 outreach message variant.
- Risk/disclaimer.
- “Next 3 actions” checklist.

## projeler.txt İlgili Notlar

- Doğrudan `HS code`, `GTIP`, `trade intelligence`, `Comtrade`, `Panjiva`, `ImportGenius` sinyali çıkmadı.
- İlgili dolaylı sinyaller: browser automation, scraping, API wrapping, crawlee-python, public APIs listesi, Scrapeless, browser-use, Vercel agent-browser, ZAPI network/API capture.
- Sonuç: Bu research konusu mevcut katalogda “ürün” olarak yok; ama mevcut scraping/browser/API yetenekleri bu rapor motorunun veri toplama katmanı için uygun.

## Ham Notlar

- **Veri tazeliği:** Trade Map monthly data genelde ITC'ye ulaştıktan sonra yaklaşık 1 hafta içinde işleniyor; ortalama gerçek ay gecikmesi 3-4 ay olabilir. Shipment-level paid data bile ülkeye göre gecikir.
- **Mirror data riski:** Ülke raporlamazsa partner-country mirror data kullanılır; direct + mirror asla toplanmamalı.
- **HS/GTIP hukuki risk:** Türkiye Ticaret Bakanlığı BTI'nin sadece hak sahibi için bağlayıcı olduğunu ve 6 yıl geçerli olduğunu söylüyor. Başka ülkedeki belge/kod Türkiye için bağlayıcı değil; ilk 6 hane ortak olsa da daha derin haneler ülkeye göre değişir.
- **AI sınıflandırma:** 2021 KoELECTRA paper top-3 %95.5 HS heading/subheading; 2023 explainable KCS model top-3 %93.9; 2024 multimodal text+image top-3 %93.5/top-5 %98.2. Bunlar “öneri” olarak müthiş; nihai GTIP kararı olarak satmak riskli.
- **ATLAS 2025 dersi:** HTS 10-digit tam doğruluk %40 ise ürünümüz “AI classified your HS” değil, “AI-assisted research + source-backed report” olmalı.
- **Reddit demand:** ImportYeti yorumlarında e-commerce, FBA, logistics, manufacturing kullanıcıları “bunu beta test ederim” diyor; 2024 logistics postunda consolidation çalışanı müşteri bulmak için deneyeceğini söylüyor. Bu tam bizim buyer persona.
- **MCPTube / Volza workflow:** Global/country/universal search → product/HSN/company/shipper/consignee → subfilters → save workspace → summary. Bizim report formu bunu kopyalamalı.
- **MCPTube / ITA workflow:** country → HS/keyword → hierarchy → duties/taxes → tariff treatment → incoterm → customs office final authority. Bizim risk bölümü bunu kopyalamalı.
- **Satış açısı:** “Platform almadan önce $39'a GTIP pazar testi” iyi wedge. Platformlar pahalı; rapor ucuz. Sonra recurring alert veya white-label danışmanlık satılır.
