# Araştırma #3 — Content Factory + SEO
**Tarih:** 2026-04-21 04:10 +03
**Konu:** 113 mevcut ürün için organik trafik, blog/pSEO fabrikası, backlink/AI-search görünürlük otomasyonu
**Kaynaklar:**
- Yerel: `STATE_SUMMARY.json` (Cycle 991), `projeler.txt`, önceki `sistem-planlama/arastirma0-2.md` çıktıları
- Google Search Central — AI content guidance: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Google Search Central — March 2024 spam/scaled content abuse: https://developers.google.com/search/blog/2024/03/core-update-spam-policies
- Google Search Central — sitemap limits: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google Search Central — SoftwareApplication structured data: https://developers.google.com/search/docs/appearance/structured-data/software-app
- Google Search Central — Product snippet structured data: https://developers.google.com/search/docs/appearance/structured-data/product-snippet
- Google Search Central — URL Inspection API: https://developers.google.com/search/blog/2022/01/url-inspection-api
- BrightEdge organic/search traffic baseline: https://www.brightedge.com/blog/organic-share-of-traffic-increases-to-53
- StrategyR / Global Industry Analysts SEO market: https://www.strategyr.com/market-report-search-engine-optimization-seo-forecasts-global-industry-analysts-inc.asp
- ResearchAndMarkets / GlobeNewswire content marketing market: https://www.globenewswire.com/news-release/2025/10/10/3164787/28124/en/Content-Marketing-Market-Global-Forecast-Report-2025-2032-Profiles-of-Adobe-Oracle-Salesforce-IBM-Sitecore-Acquia-RWS-Optimizely-BloomReach-Crownpeak-Technology.html
- DataForSEO SERP API pricing: https://dataforseo.com/apis/serp-api/pricing
- SerpApi pricing: https://serpapi.com/pricing
- Ahrefs pricing: https://ahrefs.com/pricing
- Omnius pSEO case study: https://www.omnius.so/blog/programmatic-seo-case-study
- Haley Marketing pSEO case study: https://www.haleymarketing.com/case-studies/14k-lead-secured-in-4-months-with-programmatic-seo-landing-pages/
- PageFactory/IndieHustle MRR case: https://medium.com/indie-hustle/this-no-code-tool-is-making-1-085-mrr-in-just-4-months-019820d917d3
- Reddit r/SEO SaaS case: https://www.reddit.com/r/SEO/comments/s3ry25/seo_case_study_0_to_200000_monthly_organic/
- Reddit r/SaaS pSEO anecdote: https://www.reddit.com/r/SaaS/comments/1o65an1/how_programmatic_seo_5xd_traffic_for_my_ai_saas/
- ArXiv MCP: `2509.05607` CC-GSEO-Bench (MCP get_abstract başarılı)
- ArXiv web fallback: `2507.03169`, `2306.01785`, `2602.13415`, `2511.12920`
- MCPTube: `ZT_8_uz_c-s`, `m9iaJNJE2-M`, `zOjP7Wd4M-A`

## Özet Bulgular
- UniverseCreator şu an SEO için ham cevher taşıyor: `STATE_SUMMARY.json` 113 aktif ürün, 86 live, 16 building, 10 ready_for_payment, 52 checkout bağlı, 61 checkout eksik gösteriyor. 113 ürün gerçek veri seti demek; rastgele AI blog basmaktan daha güvenli.
- Google'ın çizgisi net: AI ile içerik üretmek yasak değil; kullanıcıya değer katmayan, arama sıralaması manipülasyonu için ölçeklenen sayfalar riskli. Bu yüzden fabrika “çok sayfa” değil “ürün + veri + intent + QA” sistemi olmalı.
- En hızlı pSEO fırsatı blog yazısı değil, ürün-adjacent landing page: `X vs Y`, `best tool for task`, `how to convert A to B`, `free [developer task] tool`, `API/error/use-case guide`, `template/checklist`.
- AI search/GEO artık klasik ranking kadar önemli: ArXiv GSEO çalışmaları exposure/faithful credit/causal impact gibi metriklerle içerik etkisini ölçüyor; sadece Google sıra takibi eksik kalır.
- Pazar var ama trafik otomatik para değil. SEO sonuçları genelde haftalar/aylar ister. Kısa vadede yayın değil, indexlenebilir içerik envanteri + kalite kapısı + ilk 20-40 draft en akıllı hamle.

