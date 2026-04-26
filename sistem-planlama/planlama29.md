# Planlama #29 — Lead Generation Automation Uygulama Haritası
**Tarih:** 2026-04-21 22:13 +03  
**Bağlı Araştırma:** `arastirma29.md`  
**Konu:** Google Maps → enrichment → review intelligence → outreach angle → lead pack / managed outbound

## Swarm Agent ile Nasıl Uygulanır?

Bu işi “scraper bot” diye kurmak zayıf fikir. Scraper commodity. Doğru sistem, UniverseCreator swarm içinde **vertical lead intelligence factory** olmalı:

1. **ICP Agent** — dikey + lokasyon + teklif seçer. Örnek: “roofing companies in Austin”, “dentists in Istanbul”, “HVAC contractors in Dallas”.
2. **Source Agent** — Google Maps / website / public directory kaynaklarından işletme listesini çıkarır.
3. **Enrichment Agent** — website, phone, email, social links, review count, rating, opening hours, service pages, schema data toplar.
4. **Verifier Agent** — duplicate, boş website, geçersiz email, düşük fit, compliance risk temizler.
5. **Review Intelligence Agent** — son review’lardan pain point ve urgency çıkarır: bekleme süresi, kötü servis, fiyat şikayeti, booking friction, kötü görsel/listing kalitesi.
6. **Offer Match Agent** — bizim/cliente ait teklifi prospect pain’iyle eşleştirir: “3D tour”, “missed-call bot”, “review response automation”, “SEO content pack”.
7. **Outreach QA Agent** — 75 kelime altı email, call opener, LinkedIn note üretir; spam/jargon/abartı filtresi uygular.
8. **Human Approval Gate** — ilk 50-100 prospect mutlaka insan onayından geçer. Tam otomatik spam topu yapılmaz; saçma olur.
9. **CRM/Sheet Sync Agent** — lead pack’i Google Sheet/CSV/CRM’e yazar, status ve feedback toplar.
10. **Performance Analyst Agent** — valid contact hit rate, reply, meeting, close, cost-per-meeting, cost-per-closed-deal ölçer.

## Gerekli Bileşenler

- **Script/Bot:**
  - Google Maps/company scraper wrapper
  - Website contact scraper
  - Review collector/summarizer
  - Dedupe + normalization
  - Email verifier integration
  - Lead score calculator
  - Outreach copy generator + QA filter
  - Exporter: CSV/Google Sheet/CRM
- **MCP/Araç:**
  - Jina Reader: landing pages/docs/competitor pages
  - Playwright/Chrome DevTools: JS-heavy directories ve manual validation
  - GitHub CLI/gh-axi: açık kaynak scraper inceleme
  - MCPTube: n8n/Apify workflow transcriptleri
  - ArXiv MCP: sales agent / CRM intelligence research
- **API:**
  - POC: open-source scraper veya Apify actor
  - Enrichment: Hunter / AnyMailFinder / NeverBounce / MillionVerifier
  - LLM: OpenAI/Claude/Kimi review+copy scoring
  - Outreach ops: Instantly/Smartlead/EmailBison ileride; POC’ta manuel/Sheet daha güvenli
  - Official fallback: Google Places API; field mask kullanmadan maliyet patlar
- **İnsan Müdahalesi:**
  - Dikey ve teklif seçimi
  - İlk data kalite kontrolü
  - İlk 50 email/call opener approval
  - Reply handling ve satış görüşmesi
  - Legal/compliance kararı: CAN-SPAM/GDPR/KVKK, opt-out, veri kaynağı, no-spam policy

## Workflow Haritası

**Tetikleyici:** `vertical + city + offer + max_leads` girilir.  
**Akış:**
1. ICP Agent: vertical schema oluşturur.
2. Source Agent: Maps query listesi üretir.
3. Scraper: business records çeker.
4. Verifier: website/phone/rating/review count filtresi uygular.
5. Enrichment: website contact + social + email bulur.
6. Review Agent: son yorumlardan pain evidence çıkarır.
7. Scoring: fit / urgency / contactability / proof score hesaplar.
8. Offer Match: prospect-specific angle üretir.
9. Outreach QA: email + call opener + LinkedIn note yazar, spam filtresinden geçirir.
10. Human Gate: örnekleri onaylar.
11. Export: CSV/Sheet/CRM + “why this lead” evidence pack.
12. Analyst: sonuçları ölçer, sonraki run için query/scoring ağırlıklarını günceller.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)

**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

