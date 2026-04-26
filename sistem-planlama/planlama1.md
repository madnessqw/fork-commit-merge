# Planlama #1 — Lead Generation Automation Uygulama Haritası
**Tarih:** 2026-04-21 03:12
**Bağlı Araştırma:** arastirma1.md

## Swarm Agent ile Nasıl Uygulanır?

Doğru ürün “AI ile 10 bin kişiye spam at” değil. O aptal yol domain yakar, şikâyet toplar, ödeme hesabını riske sokar.

Doğru wedge:

**Local Lead Intelligence + Qualified Appointment Engine**

Yani: seçili bir dikey/şehir için işletmeleri bul → web sitelerinden owner/contact/context çıkar → email/phone doğrula → ICP skoru ver → kişiselleştirilmiş outreach önerisi üret → human-onaylı kampanya veya müşteri CRM’ine teslim → reply/appointment/revenue metric’i takip et.

### Başlangıç dikeyi
İlk dikey için öneri: **HVAC / plumbing / roofing gibi home services.**

Neden:
- Google Maps coverage güçlü.
- Owner-level veri Apollo/LinkedIn’de zayıf, web sitelerinde daha iyi.
- Lead/appointment fiyatları yüksek: HVAC exclusive lead yaklaşık $45-70, roofing appointment $175-$200 gibi public sinyaller var.
- İşletmenin acısı net: cevap verilmeyen form/call = rakibe giden iş.
- Voice AI research #0 ile doğal birleşir: leadgen → speed-to-lead call/reply agent.

### Swarm rolleri
- **Researcher Agent:** vertical seçer, şehir/keyword listesi çıkarır, rakip/offer/messaging tarar.
- **Source Hunter Agent:** Google Maps/Apify query planı, Reddit/forum intent search, directory/ad library source’ları üretir.
- **Scraper Pool:** liste çıkarır; duplicate’leri hashler; source riskini etiketler.
- **Website Miner Agent:** homepage + contact/about/team/staff/leadership gibi sayfaları çıkarır.
- **Contact Resolver Agent:** owner/manager/founder/office email + phone + social bulur.
- **Verifier Agent:** email status, catch-all, bounce risk, duplicate, suppression list kontrol eder.
- **ICP Scorer Agent:** lead’i 0-100 puanlar: niche fit, urgency, website weakness, reviews, ad/growth signal, location, company size.
- **Copywriter Agent:** 3-touch short cold email + first-line + subject üretir; AI/automation jargonunu yasaklar.
- **Compliance Sentinel:** CAN-SPAM footer, opt-out, physical address, no false claims, ToS risk, SMS/call consent kontrol eder.
- **Campaign Router:** başlangıçta sadece Google Sheet/CSV; onay sonrası Instantly/Smartlead upload.
- **Reply Classifier:** positive, question, objection, not interested, spam complaint, OOO sınıflandırır.
- **Analyst Agent:** cost per scraped place, cost per valid contact, reply rate, booked appointment, revenue attribution raporu yazar.
- **Human/Gokhan:** ilk müşterilerle görüşür, postal address/compliance onaylar, kampanya gönderimine final gate verir.

## Gerekli Bileşenler

- **Script/Bot:**
  - Vertical + city query generator
  - Apify/Maps source runner veya manuel export ingest
  - Website crawler/miner
  - Contact/email extractor
  - Email verifier wrapper
  - Dedupe + suppression registry
  - ICP score calculator
  - Personalized sequence generator
  - CSV/Google Sheets exporter
  - Reply classifier + weekly report generator
- **MCP/Araç:**
  - arxiv + mcptube + web fetch: sürekli araştırma ve playbook güncelleme
  - browser automation / Playwright / Chrome DevTools AXI: web/source inspection
  - Google Sheets/Airtable: ilk CRM/ops layer
  - Apify: Maps/LinkedIn/website actors; dikkat: ToS risk etiketi
  - Instantly veya Smartlead: sender layer, ama sadece onaylı kampanya aşamasında
  - Hunter/Apollo/Clay: fallback enrichment veya manual/export tabanlı kullanım
