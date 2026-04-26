# Araştırma #17 — Content Factory + SEO
**Tarih:** 2026-04-21 13:51 +03
**Konu:** Programmatic SEO, AI destekli içerik fabrikası, 113 ürün için organik trafik, AI-search/GEO görünürlüğü
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `STATE.json`, `STATE_SUMMARY.json`, `projeler.txt`, önceki `sistem-planlama/arastirma3.md` / `planlama3.md`
- Google Search Central — AI-generated content guidance: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Google Search Central — March 2024 core update/spam policies: https://developers.google.com/search/blog/2024/03/core-update-spam-policies
- Google Keyword blog — spam/low-quality update + 45% less low-quality unoriginal content: https://blog.google/products/search/google-search-update-march-2024/
- Search Engine Land — AI-generated content 16-month experiment: https://searchengineland.com/ai-generated-content-google-search-experiment-472234
- Search Engine Land / Previsible — AI traffic +527%: https://searchengineland.com/ai-traffic-up-seo-rewritten-459954
- Omnius pSEO case study — 67 → 2,100+ monthly signups: https://www.omnius.so/blog/programmatic-seo-case-study
- Santifer iRepair open-source pSEO case: https://github.com/santifer/santifer-irepair
- DataForSEO Google Ads keyword API pricing: https://dataforseo.com/pricing/keywords-data/google-ads
- Ahrefs pricing: https://ahrefs.com/pricing
- Semrush subscription/toolkits: https://www.semrush.com/kb/1011-subscriptions
- GitHub search: `programmatic seo`, `nextjs programmatic seo`, `open source seo tool`, `seo`, `static-site-generator`
- Reddit JSON API: r/SEO, r/bigseo, r/SaaS, r/SideProject, r/Blogging, r/juststart, r/content_marketing
- Reddit high-signal posts: https://reddit.com/r/SaaS/comments/1o65an1/ , https://reddit.com/r/SaaS/comments/1od8rnk/ , https://reddit.com/r/SEO/comments/1s2e2gk/ , https://reddit.com/r/SideProject/comments/1lefy3q/ , https://reddit.com/r/juststart/comments/1ri48gp/
- ArXiv MCP: `2602.02961`, `2602.16136`, `2509.08919`, `2601.16858`, `2603.12282`
- MCPTube: `ZT_8_uz_c-s`, `m9iaJNJE2-M`, önceki library `zOjP7Wd4M-A`
- ProductHunt Jina denemesi 403/CAPTCHA; fallback web search ile Seodity, sitefire.ai, SearchAtlas, Search Console Audit ürün sinyalleri incelendi.

## Özet Bulgular
- UniverseCreator artık SEO için ciddi ham madde taşıyor: `STATE.json` cycle 1023 ve `STATE_SUMMARY.json` cycle 1021 içinde **113 active / 113 healthy** görünüyor. Önceki turdaki “ürün çalışıyor mu?” riski azalmış; artık ana darboğaz dağıtım ve içerik kalitesi.
- Doğru oyun “AI blog spammer” değil. Google açık şekilde değer katmayan çok sayıda generative-AI sayfasını scaled content abuse riski olarak görüyor; ama AI'ı araştırma, yapılandırma, metadata ve özgün içeriğe destek için kullanmayı yasaklamıyor.
- pSEO hâlâ çalışıyor ama sadece gerçek data asset + gerçek kullanıcı faydası varsa. Omnius case 67 → 2,100+ aylık signup, Santifer case 15,500+ sayfa / 2.26M impression / 2,000 monthly clicks, Pinterest GEO paper 20% organic traffic growth gösteriyor.
- Kör AI içerik kısa vadede indexlenebiliyor ama dayanıklılığı zayıf. Search Engine Land/SE Ranking deneyinde 2,000 AI makalenin ~71%'i 36 günde indexlendi; ilk dönemde 122k impression aldı; yaklaşık 3 ay sonra top-100'de kalan sayfa oranı **%3** seviyesine düştü.
- AI search/GEO yeni dağıtım katmanı oldu. Previsible verisine göre 19 GA4 property'de LLM-driven sessions Jan-May 2025 döneminde 17,076 → 107,100, yani **+527%**. Bu hâlâ toplam trafikte küçük pay olabilir, ama yüksek intent B2B/devtool query'leri için erken sinyal değerli.
- En iyi fırsat: 113 ürün için blog yazısı değil, **product-led intent page** üretmek: converter/use-case page, comparison, alternative, troubleshooting, API snippet, template/checklist, “best tool for persona”. Her sayfa canlı ürüne, sample input/output'a ve ölçülebilir CTA'ya bağlı olmalı.

