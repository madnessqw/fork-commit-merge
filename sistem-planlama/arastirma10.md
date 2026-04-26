# Araştırma #10 — Micro-SaaS & API-First Data Products
**Tarih:** 2026-04-21 08:52 +03
**Konu:** $10-200/ay küçük API/veri ürünleri, API-first micro-SaaS, agent-ready API paketleme ve veri ürünü monetizasyonu.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki araştırma formatları.
- `projeler.txt` sinyalleri: API middleware, MCP/API wrappers, CLIProxyAPI, public-apis, Crawlee, scraping/browser automation, Firecrawl/SERP/screenshot/email verification benzeri API ürün fikri kümeleri.
- Postman 2025 State of API: https://www.postman.com/state-of-api/2025/
- RapidAPI provider/payout docs: https://support.rapidapi.com/hc/en-us/articles/19308532866068-How-are-payouts-calculated , https://get.rapidapi.com/api-provider/
- APILayer provider FAQ: https://marketplace.apilayer.com/docs/article/provider-faq
- API marketplace market: https://www.grandviewresearch.com/industry-analysis/api-marketplace-market-report
- ScreenshotOne: https://screenshotone.com/blog/200000-arr-and-400-paying-customers/ , https://screenshotone.com/pricing/
- Data Fetcher: https://datafetcher.com/pricing , MCPTube `NvtsM8Nk72c`
- ScrapingBee: https://www.scrapingbee.com/pricing/ , https://www.indiehackers.com/post/the-journey-to-a-1-million-arr-saas-without-traditional-vcs-1f3160c4d0
- Bannerbear pricing: https://www.bannerbear.com/pricing/
- SerpApi pricing: https://serpapi.com/pricing
- Firecrawl pricing/GitHub: https://www.firecrawl.dev/pricing , https://github.com/firecrawl/firecrawl
- IndieHackers: Semantria API story, Micro SaaS report: https://www.indiehackers.com/post/FDdtkqyKLqQ2dztt7KIb , https://www.indiehackers.com/post/f5016948df
- Reddit JSON: https://reddit.com/r/SideProject/comments/1nr4167/ , https://reddit.com/r/Entrepreneur/comments/1ov9huk/ , https://reddit.com/r/SaaS/comments/1r3kddo/ , https://reddit.com/r/webscraping/comments/1kjvv68/ , https://reddit.com/r/webscraping/comments/1sjd609/
- GitHub search snapshot: `firecrawl/firecrawl`, `serpapi/google-search-results-python`, `trumail/trumail`, `reacherhq/backend`, `staticallyio/screenshot`, `apilayer/screenshotlayer-API`.
- ArXiv: https://arxiv.org/abs/2510.19274 , https://arxiv.org/abs/2603.10133 , https://arxiv.org/abs/2512.15798 , https://arxiv.org/abs/2409.17140
- YouTube/MCPTube: https://www.youtube.com/watch?v=NvtsM8Nk72c , https://www.youtube.com/watch?v=TCGXT7ySco8 , https://www.youtube.com/watch?v=lC6Gpn0ugFI , https://www.youtube.com/watch?v=MbqSMgMAzxU

## Özet Bulgular
- **API ürünleri AI çağında tekrar iyi iş.** Postman 2025 raporunda 5,700+ katılımcı var; organizasyonların **%82**'si bir seviyede API-first yaklaşım kullanıyor, **%25** tamamen API-first, **%65** API programlarından gelir elde ediyor. Aynı rapor “AI agent'lar yeni API tüketicileri” diyor ama sadece **%24** API'lerini AI agent tüketimine göre tasarlıyor. Boşluk net: agent-ready küçük API ürünleri.
- **Micro-SaaS API modeli hâlâ çalışıyor ama “generic API marketplace’e koydum, para yağdı” masal.** RapidAPI güncel destek dokümanı API Hub işlemlerinden **%25 marketplace fee** aldığını, PayPal payout fee'sinin ayrıca gelebileceğini söylüyor; $100 işlemde net payout örneği **$73.50**. Marketplace dağıtım sağlar ama marjı yer ve alıcı çoğu zaman “developer”, nihai buyer değil.
- **Gerçek kazananlar dar, ölçülebilir, sık tekrarlanan işi API'ye çeviriyor.** ScreenshotOne, Data Fetcher, ScrapingBee, SerpApi, Bannerbear ortak pattern: tek net iş, usage quota, iyi dokümantasyon, yüksek niyetli SEO/tutorial, self-serve onboarding, support kalitesi.
- **Fiyat bantları küçük ürün için çok net:** ScreenshotOne **$17/$79/$259**, Data Fetcher yıllık ödeme bazında **$15/$30/$75/$112**, SerpApi **$25/$75/$150/$275+**, Bannerbear **$49/$149/$299**, ScrapingBee **$49/$99/$249/$599**. UniverseCreator için $19-$99/ay başlangıç, $149-$299/ay pro tier psikolojik olarak makul.
- **Büyük fırsat “API + MCP + veri raporu” hibriti.** Sadece API endpoint satmak developer ürünü; API'yi OpenAPI/MCP ile agent-consumable yapıp üstüne haftalık veri raporu/alert eklemek business buyer’a daha kolay satılır.