## Gerçek Başarı Hikayeleri
- **PageFactory:** No-code pSEO aracı olarak 2024'te $1,085 MRR seviyesine 4 ayda çıktı; erken aşamada 273 waitlist, 22 ödeme yapan kullanıcı ve $500+ MRR sinyali raporlanmıştı. Ders: pSEO sadece trafik taktiği değil, direkt ürünleştirilebilir bir otomasyon aracı.
- **Omnius / Dynamic Mockups case:** Programmatic SEO ile 10 ayda aylık signup 67 → 2,100+; toplam 11k+ signup; aylık organik trafik 102 → 8.5k; 5,742 keyword, 305 birinci sayfa, 42 top-3 keyword raporlandı. Ders: pSEO, yüksek intent ve dönüşüm yapısı varsa signup üretir.
- **Haley Marketing / recruiting firm:** Programmatic landing page 4 ay içinde $14k outplacement lead kapattı; lead'in ChatGPT üzerinden geldiği belirtiliyor. Ders: LLM citation/AI discovery gelir kanalına dönüşebiliyor, özellikle yüksek ticket B2B hizmetlerde.
- **Athenic case:** 12k otomatik sayfadan 250k aylık organik ziyaret, trafiğin %68'i pSEO sayfalarından, 24% signup conversion ve £840k pipeline iddiası var. Agency case olduğu için temkinli alınmalı ama sayfa şablonu + data source + conversion yapısının ölçek etkisini gösteriyor.
- **Reddit r/SEO case:** Bir SaaS sitesinde 0'a yakın seviyeden 200k aylık organik trafiğe <2 yılda, link-building olmadan; ana kaldıraçlar intent odaklı keyword seçimi, writer guideline, rewrite ve internal linking. Bu daha güvenilir taktik dersi: “daha fazla yaz” değil, “yanlış yazıları öldür/düzelt”.
- **Reddit r/SaaS pSEO anecdote:** Bir AI presentation SaaS'ı 1,200 sayfa, 10k+ keyword clustering, manuel intro/CTA, dinamik internal link ve batch publishing ile 3 ayda +520% trafik ve 180k aylık ziyaret iddia ediyor. Doğrulanmamış ama model UniverseCreator'a birebir uyuyor: ürün × use-case × persona.

## Pazar Büyüklüğü & Fırsat
- BrightEdge araştırmasına göre organik arama trackable web traffic'in yaklaşık %53'ünü; organik+paid search toplamı %68'ini oluşturuyor. B2B'de combined search organic share %76 diye raporlanmış. Eski ama hâlâ temel benchmark olarak kullanılıyor.
- Global Industry Analysts SEO pazarını 2024'te $89.1B, 2030'da $143.9B, 2024-2030 CAGR %8.3 olarak veriyor.
- ResearchAndMarkets içerik pazarlama pazarını 2024'te $26.11B, 2025'te $33.27B, 2032'de $177.55B, CAGR %27.07 olarak veriyor.
- AI Search riski/fırsatı aynı anda geliyor: SparkToro/Datos verisi US Google aramalarında açık web'e giden click sayısının 1,000 aramada ~360 civarında olduğunu söylüyor; AI Overviews ve zero-click yüzünden klasik trafik düşebilir. Bu yüzden hedef metrik sadece click değil: branded search, AI citation, direct visit, checkout click, email capture.
- UniverseCreator için fırsat: 113 ürünün her biri en az 5 sayfa pattern'i doğurursa 565 sayfa; 10 sayfa pattern'i doğurursa 1,130 sayfa. Google sitemap sınırı tek dosyada 50,000 URL / 50MB olduğu için ölçek teknik olarak sorun değil; kalite ve crawl budget esas mesele.

## Rakipler & Boşluklar
- **Rakip kategorileri:** Jasper/Copy.ai gibi genel AI writer'lar; Surfer/Frase/Clearscope gibi content optimizer'lar; Ahrefs/Semrush gibi SEO suite'ler; AirOps/PageFactory gibi pSEO workflow araçları; Webflow/Framer/WordPress ekosistemi.
- **Boşluk 1 — gerçek ürün verisi:** Çoğu content factory jenerik metin basıyor. UniverseCreator'da gerçek ürün adı, URL, category, checkout status, README, kullanım örneği ve demo sayfası var. Bu data asset pSEO'yu “thin AI spam” olmaktan çıkarabilir.
- **Boşluk 2 — developer-tool long-tail:** `json`, `html`, `cron`, `jwt`, `hmac`, `api`, `docker`, `regex`, `markdown`, `svg`, `color` gibi tool query'leri yüksek intent ama tek tek içerik üretmek sıkıcı. Swarm bunu sıkılmadan yapar — robotların en sevdiği iş: insanı yavaş yavaş delirten tekrar.
- **Boşluk 3 — AI citation hazır format:** Karşılaştırma tabloları, fiyat/özellik matrisleri, “when to use”, “best for”, FAQ ve kaynaklı özetler LLM cevaplarında daha kolay kullanılabilir. Haley case'te ChatGPT-originated lead buna iyi sinyal.
- **Boşluk 4 — mevcut 113 ürünün sağlık farkı:** 113 aktif ürün var ama local summary 23 healthy gösteriyor. Trafik getirilecek sayfanın çalışmaması direkt para yakmak. SEO planı, health ve checkout state ile bağlı ilerlemeli.