## Gerçek Başarı Hikayeleri
- **Omnius / AI image generator pSEO:** Müşteri başlangıçta 67 monthly signup, 13 ranked keyword, 102 monthly organic click seviyesindeydi. 10 ay içinde signup 2,100+/ay oldu; 11k+ toplam signup, 850% monthly organic traffic growth, Q1 2025'te Q4 2024'e göre 220.65% organic growth, 5,742+ organic keyword, 305+ first-page keyword raporlandı. Ders: pSEO signup üretebilir; ama long-tail intent + conversion architecture birlikte çalışmalı.
- **Santifer iRepair open-source case:** Astro + Airtable ERP + DataForSEO + Node scripts + Sharp pipeline ile 15,500+ unique page üretildi. README 2.26M impressions, 2,000 monthly clicks, 1,800+ indexed keyword ve crawl-budget için 4,084 sitemapped URL bildiriyor. En önemli nokta: her kombinasyon indexlenmiyor; DataForSEO search volume threshold ile düşük potansiyelli sayfalar `noindex` veya dışarıda bırakılıyor.
- **Pinterest GEO paper (`2602.02961`):** Pinterest, billions of images / tens of millions of collection pages ölçeğinde VLM + agent trend-mining + authority-aware interlinking kullandığını ve **20% organic traffic growth** ile multi-million MAU katkısı aldığını raporluyor. Bu akademik/industry paper, “AI search için collection page + semantic aggregation + link authority” yaklaşımını doğruluyor.
- **Reddit r/SaaS anecdote:** Bir AI presentation SaaS'ı 1,200 unique page, 10K+ keyword clustering, tutorial/comparison/use-case templates ve manual intros/CTAs ile 3 ayda +520% traffic ve 180K monthly visits iddia ediyor. Doğrulanmamış, satış kokusu var; yine de pattern doğru: persona/use-case/page family.
- **Reddit r/SideProject micro-demand:** Google Sheets içinde $49 AI SEO blog generator yapan bir side project 10 günde $948 gelir iddia etti. Bu trafik case'i değil, “SEO içerik otomasyonu için küçük bütçeli alıcı var” sinyali.
- **Anti-case — 16-month AI content experiment:** 20 yeni domain × 100 AI article = 2,000 içerik. İlk indexlenme iyi; ama otorite, E-E-A-T, özgün insight, link/internal-link ve güncelleme yoksa 3-6 ayda görünürlük çöküyor. Ders: “yayınla ve unut” modeli çöplük.

## Pazar Büyüklüğü & Fırsat
- 113 healthy ürün, tek başına pSEO data asset. 113 ürün × 6 güvenli page family = 678 sayfalık ilk teorik envanter; 10 family ile 1,130 sayfa. Ama ilk hamle tümünü basmak değil, 40-80 sayfalık kontrollü pilot.
- Klasik SEO bitmedi, biçim değiştiriyor. Search Engine Land/Previsible verisi LLM trafik payının büyüdüğünü gösteriyor; Google tarafında ise AI Overviews/zero-click riski artıyor. Bu yüzden ölçüm seti sadece rank/click değil: AI mention, citation, branded search, direct visit, checkout click, email capture.
- Programmatic SEO'nun en güçlü olduğu alanlar: veri tabanı olan sayfalar, tool/action intent, comparison intent, local/category combinations, integration/workflow combinations. UniverseCreator devtool ağı burada doğal avantaja sahip.
- Araç maliyeti POC için düşük tutulabilir: DataForSEO Google Ads Keywords Standard Queue **$0.05/task**, task başına 1,000 keyword'e kadar, yani 1M keyword ≈ **$50**; Live Mode 1M keyword ≈ **$75**. Ahrefs Lite güncel sayfada $129/ay; Semrush AI Visibility Toolkit $99/ay. POC'de pahalı suite şart değil.

