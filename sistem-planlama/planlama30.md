# Planlama #30 — Ticari İstihbarat & HS Codes Uygulama Haritası
**Tarih:** 2026-04-21 22:50
**Bağlı Araştırma:** arastirma30.md

## Swarm Agent ile Nasıl Uygulanır?

Bu turdaki net karar: **“GTIP Opportunity Snapshot” tek başına yetmez.** 2026 piyasasında daha iyi wedge:

> **GTIP Tariff Exposure Snapshot + Buyer Map + Watchlist**

Yani kullanıcıya sadece “bu HS’de pazar var” demeyeceğiz; “bu HS hangi pazarda büyüyor, hangi tarife/duty riski var, kim hedeflenir, hangi kanıtla broker’a/danışmana gidilir?” diyeceğiz.

### Swarm rolleri

1. **Lead Intake Agent**
   - Ürün adı, açıklama, mevcut GTIP/HS, hedef ülke, rol ve amaç alır.
   - Dört lane seçtirir: `opportunity`, `tariff exposure`, `buyer map`, `catalog audit`.

2. **HS Hypothesis Agent**
   - 2/4/6 haneli HS adayları çıkarır.
   - 8/10/12 haneli ülke uzantılarında “candidate only” etiketi koyar.
   - Confidence, alternatif ve gerekçe üretir.

3. **Official Evidence Agent**
   - WCO, USITC HTS, CBP, Census, WTO, UNCTAD, UN Comtrade/WITS gibi kaynaklardan kanıt toplar.
   - Her veri noktasına URL + tarih + alan adı bağlar.

4. **Tariff Exposure Agent**
   - U.S. Census `CAL_DUT_MO / GEN_VAL_MO` gibi oranları “analysis ratio” olarak çıkarır.
   - Ek tarifeler, tariff action, refund/appeal, policy change ve high-risk flag üretir.

5. **Market Opportunity Agent**
   - Hacim, büyüme, YTD, CIF/value, rakip ülke ve route sinyaliyle opportunity score verir.

6. **Buyer/Supplier Map Agent**
   - Ücretsiz fazda: LinkedIn/Apollo/association/search query pack.
   - Paid-data fazında: shipment-level company list + buyer/supplier segmentation.

7. **Compliance QA Agent**
   - AI hallucination, yanlış ülke uzantısı, lisans ihlali ve legal advice riskini yakalar.
   - “Final classification customs authority / licensed broker” uyarısını zorunlu tutar.

8. **Composer Agent**
   - PDF + CSV + TXT outreach pack üretir.
   - Raporun sonuna “ilk 3 aksiyon” ve upsell koyar.

## Gerekli Bileşenler

- **Script/Bot:**
  - HS intake formu
  - Census/USITC/WTO/UNCTAD fetch checklist veya fetcher
  - opportunity + exposure scoring sheet
  - buyer query pack generator
  - markdown/PDF report composer
  - QA checklist

- **MCP/Araç:**
  - ArXiv MCP — classifier benchmark ve compliance ML literatürü
  - MCPTube — vendor workflow ve eğitim transkriptleri
  - Jina Reader — resmi docs/vendor pricing/GitHub README okuma
  - chrome-devtools-axi / Botasaurus — JS-rendered vendor sayfaları ve dynamic snapshot
  - GitHub CLI — açık implementasyon ve veri depoları
  - Reddit JSON API — broker/KOBİ/logistics pain intelligence

- **API:**
  - U.S. Census HS imports API — ücretsiz başlangıç
  - USITC HTS / CBP rulings — ABD evidence layer
  - UN Comtrade — free/premium; premium **$2,000-$12,000/yıl**, re-dissemination dikkat
  - ImportGenius/Volza/Panjiva — paid data; satış doğrulanmadan alma
  - Apollo/Clay/LinkedIn — buyer/contact enrichment, orta vade

- **İnsan Müdahalesi:**
  - HS/GTIP kesinliğinde insan QA
  - İlk 10 raporda manuel kaynak kontrolü
  - Dışarı giden outreach’in onayı
  - Gümrük müşaviri / licensed broker gerektiren durumların ayrımı
  - Veri lisansı ve redistribution kontrolü

## Workflow Haritası

`müşteri intake` → `HS/GTIP adayları` → `official evidence collection` → `Census/WTO/UNCTAD/USITC tariff & market snapshot` → `tariff exposure score` → `market opportunity score` → `buyer/supplier query pack` → `compliance QA` → `PDF/CSV/outreach delivery` → `upsell: monthly GTIP watchlist / buyer map / catalog audit`

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