- **API:**
  - Apify Google Maps Scraper: resmi sayfada from $2.10 / 1,000 scraped places; pratikte actor/field seçimine göre artabilir.
  - Apollo: Basic $49/user/mo annual, Professional $79/user/mo annual, Organization $119/user/mo annual min 3 users; resmi export/API sınırlarıyla kullanılmalı.
  - Clay: Launch/Growth; Growth $446/mo, 40k actions/mo + 6k data credits/mo; POC için pahalı, ama enrichment waterfall tasarımı örnek alınabilir.
  - Hunter: Starter $49/mo; failed lookup free, verified email 0.5 credit.
  - Instantly: Growth $47/mo, Hypergrowth $97/mo, Light Speed $358/mo; sender + lead DB modüler.
  - Smartlead: Base $39/mo, Pro $94/mo, Unlimited Smart $174/mo; yüksek hacimde sender layer için mantıklı.
  - OpenAI/Anthropic küçük model: website text → structured extraction + personalization; düşük token maliyetli model yeterli.
- **İnsan Müdahalesi:**
  - İlk kampanya gönderim onayı.
  - İlk 100 lead kalite review.
  - İlk 20 reply/objection elle sınıflandırma.
  - Müşteri demo/satış görüşmesi.
  - Hukuki/compliance/postal address kararı.
  - Platform ToS risk değerlendirmesi.

## Workflow Haritası

**Tetikleyici → Vertical sprint seçimi**
1. Researcher “HVAC Austin TX” gibi bir vertical+geo sprint açar.
2. Source Hunter keyword havuzu üretir: `hvac repair`, `air conditioning contractor`, `plumber`, `roofing contractor`, mahalle/zip varyasyonları.
3. Compliance Sentinel source riskini belirler: official API / Apify / public website / platform ToS risk.

**Lead source → raw company list**
4. Scraper Pool işletme listesini çıkarır: name, address, phone, website, category, rating, reviews, maps URL/source URL.
5. Dedupe: `normalized_name + address + phone/domain` hash.
6. Website olmayanlar ya elenir ya phone-only segmentine ayrılır.

**Enrichment waterfall**
7. Website Miner homepage, contact, about, team, leadership, staff, service pages tarar.
8. Contact Resolver owner/manager/person email/phone/social bulur.
9. Verifier email’i valid/risky/catch-all/unknown olarak işaretler.
10. AI extraction 20-40 structured field çıkarır: services, emergency service, financing, city coverage, team size signals, recent offers, weak website signs, owner/person.
11. Paid enrichment sadece gap’ler için çalışır. Tersini yapmak para yakar.

**Scoring & segmentation**
12. ICP Scorer lead’i puanlar:
   - valid owner email +25
   - high review count/rating +10
   - weak website/no online booking +15
   - emergency/high-ticket service +15
   - recent bad review about phone/response +20
   - duplicate/shared/generic info -20
13. 80+ score “campaign-ready”; 60-79 “manual review”; <60 “nurture/archive”.

**Outreach prep**
14. Copywriter 3-touch sequence üretir:
   - Email 1: pain-based, 60-90 kelime, tek CTA.
   - Email 2: short bump + vertical proof.
   - Email 3: breakup / permission-based close.
15. Compliance Sentinel footer/opt-out/claim risk kontrol eder.
16. Human onaylamadan gönderim yok.

**Campaign & reply ops**
17. Campaign Router leads’i Instantly/Smartlead veya CSV olarak ayırır.
18. Rate limits: yeni domain/mailbox agresif gönderilmez; bounce threshold izlenir.
19. Reply Classifier cevapları sınıflandırır.
20. Positive/question reply → human/Gokhan veya appointment setter.
21. Weekly Analyst report: scraped count, valid email yield, sent, reply, positive, booked appointment, cost, learnings.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

Hemen yapılacak şey: **HVAC/Roofing Local Lead Intelligence POC**.

