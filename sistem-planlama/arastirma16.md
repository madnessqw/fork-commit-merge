# Araştırma #16 — Ticari İstihbarat & HS Codes (2. tur / 2026 doğrulama)
**Tarih:** 2026-04-21 12:19
**Konu:** Ticari İstihbarat & HS Codes — GTIP/HS bazlı pazar tarama, tarife zekâsı, buyer/supplier discovery ve rapor ürünleştirme

**Kaynaklar:**
- WCO — Harmonized System overview: https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
- Türkiye Ticaret Bakanlığı — Tariff / GTIP FAQ: https://www.trade.gov.tr/customs-formalities/frequently-asked-questions/tariff
- UNCTAD — Global trade hits record $33 trillion in 2024: https://unctad.org/news/global-trade-hits-record-33-trillion-2024-driven-services-and-developing-economies
- WTO Tariff & Trade Data / World Tariff Profiles 2025 sinyali: https://ttd.wto.org/en
- WITS database coverage: https://wits.worldbank.org/wits/witshelp/content/Basics/A4.Database_Content_Coverage.htm
- U.S. Census HS imports API docs: https://api.census.gov/data/timeseries/intltrade/imports/hs.html
- UN Comtrade pricing/licensing: https://shop.un.org/lec/node/55
- ImportGenius pricing: https://www.importgenius.com/pricing
- ImportGenius HS-code enrichment launch: https://www.importgenius.com/press-releases/importgenius-unlocks-ai-powered-hs-code-search-for-global-trade-teams
- Fortune Business Insights — Trade Management Software Market: https://www.fortunebusinessinsights.com/trade-management-software-market-106816
- Mordor Intelligence — Trade Management Software Market: https://www.mordorintelligence.com/industry-reports/trade-management-software-market
- Reddit — ImportYeti first launch: https://www.reddit.com/r/Entrepreneur/comments/hvfgm1/
- Reddit — ImportYeti logistics V9 update: https://www.reddit.com/r/logistics/comments/1d9lz3p/
- Reddit — supply-chain data pain: https://www.reddit.com/r/supplychain/comments/1n9wyuu/
- Reddit — tariff shock pain: https://www.reddit.com/r/smallbusiness/comments/1mywp7p/
- GitHub — SupplyGraph AI: https://github.com/SupplyGraphAI/supplygraph-ai
- GitHub — datasets/harmonized-system: https://github.com/datasets/harmonized-system
- GitHub — hscode_predictor: https://github.com/gattuzzo0/hscode_predictor
- ArXiv — Explainable Product Classification for Customs (2311.10922v1): https://arxiv.org/pdf/2311.10922v1
- ArXiv — Multimodal Approach for Harmonized System Code Prediction (2406.04349v1): https://arxiv.org/pdf/2406.04349v1
- ArXiv — Industrial Implementation for HS Code Prediction (2602.17102v1): https://arxiv.org/pdf/2602.17102v1
- YouTube / MCPTube — TradeInt basics: https://www.youtube.com/watch?v=NokMLIcp1vw
- YouTube / MCPTube — Volza search workflow: https://www.youtube.com/watch?v=WQ3__Rlukdw
- YouTube / MCPTube — ITA Customs Info Database: https://www.youtube.com/watch?v=oQOb3RfpK9Y
- YouTube / MCPTube — Zonos HS code automation: https://www.youtube.com/watch?v=AM1X5z2GGn4

## Özet Bulgular