### Hemen hayata geçirilecek ürün
**GTIP Tariff Exposure Snapshot — 24 saat teslim**

İçerik:
- Ürün açıklaması + HS-6 adayları + confidence
- Hedef ülke için resmi data snapshot
- Tarife/duty exposure notu
- Market opportunity skoru
- Buyer/supplier discovery query pack
- 3 outreach mesajı
- Broker-ready evidence appendix
- “Legal/tariff advice değildir” disclaimer

### En düşük çaba / en yüksek çıktı adımı
- Önce 5 demo lane hazırlanmalı:
  1. **HS 570242 — Türkiye halı → ABD**: 2026-02 import value **$56.5M**, YTD **$107.4M**.
  2. **HS 610910 — cotton T-shirt → ABD**: duty/value ratio **%30.3**; tariff pain net.
  3. **HS 940360 — wooden furniture → ABD**: Vietnam/furniture tariff panik postlarıyla satış hikayesi kurulabilir.
  4. **HS 392410 — plastic tableware → ABD**: küçük ithalatçı/FBA landed-cost use case.
  5. **HS 732393 — stainless kitchenware → ABD**: duty/value ratio yüksek; TariffCenter örnekleriyle ürün dili uyuyor.

### Hangi mevcut araç/script bu işi kısmen yapar?
- Derin araştırma pipeline zaten hazır: Jina + ArXiv + MCPTube + Reddit + GitHub.
- Browser automation kası resmi/dinamik sayfaları okumaya yeterli.
- Mevcut ProfitBridge paket mantığı direkt uyuyor:
  - **A1 $19** — mini exposure snapshot
  - **A2 $39** — 1 HS / 1 ülke evidence pack
  - **A3 $79** — buyer map + outreach pack
  - **A4 $499** — 10 HS catalog audit / agency pack

### Proof-of-concept minimum gereksinimler
- Tek rapor template’i
- 5 demo lane
- 30 hedef prospect:
  - küçük ihracatçı
  - ithalat danışmanı
  - gümrük müşaviriyle çalışan KOBİ
  - freight forwarder
  - e-commerce/FBA seller
- 2 satış mesajı:
  - Türkçe: “GTIP/tarife riskini 24 saatte kaynaklı rapora çevirelim”
  - İngilizce: “HS tariff exposure snapshot for your product/corridor”
- Manuel ödeme/teslim akışı

### Tahmini kurulum süresi ve ilk gelir beklentisi
- Kurulum: **3-5 gün**.
- İlk outbound: **7 gün içinde**.
- İlk gelir: gerçekçi **$39-$237**; iyi senaryo 1 catalog audit **$499**.
- Break-even: ücretsiz veriyle **tek satış**.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

### 1. ay hedef görüntüsü
- 20+ hazır HS lane cache’i.
- 5 adet public demo rapor.
- Haftalık “GTIP/Tariff Watch” markdown bülteni.
- 100+ prospect listesi.
- 10+ ücretli rapor veya 3+ ciddi discovery call.
- Rapor üretim süresi **90 dakikanın altına** inmeli.

### Başarı metric’leri
- `report_time_minutes < 90`
- `source_coverage >= 5 official sources/report`
- `manual_QA_required_flag_rate` takip edilecek; yüksekse classifier zayıf demektir.
- `outbound_reply_rate > %5`
- `paid_conversion > %2`
- `monthly_revenue >= $500` ilk 60-90 gün için yeterli sinyal.

### Paralel çalışabilecek adımlar
- Researcher Agent: yeni HS lane üretir.
- Tariff Agent: policy/tariff action watch yapar.
- Buyer Agent: prospect/query pack çıkarır.
- Composer Agent: raporu standardize eder.
- QA Agent: kaynak/disclaimer/hallucination check yapar.

### Ölçeklendirme için gerekenler
- İlk satışlar sonrası paid data kararı:
  - $229/mo ImportGenius yalnız 5+ rapor talebi varsa.
  - $449/mo Pro yalnız HS code search/company profiler aktif gelir getiriyorsa.
  - Global data/Volza/Panjiva yalnız agency/enterprise ödeme varsa.
- Basit CRM: hangi HS lane, hangi prospect, hangi dönüşüm, hangi rapor satıldı.
- Legal-safe copy: “customs broker değiliz; evidence pack ve first-pass intelligence sağlıyoruz.”

