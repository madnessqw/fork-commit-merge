# Planlama #15 — Lead Generation Automation Uygulama Haritası
**Tarih:** 2026-04-21 11:50
**Bağlı Araştırma:** arastirma15.md

## Swarm Agent ile Nasıl Uygulanır?

Bu işi “AI ile herkese spam atalım” seviyesinde kurmak intihar.

Doğru ürün:

**Signal-Based Lead Intelligence + Appointment Readiness OS**

Yani:
1. niche seç
2. taze problem / intent / trust leak sinyali bul
3. karar vericiyi doğrula
4. neden iyi lead olduğunu açıkla
5. niche-specific outreach hazırla
6. human gate sonrası kampanyaya veya aramaya ver
7. reply/meeting/revenue loop’unu ölç

### Önerilen ilk wedge
**Home services + lokal trust leak lead pack**

Örnek:
- HVAC
- roofing
- plumbing
- dental / medspa

Neden:
- Lokal arama ve website sinyali bol.
- Ticket size yüksek.
- “Cevap verilmeyen form / kötü site / yavaş dönüş” gibi net acılar var.
- Araştırma #14’teki speed-to-lead / voice agent katmanıyla doğal birleşiyor.

## Gerekli Bileşenler
- **Script/Bot:**
  - vertical + geo query generator
  - source risk scorer
  - website trust-leak extractor
  - contact resolver + verifier wrapper
  - lead score calculator
  - outreach draft generator
  - CSV / Sheets / Smartlead / Instantly export katmanı
  - reply / meeting analytics katmanı
- **MCP/Araç:**
  - arxiv + mcptube + web/Jina: playbook güncelleme
  - browser automation / Playwright / Chrome DevTools: site ve source kontrolü
  - Google Sheets / Airtable / Postgres: geçici CRM ve pipeline tabanı
- **API:**
  - Apify / scraper kaynakları: discovery için
  - Hunter / Apollo / alternative verify tools: fallback contact doğrulama
  - Instantly veya Smartlead: deliverability + campaign layer
  - küçük LLM modeli: trust leak çıkarma, kısa outreach draft, reply classification
- **İnsan Müdahalesi:**
  - ilk 100 lead kalite kontrolü
  - source-risk kararı
  - ilk outreach onayı
  - booked call / satış görüşmesi
  - compliance ve opt-out review

## Workflow Haritası
**Tetikleyici → Niche sprint aç**
1. Researcher Agent `roofing + Dallas` gibi sprint açar.
2. Source Hunter public source listesini çıkarır: Maps, company sites, review pages, Reddit pain post’ları, directory listings, job changes.
3. Compliance Sentinel her source’a risk etiketi koyar.

**Discovery → Raw prospect set**
4. Scraper / browser layer şirket adı, site, telefon, adres, kategori, review count, sosyal linkler toplar.
5. Dedupe yapılır.
6. Website olmayan veya çok zayıf olanlar ayrı segmentlenir.

**Enrichment → Decision-maker + pain extraction**
7. Website Miner homepage/contact/about/team/careers/testimonials/form akışını tarar.
8. Trust leak bulur:
   - broken CTA
   - no booking form
   - outdated copyright
   - weak mobile UX
   - poor review response
   - slow follow-up risk
9. Contact Resolver owner/GM/founder/manager email + LinkedIn + phone bulur.
10. Verifier valid/risky/catch-all/unknown sınıflandırması yapar.

**Scoring → Campaign readiness**
11. Signal Scorer şu matrisi üretir:
   - verified owner contact
   - high ticket niche
   - trust leak count
   - local competition intensity
   - recent review pain
   - speed-to-lead opportunity
   - source legality/risk
12. Lead üçe ayrılır:
   - **A-tier:** human review sonrası outreach-ready
   - **B-tier:** ek enrichment gerekli
   - **C-tier:** arşiv / nurture

**Outreach / Appointment**
13. Copy Agent 60-90 kelimelik, tek CTA’lı mesaj üretir.
14. Compliance Sentinel postal address, opt-out, claim risk kontrolü yapar.
15. Human gate onaylarsa Smartlead/Instantly’ye aktarılır veya voice follow-up lane’ine düşer.
16. Reply Classifier cevapları sınıflandırır.
17. Positive reply → booked call / callback / audit offer.
18. Analyst haftalık rapor üretir.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

Hemen yapılabilir olan şey:

**1 niche + 1 şehir için human-reviewed lead intelligence pack**

### En düşük çaba / en yüksek çıktı adımı nedir?
- Tek vertical seç: örn. `Dallas roofing` veya `Austin HVAC`.
- 200–300 işletme discovery.
- Buradan en az **50 doğrulanmış, açıklanabilir high-confidence lead** çıkar.
- Satılacak şey: ham CSV değil, **mini audit + why-now signal + verified contact + outreach draft**.

### Hangi mevcut araç/script bu işi kısmen yapar?
- Mevcut research stack zaten web, Reddit, browser ve scraping katmanını destekliyor.
- Apify/website scrape + Sheets + LLM extraction ile ilk veri katmanı kurulabilir.
- Araştırma #14’teki voice AI / speed-to-lead bilgisi follow-up lane olarak eklenebilir.

### Proof-of-concept için minimum gereksinimler neler?
- 1 vertical, 1 şehir
- 200 raw company
- 50 high-confidence verified contact
- her lead için `trust leak`, `source risk`, `contact confidence`, `outreach angle`
- 10 lead manuel QA
- suppression / do-not-contact listesi
- valid postal address + opt-out footer kararı