## Gerçek Başarı Hikayeleri
- **ScreenshotOne — dar screenshot API, resmi $200K ARR.** Kurucu Dmytro Krasun’un 10 Nisan 2025 blogunda ScreenshotOne’ın yaklaşık 3 yılda **$200,000 ARR** ve **400+ paying customer** seviyesine geldiği yazıyor. Aynı blogdaki ana dersler: market/positioning, tek persona, çalışan ürün, fokus. Pricing sayfası Basic **$17/ay**, Growth **$79/ay**, Scale **$259/ay**; extra screenshot ücreti planlara göre düşüyor.
- **ScreenshotOne — MCPTube/Starter Story önceki snapshot.** Videoda Dmytro, o dönemde **280 müşteri** ve yaklaşık **$12K MRR** anlattı; subscription + extra screenshot modeli, $17 başlangıç, server maliyeti **$3K-$4K/ay**, toplam gider yaklaşık **$4.5K**, profit margin **%40-60**. Churn'ü iptal sonrası tek-soru email ile **%11’den %7 civarına** indirdiğini ve hedefinin **%5 altı** olduğunu söylüyor.
- **Data Fetcher — platform üstü micro-SaaS, $23K MRR.** Starter Story/MCPTube transkriptinde Andy Cloke, Airtable extension’ı Data Fetcher’ın **600 paying customer** ve **$23K MRR** yaptığını söylüyor. En iyi insight: growing platform marketplace erken dağıtım verir; ama platform riskini kontrol etmek gerekir. Maliyet: hosting yaklaşık **$2.5K/ay**, SaaS tools yaklaşık **$1K/ay**, coworking **$150/ay**, margin yaklaşık **%85**. Growth: birkaç ayda **$1K MRR**, ilk yıl **$10K MRR**, 3 yılda **$20K+ MRR**.
- **ScrapingBee — web scraping API, içerik/SEO ile $1M ARR.** IndieHackers hikayesine göre ScrapingBee’nin **$10K MRR** eşiğine gelmesi yaklaşık 18 ay sürdü; sonraki 3 ayda **$20K MRR** oldu; 2.5 yıl sonra **$1M ARR** seviyesine ulaştı. Pricing bugün Freelance **$49**, Startup **$99**, Business **$249**, Business+ **$599**.
- **Semantria — sentiment analysis API, $150K MRR exit.** IndieHackers röportajında Oleg Rogynskyy, önce Salesforce app yaptıklarını ama talebin API tarafına geldiğini; recurring API subscriptions ile satışta yaklaşık **$150K MRR** zirve gördüklerini anlatıyor. Kritik ders: tek seferlik credit bucket API işinde çalışmamış; subscription daha iyi.
- **Micro SaaS report — küçük API/veri ürünleri çok sayıda.** IndieHackers H1 2023 raporunda Web3Forms contact form API **$5K+ ARR**, ScreenshotOne **$2.5K monthly revenue** o dönem, Treblle API management **$10K/month**, DataReportive database reporting **$4.3K/month**, scrapingfish web scraping API **$5K/month** olarak geçiyor. Hepsi devasa değil ama micro-SaaS için yeterli para.
- **Reddit — cookieless LinkedIn scraper API, €4.5K MRR ama legal mayın.** r/SideProject postunda kurucu 9 ayda “cookieless LinkedIn scraper API” ile **€4.5K MRR** gördüğünü, outbound yapmadan n8n template’leri ve word-of-mouth ile büyüdüğünü söylüyor. Yorumların tepesi ise dava/TOS riski uyarısı. Ders: scraping API para eder; LinkedIn tarzı hedeflerde gelir ile hukuk riski aynı pakette gelir.
- **Reddit — RapidAPI popularity ≠ customer.** Bir kullanıcı kişiselleştirilmiş QR Code API’sinin RapidAPI’de popülerlik aldığını ama **0 kullanıcı** getirdiğini yazdı. En iyi yorum: developer’lar API’yi beğenebilir ama buyer marketing agency/restaurant/event business olabilir; GTM’i marketplace değil gerçek use-case belirler.
- **Reddit — review scraper micro data product.** r/SaaS postunda App Store review scraper 5 haftada 400 kullanıcı, 32 paying user, **$19/ay** tier ile **$228 MRR** anlattı. Rakamlar self-report ve küçük; ama pattern iyi: önce veri seti, sonra kategori genişletme, sonra kullanıcı “buna para veririm” dediğinde ücretli tier.