**Hemen yapılacak MVP:** “100 scored local leads + outreach angles” lead pack generator.

- **En düşük çaba / en yüksek çıktı adımı:** Tek dikey seç: roofing/HVAC/dental. Tek lokasyon seç. 100 işletme çıkar, website/email/review pain ile skorla, CSV + 5 örnek kişiselleştirilmiş email üret.
- **Mevcut araç/script:** Açık kaynak `gosom/google-maps-scraper` veya Apify Google Maps actor; email validation için Hunter/AnyMailFinder; review/copy için mevcut LLM API; çıktı Google Sheet.
- **Minimum POC gereksinimleri:**
  - 100 raw business record
  - En az 35 valid website/contact
  - Her lead için 1 pain evidence + 1 outreach angle
  - Bounce risk kontrolü
  - İnsan onaylı ilk 30-50 outreach
- **Tahmini kurulum süresi:** 3-5 gün araştırma+script bağlama, 2-3 gün data quality/prompt tuning, toplam 1 hafta içinde demonstrable lead pack.
- **İlk gelir beklentisi:**
  - One-off lead intelligence pack: **$99-$299**
  - Managed outreach pilot: **$500-$1,500/month**
  - High-ticket local vertical/agency client yakalanırsa ilk ay **$1k-$3k** mümkün; bunu tahmin olarak etiketle, garanti değil.

Kısa vadede hedef SaaS değil. SaaS yazmaya kalkmak burada yavaş ve gereksiz. İlk para **servisleştirilmiş lead intelligence pack**’ten gelir.

## 📆 Orta Vade (1-3 ay içinde)

**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay hedef görünüm:**
  - 3 dikey: roofing/HVAC/dental veya real estate/medspa/agency
  - Her dikey için 3 şehir test edilmiş
  - 1,000-3,000 temiz business record
  - 300-800 verified contact
  - 100-200 human-approved outreach
  - Reply/meeting/lead-quality dashboard
- **Başarı metrikleri:**
  - Raw → qualified dönüşüm: **%20-40**
  - Qualified → verified contact: **%30-60**
  - Bounce: **<%3-5**
  - Cold email reply: **%3-8** başlangıç, iyi listede **%8+**
  - Positive reply/action: **%1-3** başlangıç
  - Meeting booked: **%0.5-2**
  - Cost per verified contact: **<$0.20-$0.80** POC hedefi
  - Cost per booked meeting: dikeye göre ölçülür; roofing gibi yüksek LTV’de daha pahalı meeting kabul edilebilir.
- **Paralel çalışacak adımlar:**
  - Data pipeline hardening
  - Prompt/scoring eval
  - Dikey landing/pitch deck
  - Agency outreach
  - Deliverability setup
  - CRM feedback loop
- **Ölçeklendirme gereksinimi:**
  - 1 operator/sales closer
  - $100-$300/month tool budget POC
  - $300-$800/month enrichment/outreach budget growth phase
  - Domain/inbox yönetimi ama agresif volume yok
- **Checkpoint’ler:**
  - Hafta 2: İlk 100 lead pack kalite raporu
  - Hafta 4: İlk paid pilot veya 3 ciddi satış görüşmesi
  - Ay 2: 2 dikeyde tekrarlanabilir pipeline
  - Ay 3: 3+ müşteri veya net pivot kararı

## 🚀 Uzun Vade (3-12 ay) ve Evrim

**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator içinde sürekli çalışan “Local Signal Engine” olur. Her gece seçili şehir/dikeylerde yeni businesses, rating düşüşleri, kötü review patlamaları, yeni website/social sinyalleri, hiring/ad-spend sinyalleri toplanır; sistem satış fırsatı doğduğu anda lead pack üretir.
- **Yan ürünler / gelir kolları:**
  1. Lead intelligence packs: $99-$499 one-off
  2. Managed local outbound: $1k-$3k/mo + success fee
  3. Agency white-label dashboard: $199-$999/mo
  4. Vertical data API: “review pain score for dentists/HVAC/roofing”
  5. Existing 113 product için prospect finder: örn. QR, PDF, URL, webhook, review automation ihtiyacı olan işletmeleri bulmak
- **Rakiplerin yapamadığı şey:** Swarm yaklaşımıyla sadece data değil, **kanıtlı satış gerekçesi** üretmek: review snippet → pain category → teklif angle → email/call opener → CRM outcome → next-run learning.
- **White-label / SaaS ihtimali:** Evet, ama 3 ay veri ve müşteri konuşması olmadan SaaS’a gömülmek yanlış. Önce managed service + CSV/Sheet. Sonra dashboard. En son self-serve SaaS.
- **Moat:** Data freshness + vertical scoring rubric + closed-loop performance history. Scraper moat değil; herkes scraper kurar.