- **HS/GTIP katmanı sıkıcı görünüyor ama paranın damarı burada.** WCO'ya göre HS, gümrük tarifeleri ve ticaret istatistikleri için **200+ ülke ve ekonomi** tarafından kullanılıyor. Türkiye tarafında GTIP hâlâ kritik: Ticaret Bakanlığı'na göre yapı **12 haneli**; ilk 6 hane HS, 7-8 AB Combined Nomenclature, 9-10 ulusal açılım, 11-12 istatistik kodu.
- **Makro pazar devasa, mikro ürün hâlâ eksik.** UNCTAD, 2024 küresel ticareti **$33T** ve yıllık büyümeyi **%3,7 / $1,2T** olarak veriyor. Buna rağmen küçük ihracatçı hâlâ “hangi HS ile hangi pazara gireyim, tarife darbesi nereden gelir, kimi hedefleyeyim?” sorusuna düzgün cevap bulamıyor.
- **Bu bilgi pahalı satılıyor; o yüzden düşük girişli rapor fırsatı var.** ImportGenius bugün **$229/mo**, **$449/mo** ve **$1,999/mo** seviyesinde; dataset erişimi **$199**’dan başlıyor. UN Comtrade premium bireysel erişim **$2,000/yıl**, özel sektör kurumsal plan **$12,000/yıl**. Sonuç net: dashboard satın almak istemeyen KOBİ’ye düşük fiyatlı, kaynaklı rapor satmak mantıklı.
- **AI sınıflandırma tarafı ilerledi ama “nihai karar” hâlâ insan + resmi otorite işi.** 2023 KCS çalışması zor alt-başlıklarda top-3 **%93,9** doğruluk; 2024 multimodal çalışma top-3 **%93,5**, top-5 **%98,2**; 2026 sanayi implementasyonu **%98** accuracy iddiası veriyor. Ama ITA videosu açık: son HS/tarife kararını **ithalatçı ülkenin gümrük otoritesi** verir.
- **Community tarafı aynı şeyi bağırıyor:** veri dağınık, pahalı ve güncel karar akışına çevrilmemiş. 6 Eylül 2025 tarihli r/supplychain postu “kim 10.000 ton çelik alıyor öğrenmek niye bu kadar zor” diye patlıyor; 24 Ağustos 2025 tarihli r/smallbusiness tarife postu **845 score** alıyor. Problem canlı. Sadece spreadsheet değil, **karar ürünü** gerekiyor.

## Gerçek Başarı Hikayeleri

### 1) ImportYeti — kamuya açık veriyi kullanılabilir ürüne çevirmek
- **21 Temmuz 2020** tarihli r/Entrepreneur postunda kurucu, **70.000.000 bill of lading** üzerinde ücretsiz arama sunduğunu anlattı; post **786 score / 883 comment** aldı.
- Yorumlar doğrudan talep sinyali verdi: Amazon satıcıları beta istedi, kullanıcılar supplier discovery için hemen kullanmak istedi.
- **6 Haziran 2024** tarihli r/logistics güncellemesinde kurucu **155+ görüşme** ve **300+ ürün değişikliği** yaptığını yazdı; yorumlarda konsolidasyon, handicraft export ve genel logistics kullanımı için somut fayda anlatılıyor.
- Çıkarım: ham trade data tek başına ürün değil; ama doğru UX ile supplier/buyer discovery aracı oluyor.

### 2) ImportGenius — bu acı gerçek para ediyor
- ImportGenius pricing sayfası bugün üç çıplak gerçek söylüyor: **USA Essentials Flex $229/mo**, **USA Pro Flex $449/mo**, **Global Enterprise $1,999/mo**.
- Aynı sayfada kullanım alanları boş laf değil: **sales & lead generation**, **supplier discovery**, **tariff & compliance**, **market intelligence**.
- **7 Ağustos 2025** tarihli press release'e göre yeni HS code enrichment katmanı ile **2024–2025 U.S. import kayıtlarının yaklaşık %70'i** HS kodla zenginleştirildi; amaç yalnız sınıflandırma değil, **supplier/competitor/buyer search** akışını açmak.
- Çıkarım: insanlar trade data'ya sırf merak için para vermiyor; **lead, sourcing, compliance ve tarife kararı** için veriyor.