### Tahmini kurulum süresi ve ilk gelir beklentisi?
- Kurulum: **4–7 gün**
- İlk usable dataset: **2–3 gün**
- İlk satış formatı:
  - one-off lead intelligence pack: **$99–$299**
  - mini outbound pilot: **$500–$1,500**
  - appointment bonus: **$75–$150/meeting** intro pricing
- Tahmini ilk gelir: **ilk 1–2 hafta içinde 1 pilot kapatılırsa $500+**

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

1. ay sonunda hedef sistem bir scraper değil, bir **lead intelligence operating system** olmalı.

### Hangi metric’ler başarıyı gösterir?
- verified contact rate
- owner/decision-maker match rate
- A-tier lead ratio
- bounce rate
- reply rate
- positive reply rate
- booked meeting rate
- cost per A-tier lead
- time-to-first-qualified-list
- signal→meeting conversion

### Başarı hedefleri
- verified contact rate: **>%30 başlangıç**, **>%50 iyi**
- bounce rate: **<%3**
- reply rate: **%2–5+** (Belkins 2025 benchmark ortalığına yakın veya üstü)
- positive reply rate: **>%1** başlangıçta yeterli
- booked call rate: **>%0.5** ilk pilot için kabul edilebilir
- cost per A-tier lead: **<$1** hedef, **<$0.50** iyi

### Hangi adımlar paralel çalışabilir?
- vertical research
- source discovery
- website enrichment
- verification
- signal scoring
- copy generation
- deliverability prep

### Ölçeklendirme için ne gerekiyor?
- 3 vertical template
- 3–5 şehir deney seti
- Postgres/Airtable tabanlı lead memory
- domain/mailbox health tracking
- client-facing report template
- human QA SOP
- source legality policy

### Checkpoint’ler ve başarı kriterleri?
- **Hafta 2:** 1 usable lead pack + 1 sample campaign
- **Hafta 4:** 3 vertical / 3 city karşılaştırması
- **Ay 2:** 1–3 ücretli pilot müşteri
- **Ay 3:** weekly recurring ops + measurable meetings pipeline

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo
- Sistem her gün yeni lead bulur, risk etiketler, score eder, campaign-ready hale getirir.
- Human sadece gate ve closing tarafında kalır.
- Reply ve meeting verileri sisteme geri akar; hangi sinyalin para getirdiği öğrenilir.

### Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?
- **Lead Intelligence API** — niche + geo + signal tabanlı lead feed
- **Trust Leak Audit ürünleri** — “website / follow-up / reputation leak” raporu
- **Appointment Recovery OS** — missed call + form follow-up katmanı
- **Vertical playbook paketleri** — roofing, HVAC, dental, medspa, legal
- **White-label outbound OS** — agency’lere altyapı olarak satış

### Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?
- Tek araç yerine multi-source signal fusion
- lead başına explainable scorecard
- research + outreach + voice follow-up aynı sistemde
- her vertical için yaşayan knowledge base
- buyer-intent, website pain ve contact confidence’ı tek kartta birleştirme

### White-label veya SaaS olarak satılabilir mi?
- **Evet, ama hemen değil.**
- İlk para service + semi-productized ops’tan gelir.
- Gerçek kullanım verisi toplandıktan sonra white-label / SaaS katmanı mantıklı olur.
- En doğal evrim: `agency OS` → `niche OS` → `API/data product`.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** 5–10 gün
- **Aylık İşletme Maliyeti:** yaklaşık **$100–$300** (hafif POC), ölçeklenirse **$300–$1,000+**
- **Potansiyel Gelir:** erken safhada **$1k–$5k/mo**, iyi productized service ile daha yüksek
- **ROI Beklentisi:** ilk ücretli pilotla **aynı ay içinde break-even** mümkün

## Mevcut Sistemle Entegrasyon
- UniverseCreator araştırma stack’i günlük vertical scouting için kullanılır.
- Browser / scraping / Jina / Reddit katmanı lead discovery için zaten hazır.
- Araştırma #14’teki voice AI bulguları ikinci faz follow-up motoruna bağlanır.
- `universe_loop.sh` mantığında günlük scan → shortlist → human review → outreach/export zinciri kurulabilir.
- 113 ürün portföyü içinden bağımsız bir ürün yerine, önce **servis olarak çalışan iç operasyon** kurulmalı.

## Riskler & Dikkat Edilecekler
- Google Maps source-risk: ToS açıkça scraping/export’u yasaklıyor.
- CAN-SPAM: opt-out, postal address, unsubscribe SLA ihlal edilirse ceza büyük.
- GDPR/PECR: Avrupa’ya açılırsan kurallar daha sert.
- Public scraper’lara aşırı güvenmek kalite ve süreklilik riski yaratır.
- Low-quality data domain yakar; sender reputation çökünce oyun biter.
- Automation kolayca spam motoruna döner; human gate şart.
- Public revenue anekdotlarının çoğu pazarlama kokuyor; benchmark diye okunmalı, garanti diye değil.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek vertical + tek şehir seç ve source-risk policy yaz.** Home services ile başla; hangi source kullanılacak, hangisi yasak/gri net olsun.
2. **50 A-tier lead çıkaran mini pipeline kur.** Her lead için verified contact + trust leak + outreach angle üret.
3. **Human-reviewed sample offer hazırla.** `Lead intelligence pack + outreach draft + optional speed-to-lead follow-up` şeklinde satılabilir demo dosyası oluştur.