## Pazar Büyüklüğü & Fırsat
- **API marketplace pazarı büyük ve büyüyor:** Grand View Research, global API marketplace market size’ı **2025’te $21.3B**, **2033’te $82.1B**, **%18.4 CAGR** olarak veriyor. Raporda North America **%34.6** revenue share, platform segment **%61.7**, consumer end-use **%58.8**.
- **API-first artık internal engineering değil revenue engine.** Postman, API’lerin sadece uygulama altyapısı değil agent tüketimi ve gelir motoru olduğunu yazıyor. En kritik sayı: **%65** organizasyon API programlarından gelir üretiyor.
- **AI-agent tarafı erken boşluk:** Postman’a göre geliştiricilerin **%89**’u AI kullanıyor; ama sadece **%24** API’leri AI agent tüketimine göre tasarlıyor. MCP farkındalığı yüksek (**%70** civarı) ama düzenli kullanım **%10**. Bu şu demek: “OpenAPI + examples + rate limits + MCP wrapper” olan küçük API ürünleri, sıradan endpoint’lerden daha görünür olabilir.
- **Küçük fiyatlar gerçek pazar davranışına uyuyor:** ScreenshotOne **$17** ile başlıyor; Data Fetcher **$15**; SerpApi **$25**; Bannerbear/ScrapingBee **$49**. $10-$49 starter tier, developer adoption için mantıklı; $79-$299 pro tier, usage arttıkça marjı taşır.
- **Marketplace mi direct mi?** RapidAPI provider sayfası büyük dağıtım iddia ediyor: 500K developer ve 350B API call/month gibi rakamlar. Ama güncel payout dokümanı **%25 fee** gösteriyor. APILayer daha curated; bireylerin de provider olabileceğini ve kişisel payout alabileceğini söylüyor. Kısa vade için en iyi strateji: direct landing + docs + SEO; marketplace sadece discovery/backlink/ilk ödeme testi.

## Rakipler & Boşluklar
- **RapidAPI / APILayer:** Hızlı listelenme, billing, auth, docs, marketplace trafiği. Boşluk: yüksek komisyon, kalite gürültüsü, payout friksiyonu, provider support yükü, marketplace buyer’ının çoğu zaman gerçek iş alıcısı olmaması.
- **SerpApi / DataForSEO / ScrapingBee / Firecrawl:** Search, scraping, extraction API tarafında güçlü. Boşluk: enterprise-heavy pricing ve genel amaçlı API yerine vertical, hazır rapor/alert isteyen küçük işletmeler.
- **ScreenshotOne / Bannerbear / APITemplate/CraftMyPDF:** Render/görsel/PDF API kalabalık ama hâlâ para var. Boşluk: genel screenshot değil; “AI agent visual evidence API”, “checkout proof snapshot”, “product card/social creative generator” gibi dar use-case.
- **Firecrawl’ın traction’ı açık kaynak sinyali:** 2026-04-21 GitHub snapshot’ında `firecrawl/firecrawl` **111K+★**, `firecrawl-mcp-server` **6.1K+★**, `open-scouts` **1.2K+★**, `fire-enrich` **1.1K+★**. Bu veri/web extraction API + agent tooling damarının sıcak olduğunu gösteriyor.
- **Email verification / screenshot OSS:** `trumail/trumail` **1,049★**, `reacherhq/backend` **221★**, screenshot API repoları daha küçük. Bu alanlar yapılabilir ama commodity. Farklılaşma şart.
- **Boşluk #1 — agent-ready API catalog:** Çoğu küçük API hâlâ insan dokümanı ve curl örneğiyle yetiniyor. OpenAPI spec + Postman collection + MCP server + typed errors + usage examples veren mini ürün ayrışır.
- **Boşluk #2 — TR/MENA/local data products:** English/global API pazarı kalabalık; Türkiye/MENA verisi, GTIP/HS, yerel e-commerce, local directory, fiyat/stock izleme gibi konularda daha az “developer-first API” var.
- **Boşluk #3 — API + rapor:** Developer API tek başına zayıf GTM. Aynı veriyi haftalık PDF/CSV/alert olarak business buyer’a vermek conversion’ı artırır.

