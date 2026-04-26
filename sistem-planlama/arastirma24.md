# Araştırma #24 — Micro-SaaS & API-First Data Products
**Tarih:** 2026-04-21 19:13 +03
**Konu:** $10-200/ay API-first micro-SaaS, agent-ready data APIs, kullanım bazlı monetizasyon ve gerçek traction sinyalleri. 2. tur / 2026 doğrulama.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, `sistem-planlama/arastirma10.md`, `sistem-planlama/planlama10.md`.
- ddgr: `micro SaaS API data product revenue 2026 indie hackers`, `API monetization marketplace developer data API pricing 2026 case study`, `agent ready API MCP data product pricing 2026`.
- Postman 2025 State of API: https://www.postman.com/state-of-api/2025/
- Grand View Research API marketplace: https://www.grandviewresearch.com/industry-analysis/api-marketplace-market-report
- Zuplo API monetization 2026: https://zuplo.com/learning-center/api-monetization-2026-integrated-billing-platforms
- RapidAPI payout docs: https://support.rapidapi.com/hc/en-us/articles/19308532866068-How-are-payouts-calculated
- APILayer provider FAQ: https://marketplace.apilayer.com/docs/article/provider-faq
- APILayer MCP-ready APIs 2026: https://blog.apilayer.com/top-10-mcp-ready-apis-for-ai-integration-in-2026making-your-api-data-accessible-to-chatgpt-and
- Stripe usage-based billing docs: https://docs.stripe.com/billing/subscriptions/usage-based
- Data Fetcher pricing: https://datafetcher.com/pricing
- ScreenshotOne ARR/pricing: https://screenshotone.com/blog/200000-arr-and-400-paying-customers/ , https://screenshotone.com/pricing/
- Firecrawl pricing/GitHub: https://www.firecrawl.dev/pricing , https://github.com/firecrawl/firecrawl
- SerpApi pricing: https://serpapi.com/pricing
- IndieHackers SaaS Market Report 2026 post: https://www.indiehackers.com/post/saas-market-report-2026-is-here-0aa0de2688
- Reddit JSON: r/SaaS `1mn0eo9`, `1lwlk57`, `1q5lfur`, `1muz5bq`; r/microsaas `1nim076`; r/SideProject/r/SaaS/r/Entrepreneur search snapshots.
- Hacker News Algolia: Lago usage-based billing, Stigg pricing-plan SDK, API monetization searches.
- GitHub: `firecrawl/firecrawl`, `getlago/lago`, `janwilmake/openapi-mcp-server`, `Azure/data-api-builder`, `Canner/vulcan-sql`, `lineofflight/frankfurter`.
- ArXiv MCP: `2507.16044`, `2603.06029`, `2601.12735`, `2509.05540`, `2411.07098`, `2504.05738`.
- MCPTube: `NvtsM8Nk72c` Data Fetcher $23K/month micro-SaaS, `MbqSMgMAzxU` Fireship API monetization tutorial.
- ProductHunt: Jina ve `chrome-devtools-axi` denendi; Cloudflare security verification nedeniyle okunabilir ürün sinyali alınamadı.

## Özet Bulgular
- **2026’da API-first küçük ürün fırsatı hâlâ güçlü; ama “API marketplace’e koy, para gelsin” zayıf strateji.** Pazar büyüyor, fakat dağıtım ve ürünleşme asıl mesele. API’yi sadece endpoint olarak değil; docs, metering, billing, OpenAPI, MCP wrapper, örnek workflow ve rapor çıktısıyla paketlemek gerekiyor.
- **AI agent’lar yeni API tüketicisi.** Postman 2025 raporu 5,700+ katılımcıyla API stratejisinin AI stratejisine dönüştüğünü söylüyor: organizasyonların **%82**’si bir seviyede API-first, **%25**’i tamamen API-first; geliştiricilerin **%89**’u AI kullanıyor ama sadece **%24** API’leri AI agent tüketimine göre tasarlıyor. Bu boşluk direkt ürün fırsatı.
- **MCP/OpenAPI katmanı artık “nice-to-have” değil, dağıtım avantajı.** Postman raporunda MCP farkındalığı **%70**, düzenli kullanım **%10**. ArXiv `2507.16044`, 116 resmi MCP server analizinde serverların **%88.6**’sının tamamen/kısmen REST-backed olduğunu, **%92**’sinin bare API wrapper gibi çalıştığını gösteriyor. Yani küçük API ürünleri için OpenAPI→MCP wrapper yolu pratik.
- **API monetizasyon araçları olgunlaşıyor.** Zuplo 2026 makalesi API ekonomisini **$16.29B** olarak projekte ediyor, enterprise’ların ortalama **354+ API** yönettiğini ve 2026’da metering+billing+developer portal’ın tek stack’e kaydığını söylüyor. Lago GitHub’da **9.5K★** ile usage-based billing altyapısı; Firecrawl **111K+★** ile AI/web extraction API talebinin açık sinyali.
- **En iyi wedge: agent-ready narrow data API + business-facing report/alert.** Tek başına API developer’a satılır; aynı verinin PDF/CSV/Telegram alert versiyonu business buyer’a satılır. UniverseCreator için doğru ürün “generic SaaS” değil: ölçülebilir, dar, taze veri sağlayan data API/report hibriti.

