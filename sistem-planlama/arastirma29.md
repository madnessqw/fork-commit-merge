# Araştırma #29 — Lead Generation Automation: Google Maps → Enrichment → Outreach
**Tarih:** 2026-04-21 22:13 +03  
**Konu:** Lead Generation Automation — HVAC/solar/roofing/dental/local services için Google Maps, website scraping, enrichment, review-intelligence, cold email/call, cost-per-lead ve gerçek implementasyonlar  
**Counter:** N=29 → konu indeksi `29 % 14 + 1 = 2`

**Kaynaklar / kullanılan katmanlar:**
- Yerel katalog: `/home/gokhan/UniverseCreator/projeler.txt` içinde `lead|scrape|outreach|cold email|apify|google maps|maps|enrich|solar|roofing|dental|hvac` taraması.
- ddgr: `Lead Generation Automation araştırma keywords 2025` ve dikey CPL sorguları denendi; DuckDuckGo `HTTP Error 202: Accepted` + boş JSON döndürdü, bu yüzden factual kaynak olarak kullanılmadı.
- Web/Jina Reader:
  - WordStream / LocaliQ 2025 Google Ads benchmarks: https://www.wordstream.com/blog/2025-google-ads-benchmarks
  - MapiLeads B2B lead workflow: https://mapileads.com/blog/maps-scraper-automate-b2b-lead-generation-workflow-2025
  - Artemis 2025 cold email benchmarks: https://www.artemisleads.com/resources-outbound-lead-generation/cold-email-response-rates-benchmarks-2025
  - Apify pricing: https://apify.com/pricing
  - Hunter pricing: https://hunter.io/pricing
  - Google Places API usage/billing: https://developers.google.com/maps/documentation/places/web-service/usage-and-billing
  - ProductHunt 2025 leaderboard: https://www.producthunt.com/leaderboard/yearly/2025/all
- Reddit JSON API:
  - Local business → email scrape → review intelligence tool: https://reddit.com/r/SideProject/comments/1s8wmu7/i_built_a_tool_that_lets_you_find_local/
  - Cold call opener metrics: https://reddit.com/r/Entrepreneur/comments/1r3ubz0/the_cold_call_opener_that_gets_me_past/
  - Roofing marketing cost-per-deal breakdown: https://reddit.com/r/RoofingSales/comments/1ru613z/i_tracked_every_dollar_spent_on_marketing_for_6/
  - Cold email campaign anecdote: https://reddit.com/r/coldemail/comments/1p0cf0n/how_i_sent_9158_emails_and_landed_50000_in_leads/
  - “907 leads” cold email process: https://reddit.com/r/LeadGeneration/comments/1jhey14/i_generated_907_leads_this_month_so_far_steal_my/
- GitHub gerçek implementasyonlar:
  - https://github.com/gosom/google-maps-scraper
  - https://github.com/omkarcloud/google-maps-scraper
  - https://github.com/asiifdev/business-leads-ai-automation
  - https://github.com/Astoriel/LeadGenius
  - https://github.com/growthenginenowoslawski/coldoutboundskills
  - https://github.com/PaulleDemon/Email-automation
- derin-arastirma:
  - ArXiv: Sales Research Agent / Sales Research Bench: https://arxiv.org/abs/2602.17017
  - ArXiv: Enterprise Sales Copilot: https://arxiv.org/abs/2603.21416
  - MCPTube videoları/transkriptleri: 
    - Michele Torti — “How I Built a Fully Automated Lead Gen System (n8n Tutorial)” https://www.youtube.com/watch?v=XPK7D1qd2XY
    - Chase AI — “This n8n Automation Scrapes Google Maps AND gets emails!” https://www.youtube.com/watch?v=Dxqhe26dXzc
    - Fabian Markl — “Build a Lead Gen AI Agent in Under 30 Minutes” https://www.youtube.com/watch?v=6nZ1oYu78_o
    - Taylor Haren — “How I Get Unlimited Leads Using Claude Code” https://www.youtube.com/watch?v=Vo9VUnzYqpw