## Teknik Gereksinimler
- **Ürün tanımı:** Tek cümlelik problem, tek persona, net input/output schema. “Her şeyi scrape eden API” değil; “HS code için buyer/import trend snapshot API” gibi dar endpoint.
- **API sözleşmesi:** OpenAPI 3.x spec, örnek request/response, typed errors, 429/rate limit dokümanı, idempotency, pagination, webhooks gerekiyorsa event schema.
- **Auth & metering:** API key generation, per-key quota, request log, usage counter, overage guardrail, abuse detection, free-tier limit.
- **Billing:** Direct Stripe/LemonSqueezy/Paddle mümkünse daha iyi marj; marketplace testinde RapidAPI fee hesaba katılmalı. RapidAPI’de $100 işlem ≈ $73.50 net provider payout örneği var.
- **Data pipeline:** Source fetcher, cache, normalization, freshness timestamp, dedupe, data provenance/evidence URL, legal/TOS risk sınıflandırması.
- **Reliability:** Status page, uptime monitor, retry/backoff, background jobs, queue, request timeout, failed request charging policy.
- **Docs & DX:** Docs sayfası, Postman collection, SDK snippets, copy-paste curl, sample CSV/JSON, sandbox mode, examples for n8n/Make/Zapier.
- **Agent-readiness:** OpenAPI + MCP wrapper + machine-readable descriptions + scoped API keys + usage headers. Postman’ın agent-ready önerileriyle uyumlu: predictable patterns, robust error handling, rate limiting, auth designed for automated access.
- **Support:** Email/chat support, cancellation reason tracking, usage alerts at 80/90/100%, onboarding email, templates/tutorials.
- **Compliance:** Scraping/data source TOS, robots/rate limits, personal data, LinkedIn/Amazon gibi high-risk kaynakları red/yellow/green sınıflandırma.

## Ham Notlar
- `ddgr` bu ortamda `HTTP Error 202: Accepted` verip boş JSON döndürdü. Komut çalıştırıldı; kaynak keşfi web fallback/Jina ile tamamlandı.
- ProductHunt Jina araması zayıf içerik verdi; `chrome-devtools-axi` ile ProductHunt açılınca Cloudflare “Performing security verification” sayfasında kaldı. Buradan ciddi sinyal çıkarılmadı.
- MCPTube `parallel_add.py` videoları “başarılı” dedi ama kütüphanede görünmedi; önceki cycle’daki sürtünme tekrarlandı. Tek tek `mcp__mcptube__add_video` ile görünür hale getirildi.
- Fireship “Make Money from your API Tutorial” videosunun transcript’i boş geldi; sadece chapter metadata vardı: metered billing, Stripe Checkout, webhooks, API keys, usage recording. Bu teknik akış yine faydalı ama kaynak olarak transcript kadar güçlü değil.
- `gh search repos` JSON alanı `stargazerCount` değil `stargazersCount`; ilk GitHub parse boş geldi. Düzeltildikten sonra Firecrawl/SerpApi/email/screenshot API repoları çıktı.
- Net hüküm: **UniverseCreator için en iyi API ürün yolu generic API marketplace’e ürün atmak değil; mevcut araştırma/otomasyon kabiliyetini “agent-ready narrow data APIs + rapor/alert” olarak paketlemek.** İlk wedge LLM cost/pricing, HS/GTIP trade snapshot, competitor price/stock, website health/checkout evidence veya local business enrichment olabilir.