## Gerçek Başarı Hikayeleri
- **Data Fetcher — platform üstü data/API micro-SaaS.** MCPTube/Starter Story videosunda Andy Cloke, Airtable extension’ı Data Fetcher’ın **600 paying customer** ve **$23K MRR** yaptığını söylüyor. Maliyet: hosting yaklaşık **$2.5K/ay**, SaaS araçları **$1K/ay**, coworking **$150/ay**, toplam margin yaklaşık **%85**. Growth path: birkaç ayda **$1K MRR**, ilk yıl **$10K MRR**, 3 yılda **$20K+ MRR**. Ana ders: büyüyen platform + marketplace + forumlardan pain bul + en popüler entegrasyonlara içerik üret.
- **ScreenshotOne — dar screenshot/render API, $200K ARR.** 10 Nisan 2025 blogunda ScreenshotOne **$200K ARR** ve **400+ paying customer** eşiğini açıkladı. Güncel pricing: Basic **$17/ay** 2,000 screenshot, Growth **$79/ay** 10,000 screenshot, Scale **$259/ay** 50,000 screenshot. Başarı “her şeyi yapan automation API” değil; tek net iş + güvenilir altyapı + iyi docs.
- **Reddit self-report: feedback widget SaaS, $8.2K MRR → $285K exit.** r/SaaS postu: 14 ayda **$8,200 MRR**, **283 paying customers**, **$1,400/ay** expenses, yaklaşık **$6,800/ay** profit, **%3 monthly churn**, satış **$285K**. En değerli ders: feature kesmek activation’ı **%24 → %61** yükseltmiş; $29’dan $79 tek fiyat modeline geçince profit artmış. Kaynak self-report, doğrulanmış finansal belge değil.
- **Reddit self-report: dosya yeniden adlandırma app’i $5K revenue ama sadece $170 MRR.** r/microsaas postu: 275 kullanıcı, aylık **$5K** gelir, fakat recurring kısmı **$170 MRR**; gelirlerin %90’ı one-time purchase. Ders: micro-tool para getirebilir ama recurring model yoksa “MRR” illüzyonu kurulmasın. Ayrıca SEO hedef kitlesi değil Mac productivity blogger’ları çalışmış; beklenmedik niche ciddi.
- **Reddit self-report: Claude ile complaint mining → $2.3K MRR.** r/SaaS postu, Reddit/Quora/G2 şikayetlerinden cold email personalization problemi bulup ürünü **$2.3K MRR** seviyesine taşıdığını iddia ediyor. Yorumlarda prompt paylaşılıyor ama en iyi uyarı net: LLM skorlarına kör güvenme; raw complaint data + ödeme sinyali şart.
- **Firecrawl — açık kaynak + API product flywheel.** GitHub snapshot: `firecrawl/firecrawl` **111,296★**, `firecrawl-mcp-server` **6,111★**, `open-agent-builder` **2,176★**, `open-scouts` **1,274★**. Pricing Jina snapshot: Free 500 one-time credits; Hobby yaklaşık **$16/ay** yıllık; Standard **$83/ay** yıllık; Growth **$333/ay** yıllık. Ders: AI ajanların web data ihtiyacı gerçek; open-source dağıtım + hosted API monetizasyonu güçlü.
- **Lago — usage-based billing altyapısı.** `getlago/lago` **9,551★**; açıklama: metering, usage-based billing API, subscription management, pricing iterations, payment orchestration, revenue analytics. Bu, API micro-SaaS için “önce kendi billing motorunu yaz” yerine hazır/OSS altyapı düşünülmesi gerektiğini gösteriyor.