- ProductHunt: Jina Reader ProductHunt search/topic sayfalarında Cloudflare/403 verdi; fallback olarak ProductHunt yearly leaderboard sayfası kullanıldı. SocLeads 2.0 gibi “social media + maps lead generation” araçları listede görünür durumda, ama bu tek başına satış kanıtı değil.

## Özet Bulgular

1. **En iyi wedge “lead listesi” değil, “pain-scored lead intelligence pack”.** Google Maps’ten işletme adı/telefon/web sitesi çekmek artık commodity. Para; Google reviews, web sitesi, kategori, lokasyon, rating/review count, karar verici email’i ve teklif-eşleşme skoru birleşince çıkıyor.
2. **Paid ads CPL’i yüksek olduğu için local services mantıklı dikey.** WordStream/LocaliQ 2025 verisi 16,000+ kampanya analizine dayanıyor; ortalama Google Ads CPL **$70.11**, Home & Home Improvement **$90.92**, Dentists & Dental Services **$83.93**. Aynı raporda average CPC **$5.26**, Home & Home Improvement ve Dentists CPC **$7.85**. Yani iyi filtrelenmiş outbound listesi “ucuz lead” değil, paid-search waste’ini azaltan satış zekâsı diye satılmalı.
3. **Reddit sinyali net: API maliyeti ve deliverability, ürünün boğazı.** Local-business scraping + review intelligence aracının postunda ilk eleştiriler Maps/API maliyeti, AI maliyeti, email scraping ve sender reputation etrafında dönüyor. “Scrape edip spam at” fikri ucuz ama aptalca; sistemin compliance + opt-out + human approval + düşük hacimli personalization içermesi şart.
4. **GitHub tarafında Google Maps scraper olgun; moat scraping değil orkestrasyon.** `gosom/google-maps-scraper` aramada **3,734★**, `omkarcloud/google-maps-scraper` **2,595★**; ikisi de phone, website, rating/reviews, emails/enrichment/API gibi alanlara gidiyor. Açık kaynak scraper var; fark yaratacak yer dedupe, validation, review intelligence, lead scoring, CRM sync ve campaign QA.
5. **Cold outbound hâlâ çalışıyor ama sadece yüksek niyet + düşük hacim + iyi data ile.** Artemis 2025 benchmark’ı ortalama reply rate’i **%8.5** bandında, positive action rate’i çoğu kampanyada **%1-5** aralığında veriyor; multi-channel kampanyalar email-only’den belirgin daha iyi. Reddit anekdotları yüksek hacimde başarı iddia ediyor ama yorumlarda güven şüphesi yüksek. Ölçekli cold email’i gelir kanalı diye değil, kontrollü test kanalı diye düşünmek lazım.

## Gerçek Başarı Hikayeleri / Vaka Sinyalleri

### 1) MapiLeads senaryosu — Maps + reviews + AI scoring ile satış pack’i
- MapiLeads’in workflow yazısı Google Maps scraper, CRM, AI analysis, review intelligence ve smart email generation’ı tek hatta bağlıyor.
- Verdiği örnek senaryoda aylık **800 lead**, **200 hot prospect**, **120 verified email**, **18 response**, **8 meeting**, **2-3 closed client** ve **$5,000-$7,500 monthly recurring revenue** iddiası var.
- Aynı senaryoda maliyet stack’i yaklaşık **$108/month** olarak veriliyor.
- Not: Bu vendor kaynaklı simülasyon/case; bağımsız doğrulanmış müşteri finansalı gibi okunmamalı. Yine de unit economics modellemek için kullanışlı.

Kaynak: https://mapileads.com/blog/maps-scraper-automate-b2b-lead-generation-workflow-2025