### En düşük çaba / en yüksek çıktı
- Tek dikey + tek şehir seç: örn. **HVAC contractors in Austin TX** veya **roofing contractors in Dallas TX**.
- 300-500 raw business scrape/export.
- Website olanları zenginleştir.
- İlk hedef: **100 verified/contactable lead** ve **20 “high-confidence owner/manager” lead**.
- Çıktı: müşteri satılabilir CSV + 3-email sequence + mini rapor.

### Hangi mevcut araç/script bu işi kısmen yapar?
- `projeler.txt` içinde web scraping/agentic browser kaynakları var; yeni ürün yazmadan research/source discovery yapılabilir.
- MCPTube n8n şablonlarından Google Sheets → Apify → website scrape → AI extraction akışı POC olarak klonlanabilir.
- UniverseCreator’ın mevcut araştırma stack’i: arxiv, mcptube, web fetch, browser automation; lead source ve vertical research için yeterli.
- İlk aşamada production script yazmak şart değil; CSV/Sheets + elle kontrollü workflow daha güvenli.

### Proof-of-concept minimum gereksinimleri
- Google Sheet kolonları:
  - `company_name`, `category`, `city`, `state`, `address`, `phone`, `website`, `source_url`, `rating`, `review_count`
  - `owner_name`, `owner_email`, `role`, `email_status`, `socials`, `services`, `pain_signal`, `icp_score`
  - `first_line`, `email_1`, `email_2`, `email_3`, `compliance_status`, `send_status`
- Dedupe hash.
- Suppression list.
- 10 lead sample human review.
- Offer: “We find local businesses losing booked jobs because they respond too slowly; we deliver verified owner contacts + response-risk score + outreach copy.”

### Tahmini kurulum süresi ve ilk gelir beklentisi
- Research/source setup: 1 gün.
- 300-500 lead scrape/enrich: 1-2 gün.
- Quality review + scoring: 1 gün.
- Offer page / sample report / demo CSV: 1 gün.
- Outreach to first buyers: 3-5 gün.
- İlk gelir hipotezi:
  - Lead intelligence pack: **$49-$199** tek seferlik.
  - Done-for-you appointment pilot: **$500-$1,500 setup + $300-$800/mo**.
  - Pay-per-booked-appointment model: home services için **$150-$300/appointment** benchmark; ilk pilotta düşük risk için $75-$150 intro pricing.
- Break-even: Apify + verifier + LLM POC maliyeti muhtemelen **<$50**; tek $99 pack bile maliyeti çıkarır.

### Bu hafta yapılacak POC tanımı
- 1 vertical, 1 şehir, 300 business.
- Goal: valid email yield, owner match rate, cost per valid contact ölçmek.
- Gönderim yok; sadece lead pack + sample pitch. Gönderim ancak ayrı onayla.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

1. ay sonunda sistem “bir scrape dosyası” değil, **tekrarlanabilir leadgen swarm pipeline** olmalı.

### 1. ay hedef mimari
- 3 vertical template:
  1. HVAC/plumbing
  2. Roofing
  3. Dental/medspa
- Her vertical için:
  - query pack
  - source-risk policy
  - scoring rubric
  - 3-email sequence templates
  - objection handling
  - sample report
- 5 şehirde test:
  - Austin, Dallas, Phoenix, Orlando, Tampa gibi home-services yoğun şehirler.
- Metrics dashboard:
  - raw businesses scraped
  - website coverage %
  - email found %
  - valid email %
  - owner/person match %
  - cost per raw lead
  - cost per valid contact
  - high-score lead %
  - reply % / positive reply % / booked appointment %

### Hangi metric’ler başarıyı gösterir?
- **Data quality:** valid email yield >%30 başlangıç için kabul; >%50 iyi; owner match >%20 başlangıç; >%40 iyi.
- **Cost:** cost per valid contact <$0.20 hedef; worst-case <$0.75.
- **Sales:** 100 onaylı outreach’te positive reply >%2; booked call >%0.5 başlangıç.
- **Client value:** client başına haftalık 20+ high-confidence lead veya 2+ booked appointment.
- **Retention:** müşteri “lead list” değil “haftalık pipeline report” bekler hale gelmeli.