## Pazar Büyüklüğü & Fırsat
- **API marketplace pazarı:** Grand View Research, global API marketplace market size’ı **2025’te $21.3B**, **2033’te $82.1B**, **%18.4 CAGR** olarak veriyor. North America revenue share **%34.6**.
- **API revenue artık marjinal değil:** Postman’a göre organizasyonların **%65**’i API programlarından gelir üretiyor; fully API-first organizasyonların **%43**’ü toplam gelirlerinin **%25+** kısmını API’lerden elde ediyor.
- **Agent-ready boşluk:** Postman’da geliştiricilerin **%89**’u AI kullanıyor ama API’leri AI agent için tasarlayan sadece **%24**. Bu, küçük ekiplerin “predictable schema + typed errors + rate limits + least-privilege keys + MCP wrapper” ile dev firmalardan hızlı ayrışabileceği boşluk.
- **Monetization stack hızlanıyor:** Zuplo, geçmişte API monetizasyonunun gateway + metering + billing + developer portal gibi 4+ sistemi dikmeyi gerektirdiğini; 2026’da entegre platformların bu süreci “aylardan saatlere” indirdiğini söylüyor. Micro-SaaS için bu çok önemli: billing altyapısı ürün kurmayı boğmamalı.
- **Marketplace marjı gerçek:** RapidAPI payout dokümanı 09 Aralık 2025 güncellemesiyle **%25 marketplace fee** ve PayPal payout fee riskini yazıyor. Örnek: **$100** transaction → **$73.50** net provider payout. Direct satış daha iyi marj; marketplace discovery/backlink/test kanalı olarak düşünülmeli.
- **Fiyat psikolojisi net:** Data Fetcher yıllık planları **$15/$30/$75/$112**; ScreenshotOne **$17/$79/$259**; SerpApi **$25/$75/$150/$275**; Firecrawl **$16/$83/$333** bandında. UniverseCreator için ilk API/report paketi **$19-$49 starter**, **$79-$149 pro**, **$299+ managed** mantıklı.
- **IndieHackers 2026 sinyali:** SaaS market growth 2020-2023’e göre yavaşlıyor; fakat Data Analytics & Management top-performing kategori, AI ile güçleniyor. API-first design, Data-as-a-Service, security/compliance automation öne çıkan trendler olarak geçiyor.

## Rakipler & Boşluklar
- **RapidAPI/APILayer:** Dağıtım, auth, billing, marketplace trust. Boşluk: fee, payout friksiyonu, kalabalık katalog, curated review ve gerçek buyer’a ulaşamama. APILayer bireylerin de provider olabileceğini söylüyor; bu güzel, ama API yine provider tarafından host ediliyor ve review gerekiyor.
- **Firecrawl/SerpApi/ScrapingBee/DataForSEO:** Web/search/data extraction tarafında güçlü. Boşluk: genel-purpose API’lerin üstünde vertical workflow/result yok. Küçük işletme “scrape API” değil “rakibim fiyatı değiştirdi mi?” cevabı ister.
- **ScreenshotOne/Bannerbear/render API’leri:** Screenshot/render alanı para ediyor ama commodity. Boşluk: evidence-first QA, legal/checkout proof, agent visual verification gibi workflow’a gömülü mikro paketler.
- **Lago/Stigg/Stripe billing stack:** Monetizasyon altyapısı var. Boşluk: UniverseCreator gibi solo/swarm sistemler için “billing kurmadan önce paid pilot / report-first satış” gerekiyor; payment provider blokeri varken self-serve subscription’a erken gömülmek aptalca olur.
- **OpenAPI→MCP araçları:** `janwilmake/openapi-mcp-server` **888★**, Azure Data API Builder **1,368★**, Vulcan SQL **793★**. Boşluk: çoğu wrapper her endpoint’i açmaya çalışıyor. ArXiv `2507.16044` median operasyon exposure’ın **%19** olduğunu gösteriyor; iyi MCP server, API’nin tamamını değil en güvenli/değerli subset’i expose etmeli.
- **Reddit opportunity mining:** 9,363 “I wish there was an app” postunu analiz eden r/SaaS self-report’ta productivity 1,231, education/self-improvement 698, business tools 696 request; isteklerin yaklaşık **%7**’si offline-first/privacy-focused. Boşluk: micro-SaaS fikri için subreddit saymak yetmez; ödeme niyeti ve dağıtım kanalı ayrı doğrulanmalı.

