# Araştırma #1 — Lead Generation Automation
**Tarih:** 2026-04-21 03:12
**Konu:** Lead Generation Automation — pool agent pattern ile lokal/B2B lead bulma, enrichment, outreach ve appointment akışı

**Kaynaklar:**
- Proje kataloğu taraması: `/home/gokhan/UniverseCreator/projeler.txt` içinde `lead|scrape|outreach|cold email|hvac|solar|roofing|apollo|clay|instantly|smartlead` keyword taraması.
- Lucintel — Lead Generation Solution Market: https://www.lucintel.com/lead-generation-solution-market.aspx
- Emergen Research — Lead Generation Solution Market: https://www.emergenresearch.com/industry-report/lead-generation-solution-market
- Emergen Research — B2B Lead Generation Market: https://www.emergenresearch.com/industry-report/b2b-lead-generation-market
- Grand View Research Horizon — Lead Generation BPO market: https://www.grandviewresearch.com/horizon/statistics/business-process-outsourcing-market/sales-marketing/lead-generation/global
- Apollo pricing/2026 prospecting note: https://www.apollo.io/insights/best-prospecting-tool-with-flexible-pricing
- Clay pricing: https://www.clay.com/pricing
- Clay March 2026 pricing update: https://community.clay.com/x/announcements/ascrvx12878n/introduction-of-clays-new-pricing-model-with-cheap
- Instantly pricing: https://instantly.ai/pricing
- Instantly help center plan overview: https://help.instantly.ai/en/articles/10273259-plans-overview
- Smartlead pricing: https://www.smartlead.ai/pricing
- Hunter pricing: https://hunter.io/pricing
- Apify Google Maps Scraper: https://apify.com/compass/crawler-google-places
- Google Maps Platform pricing/FAQ/terms: https://mapsplatform.google.com/pricing/ , https://developers.google.com/maps/faq , https://cloud.google.com/maps-platform/terms/index-20190502
- Apollo Terms of Service: https://www.apollo.io/terms-of-service
- FTC CAN-SPAM guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FDIC TCPA overview / FCC consent references: https://www.fdic.gov/consumer-compliance-examination-manual/viii-5-telephone-consumer-protection-act
- Reddit r/coldemail — Google Maps pipeline under $0.01/lead: https://www.reddit.com/r/coldemail/comments/1r676eb/built_a_google_maps_lead_scraping_pipeline_for/
- Reddit r/LeadGeneration/r/Roofing snippets: home services CPL / booked appointment anecdotes.
- IndieHackers — Reddit lead gen playbook: https://www.indiehackers.com/post/wnH39S8GTmmBj3vtjLg8
- IndieHackers — 12,500 cold leads to projected $8K MRR: https://www.indiehackers.com/post/from-12-500-cold-leads-to-a-projected-8k-mrr-the-funnel-i-wish-i-d-built-sooner-88580fb0a0
- IndieHackers — Sales.co cold email agency to $90K MRR: https://www.indiehackers.com/post/turning-cold-email-into-a-90k-mrr-business-while-traveling-the-world-eQa83dCBNztwvK9KqqH5
- IndieHackers — $200K AI sales/marketing workflow validation: https://www.indiehackers.com/post/seeking-technical-co-founder-200k-usd-generated-ai-marketing-sales-workflow-000c36d446
- IndieHackers — med spa AI follow-up failure note: https://www.indiehackers.com/post/im-17-mass-cold-outreaching-med-spas-with-an-ai-follow-up-system-i-built-600-messages-0-revenue-here-s-everything-i-ve-learned-13e91611a7
- MCPTube videoları:
  - Zinho Automates — “This N8N Lead Generation Agent Scrapes FREE Leads (Using Google Maps)” — https://www.youtube.com/watch?v=A2e4VdN35Fw
  - Michele Torti — “How I Built a Fully Automated Lead Gen System (n8n Tutorial)” — https://www.youtube.com/watch?v=XPK7D1qd2XY
  - Chase AI — “n8n & Apollo Lead Generation Finally Solved” — https://www.youtube.com/watch?v=WBSNjimEe7Y
  - Taylor Haren — “How I Get Unlimited Leads Using Claude Code (For Cold Email)” — https://www.youtube.com/watch?v=Vo9VUnzYqpw
- ArXiv:
  - 2603.27476v1 — “PeopleSearchBench: A Multi-Dimensional Benchmark for Evaluating AI-Powered People Search Platforms”
  - 2602.17017v1 — “Sales Research Agent and Sales Research Bench”
  - 2412.05449v1 — “Towards Effective GenAI Multi-Agent Collaboration: Design and Evaluation for Enterprise Applications”
  - 2506.10991v1 — “What is Business Process Automation Anyway?”