## Öncelik & Çaba Tahmini

- **Öncelik:** Yüksek — ama sadece “vertical pain-scored lead packs” olarak. Generic lead scraper fikri düşük değerli.
- **Kurulum Süresi:**
  - POC: 5-10 gün
  - İlk paid pilot: 2-4 hafta
  - Repeatable ops: 6-10 hafta
- **Aylık İşletme Maliyeti:**
  - POC: **$100-$300/month**
  - Growth: **$300-$1,000/month**
  - Scale/high volume: deliverability, enrichment ve proxy maliyetleriyle **$1k+**
- **Potansiyel Gelir:**
  - İlk ay: **$500-$3,000** tahmini
  - 3 ay: 3-5 managed client ile **$3k-$10k MRR** tahmini
  - 12 ay: agency white-label + managed service ile **$10k-$50k MRR** mümkün ama satış execution şart.
- **ROI Beklentisi:** İlk paid client ile break-even. Tool maliyeti düşük; risk zaman ve deliverability.

## Mevcut Sistemle Entegrasyon

UniverseCreator’da 113 ürün + swarm zaten var. Leadgen sistemi iki yönde bağlanır:

1. **Yeni gelir hattı:** Local businesses/agencies için lead intelligence pack üretip satmak.
2. **Mevcut ürünlere demand gen:** 113 ürünün her biri için “bu ürüne ihtiyaç duyabilecek işletmeler” listesi üretmek. Örnek:
   - QR/URL tool → restoran, salon, etkinlik, real estate agency
   - PDF/webhook/API tools → ajanslar, küçük SaaS’lar, e-commerce ops
   - Review/voice automation → dental/HVAC/medspa/auto services

`universe_loop.sh` bu aşamada değiştirilmez. Araştırma sonrası uygulamada ayrı bir `lead-intel` workflow veya agent task queue tasarlanmalı. İlk entegrasyon dosya tabanlı olabilir: `leads/YYYY-MM-DD-vertical-city.csv`, score JSON ve outreach draft markdown.

## Riskler & Dikkat Edilecekler

- **Scraping ToS / legal:** Google Maps scraping ve personal data kullanımı riskli. Official API veya düşük-risk public business data + opt-out yaklaşımı seçilmeli.
- **CAN-SPAM/GDPR/KVKK:** Opt-out, physical address, legitimate interest/consent değerlendirmesi, veri kaynağı ve silme talebi mekanizması olmadan outbound büyütülmez.
- **Deliverability:** Yeni domainleri yakmak kolay. 30 email/day/inbox, SPF/DKIM/DMARC, warmup, bounce cap ve no-open-tracking gibi disiplin şart.
- **AI hallucination:** Review pain veya sales angle uydurursa marka yanar. Her outreach “evidence-backed” olmalı.
- **Shared lead kalitesi:** Ucuz lead vendor’lar cost-per-deal’i mahvedebilir. Exclusive/first-party/intelligence-enriched data daha iyi konumlanmalı.
- **API maliyet patlaması:** Reviews + Places + enrichment + LLM maliyeti hızla artar. Field mask, cache, dedupe ve batch şart.
- **Human sales bottleneck:** Lead üretmek satış yapmak değildir. Reply handling ve closing sahibi yoksa pipeline sadece vanity metric üretir.

## Önce Yapılacak 3 Adım (Bu Hafta)

1. **Tek ICP seç:** Roofing/HVAC/dental içinden birini seç, tek şehirde 100 lead hedefle. Tavsiyem roofing veya HVAC: ticket büyük, lead economics acı, ROI anlatması kolay.
2. **Manual-quality POC çıkar:** 100 business → website/contact/review pain → 30-50 verified leads → her biri için “why this lead” + 1 email + 1 call opener üret. Henüz tam otomatik gönderim yok.
3. **Satılabilir pack yap:** “100 scored HVAC prospects in [city] + review pain evidence + personalized outreach angles” başlığıyla $99-$299 pilot teklif hazırla; 10 agency/local-service owner’a manuel gönder.

Kısa karar: **Bu hafta SaaS değil, lead intelligence pack.** Spam bot yapmak kolay; para eden şey kanıtlı ve dikey odaklı satış zekâsı.