## Teknik Gereksinimler
- **Spec-first ürünleşme:** Her API adayı için önce OpenAPI 3.x, JSON schema, örnek request/response, typed errors, rate limit contract, freshness timestamp, evidence URL ve pricing hypothesis yazılmalı.
- **MCP wrapper ama güvenli subset:** OpenAPI’den MCP generate edilecekse bütün endpoint’leri açmak yok. Tool count düşük, açıklamalar net, auth scope küçük, read-only default olmalı. ArXiv `2507.16044` tool filtering/regrouping’in median tool count’u üçte bir azalttığını gösteriyor.
- **Metering & billing:** Başlangıçta manual key + usage ledger yeterli. Sonra Stripe usage-based billing, Lago veya benzeri metering stack düşünülür. Zorunlu alanlar: key, plan, quota, calls, successful calls, failed calls, cost/call, customer-visible usage.
- **Data freshness & provenance:** Her response `source`, `fetched_at`, `freshness_sla`, `confidence`, `evidence_url` taşımalı. Data API’nin değeri modelden değil tazelikten ve kanıttan gelir.
- **Test & verifier:** OpenAPI contract tests, happy-path/negative-path tests, 429/auth tests, schema drift alert. ArXiv `2603.06029` APIDiffer 11 Ethereum client’ta 72 bug buldu; API consistency production’da gerçek risk.
- **Security:** Agent traffic için rate limiting, least-privilege API keys, rotation, monitoring, 401/403 spike alert. Postman’da **%51** unauthorized/excessive AI agent calls endişesi var; bu endişe pricing kadar ürün gereksinimi.
- **Distribution assets:** Docs, Postman collection, curl examples, n8n/Make workflow template, “copy into agent” MCP config snippet, demo CSV/PDF report, changelog.
- **Legal/TOS risk:** LinkedIn/Amazon kapalı kaynak scraping gibi kırmızı alanlardan uzak dur. Public pricing pages, public trade/open data, müşteri-provided URLs ve kendi portföy health data daha güvenli.

## Ham Notlar
- `ddgr` bu tur çalıştı ve 2026 odaklı sonuçlar verdi: IndieHackers 2026 SaaS report, API monetization 2026 yazıları, agent-ready/MCP API içerikleri. Bazı sonuçlar vendor blog’u; sayılar cross-check edilmeden mutlak gerçek kabul edilmemeli.
- Jina Reader Postman domaininde 451 blok verdi; doğrudan `curl -4` ile sayfa HTML’i çekildi ve rapor metni çıkarıldı. ProductHunt hem Jina hem `chrome-devtools-axi` tarafında Cloudflare “Performing security verification” verdi; ürün sinyali olarak kullanılmadı.
- Reddit başarı hikayeleri self-report. Özellikle “$20K MRR zero ads” postunun top comment’i AI slop kokusu aldığını söylüyor; bu yüzden rakam planlamada kanıt değil, sinyal olarak ele alınmalı.
- ArXiv tarafında ilk arama IP 429 verdi; 60 saniye sonra retry başarılı oldu. Akademik kaynaklar doğrudan “micro-SaaS gelir” değil, API reliability/OpenAPI/MCP/testing tarafına güçlü teknik kanıt sağladı.
- GitHub’da `gh search repos` ilk spesifik query’lerde boş döndü; geniş query’lerle Firecrawl, Lago, OpenAPI-MCP, Azure Data API Builder, Vulcan SQL, Frankfurter bulundu.
- Araştırma sırasında bir kez yine `cmd | python3 - <<` parser anti-pattern’i tekrarlandı; veri kaybı olmadan temp parser ile düzeltildi ve `/home/gokhan/mind/ERRORS.md` güncellendi. Bu aptallık tekrar etmemeli.
- Net hüküm: **UniverseCreator için en iyi Micro-SaaS/API yolu “API Product Foundry v2”: önce report-first paid pilot, sonra agent-ready narrow data API, sonra MCP wrapper + usage billing. Self-serve marketplace en son; ilk para business-facing rapor/alert’ten gelmeli.**