## Özet Bulgular
- **Leadgen hâlâ para ediyor ama “liste satma” seviyesi commodity oldu.** Kazançlı wedge artık ham lead değil: intent yakalama + enrichment waterfall + doğrulama + kişiselleştirme + reply/appointment routing.
- **Pool agent pattern bu işe çok uygun:** scraper agent havuzu, website/contact-page enrichment agent havuzu, verifier agent, ICP scorer, copywriter, compliance guard, sender/CRM agent ve analyst agent paralel çalışabilir. Darboğaz tek model değil; veri kalitesi, dedupe, domain reputation ve follow-up disiplini.
- **Lokal hizmetler en iyi başlangıç dikeyi:** HVAC, plumbing, roofing, dental, medspa, legal, auto shops. Çünkü bu işletmeler Google Maps’te var, LinkedIn/Apollo’da zayıf; owner-level veri web sitelerinde saklı duruyor.
- **Unit economics POC için güzel:** Reddit örneğinde Apify Maps $0.004/place + contact enrichment $0.002 + Claude Haiku extraction ~$0.002 → toplam ~$0.008/lead iddiası var. Apify resmi actor sayfası Google Maps Scraper için “from $2.10 / 1,000 scraped places” gösteriyor; bu daha da düşük giriş maliyeti demek, ama alan/ek özelliklere göre oynar.
- **Cold outreach tek başına çöp olabilir; failure case bunu net gösteriyor.** IndieHackers med spa örneğinde 600+ kişiselleştirilmiş mesaj → $0 revenue. Problem gerçek olsa bile kanal/offer/trust yanlışsa sistem çalışmıyor. İlk ürün “lead listesi” değil, “nitelikli randevu/cevap sistemi” olmalı.

## Gerçek Başarı Hikayeleri

### 1) Reddit — Google Maps local business pipeline, ~$0.008/lead anekdotu
- Hedef: plumbers, electricians, HVAC, roofing contractors gibi Google Maps’te yaşayan ama LinkedIn’de zayıf lokal işletmeler.
- Pipeline maliyeti iddiası:
  - Google Maps scrape: $0.004/place
  - Apify contact details: $0.002/place
  - Claude Haiku structured extraction: ~$0.002/lead
  - Website scraping, DuckDuckGo enrichment, Google Sheets: free
  - Toplam: ~$0.008/lead; 100 lead ≈ $0.80, 1,000 lead ≈ $8.
- Output: 36 field — business basics, contact info, socials, owner info, team contacts, business hours.
- Gözlenen kalite: usable email %70-75, owner name %40-50, social profile ~%60; 403/503/site-block oranı %10-15.
- Kritik ders: düşük maliyet tek avantaj değil; owner-level veri Apollo/ZoomInfo’da yokken küçük işletmenin `/about` sayfasında var.
- Güven seviyesi: **orta/düşük** — Reddit anekdotu, ama teknik stack ve maliyet kalemleri tutarlı.

### 2) MCPTube/n8n — Google Maps → email finder → AI icebreaker → Sheets/Instantly
Michele Torti videosunda uçtan uca akış gösteriliyor:
- Input: Google Sheet’te business type, location, number, status=run.
- Scrape: Apify Google Maps actor; fields: title/category/address/city/postcode/state/country/website/phone.
- Filtering: website yoksa lead elenir.
- Batch strategy: 1,000 sonuç için 200’lük chunk’lar; AI overload ve workflow error azaltılıyor.
- Email discovery: Anymailfinder ile domain + decision-maker category; yalnızca `valid` email status ve full name olanlar geçiriliyor.
- AI personalization: website text scrape → GPT-4.1 mini ile custom icebreaker.
- Output: full name, email, company name, type, icebreaker → Google Sheets; sonra Instantly/Smartlead’e kampanya için aktarılabilir.
- Somut demo metriği: 190 item → 36 geçerli email/output; bu yaklaşık %19 valid-output yield. Bu iyi bir uyarı: scrape volume yüksek olsa bile qualified contact yield düşük olabilir.

### 3) Chase AI — Apollo scraper dönemi bitiyor, enrichment + upload otomasyonu kalıyor
- Video iddiası: Apollo/Apify scraper dönemi kapandı; illegal/ToS-gri “1,000 Apollo lead for $1.50” dönemi pratikte bitti.
- Yeni gerçek: Apollo veya alternatiflerinden export alınır; otomasyon %80 aynı kalır.
- Workflow:
  1. Apollo/lead source export → Google Sheets
  2. LinkedIn profile scrape + Perplexity company/person research
  3. LLM custom first-line / normalized company name
  4. Instantly API’ye email, first/last name, company, custom variables, campaign ID gönder