### 2) Reddit SideProject — local business intelligence tool
- Araç akışı: kullanıcı “real estate agencies + şehir/ülke” gibi sorgu giriyor; Google Maps’ten **30+ business field** alıyor; web sitelerinden email/telefon/sosyal profil çıkarıyor; **işletme başına 50’ye kadar Google review** analiz ediyor; pain point + lead score + cold email taslağı üretiyor.
- Community ilgisi var ama ilk sorular “Maps API cost?”, “AI API fees?”, “email scraping + deliverability sender reputation?” etrafında. Yani müşterinin satın alacağı şey sihirli scraper değil, **maliyet kontrollü ve güvenli satış prosesi**.
- Ürün fikri güçlü: review intelligence ile teklif eşleştirme, klasik “email finder” araçlarından daha iyi bir ayrışma.

Kaynak: https://reddit.com/r/SideProject/comments/1s8wmu7/i_built_a_tool_that_lets_you_find_local/

### 3) Reddit / coldemail — yüksek hacimli outbound anekdotu
- Post sahibi **23,116 email** gönderdiğini, open tracking kapalı tuttuğunu, **167 reply (%1.8)**, **50 warm lead** ve **$50,000 opportunity** ürettiğini söylüyor.
- Yorumlarda başka bir kullanıcı **40k email/week**, **300-400 account** ölçeğinde Ağustos sonrası sonuçların düştüğünü yazıyor; bu, deliverability’nin kırılgan olduğunu gösteriyor.
- Bu vaka “email cannon kur” demiyor; tam tersine: hacim büyüyünce domain/account operasyonu ayrı ürün oluyor ve en küçük deliverability hatası tüm sistemi yakıyor.

Kaynak: https://reddit.com/r/coldemail/comments/1p0cf0n/how_i_sent_9158_emails_and_landed_50000_in_leads/

### 4) RoofingSales — cost-per-lead değil cost-per-closed-deal takip et
- 6 roofing company için 90 günlük anekdot breakdown:
  - Facebook ads: **$5,200/month**, 190 leads, 5 closed deal → **$1,040 per closed deal**
  - Shared lead vendor: **$4,800/month**, 32 bought leads, 1 deal → **$4,800 per closed deal**
  - Door knocking: **$8,400/month**, 9 deals → **$933 per closed deal**
  - Cold calling team: **$4,300/month**, 6 deals → **$716 per closed deal**
  - Google Ads/LSA/PPC: **$6,100/month**, 5 deals → **$1,220 per closed deal**
  - Storm chasing + cold calling: **$5,500/month**, 11 deals → **$500 per closed deal**
- Yorumlarda biri kendi Google leads sold-deal cost’unun yaklaşık **$1,250** olduğunu ve ortalama iş kârının **$8,000** olduğunu yazıyor. Bu bize satış argümanını veriyor: “$80 lead” değil, “$1,250 acquisition cost’u düşür ve lead leak’i kapat.”
- Not: Reddit verisi bağımsız audit değil; ama local-services economics’i anlatmak için çok iyi saha sinyali.

Kaynak: https://reddit.com/r/RoofingSales/comments/1ru613z/i_tracked_every_dollar_spent_on_marketing_for_6/

### 5) MCPTube / n8n workflow demo’ları — pratik akış netleşmiş
- Michele Torti videosunda akış: Google Sheet trigger → Apify Google Maps scraper → website exists filtresi → batch/loop → AnyMailFinder → website scrape → AI icebreaker/email → Google Sheet status update → Instantly/Smartlead’e aktarım.
- Demo’da **190 scraped item → 36 valid lead** gibi bir kalite filtresi görülüyor. Bu çok önemli: ham scrape’in çoğu değersiz; sistemin değeri “elenmiş, doğrulanmış, gerekçeli” lead üretmek.
- Video ayrıca 200’lük batch’lerle AI/automation overload riskini azaltmayı anlatıyor. Bu, UniverseCreator swarm için doğrudan pattern: scrape agent ayrı, verifier ayrı, AI-personalization ayrı, QA gate ayrı.

Kaynaklar:
- https://www.youtube.com/watch?v=XPK7D1qd2XY
- https://www.youtube.com/watch?v=Dxqhe26dXzc
- https://www.youtube.com/watch?v=6nZ1oYu78_o