### Checkpoint’ler
- 2. hafta: 5 demo rapor + 30 prospect + 1 satış denemesi.
- 1. ay: 20 HS cache + 100 prospect + ilk paid signal.
- 2. ay: monthly watchlist beta.
- 3. ay: catalog audit / white-label advisor pack.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo
- Sistem her hafta belirli HS/GTIP corridor’ları tarar.
- Tariff/risk değişimlerini watchlist’e işler.
- Müşteri kataloglarını HS-risk profiline göre skorlar.
- Buyer/supplier route değişim önerileri üretir.
- İnsan sadece high-risk classification ve müşteri teslim QA yapar.

### Yan ürünler / yeni gelir kolları
- **GTIP Watchlist Newsletter** — $49-$99/mo.
- **Catalog HS Audit** — $499-$1,500 one-off.
- **Tariff Shock Alert** — $99/mo vertical-specific.
- **Buyer Map CSV Pack** — $79-$299.
- **Freight Forwarder Lead Pack** — logistics firmaları için monthly.
- **Shopify/WooCommerce HS Audit Pack** — e-commerce catalog risk.
- **White-label Export Advisor Pack** — danışman/freight forwarder ajanslarına.

### Rakiplerin yapamadığı swarm avantajı
- Enterprise platformlar veri verir; bizim swarm **karar paketi** verir.
- AI HS finder’lar kod önerir; bizim sistem **kanıt, risk, alternatif, buyer strategy ve QA** verir.
- Broker’lar uzmanlık verir ama ölçekli içerik/outreach üretmez; bizim sistem broker-ready evidence hazırlar.

### SaaS / white-label olabilir mi?
Evet, ama hemen değil. İlk 3 ay productized service. 3-6 ayda dashboard değil, **client portal + watchlist + report history**. 6-12 ayda API-first “HS evidence pack generator” veya white-label portal.

## Öncelik & Çaba Tahmini

- **Öncelik:** Yüksek
- **Kurulum Süresi:** 3-5 gün ilk POC; 2-3 hafta ilk satış sistemi
- **Aylık İşletme Maliyeti:** $0-$50 başlangıç; paid trade data alınırsa $229-$449/mo
- **Potansiyel Gelir:** ilk 30 gün $39-$499; 90 gün $500-$3,000; 12 ay white-label ile $3K-$10K MRR mümkün ama ödeme/teslim kanıtı ister
- **ROI Beklentisi:** ücretsiz veriyle ilk satışta; paid data ile 2-3 Pro rapor veya 1 catalog audit sonrası

## Mevcut Sistemle Entegrasyon

- UniverseCreator mevcut ürün portföyüne yeni kod yazmadan “rapor ürünü” olarak eklenebilir.
- `sistem-planlama` çıktıları demo rapor taslaklarına dönüştürülebilir.
- Swarm loop’ta haftalık lane üretimi yapılır:
  - Pazartesi: 3 HS lane research
  - Çarşamba: tariff watch update
  - Cuma: outbound pack + rapor QA
- ProfitBridge fiyat paketleriyle uyumlu:
  - A1/A2/A3/A4 seviyeleri doğrudan rapor kapsamına bağlanır.
- Mevcut browser/scraping kası resmi kaynak kontrolü ve vendor benchmark için kullanılır.

## Riskler & Dikkat Edilecekler

- **Customs legal risk:** Ürün “classification advice” veya “customs filing” yapıyormuş gibi görünmemeli.
- **AI hallucination:** 10 haneli HTS/12 haneli GTIP için confidence düşükse insan/broker flag zorunlu.
- **Lisans riski:** UN Comtrade ve paid shipment data ham redistribüsyon kurallı; rapor içindeki aggregate/analysis ayrımı korunmalı.
- **Data lag:** Trade data çoğu zaman gecikmeli; “latest available as of date” yazılmalı.
- **Vendor claims:** TariffCenter/DutyDecoder gibi sayfalardaki penalty/ROI iddiaları bağımsız doğrulanmadan satış metnine ham alınmamalı.
- **Outreach compliance:** Email/LinkedIn gönderimi insan onaylı ve spam/KVKK/GDPR farkındalıklı olmalı.

## Önce Yapılacak 3 Adım (Bu Hafta)

1. **5 demo lane için tek sayfalık GTIP Tariff Exposure Snapshot hazırla.** Halı, T-shirt, furniture, plastic tableware, stainless kitchenware.
2. **Rapor template’ini standardize et:** HS candidate, official evidence, duty/value ratio, opportunity score, buyer query pack, disclaimer.
3. **30 prospect’e founder-led outbound başlat:** dış ticaret danışmanı, freight forwarder, küçük ihracatçı, e-commerce importer. Otomatik gönderme yok; manuel ve ölçümlü.