- Araç maliyeti notları:
  - Instantly lead source seçenekleri yaklaşık $47/$97/$197 bandı.
  - Apollo tarafında 100 dolar civarı aylık planlar 2k-4k email bandı için konuşuluyor.
  - LinkedIn profile scraping actor örneği $10/1,000 sonuç; Apify entry $39/mo credit modeli.
- Ders: sourcing API kırılırsa bile enrichment/copy/upload sistemi korunmalı; kaynak bağımlılığını azalt.

### 4) Taylor Haren — high-volume custom lead processor
- İddia edilen operasyon: 5M lead/week işlendi; custom system 272k rows/sec; 1M lead ~5 sec; Railway + GitHub + Postgres/Convex + 50 worker.
- Clay scale pain: 50k rows/table ve workspace row limitleri; Clay büyük ölçekli batch için pahalı/yavaş olabilir.
- Maliyet iddiası: lead processor Railway ~$1,966-$2,012/month; Claude Code $200/seat/month; Clay yerine internal tooling.
- Google Maps scrape stratejisi: city/state yerine ZIP code bazlı çalışmak; ABD’de ~32k zip code olduğu için coverage artıyor.
- Enrichment: şirket başına 3 lead bulma; AI contact search + confidence scores + vendor waterfall.
- Valid email uplift iddiası: Apollo/LinkedIn doğrudan ~%30 valid match’ten waterfall ile ~%95 valid contact seviyesine çıkarma.
- Gelir proof iddiaları: RB2B için 4 ayda $4M ARR scale; %42 revenue cold emailden; Fixer AI için $4.3M annual pipeline; Directive Consulting için 15-20 meeting/day.
- Güven seviyesi: **orta** — public video iddiası; doğrulanmış audit değil. Ama mimari ders çok değerli: own database + vendor waterfall + analytics moat.

### 5) IndieHackers — Reddit intent leadgen: 0 → $300 MRR / 21 gün
- Leado örneği: broad keyword değil “pain phrase” takibi.
- Sistem: binlerce subreddit tarama, explicit buying intent filtreleme, context-aware helpful reply draft, human approval.
- Sonuç iddiası: ~100 high-intent lead/week, $300 MRR in 21 days, $0 marketing cost.
- Ders: leadgen sadece email değil; community intent mining + human-in-loop daha düşük spam riskiyle çalışabilir.

### 6) IndieHackers — Sales.co cold email agency: $90K MRR
- Başlangıç: Magic Sales Bot ile $1,000 MRR; sonra “cold email for people” agency modeli.
- İlk satış taktiği: 3 şirkete 1 hafta ücretsiz hizmet; devam için $500/mo → $1,000 → $1,500 → $2,000; 2 şirket kaldı.
- 4-5 ay içinde $10K MRR, sonra röportaj başlığında $90K MRR.
- Operasyon: own lead scraping tools, personalization tooling, GPT ile reply categorization (`positive`, `neutral`, `has a question`) ve Airtable routing.
- Ders: ürünleşmeden önce service model cashflow yaratıyor; otomasyon önce içeride kullanılıp sonra SaaS’a dönebilir.

### 7) IndieHackers — 12,500 cold leads → projected $8K MRR funnel
- Girdi: 14,100 contacts uploaded, 12,500 validated.
- Maliyet: $10/1,000 → $140 total cold email spend.
- Funnel varsayımları:
  - 3-email sequence, Email 1 open rate %61.
  - Base reply %0.5 → 43 warm leads.
  - Content CTA 3% → 41 booked calls.
  - 25% close → $1,025 MRR.
  - Upsell/appointment layer ile projected $8K+ MRR.
- Güven seviyesi: **düşük/orta** — “projected”, gerçek MRR değil. Yine de funnel modelleme ve tagging mantığı iyi.

### 8) IndieHackers — $200K AI sales/marketing workflow satışı
- Non-technical marketer, B2B leadgen SaaS background.
- İddia: satış/marketing AI workflow’larını 4 ayda 1,000+ sales professional’a satarak $200K+ revenue.
- Ders: önce workflow/template/hizmet olarak sat, PMF görünce SaaSlaştır. UniverseCreator için “ürün yazmadan önce otomasyon paketi satma” doğrulanmış bir yol.