### 3) Açık implementasyon tarafı — agentic compliance stack gerçek oluyor
- `SupplyGraphAI/supplygraph-ai` sadece sunum reposu değil; agent library içinde **Customs Classification Agent**, **U.S. Tariff Calculation Agent** ve **Due Diligence Agent** tanımlıyor. Bu, pazarın “tek model → tek cevap”tan “ajan zinciri + kanıt zinciri”ne kaydığını gösteriyor.
- `gattuzzo0/hscode_predictor` daha küçük ama daha dürüst: Chroma tabanlı RAG + Streamlit ile açıklamadan HS tahmini yapıyor, belirsizlikte alternatif kod öneriyor. Yani küçük ekipler için de uygulanabilir pattern var.
- `datasets/harmonized-system` gibi açık veri depoları, resmi WCO/UN Comtrade nomenclature katmanını ürünün temel sözlüğü olarak paketlemeyi kolaylaştırıyor.
- Çıkarım: sıfırdan “trade intelligence engine” yazmak gerekmiyor; açık nomenclature + retrieval + resmi veri + QA ile başlanabilir.

## Pazar Büyüklüğü & Fırsat

### Makro hacim
- **UNCTAD:** 2024 küresel ticaret hacmi **$33T**, büyüme **%3,7**.
- **WTO / World Tariff Profiles 2025:** ortak tarife ve non-tariff görünürlüğü **170+ ülke ve gümrük bölgesi** için yayınlanıyor.
- **WITS:** UN COMTRADE akışları **1962**'den beri, HS sınıflaması **1988**'den beri; UNCTAD TRAINS ulusal tarife çizgilerinde **15.000** satıra kadar gidiyor.

### Yazılım pazarı (harici tahminler, resmi istatistik değil)
- **Fortune Business Insights:** trade management software pazarı **$1,267.1M (2025)** → **$1,368.8M (2026)** → **$2,629.8M (2034)**, CAGR **%8,5**.
- **Mordor Intelligence:** **$1,45B (2025)** → **$2,33B (2030)**, CAGR **%9,9**.
- Bu tahminler birebir aynı değil; ama ikisi de aynı şeyi söylüyor: compliance + trade analytics çözümleri büyüyor, özellikle cloud/SaaS tarafında.

### Somut ürün/ülke sinyali — U.S. Census API, Türkiye → ABD, 2026-02
Aşağıdaki veriler U.S. Census Monthly Imports by HS API'dan çekildi (`time=2026-02`, `CTY_CODE=4890`, ülke=Turkey):

| HS | Açıklama | 2026-02 aylık import değeri | 2026 YTD değeri | 2026-02 CIF değeri |
|---|---|---:|---:|---:|
| 570242 | MMF pile carpets | $56,535,522 | $107,415,249 | $59,269,992 |
| 870899 | Motor vehicle parts, nesoi | $4,873,406 | $12,876,674 | $5,088,270 |
| 610910 | Cotton knit T-shirts | $3,062,808 | $6,650,531 | $3,287,051 |
| 080222 | Shelled hazelnuts | $587,297 | $931,273 | $589,081 |

**Yorum:** Tek bir ücretsiz API katmanında bile halı, otomotiv parçası, tekstil ve fındık için satış konuşmasına çevrilebilecek kadar net sinyal var. Demek ki ilk ürün “tam platform” değil; **HS bazlı karar raporu** olabilir.

## Rakipler & Boşluklar

### Rakip kümeleri
1. **Enterprise trade intelligence:** ImportGenius, Panjiva, Volza, Datamyne, Global Trade Atlas.
   - Güçlü: shipment-level görünürlük, buyer/supplier isimleri, filtreleme.
   - Zayıf: pahalı, onboarding ağır, KOBİ için fazla geniş.

2. **Resmi veri / yarı-resmi araçlar:** WCO, WITS, WTO TTD, U.S. Census API, Türkiye Ticaret Bakanlığı, ITA Customs Info Database.
   - Güçlü: güvenilir, açıklanabilir, çoğu ücretsiz.
   - Zayıf: parçalı, UX kötü, karar çıktısı üretmiyor.

3. **AI classification araçları:** kurum içi modeller, GitHub RAG örnekleri, vendor classifier katmanları.
   - Güçlü: hız ve öneri üretimi.
   - Zayıf: hukuki kesinlik sağlayamaz; explanation + human QA şart.