## Teknik Gereksinimler
- **Canonical ürün envanteri:** `STATE_SUMMARY.json` + ürün README/product.json + canlı URL + checkout URL + status/health + kategori.
- **Keyword miner:** DataForSEO Standard Queue düşük maliyetli: $0.0006 / 10 sonuç SERP, 1,000 SERP ≈ $0.6; minimum deposit $50. Alternatif SerpApi: $25/1k, $75/5k, $150/15k, $275/30k arama/ay.
- **Template seti:**
  1. `How to [task] online`
  2. `[A] to [B] converter`
  3. `[Tool] alternative`
  4. `[Tool A] vs [Tool B]`
  5. `Best [category] tools for [persona]`
  6. `[error/code] fix guide`
  7. `Free [developer workflow] checklist`
  8. `API/example/snippet page`
- **Quality gate:** Her sayfada gerçek ürün/demo linki, özgün örnek, UI screenshot veya sample input/output, structured data, internal links, noindex kararı, duplicate similarity check, fact/source check.
- **SEO teknikleri:** SoftwareApplication/Product JSON-LD; sitemap + lastmod; canonical URL; breadcrumb; title/meta; Search Console URL Inspection API ile önemli URL'leri denetleme. Google URL Inspection API limiti 2,000 sorgu/gün ve 600 sorgu/dakika/site property.
- **AI-search metrikleri:** Klasik rank takibine ek olarak ChatGPT/Perplexity/Gemini prompt check, source citation, answer overlap, brand mention, cited URL ölçümü.
- **İnsan müdahalesi:** İlk 50-100 sayfa insan onayı olmadan yayınlanmamalı. Google'ın scaled content abuse riski yüzünden kör autopublish dumb idea; ucuz trafik diye siteyi çöpe atmak gereksiz kahramanlık.

## Ham Notlar
- `projeler.txt` sinyalleri:
  - `github.com/waynesutton/markdown-site`: AI agent/developer için terminalden markdown sync ile website/docs/blog publish framework.
  - `github.com/coreyhaines31/marketingskills`: Claude Code/AI agent için CRO, copywriting, SEO, analytics, growth engineering skill seti.
  - Notlarda “SEO testing: Agent tries headline variants, tracks CTR, keeps the winner” fikri var; bu content factory'nin deney katmanı olabilir.
  - Botasaurus da catalog/screenshot/scrape tarafında kullanılabilir.
- MCPTube `ZT_8_uz_c-s`: DataForSEO MCP → 25 commercial keyword / 23k search volume → Perplexity gap analysis → Claude 1,247 sayfa stratejisi: 420 comparison, 312 industry guide, 215 feature page, 150 budget recommendation, 150 integration/workflow guide; Playwright screenshot ile zengin landing page.
- MCPTube `m9iaJNJE2-M`: n8n + Apify + OpenRouter/Claude akışı; research agent → content idea generator → content agent → Slack approve gate → publish. Önemli nokta: insan review aşaması var.
- MCPTube `zOjP7Wd4M-A`: programmatic SEO'da dynamic sitemap, internal/external links, knowledge base, review/approve workflow, lead magnet ve çok dilli yayın vurgusu var.
- ArXiv `2509.05607`: GSE/GEO için Exposure, Faithful Credit, Causal Impact, Readability/Structure, Trustworthiness/Safety metrikleri. UniverseCreator “AI citation scorecard” tasarlarsa akademik mantığı buradan alınabilir.
- ArXiv `2507.03169`: GEO optimize edilmiş içerik, LLM cevaplarında absolute word count +15.63%, position-adjusted word count +30.96% görünürlük artışı iddia ediyor; küçük domain-specific fine-tune bile işe yarayabiliyor.
- ArXiv `2306.01785`: 67k keyword, 6M click, 24M view dataset ile SERP feature'ların CTR'ı ciddi modüle ettiği gösteriliyor; sadece rank bakmak eksik.
- ArXiv `2602.13415`: 24k query, 243 country, 2.8M AI/traditional result; Google AIO exposure 2024'te 7 ülkeden 2025'te 229 ülkeye genişlemiş, Türkiye hariç tutulmuş. Global içerik planında bölgesel AI-search farkı önemli.