### 9) IndieHackers failure case — 600+ med spa outreach, $0 revenue
- Ürün: missed-call/form follow-up system; n8n + Twilio + OpenAI; 20 saniye içinde personalized SMS/email.
- Outreach: 600+ messages; 1 “interested” reply, sonra sessizlik; revenue $0.
- Dersler:
  - Contact forms zayıf kanal; owner call/email daha iyi.
  - “AI automation” diye satmak öldürüyor; pain-based pitch daha iyi: “new leads wait hours and book competitors.”
  - <1% response rate varsa yüzlerce touch normal.
- Bu failure case’i görmezden gelmek aptallık olur. Aynı hatayı yapmamak için GTM planında offer + trust + channel ayrı test edilmeli.

## Pazar Büyüklüğü & Fırsat

### Market numbers
- Lucintel: global lead generation solution market 2030’da **$9.7B**, 2024-2030 CAGR **%17.2**.
- Emergen Research: lead generation solution market 2024’te **$3.20B**, 2034’te **$8.70B**, CAGR **%10.5**.
- Emergen B2B lead generation market: 2024’te **$3.2B**, 2034’te **$8.1B**, CAGR **%9.7**; email marketing segmenti 2024’te **%34**, cloud deployment **%78**, North America **%42.3**.
- Grand View Horizon: lead generation BPO segmenti 2025’te **$14.457B**, 2033’te **$31.451B**, CAGR **%10.3**.

### Vertical economics — lokal hizmetler
Kaynaklar agency/vendor ağırlıklı olduğu için rakamları “directional benchmark” olarak kullanmak lazım:
- HVAC 2026 guide kaynakları: Google LSA yaklaşık **$25-75/lead**, Google PPC **$75-200/lead**, Angi/HomeAdvisor shared **$15-80/lead** ve düşük close rate.
- HVAC exclusive lead kaynakları: exclusive **$45-70/lead**, close **%25-35**; shared lead **$80-200/lead**, close **%5-12** iddiası.
- Roofing appointment pricing örnekleri: verified homeowner appointment **$175-$200/appointment** paketleri; Reddit roofing anekdotlarında residential exclusive lead **~$130** ve **%20-25 appointment rate** gibi sinyaller var.
- LeadGeneration subreddit anekdotu: home services (roofing/HVAC/solar) **$25-75 CPL**, **$150-300 booked appointment** aralığı.

### Fırsat nerede?
Ham lead listesi satarsak commodity oyuncularla yarışırız. Daha iyi wedge:
1. **Local business lead intelligence pack:** “Austin plumbers with weak websites + owner email + review pain + ad intent.”
2. **Booked appointment engine:** raw lead değil, verified/qualified appointment satışı.
3. **Intent monitor:** Reddit/forum/job post/ad library/Google Maps değişimi ile sıcak sinyal yakalama.
4. **Done-for-you outbound ops:** lead pool + enrichment + copy + sender + reply routing + weekly report.
5. **Private lead database moat:** her scrape/enrichment sonucu tekrar kullanılabilir; vendor cost zamanla düşer.

## Rakipler & Boşluklar

### Rakip/tool haritası
- **Apollo:** 230M+ verified contact DB, 65+ filters, multi-channel engagement; annual planlarda Free $0/900 credits/year, Basic $49/user/mo 30k credits/year, Professional $79/user/mo 48k, Organization $119/user/mo min 3 users 72k.
- **Clay:** enrichment/orchestration kralı; 2026 pricing modelinde Actions + Data Credits ayrımı. Launch 15k actions/mo + 2.5k data credits/mo; Growth $446/mo, 40k actions/mo + 6k data credits/mo. Data Credits $0.05’ten başlıyor, Actions < $0.01.
- **Instantly:** outreach Growth $47/mo, 1k uploaded contacts, 5k emails/mo; Hypergrowth $97/mo, 25k contacts, 100k-125k emails/mo; Light Speed $358/mo, 500k emails/mo. Lead database/credits modülü ayrıca.
- **Smartlead:** Base $39/mo (2k contacts, 6k sends, 2k verified emails), Pro $94/mo (30k contacts, 90k sends, 30k verified emails), Unlimited Smart $174/mo, Unlimited Prime $379/mo.
- **Hunter:** Starter $49/mo, Growth $149/mo, Scale $299/mo; 1 credit = 1 found email; 0.5 credit = 1 verified email; failed lookup free; unlimited team members.
- **Apify:** Google Maps Scraper resmi sayfasında “from $2.10 / 1,000 scraped places”; API, schedule, webhook, Zapier/Make/Airbyte/GSheets entegrasyonları var.