## Pazar Büyüklüğü & Fırsat

### Paid acquisition baskısı
- WordStream/LocaliQ 2025: Search advertising costs son beş yıldır artıyor; 2025’te CPC **23 endüstrinin 20’sinde** yükseldi. CPL artışı 2024’e göre daha sakin ama hâlâ **23 endüstrinin 13’ünde** artmış.
- Ortalama Google Ads CPL: **$70.11**.
- Dikeyler:
  - Dentists & Dental Services: CTR **%5.44**, CPC **$7.85**, CPL **$83.93**.
  - Home & Home Improvement: CTR **%6.37**, CPC **$7.85**, CPL **$90.92**.
- Sonuç: Dental/HVAC/roofing gibi yüksek LTV’li local services’ta “lead başına $50-$150 reklam harcıyorum ama takip/kalite zayıf” acısı gerçek. Bu pazara “lead scraping” değil, **exclusive qualified opportunity** diye girilir.

Kaynak: https://www.wordstream.com/blog/2025-google-ads-benchmarks

### Cold outbound benchmark gerçekliği
- Artemis 2025: Ortalama reply rate **%8.5**; iyi kampanyalar **%10-20+**, zayıf kampanyalar **%5 altı**. Positive action rate çoğu kampanyada **%1-5**.
- Aynı kaynak multi-channel sequence’lerde positive action rate aralığını email-only’den daha yüksek gösteriyor: email-only yaklaşık **%0.7-4.2**, email + LinkedIn + phone yaklaşık **%1.4-8.2**.
- Bu, planın tek kanal spam olmaması gerektiğini söylüyor: email + LinkedIn + call + CRM follow-up ama düşük hacimli ve izin/opt-out kontrollü.

Kaynak: https://www.artemisleads.com/resources-outbound-lead-generation/cold-email-response-rates-benchmarks-2025

### ProductHunt / yeni araç sinyali
- ProductHunt yearly leaderboard içinde SocLeads 2.0 “Lead Generation from Social Media and Maps” olarak listeleniyor. Bu, pazarın araç üretmeye devam ettiğini gösterir ama tek başına revenue kanıtı değil.
- ProductHunt/Jina search Cloudflare ile 403 verdi; bu yüzden PH tarafını “trend sinyali” olarak düşük ağırlıkla kullanmak doğru.

Kaynak: https://www.producthunt.com/leaderboard/yearly/2025/all

## Rakipler & Boşluklar

### Mevcut çözüm kümeleri
- **Generic scrapers:** gosom, omkarcloud, Apify actors, Outscraper, SerpApi, HasData. Sorun: ham data verir, satış gerekçesi vermez.
- **Email finders/enrichment:** Hunter, AnyMailFinder, Apollo, Clay, LeadMagic, Wiza. Sorun: pahalılaşır, hit rate ICP’ye göre değişir, verified contact yetmez.
- **Cold email platforms:** Instantly, Smartlead, EmailBison. Sorun: deliverability ve kampanya kalite sorumluluğu müşteride kalır.
- **All-in-one lead tools:** MapiLeads/SocLeads benzeri araçlar. Sorun: çoğu “list builder” olarak kalıyor; local-service teklif eşleştirme ve review-pain narrative’i zayıf.

### Boşluklar
1. **Verticalized pain scoring:** “Dentist lead” değil; “son 30 review’da appointment wait complaint yüksek + online booking yok + rating düşüyor” gibi satış gerekçesi.
2. **Cost-per-closed-deal dashboard:** Rakipler lead sayar; müşteri closed deal maliyeti ister. CRM bağlantısı varsa en güçlü fark burada.
3. **Review intelligence + offer matching:** Google reviews, website/service pages ve teklif metni birlikte okunup kişiye özel angle çıkarılmalı.
4. **Compliance-first outbound:** Opt-out, consent source, data provenance, düşük hacim, domain warmup, bounce cap, human approval. Bu yoksa sistem spam makinesi olur.
5. **Agency-ready packs:** Local agency’lere “100 scored HVAC prospects + outreach angles + call openers + review pain evidence” olarak satılabilir. SaaS’tan önce servis/rapor daha hızlı para getirir.

