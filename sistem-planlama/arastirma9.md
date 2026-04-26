# Araştırma #9 — Browser Agent + Otomasyon
**Tarih:** 2026-04-21 08:18 +03
**Konu:** Browser-use, Skyvern, Stagehand/Browserbase, Playwright MCP ve cloud browser altyapılarıyla gerçek web işlerinin otomasyonu.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma8.md` / `planlama8.md`
- `projeler.txt` sinyalleri: Browser-Use Desktop, Browser-Use Agent SDK, Browser-Use QA, Stagehand, Skyvern, Crawlee, Obscura, agent-browser / browser automation CLI kayıtları
- Browser Use pricing/docs: https://docs.browser-use.com/cloud/pricing
- Browser Use WebVoyager raporu: https://browser-use.com/posts/sota-technical-report
- Browser Use repo: https://github.com/browser-use/browser-use
- Skyvern pricing: https://www.skyvern.com/pricing/
- Skyvern products: https://www.skyvern.com/products
- Skyvern repo: https://github.com/Skyvern-AI/skyvern
- Stagehand repo/docs: https://github.com/browserbase/stagehand , https://stagehand.dev/
- Browserbase plans: https://docs.browserbase.com/account/billing/plans
- Playwright MCP docs: https://playwright.dev/mcp/introduction
- GitHub repos: https://github.com/microsoft/playwright , https://github.com/microsoft/playwright-mcp , https://github.com/steel-dev/steel-browser , https://github.com/bytedance/UI-TARS-desktop , https://github.com/Skyvern-AI/n8n-nodes-skyvern , https://github.com/kushal238/job-app-automation , https://github.com/BjornMelin/grammarly-mcp
- Reddit JSON: https://reddit.com/r/webscraping/comments/1rqsvgp/python_selenium_at_scale_50_nodes_39m_records/ , https://reddit.com/r/webscraping/comments/1sjd609/stop_defaulting_to_seleniumplaywright_check_the/ , https://reddit.com/r/automation/comments/1lgvmf7/i_automated_my_reselling_business_and_made_it/ , https://reddit.com/r/automation/comments/1sl1um7/browserbase_review_after_running_10k_sessions/ , https://reddit.com/r/SideProject/comments/1l6ndn3/this_ai_agent_can_read_your_resume_find_matching/
- ArXiv / akademik: https://arxiv.org/abs/2307.13854 , https://arxiv.org/abs/2403.07718 , https://arxiv.org/abs/2510.04363 , https://arxiv.org/abs/2504.12516 , https://arxiv.org/abs/2506.01952 , https://arxiv.org/abs/2601.07262
- UI-TARS benchmark repo: https://github.com/bytedance/ui-tars
- Pazar: https://www.grandviewresearch.com/industry-analysis/robotic-process-automation-rpa-market , https://www.marketresearch.com/Global-Industry-Analysts-v1039/Web-Scraping-Software-42949024/
- YouTube/MCPTube: https://www.youtube.com/watch?v=2716IUeCIQo , https://www.youtube.com/watch?v=eFz2OUN3BYw , https://www.youtube.com/watch?v=FhDYo2VKu5E , https://www.youtube.com/watch?v=PPutzww1RaM , https://www.youtube.com/watch?v=PCNMoJhq_Go , https://www.youtube.com/watch?v=9L7PF56JWSI

## Özet Bulgular
- **Browser agent pazarı artık “demo bot” değil, yeni RPA katmanı.** Klasik RPA rule-based ve selector-heavy; yeni dalga Playwright + erişilebilirlik snapshot'ı + LLM reasoning + credential/session/proxy altyapısı ile kırılgan portalları, formları, fiyat izlemeyi, lead enrichment'i ve QA akışlarını hedefliyor.
- **Kazanan pratik: API-first, browser-last.** Reddit/webscraping community aynı şeyi tekrar ediyor: önce Network/XHR endpoint'i bulunur; doğrudan API varsa Selenium/Playwright ile UI savaşına girilmez. Browser agent pahalı ve yavaş katmandır; gerçek kaldıraç API yoksa veya login/portal/JS zorunluysa gelir.
- **Açık kaynak çekişi çok güçlü.** 2026-04-21 GitHub snapshot'ında `browser-use/browser-use` **89,036★ / 10,181 fork**, `microsoft/playwright` **86,912★**, `microsoft/playwright-mcp` **31,162★**, `bytedance/UI-TARS-desktop` **29,467★**, `browserbase/stagehand` **22,216★**, `Skyvern-AI/skyvern` **21,300★**, `steel-dev/steel-browser` **6,877★**. Bu alan fringe değil.
- **Ama güvenilirlik hâlâ pahalı.** WebArena'da eski GPT-4 tabanlı en iyi ajan **%14.41** başarıda kalırken insan **%78.24**. MacroBench'te modeller basit görevlerde **%91.7** güvenilirken kompleks workflow'larda **%0.0** başarı görüyor ve üretim kalitesinde kod yazamıyor. Sonuç: prod için “tam otonom browser agent” değil, **dar görev + guardrail + retry + insan kapısı** gerekir.
- **UniverseCreator için en iyi wedge:** genel “her şeyi otomatik yapan ajan” satmak değil; **portal/login gerektiren tekrarlı işlerin managed automation'ı**. En yakın para alanları: e-commerce fiyat/stok izleme, marketplace deal finder, lead/contact form enrichment, rakip fiyat takibi, ürün QA/checkout health, invoice/document download, job board scraping değil spam başvuru.

## Gerçek Başarı Hikayeleri
- **Browser-use benchmark başarısı:** Browser Use ekibi WebVoyager üzerinde **586 görevde %89.1** başarı iddia ediyor; domain bazında HuggingFace **%100**, Google Flights **%95**, Amazon/GitHub **%92**, Booking **%80**. Bu iyi sinyal ama vendor benchmark: 55 görevin çıkarıldığı, tarihlerin güncellendiği ve bazı değerlendirmelerin manuel düzeltildiği açıkça yazıyor. Yani “pazarlama verisi ama faydalı yön işareti”.
- **Reddit — 50 node Selenium scraper:** r/webscraping kullanıcısı 2+ yıldır **50 node** üzerinde çalışan sistemle **3.9M+ kayıt** topladığını anlattı. Dersler: headless yerine full Chrome, `navigator.webdriver`/automation flag mitigasyonu, VPN/proxy, class selector yerine tag/text XPath, 429 handling ve dedup kritik.
- **Reddit — reselling automation:** r/automation post'unda Playwright tabanlı headless browser filosu + AI parser + finans modeliyle marketplace deal finder anlatıldı. Örnek: iPhone 15 Pro Max **$450** listelenmiş, ortalama satış **$650**, seyahat/zaman/fee sonrası **$60 potansiyel profit**; sistem ayda **20k sayfa** seviyesinde scrape ettiğini söylüyor. Bu küçük ama net para sinyali: browser agent “iş yapıyor” değil, **arbitraj kararı hızlandırıyor**.
- **Reddit — Browserbase 10k+ session review:** r/automation kullanıcısı **10k+ Browserbase session** sonrası stealth/fingerprint ve session spin-up tarafını olumlu, **1 dakika minimum billing** tarafını maliyet riski olarak yazdı. En işe yarar taktik: kısa scrape'leri aynı session içinde batch'lemek; yorumlarda bunun maliyeti **~%70** düşürebildiği anekdotu var.
- **Browserbase/Stagehand positioning:** Browserbase sitesinde “10,000+ companies building beyond the API” iddiası var; Stagehand ise Selector/Selenium kırılganlığına karşı `act()`, `extract()`, `observe()`, `agent()` ile code + natural language hibriti sunuyor. Botasaurus ile canlı sayfa okunabildi; Stagehand ana mesajı “Smarter than Selenium, safer than an agent”.
- **Skyvern workflow örnekleri:** Skyvern ürün sayfası form doldurma, veri çıkarma, portal login, document download, çok-adımlı cross-site workflow, CAPTCHA/2FA/proxy/credential vault ve n8n/Zapier/Make entegrasyonunu doğrudan hedefliyor. Bu, UniverseCreator'ın local business / e-commerce / lead-gen araştırmalarıyla aynı para damarına denk geliyor.

## Pazar Büyüklüğü & Fırsat
- **RPA ana pazar büyüyor:** Grand View Research, global RPA pazarını **2025'te $4.68B**, **2033'te $35.84B**, **%29.0 CAGR** olarak veriyor. Browser agent'lar bunun “legacy portal + AI + browser infra” alt dalı.
- **Web scraping/veri çıkarma pazarı ayrı fırsat:** Global Industry Analysts rapor özeti web scraping software pazarını **2024'te $909.9M**, **2030'da $1.9B**, **%13.4 CAGR** olarak veriyor. Fiyat/stok/lead/research veri ürünleri için doğrudan pazar var.
- **Cloud browser altyapısı fiyatları küçük ekip için artık ulaşılabilir:** Browserbase Free **1 saat/ay**, Developer **$20/ay + 100 browser hour**, Startup **$99/ay + 500 browser hour**; overage Developer **$0.12/hour**, Startup **$0.10/hour**. Bu, POC maliyetini eski RPA lisanslarına göre komik derecede düşük yapıyor.
- **AI-agent cloud pricing de granular:** Browser Use sayfasında agent LLM cost **$0.002/step'ten**, task init **$0.01/task**, browser session **$0.06/hour**, proxy **$5/GB**, skill creation **$2/skill**, skill execution **$0.02/API call** görünüyor. Aynı sayfada subscription kartı **$75/mo / $100 credits** ve comparison içinde “From $40/mo” var; satın alma öncesi teyit şart, ama POC için rakamlar hâlâ düşük.
- **Skyvern fiyatları agency için net:** Free **1,000 credits**, Hobby **$29/ay + 30,000 credits + 10 concurrent runs**, Pro **$149/ay + 150,000 credits + 25 concurrent runs + 2FA/TOTP + advanced CAPTCHA**. Eğer müşteri başı $300-$1,500/ay paket satılıyorsa altyapı maliyeti makul kalır.
- **Asıl fırsat SaaS değil managed outcome.** “Browser agent API” satmak kalabalık. Daha iyi hamle: “rakip fiyatları her sabah çıkarıyorum”, “supplier portal invoice'larını indiriyorum”, “lead form/contact enrichment yapıyorum”, “checkout regression'ı insan gibi geziyorum” gibi sonuç satmak.

## Rakipler & Boşluklar
- **Playwright MCP:** En ucuz ve kontrol edilebilir başlangıç katmanı. Accessibility snapshot ile çalışıyor; Playwright docs snapshot'ın **~200-400 token** olduğunu, DOM/screenshot'ın binlerce token tuttuğunu söylüyor. 40+ tool, persistent session, headed default. Zayıf tarafı: karmaşık hedeflerde agent reasoning'i sen tasarlarsın; altyapı/captcha/proxy hazır gelmez.
- **Stagehand + Browserbase:** Production için en dengeli yaklaşım: `goto/observe/act/extract/agent` + code/natural language karışımı. Stagehand açıkça “yüksek seviye agent unpredictability” ile “düşük seviye selector kodu” arasında köprü kuruyor. Zayıf taraf: Node/TS ekosistemi ve Browserbase maliyeti; kısa görevlerde 1 dakika billing floor maliyet doğurabilir.
- **Skyvern:** No-code workflow builder, SDK, credential vault, CAPTCHA/2FA/proxy, MCP ve n8n/Make/Zapier entegrasyonu ile agency/ops tarafına çok uygun. Zayıf taraf: AGPL lisans / self-host karmaşıklığı / vendor cloud'a bağımlılık kararı dikkat ister.
- **Browser Use:** En büyük OSS traction. Python-first, cloud API ve skill modeline doğru gidiyor. POC ve agentic experimentation için güçlü. Zayıf taraf: community'de yavaş/pahalı/karmaşık task'ta fail yorumları var; vendor benchmark'leri gerçek müşteri workflow'u yerine benchmark üstünde iyi görünebilir.
- **Steel / Browserbase / cloud browser APIs:** Eğer ihtiyaç sadece “ajan için browser sandbox” ise framework değil altyapı seçimi yapılmalı. Session reuse, recording, proxy, captcha, stealth, isolation ve cost floor ana karar kriterleri.
- **Boşluk #1 — workflow packaging:** Çoğu araç toolkit. Müşteri ise “hangi portal, hangi çıktı, hangi SLA?” ister. UniverseCreator burada vertical template + managed ops satarak ayrışabilir.
- **Boşluk #2 — cost-aware browser routing:** İnsanlar her işe browser açıyor; bu aptalca. Network/API-first → deterministic Playwright → Stagehand/Skyvern AI fallback → human review şeklinde routing yapan paket az.
- **Boşluk #3 — güvenlik ve spam disiplini:** Job apply agent örneğinde community tepkisi sert: otomatik başvuru spam'e dönüşüyor. Browser agent ürünü compliance, consent ve rate limit olmadan markayı yakar.

## Teknik Gereksinimler
- **Task taxonomy:** her iş `API-first`, `deterministic Playwright`, `AI-augmented browser`, `human-in-loop`, `blocked/TOS-risk` sınıfına ayrılmalı.
- **Session ve credential yönetimi:** persistent cookies, vault, 2FA handoff, secrets'ın LLM'e gösterilmemesi, domain allowlist.
- **Cost guardrail:** task başına max step, max session dakika, proxy GB limiti, retry limiti, batch/session reuse kuralı.
- **Observation stack:** accessibility snapshot, screenshot, DOM/HTML, network trace, console log, session recording, action log.
- **Fallback chain:** doğrudan API → HTTP/curl → Playwright selector → Playwright a11y ref → Stagehand/Skyvern natural language → insan onayı.
- **Anti-bot / compliance:** proxy/stealth teknik olarak mümkün diye yapılmaz. Robots/TOS, rate limit, account risk, spam, CAPTCHA solving etik/sözleşme riski ayrı sınıflanmalı.
- **Eval:** her workflow için success assertion şart: beklenen JSON schema, sayfa state doğrulama, downloaded file checksum, form submission confirmation, human review sample.
- **Infrastructure:** başlangıçta local Chrome + chrome-devtools-axi + Playwright MCP; ölçek gerekirse Browserbase/Skyvern cloud; high-risk workflow'larda visible headed browser + manual checkpoints.

## Ham Notlar
- `projeler.txt` içinde Browser-Use Desktop, Browser-Use Agent SDK, Browser-Use QA, Stagehand, Skyvern, Crawlee, Obscura ve browser automation CLI sinyalleri çıktı. Yerel katalog bu konu için güçlü.
- `ddgr` sonuçları ağırlıkla vendor karşılaştırması ve blog verdi; resmi fiyat/doküman için Jina + web doğrulaması daha değerli oldu.
- `mcp__arxiv__search_papers` bu cycle'da 429 rate-limit verdi. Araştırma akademik katmanı web/arXiv URL okuması ile tamamlandı; rate-limit loglandı.
- MCPTube `parallel_add.py` 6 video için “başarılı” döndü ama MCP library'de görünmedi; tek tek `add_video` ile görünür hale geldi. Aynı entegrasyon sürtünmesi önceki cycle'da da yaşanmıştı.
- Botasaurus ilk denemede yanlış `data` kullanımı yüzünden hata verdi; ikinci denemede `stagehand.dev` ve `browserbase.com` canlı DOM/headings başarıyla okundu.
- Net hüküm: **Browser agent sistemi gelir üretir, ama sadece dar ve ölçülebilir görevlerde.** “Her siteyi gezen özgür ajan” romantizmi pahalı oyuncak; “portal X'ten veri Y'yi çıkar, Z formatında teslim et” para eder.