### Açık boşluklar
- **Türkçe GTIP → pazar → outreach köprüsü yok.** Mevcut oyuncular veri veriyor ama “şimdi kime ne yazayım?” demiyor.
- **Tarife şoklarını KOBİ diline indiren ürün yok.** r/smallbusiness’taki panik bunun sinyali; çoğu insan gümrük jargonunu değil, “hangi HS beni vuruyor?” cevabını istiyor.
- **Public-data-first düşük bilet ürün boşluğu var.** $229-$1,999/mo arasında platform var; ama **$19-$79 rapor**, ya da **$49-$199/ay watchlist** katmanı neredeyse boş.
- **Agentic açıklanabilirlik boşluğu var.** Sadece kod öneren model değil; kaynak veren, confidence gösteren, resmi uyarı ekleyen sistem kazanır.

## Teknik Gereksinimler

### Zorunlu veri katmanı
- WCO / HS nomenclature referansı
- Türkiye GTIP/BTI/Tariff kaynakları
- WTO TTD / WITS / U.S. Census API gibi resmi veri uçları
- Açık HS sözlüğü (`datasets/harmonized-system`) veya eşdeğer veri tabanı

### Opsiyonel ücretli veri katmanı
- ImportGenius veya benzeri shipment-level provider
- UN Comtrade premium (yalnızca ölçek / lisans ihtiyacı netleşirse)
- Sonraki aşamada Apollo/Clay/LinkedIn enrichment

### Agent mimarisi
1. **Intake Agent** — ürün açıklaması, hedef ülke, rol (ihracatçı/ithalatçı/lojistikçi) alır.
2. **HS Hypothesis Agent** — 2/4/6 haneli adayları ve confidence çıkarır.
3. **Official Data Agent** — WITS/WTO/Census/ITA/Türkiye kaynaklarını tarar.
4. **Tariff Shock Agent** — mevcut tarife/risk/sürpriz değişim ihtimalini özetler.
5. **Buyer/Supplier Strategy Agent** — public veriden buyer hipotezi, ülke önceliği, outreach açısı üretir.
6. **Compliance QA Agent** — “nihai karar gümrükte” uyarısı, kaynak tarihi, lisans sınırı ve confidence kontrolü yapar.
7. **Composer Agent** — PDF/Markdown/CSV paketler.

### Mevcut repo ile teknik kaldıraç
- `projeler.txt` içinde doğrudan trade-intelligence ürünü yok; ama **browser-use**, **crawlee-python**, **Scrapeless** ve API/scraping sinyalleri var.
- Yani veri toplama ve resmi kaynaklardan extraction tarafı için sıfırdan kas inşa etmiyoruz; kas zaten var.

## Ham Notlar

- **Zonos videosu kritik bir detay veriyor:** ülkeye özgü alt kodlar neredeyse günlük değişebilir; evrensel 6 haneli HS ise daha yavaş değişir. Bu yüzden sistemin çekirdeği **HS-6 sabit**, ülke uzantısı **ayrı katman** olmalı.
- **TradeInt videosu karar cümlesini net koyuyor:** trade data intelligence = ham shipment kayıtlarını “kim alıyor / hangi ülke büyüyor / rakip nereye satıyor” cevabına çevirmek.
- **Volza videosu ürün tasarımını ele veriyor:** global search + country search + universal search + save workspace + 3 yıllık shipment summary. Bunu rapor formuna küçülterek kopyalamak mantıklı.
- **ITA videosu frene basıyor:** importing country customs office final authority. Yani ürün “AI gümrük müşaviri” diye değil, “kaynaklı ticari zekâ + classification assist” diye satılmalı.
- **ProductHunt katmanı zayıf kaldı.** 2026-04-21 denemesinde ProductHunt aramaları Cloudflare doğrulamasına takıldı; bu başlıkta güvenilir PH sinyali çıkmadı.
- **Reddit community insight kaba ama dürüst:** sorun veri yokluğu değil; veri dağınıklığı + fiyat + karar çıktısına dönüşememesi.