### Boşluklar
- **Tool fragmentation:** Data source başka, enrichment başka, sender başka, reply routing başka, reporting başka. Local SMB bunu kuramaz.
- **Local SMB owner data gap:** Apollo/LinkedIn küçük işletme owner bilgisinde zayıf; site scrape + maps + local directories daha iyi.
- **Compliance + deliverability gap:** Çoğu “AI leadgen” içeriği spam ateşliyor. CAN-SPAM, opt-out, physical postal address, domain warmup, bounce kontrolü, suppression list yoksa domain ölür.
- **Outcome reporting gap:** Müşteri “kaç lead” değil “kaç booked appointment / kaç teklif / kaç revenue” görmek ister.
- **Vertical-specific copy gap:** HVAC, roofing, medspa, dental aynı mesajla çalışmaz. Pool agent’in avantajı burada: segment başına copy/test/metric hafızası oluşturur.

## Teknik Gereksinimler

### Minimum sistem bileşenleri
- **Lead source layer:** Google Maps/Apify, official Places API gerektiğinde, Reddit/forum intent, job postings, ad libraries, directory scrape, Apollo/Hunter fallback.
- **Queue/pool layer:** Her query/task küçük job’a bölünür; worker pool paralel çalışır. Örn: `plumbers + Austin zip` → `places scrape` → `site scrape` → `email extract` → `verify` → `score`.
- **Enrichment waterfall:**
  1. Maps listing data
  2. Business website homepage/contact/about/team pages
  3. Search query enrichment
  4. Email finder / Hunter / Apollo / provider fallback
  5. AI structured extraction
  6. Verification + suppression
- **Scoring:** ICP fit, owner/decision-maker confidence, website weakness, review pain, ad spend/growth signal, response likelihood.
- **Outreach prep:** personalized first line, offer-specific email body, opt-out footer, sender account assignment, throttle.
- **CRM/reporting:** Sheets/Airtable ilk aşama; sonra Postgres/Convex + dashboard.
- **Compliance guard:** source legality flag, CAN-SPAM checklist, opt-out/suppression, no contact list, country rules, platform ToS risk flag.

### Pool agent rolleri
- **Source Hunter Agent:** vertical + geo query üretir.
- **Scraper Pool:** Apify/HTTP/browser ile liste çıkarır.
- **Website Miner:** `/contact`, `/about`, `/team`, `/staff`, `/leadership`, footer, schema.org, social links tarar.
- **Contact Resolver:** domain → owner/founder/manager/decision-maker email ve phone bulur.
- **Verifier:** email status, catch-all, bounce risk, duplicate, suppression.
- **ICP Scorer:** dikey-fit + büyüme sinyali + satın alma olasılığı.
- **Copywriter:** short, pain-based, vertical-specific first line + sequence.
- **Compliance Sentinel:** opt-out, address, claim risk, platform ToS, no spam.
- **Campaign Router:** Instantly/Smartlead/CRM upload; rate limit; mailbox rotation.
- **Reply Classifier:** positive/neutral/question/not interested/out of office/spam complaint.
- **Analyst:** CPL, cost per valid email, reply rate, booked appointment, revenue, vendor hit-rate raporu.

## Ham Notlar
- `projeler.txt` doğrudan “Apollo leadgen template” dolu değil; daha çok scraper/browser automation/agentic web stack sinyali verdi. Bu kötü değil: UniverseCreator’ın avantajı hazır database değil, kendi workflow’unu kurabilmesi.
- Google Maps konusu gri/riski yüksek: Google Platform Terms “extract/export/scrape Google Maps Content outside Services” tarafında kısıt koyuyor. Apify actor çalışıyor olabilir ama ToS riski yok sayılmamalı. Production’da “source risk” etiketi tutulmalı.
- Apollo da otomatik bot/crawler/data scraping’i yazılı onay olmadan yasaklıyor. Apollo kullanacaksak resmi export/API/plan sınırlarıyla kalmak daha güvenli.
- CAN-SPAM minimumları: yanıltıcı header/subject yok, reklam olduğu net, valid postal address, açık opt-out, opt-out hızlı işlenir. Soğuk email ABD’de tamamen yasak değil ama sloppy setup pahalıya patlar.
- TCPA/AI voice/SMS tarafı e-posta kadar rahat değil; automated calls/texts ve artificial/prerecorded voice için prior express written consent gerekebilir. Leadgen planı email + human-approved replies ile başlamalı; call/SMS sadece consent-based.
- En büyük fırsat “pool agent” ile **test hızı**: 10 vertical × 10 şehir × 3 offer × 2 sequence = 600 micro-test. İnsan bunu elle yapamaz.
- En büyük risk de aynı: kontrolsüz otomasyon spam motoruna dönüşür. Compliance sentinel ve human approval şart.