## Rakipler & Boşluklar
- **Rakip kategorileri:** Semrush/Ahrefs/Surfer/Seodity/SearchAtlas gibi SEO suite/content optimizer; sitefire.ai/Profound/Evertune gibi AI-search/GEO visibility araçları; PageFactory/SEOmatic gibi pSEO builders; Jasper/Copy.ai/Writesonic gibi generic AI writer; WordPress/Webflow/Framer publish ekosistemi.
- **Boşluk 1 — generic content değil çalışan ürün:** Rakiplerin çoğu “metin üret” diyor. UniverseCreator'da canlı URL, product metadata, README, checkout, health status, sample workflows var. Bu data, thin content riskini düşüren gerçek differansiyel.
- **Boşluk 2 — publish gate:** Çoğu pSEO tool'u çok sayfa basmaya çalışıyor. Asıl değer `publish / noindex / rewrite / kill` karar katmanı. Santifer bunu DataForSEO threshold + filtered sitemap ile yapmış; UniverseCreator bunu health + checkout + intent score + QA ile yapabilir.
- **Boşluk 3 — AI-search citation readiness:** LLM'ler açık, kaynaklı, yapılandırılmış, machine-scannable ve üçüncü taraf sinyali olan içeriği daha iyi kullanıyor. ArXiv GEO papers earned-media bias ve machine scannability vurguluyor. UniverseCreator'ın sadece kendi sitesinde değil GitHub README, docs, listings, Reddit/HN/PH mentions gibi earned signals üretmesi lazım.
- **Boşluk 4 — internal link graph:** 113 ürün birbirine converter → API → security → devtool kümeleriyle bağlanabilir. Tekil bloglar değil, topic graph kazanır.

## Teknik Gereksinimler
- **Source-of-truth inventory:** `STATE.json` + `STATE_SUMMARY.json` + ürün README/product metadata + canonical URL + health + checkout + category + sample input/output.
- **Keyword/data layer:** DataForSEO keyword API, Google Search Console, mümkünse Ahrefs/Semrush yalnızca rekabet/gap için. POC'de DataForSEO + GSC yeterli.
- **Page families:**
  1. `free [task] tool`
  2. `[A] to [B] converter`
  3. `[tool/category] alternative`
  4. `[tool A] vs [tool B/manual workflow]`
  5. `best [category] tools for [persona]`
  6. `[error/code] fix guide`
  7. `[API/example/snippet]`
  8. `[template/checklist]`
- **Quality gate:** unique data, real screenshot/sample, schema plan, internal links, source links, no duplicate skeleton, no unsupported claim, current pricing/date if comparison page, publish/noindex/rewrite decision.
- **Technical SEO:** sitemap index, canonical, lastmod, breadcrumbs, SoftwareApplication/Product/FAQ/HowTo where uygun, OpenGraph, title/meta, rendered HTML check, broken link check, Core Web Vitals sanity.
- **Indexing caution:** GitHub'da popüler `goenning/google-indexing-script` 7.6k+ star; README açıkça Google Indexing API'nin yalnızca `JobPosting` veya `BroadcastEvent` structured data için çalıştığını ve “indexing != ranking” olduğunu söylüyor. Yani bunu devtool pSEO sayfaları için sihirli index hack'i diye kullanmak yanlış.
- **AI-search tracking:** ChatGPT/Perplexity/Gemini/Copilot prompt seti, cited URL, brand mention, answer rank, source type, competitor mentions.
- **Human review:** İlk 50-100 sayfada zorunlu. Kör autopublish burada aptalca; domain yakmak SEO değil, dijital kundakçılık.

## Ham Notlar
- `projeler.txt` taramasında doğrudan SEO/content factory sinyalleri az ama değerli: AI-agent publishing framework, marketing skills for Claude Code, SEO headline testing, CTR winner selection, markdown/docs/blog publish fikri.
- `ddgr` bu turda çalıştırıldı fakat anlamlı JSON sonuç döndürmedi. Boş kaldığı için web search + Jina + Reddit JSON + GitHub + ArXiv + MCPTube ile kapsam tamamlandı.
- Reddit community intelligence net: pSEO savunucuları bile “unique data asset yoksa çalışmaz” diyor. r/SEO tarafında 1,151 sayfa / 101 keyword / 124 users gibi erken spike'lar var; r/Blogging tarafında AI/pSEO sitelerin Google update sonrası çöküş hikâyeleri çok.
- MCPTube `ZT_8_uz_c-s`: DataForSEO MCP ile 25 commercial keyword / 23k monthly search volume, Perplexity gap analysis, Claude strategy, Playwright screenshots, 1,247 page planı: 420 comparison, 312 industry guide, 215 feature page, 150 budget recommendation, 150 integration/workflow guide. Güzel playbook ama bu çıktılar yayın değil, strateji adayı.
- MCPTube `m9iaJNJE2-M`: n8n + Apify + X/YouTube scrape + OpenRouter/Perplexity/Claude + Slack approve gate. En kritik parça approve gate; tam otomatik yayın değil.
- ProductHunt doğrudan Jina ile 403/CAPTCHA verdi; fallback arama Seodity, SearchAtlas, sitefire.ai ve Search Console Audit gibi ürünlerin “AI SEO / GEO / Search Console insights / 1-click publish” konumlandığını gösterdi. Bu kategori kalabalık; wedge ürün içeriği değil, **113 canlı ürün için product-led growth OS** olmalı.