## Teknik Gereksinimler

### Data source / scraping
- Google Maps source: open-source `gosom/google-maps-scraper` veya `omkarcloud/google-maps-scraper`; production’da Apify actor/SerpApi/official Places API seçenekleri değerlendirilmeli.
- Google Places API resmi hat: pay-as-you-go; field mask kullanmak maliyet kontrolü için şart. Google dokümanı, istenen fields’a göre en yüksek SKU’nun faturalandığını söylüyor.
- Scraper alanları: business name, category, address, phone, website, Google rating, review count, recent reviews, opening hours, social profiles, coordinates.

### Enrichment / validation
- Website scraper: contact page, footer, schema.org, mailto, social links.
- Email verifier: Hunter / AnyMailFinder / NeverBounce / MillionVerifier / Scrubby benzeri.
- Dedupe: domain, phone, address, Maps URL, normalized company name.
- Decision-maker enrichment: Apollo/Clay/LinkedIn Sales Nav kullanılabilir ama maliyet ve ToS riski yüksek; POC’ta company-level contact yeterli.

### AI layer
- Review summarizer: pain points, sentiment, recurring complaints, service gaps.
- Offer matcher: kullanıcının sattığı hizmet ile prospect pain’ini eşleştirir.
- Lead score: fit, urgency, contactability, proof strength, compliance risk.
- Outreach generator: 75 kelime altı email, call opener, LinkedIn note, follow-up 1/2. AI metinleri insan approval’dan geçmeli.

### Outreach / CRM
- İlk POC: CSV + Google Sheet + manuel outreach daha güvenli.
- Sonra: Instantly/Smartlead/EmailBison integration, HubSpot/Pipedrive sync, call queue.
- Metrics: valid contact hit rate, bounce rate, reply rate, positive reply, meeting booked, cost per meeting, cost per closed deal.

### Maliyet sinyalleri
- Apify: free plan $5 platform usage credit; Starter **$39/month** ve **$39 included usage credit**; Personal **$49/month** ve **$49 included usage credit**; Actor run maliyeti compute unit, storage, proxy ve data transfer’a bağlı.
- Hunter: Free **50 credits/month**, Starter **2,000 monthly credits** ve yıllık **24,000 credits**; pricing page API-only access seçeneği de sunuyor.
- Google Places API: field mask ve SKU seçimi maliyet kontrolünün merkezi; gereksiz Pro/Enterprise fields maliyeti şişirir.

Kaynaklar:
- https://apify.com/pricing
- https://hunter.io/pricing
- https://developers.google.com/maps/documentation/places/web-service/usage-and-billing

## Ham Notlar

- `projeler.txt` tarafında mevcut bilgi tabanı Apify/Crawlee, Scrapeless, CyberScraper, Google Maps/Ask Maps ve scraper/agent başlıkları içeriyor. Direkt leadgen ürün linki az; scraper altyapısı bilgisi var.
- GitHub aramasında `lead generation automation scraper` fazla dar kalınca sonuç çıkmadı; `leadgen`, `google maps scraper`, `cold email` gibi daha kısa sorgular iyi sonuç verdi. Bu, pazarın keyword realitesini de gösteriyor: repo’lar “leadgen” ve “google maps scraper” diye adlanıyor.
- ProductHunt Jina 403 verdi; web snapshot yeterli ama PH’yi ana kaynak yapmak zayıf olur.
- ArXiv doğrudan “Google Maps lead scraping” alanında işe yarar değil. Daha değerli akademik sinyal, enterprise sales agentlarının CRM/RAG + benchmark + real-time copilot tarafına kayması: sales automation’ın geleceği “lead çıkar” değil, “satış kararını kanıtlı destekle”.
- Reddit’te outbound metrikleri bol ama çoğu self-reported. Planlama dosyasında bu yüzden revenue iddialarını “anekdot / doğrulanmamış” diye etiketlemek şart.