### Hangi adımlar paralel çalışabilir?
- Researcher 3 vertical query pack hazırlar.
- Scraper Pool şehir/zip işleri paralel böler.
- Website Miner contact/about/team sayfalarını paralel tarar.
- Verifier email doğrulamayı async çalıştırır.
- Copywriter sadece score>60 lead’ler için sequence üretir.
- Analyst her batch sonrası vendor/source hit-rate raporu çıkarır.

### Ölçeklendirme için ne gerekiyor?
- **İnsan:** İlk 1-2 ay human QA şart; %100 otomasyon erken dönemde saçmalık üretir.
- **Araç:** Apify $39/mo credit, Hunter/verification $49/mo veya pay-as-you-go, sender layer $39-$97/mo, domain/mailbox maliyetleri.
- **Bütçe:** İlk ay test bütçesi **$100-$300** yeterli; aktif kampanya ve mailbox setup ile **$300-$800/mo** bandına çıkar.
- **Operasyon:** suppression list, domain reputation monitoring, bounce thresholds, unsubscribe handling.
- **Legal:** CAN-SPAM footer/opt-out; SMS/call için prior consent olmadan otomasyon yok.

### Checkpoint’ler ve başarı kriterleri
- **Hafta 2:** 1 şehir/vertical POC, 100 verified contacts, sample report.
- **Hafta 4:** 3 vertical × 3 şehir dataset; en iyi vertical seçimi.
- **Ay 2:** 1 paying pilot veya 5 ciddi demo; reply classifier ve reporting oturmuş.
- **Ay 3:** 3 paying clients veya toplam $1K+ revenue; en az 1 vertical’da repeatable playbook.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo: tam otomatik sistem nasıl çalışır?
- Sistem her hafta vertical/geo fırsatlarını tarar.
- Query agent yeni şehirleri ve ZIP code batch’lerini açar.
- Lead source pool işletmeleri toplar.
- Private lead DB duplicate ve historical vendor hit-rate ile maliyeti düşürür.
- Enrichment waterfall her vertical için optimize olur.
- Copy/testing agent hangi subject/hook/social proof türünün hangi ICP’de çalıştığını öğrenir.
- Reply classifier human’a sadece pozitif/kararsız/hot reply taşır.
- Dashboard client’a “bu hafta 427 raw, 143 valid, 38 high-score, 7 positive replies, 2 booked calls” diye rapor verir.

### Yan ürünler / yeni gelir kolları
1. **Lead Intelligence Packs:** dikey/şehir başına CSV + mini report. $49-$199.
2. **Booked Appointment Engine:** qualified appointment başına $75-$300 veya retainer + performance.
3. **White-label Leadgen Ops:** agency’lere altyapı; $500-$2,000/mo.
4. **Vertical Data API:** “home services owner/contact/pain signals API”.
5. **Review Pain Miner:** Google/Yelp/reviewlerden “missed call / slow response / bad website” sinyali çıkaran ürün.
6. **Speed-to-Lead Bundle:** Araştırma #0’daki voice AI ile birleşir: yeni lead geldiğinde AI/human follow-up.
7. **Outbound Benchmark Reports:** sektör bazlı reply/booking benchmarks; data moat yaratır.

### Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek nedir?
- Clay/Apollo tek platform içinde güçlü ama pahalı/limitli; swarm daha ucuz vendor waterfall kurabilir.
- Klasik agency rapor üretmez; swarm her batch’te evidence, cost, quality, reply outcome raporu çıkarır.
- Scraper’lar data verir; swarm data + context + copy + routing + learning loop verir.
- Human operator her şeyi elle taşımaz; sadece high-risk/high-value kararları onaylar.

### White-label veya SaaS olarak satılabilir mi?
Evet, ama SaaS’a erken dalmak hata olur. Sıralama:
1. **DFY service:** ilk para ve öğrenme.
2. **Productized service:** dikey paket + standart rapor.
3. **Internal dashboard:** kendi operasyonu hızlandırmak için.
4. **White-label dashboard:** başka ajanslara.
5. **SaaS/API:** ancak 3+ vertical’da data quality ve buyer repeatability kanıtlanınca.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek.
- **Kurulum Süresi:** İlk POC 5-7 gün; ilk paying pilot 2-4 hafta; repeatable system 1-3 ay.
- **Aylık İşletme Maliyeti:**
  - POC: $0-$50.
  - Aktif leadgen ops: $100-$300.
  - Sender + verifier + multiple clients: $300-$800.
  - High-volume private DB/worker: $1K-$3K+, ama bu erken değil.
- **Potansiyel Gelir:**
  - Lead pack: $49-$199 each.
  - DFY campaign setup: $500-$1,500.
  - Retainer: $300-$1,500/mo/client.
  - Booked appointment: $75-$300 each vertical’a göre.
- **ROI Beklentisi:**
  - Lead pack modelinde ilk satışla break-even.
  - DFY pilotta 1 müşteriyle ay içi break-even.
  - Appointment modelinde 2-5 booked appointment maliyeti çıkarır.

## Mevcut Sistemle Entegrasyon

UniverseCreator’ın mevcut 113/ürün/Vercel portföyüyle birleşim şu şekilde olmalı:

- **Var olan ürünler landing/demo olarak kullanılabilir:** `email verifier`, `url tools`, `webhook tester`, `csv/json tools`, `regex tools` gibi ürünler leadgen agency stack içinde yardımcı/demo asset olur.
- **Araştırma swarm doğal rol alır:** Bu dosya zaten Researcher output’u; sonraki cycle’larda Builder/Codex execution moduna geçmeden planlar seçilir.
- **Payment blocker çözülene kadar düşük-friction satış:** Lemon/iyzico blokeri sürerken ilk satış PayPal/direct/manual invoice üzerinden olabilir; ama kullanıcı onayı olmadan dış mesaj yok.
- **Analysis artifacts:** `sistem-planlama/` strateji deposu; ileride seçilen plan `analysis/oneri.md` ve görev dosyalarına taşınabilir.
- **Voice AI entegrasyonu:** Araştırma #0’daki speed-to-lead sistemi leadgen pipeline’ın downstream ürünü olur. Leadgen → reply/call → appointment.
- **Swarm metric loop:** Her batch sonunda markdown/JSON rapor üretilebilir; ama bu turda kod yok.

## Riskler & Dikkat Edilecekler

- **Spam riski:** Soğuk outreach kontrolsüz yapılırsa domain/mailbox ölür. Human approval ve throttling şart.
- **Legal risk:** CAN-SPAM minimumlarını uygulamadan email gönderilmez; SMS/AI call için consent yoksa otomasyon yok.
- **Platform ToS riski:** Google Maps ve Apollo scraping kısıtlı. Official API/export veya ToS-risk etiketli veri kullanılmalı. “Çalışıyor” demek “güvenli” demek değil.
- **Data quality riski:** 500 raw lead → 100 usable contact normal olabilir. Yield metric’i en baştan ölçülmeli.
- **False personalization riski:** AI uydurma bilgiyle first line yazarsa güven biter. Copywriter sadece kaynaklı/verifiable context kullanmalı.
- **Deliverability riski:** catch-all/risky email’lere yüklenmek bounce/complaint doğurur. Verification + suppression şart.
- **Offer riski:** “AI leadgen automation” diye satmak zayıf. Pain/outcome sat: “missed opportunities”, “verified appointments”, “owner contacts”, “response time”.
- **Overbuilding riski:** Direkt dashboard/SaaS yapma. Önce bir CSV + rapor sat. Para gelmeden SaaS mimarisi yapmak builder porn olur.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek POC sprint seç:** `HVAC contractors in Austin TX` veya `roofing contractors in Dallas TX`; 300 business target, source-risk notuyla dataset çıkar.
2. **Lead quality benchmark üret:** website coverage, valid email yield, owner match, cost per valid contact, top 20 high-score lead ve 3-email sequence.
3. **Satılabilir demo paketi hazırla:** 10 örnek lead sansürlü preview + “weekly local lead intelligence / booked appointment engine” teklif metni + fiyat: $99 lead pack veya $500 pilot setup.
