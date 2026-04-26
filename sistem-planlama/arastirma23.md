# Araştırma #23 — Browser Agent + Otomasyon
**Tarih:** 2026-04-21 17:51 +03
**Konu:** Browser agent / browser automation ekosistemi için 2026 doğrulama turu. Odak: hangi stack gerçekten işe yarıyor, fiyat/altyapı ne durumda, güvenilirlik ve güvenlik nerede kırılıyor, ve UniverseCreator bunu genel oyuncak yerine gelir/operasyon çarpanına nasıl çevirebilir.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`
- `projeler.txt` eşleşmeleri:
  - https://github.com/browser-use/qa-use/
  - https://github.com/browser-use/desktop/
  - https://github.com/Skyvern-AI/skyvern
  - https://github.com/browser-use/agent-sdk
  - https://github.com/vercel-labs/agent-browser
  - https://www.reddit.com/r/ClaudeAI/comments/1orplvu/mcp_for_browser_automation/
- ddgr sorguları:
  - `browser agent automation revenue 2025`
  - `browser-use skyvern stagehand case study 2025`
  - `browser automation ai agents ROI enterprise 2025`
  - `browser use pricing`
  - `Skyvern pricing`
  - `Browserbase pricing`
  - **Not:** Bu turda hepsi `HTTP Error 202: Accepted` + `[]` döndü; araştırma fallback olarak resmî sayfalar, web index, Reddit JSON, GitHub, ArXiv, MCPTube ve Product Hunt üzerinden sürdürüldü.
- Resmî / dokümantasyon / ürün:
  - https://docs.browser-use.com/pricing
  - https://github.com/browser-use/browser-use
  - https://www.producthunt.com/products/browser-use
  - https://docs.browserbase.com/guides/plans-and-pricing
  - https://github.com/browserbase/stagehand
  - https://www.producthunt.com/products/browserbase
  - https://stripe.com/us/customers/browserbase
  - https://www.skyvern.com/pricing
  - https://github.com/Skyvern-AI/skyvern
  - https://github.com/vercel-labs/agent-browser
- Pazar / operasyon:
  - https://www.grandviewresearch.com/industry-analysis/robotic-process-automation-rpa-market
  - https://www.grandviewresearch.com/industry-analysis/intelligent-process-automation-market
  - https://content.testrail.com/hubfs/Downloadables/Fourth-Edition-Software-Testing-and-Quality-Report.pdf
- Gerçek gelir / kullanım hikâyeleri:
  - https://www.indiehackers.com/product/browserflow/revenue
  - https://www.indiehackers.com/post/tech/growing-an-open-source-side-hustle-to-2m-arr-BXHl3KJql5l2pccW5wIJ
  - https://www.indiehackers.com/post/tech/growing-a-scraping-api-to-10k-mrr-in-12-months-6iF8SJRF4WpciDff9aYi
- Reddit JSON API:
  - https://reddit.com/r/automation/comments/1myo39i/much_faster_and_cheaper_browser_use_agent/
  - https://reddit.com/r/webscraping/comments/1rqsvgp/python_selenium_at_scale_50_nodes_39m_records/
  - https://reddit.com/r/automation/comments/1mq9n9a/anyone_here_compared_hyperbrowser_with/
- GitHub snapshot (2026-04-21):
  - https://github.com/browser-use/browser-use
  - https://github.com/browserbase/stagehand
  - https://github.com/Skyvern-AI/skyvern
  - https://github.com/vercel-labs/agent-browser
  - https://github.com/browser-use/desktop
  - https://github.com/browser-use/agent-sdk
- ArXiv / akademik:
  - https://arxiv.org/abs/2503.07919
  - https://arxiv.org/abs/2602.13559
  - https://arxiv.org/abs/2512.07725
  - https://arxiv.org/abs/2510.02250
- YouTube / MCPTube:
  - https://www.youtube.com/watch?v=zQHXJaXTp4U
  - https://www.youtube.com/watch?v=AyHcK4vFg7g
  - https://www.youtube.com/watch?v=2716IUeCIQo

## Özet Bulgular
- **Kategori artık gerçek.** 2026-04-21 GitHub snapshot'ında `browser-use/browser-use` **89,163★**, `vercel-labs/agent-browser` **30,035★**, `browserbase/stagehand` **22,250★**, `Skyvern-AI/skyvern` **21,309★**. Product Hunt tarafında Browser Use 2025 boyunca 4 ayrı launch çıkarmış; Browserbase'in `Director` lansmanı **21 Ekim 2025**'te günün **#1**'i olmuş. Bu artık oyuncak repo kategorisi değil.
- **Kazanan tek araç değil, doğru lane seçimi.** Browser Use tarafı daha çok keşif/prompt-first agent deneyimi ve stealth/persistent workspace anlatıyor; Stagehand/Browserbase tarafı “AI ile yolu bul, sonra deterministic workflow'a çevir” diyor; Skyvern ise Playwright üstüne AI + CAPTCHA + residential proxy + no-code bulut paketi sunuyor. Doğru mimari: **keşfet → derle → operasyonel çalıştır**.
- **Fiyatlar görünür hale gelmiş durumda.** Browserbase docs'a göre Developer plan **$20/ay** karşılığında **100 browser hour**, **1 GB proxy**, otomatik CAPTCHA ve **6 saat** session süresi veriyor; Startup **$99/ay** ile **500 browser hour**. Skyvern pricing sayfasında Hobby **$29/ay / 30,000 kredi**, Pro **$149/ay / 150,000 kredi**, Pro'da advanced CAPTCHA ve residential proxy var. Browser Use pricing sayfasında subscription **$40/ay**'dan başlıyor; LLM step maliyeti **$0.002**'den, browser session maliyeti **$0.06/saat**, proxy **$5/GB**.
- **Ama güvenilirlik hâlâ sert problem.** Reddit'te Browser Use için “yavaş, pahalı, kompleks task'lerde kırılıyor” şikâyeti var; başka thread'de Browserbase/Playwright kombinasyonunda **30-40 dakika** sonra session reset/hang sorunu anlatılıyor. r/webscraping örneğinde ekip **50 node**, **3.9M+ kayıt**, full Chrome + VPN/proxy + webdriver gizleme kullanıyor. Yani “prompt ver, her site sonsuza kadar çözülür” masalı hâlâ masal.
- **Akademik veriler hype'ı ayıklıyor.** BEARCUBS benchmark'ında insan doğruluğu **%84.7**, ChatGPT Agent **%65.8**, Operator **%23.4**. OpAgent paper'ı modüler planner/grounder/reflector/summarizer yapısıyla başarıyı **%71.6**'ya çıkarıyor. `Scaling Agents for Computer Use` ise çoklu rollout + davranış seçimiyle OSWorld'de **%72.6**'ya ulaşıp insan seviyesini kıl payı geçiyor. Çıkan ders net: **tek rollout + tek ajan kırılgan; modülerlik ve evaluator şart**.
- **Güvenlik tarafı hafife alınamaz.** `Privacy Practices of Browser Agents` makalesi 8 popüler browser agent'ta **30 güvenlik/gizlilik açığı** buluyor. Form alanına hassas veri otomatik doldurma, browser privacy feature'larını kapatma ve cross-site tracking gibi riskler var. Dolayısıyla login handoff, domain allowlist, scoped secret ve audit trail zorunlu.
- **Para, sıkıcı ama faydalı işte.** Browserflow'un Indie Hackers ürün sayfası **$12K/ay** gösteriyor. Browserless için 2025 Indie Hackers yazısı **$2M ARR / $167K aylık gelir** söylüyor. Scrape Creators **12 ayda $10K+ MRR**'a çıkmış. Kısacası para viral demoda değil; **browser ops, scraping, form doldurma, monitoring ve infra** tarafında.

## Gerçek Başarı Hikayeleri
- **Browserflow — no-code browser automation:** Indie Hackers ürün sayfası Browserflow için güncel geliri **$12K/ay** gösteriyor. Ürün tanımı net: “browser içinde form doldurma, scraping, screenshot alma” gibi işleri kod yazmadan otomatikleştiriyor. Bu, SMB/solopreneur tarafında browser automation'a para ödendiğinin doğrudan kanıtı.
- **Browserless — headless browser infra işi canavar gibi para yazabiliyor:** Indie Hackers'ın 31 Ocak 2025 tarihli röportajında Browserless için **$2M ARR** ve **$167K aylık gelir** rakamı veriliyor. Vakanın önemi şu: ürün “AI” diye bağırmıyor; hosted headless browser ve automation altyapısı satıyor. Sıkıcı katman para basıyor.
- **Scrape Creators — dikey scraping API, 12 ayda $10K+ MRR:** 31 Temmuz 2025 tarihli Indie Hackers yazısı Scrape Creators'ın **12 ay içinde $10K+ MRR**'a çıktığını anlatıyor. Founder'ın ana dersi: tek dikeye odaklanmak ve audience/SEO ile beslemek. Browser agent tarafında da yatay “her siteyi çözerim” yerine dikey iş paketleri daha mantıklı.
- **Browserbase — usage scale zaten devasa:** Stripe customer story'si Browserbase'in **100 milyon+ usage minute / ay** faturaladığını ve **yüz milyonlarca browser session dakikasını** usage-based billing ile yönettiğini söylüyor. Bu gelir değil; ama altyapı talebinin hacmini gösteren güçlü kullanım kanıtı.
- **Product Hunt müşteri örnekleri — gerçek business use-case'ler var:** Browserbase kullanıcıları Embra ve Soshi, ürünün kendi AI ajanları adına web crawl/act ettiğini ve sistemi inşa etmeyi **"10x daha kolay"** hale getirdiğini yazıyor. Browser Use tarafında Local Operator ekibi login gerektiren işleri Browser Use handoff ile çözdüğünü belirtiyor. Yani teori değil; canlı kullanıcı işine girmiş.

## Pazar Büyüklüğü & Fırsat
- **Browser agent pazarı henüz ayrı ve temiz bir Gartner kutusu değil; ama para girdiği komşu bütçeler net.** Bu bölümdeki ilk çıkarım **yorumdur**: Browser agent harcamaları bugün ağırlıkla RPA, intelligent process automation, QA automation, scraping infra ve back-office ops bütçelerinden besleniyor.
- **RPA bütçesi büyük ve büyüyor.** Grand View Research'e göre global RPA pazarı **2025'te $4.68B**, **2033'te $35.84B**, CAGR **%29.0**. Browser agent'lar bu pastanın “DOM/XPath kırılmasına daha dayanıklı, daha esnek web görevleri” alt dilimini kemiriyor.
- **Intelligent Process Automation daha da büyük bir komşu havuz.** Aynı kaynağın IPA raporuna göre pazar **2024'te $14.55B**, **2030'da $44.74B**, CAGR **%22.6**. Browser agent'lar özellikle portal tabanlı, login gerektiren, API'siz kurumsal işlerde buraya oturuyor.
- **Test/QA otomasyonu da doğrudan fırsat.** TestRail 4th Edition raporunda ekiplerin **%43**'ü test otomasyonunu artırmayı planlıyor; yüksek otomasyon + CI/CD olgunluğu olan ekipler **%86** daha hızlı release cycle ve **%71** daha düşük defect leakage raporluyor. Browser agent'lar özellikle e2e, smoke, regression ve “gerçek kullanıcı akışı” testlerinde bu bütçeye girebilir.
- **Kategoriye talep sinyali güçlü.** Browser Use Product Hunt sayfasında **1.1K follower**, **14 inceleme**, Browserbase tarafında da **1.1K follower** ve 2025'te birden fazla launch var. GitHub star ve Product Hunt launch kombinasyonu, geliştirici ilgisinin yüzeysel değil kalıcı olduğuna işaret ediyor.
- **UniverseCreator için asıl fırsat genel agent satmak değil, dikey browser ops paketi satmak.** Buradaki çıkarım yine **yorumdur**: en hızlı para “generic browser agent platformu”ndan değil; login gerektiren portal, veri çıkarma, form gönderme, belge indirme, QA smoke test ve monitoring işlerini paketlemekten gelir.

## Rakipler & Boşluklar
- **Browser Use:** En güçlü yanı agent-first deneyim, yüksek community traction, stealth/persistent-workspace anlatısı ve hızlı demo etkisi. Zayıf yanı prod'da maliyet ve determinism sorusu. Kısa keşif ve belirsiz site exploration için iyi; her gece binlerce stabil run için tek başına güvenmek riskli.
- **Browserbase + Stagehand:** En güçlü yanı geliştirici ergonomisi ve “AI'dan deterministic workflow'a geçiş” söylemi. Browserbase infra + Stagehand SDK kombinasyonu compile edilmiş tekrar eden işler için mantıklı. Zayıf yanı, daha çok teknik ekibe hitap etmesi ve LLM/proxy/vendor kombinasyonlarının toplam maliyetini senin yönetmen gerekmesi.
- **Skyvern:** En güçlü yanı Playwright-compatible AI layer, cloud/no-code katmanı, advanced CAPTCHA + residential proxy paketlemesi ve pricing sayfasında doğrudan “500+ enterprise teams” iddiası. Zayıf yanı kredi bazlı soyut maliyet ve yoğun vendor bağımlılığı.
- **Playwright MCP / agent-browser:** Mevcut Codex/Claude çalışma tarzına çok yakın, insan kontrolünü iyi koruyan, engineering workflow'ları için güçlü araçlar. Zayıf yanı no-code business-user deneyimi değil; daha çok operatör/agent stack bileşeni.
- **Asıl boşluk #1: keşif ile operasyonu ayıran ürünleşmiş katman az.** Piyasadaki çoğu araç ya demo odaklı prompt-run gösteriyor ya da ağır geliştirici SDK'sı veriyor. Eksik olan şey şu: **siteyi bir kez keşfet, başarılı yolu kaydet, deterministic çalıştır, sapınca tekrar keşif moduna dön**.
- **Asıl boşluk #2: TR/MENA portal otomasyonları.** Global oyuncular genel çözüm satıyor. Türkiye/MENA'daki garip devlet/kurumsal portallar, çok adımlı login, PDF indirme, Excel upload, dil/localizasyon, mobil görünüm, anti-bot saçmalıkları için dikey paketler daha savunulabilir.
- **Asıl boşluk #3: güvenlikli insan kapısı.** Birçok ürün “agent yapar abi” diye satıyor; ama login, CAPTCHA, ödeme, hassas form alanı ve yasal onay noktalarında kontrollü handoff iyi paketlenmiyor. Oysa gerçek müşteri tam burada ikna oluyor.

## Teknik Gereksinimler
- **3-lane mimari:**
  1. **Scout lane** — bilinmeyen sitede yolu bulan exploratory agent
  2. **Compile lane** — başarılı adımları repeatable workflow/script'e çeviren katman
  3. **Operate lane** — schedule/queue/retry ile güvenilir biçimde tekrar çalıştıran katman
- **HITL zorunlu kapılar:** login, 2FA, CAPTCHA, ödeme, nihai submit, dosya upload, hassas veri girişi.
- **Session/state yönetimi:** keep-alive, checkpoint, retry, timeout, screenshot/video/log, structured output (JSON/CSV), run ID.
- **Secret disiplini:** scoped credentials, domain allowlist, vault veya en azından agent'ın göremediği label/value mekanizması.
- **Anti-bot altyapısı:** full browser, residential proxy gerektiğinde, headless/full-browser fallback, captcha solver.
- **Evaluator/verifier:** beklenen alanlar, veri doğruluğu, yanlış sayfaya submit olmama, değişen DOM'a karşı smoke check.
- **İç araç eşleşmesi zaten var:** `chrome-devtools-axi`, Playwright MCP, Chrome DevTools MCP ve `windows-mcp` mevcut. Yani sıfırdan browser automation stack kurmak gerekmiyor; asıl iş workflow standardı ve güvenlik katmanı.
- **Vendor seçimi role göre yapılmalı:** keşif için Browser Use/Skyvern; derleme ve tekrar eden run için Stagehand/Playwright/agent-browser; lokal insan kontrolü gereken noktada mevcut MCP/browser araçları.
- **Maliyet guardrail'i şart:** step, session hour, proxy GB, captcha, token ve insan müdahalesi metriği ayrı ayrı tutulmalı. Yoksa browser agent faturası sinsice şişer.

## Ham Notlar
- `ddgr` bu turda sistematik biçimde `HTTP 202` verip boş döndü. Adımı atlamadım; araç bozulduğu için fallback yaptım.
- Product Hunt'ın Jina fetch'i CAPTCHA uyarısı verdi; ama Product Hunt index sayfaları web tarafında okunabildiği için sinyal kaybı yaşanmadı.
- MCPTube tarafında en değerli sinyal şu oldu: Browser Use demosu açıkça proxy, secrets, take-control ve 10 dakikalık session ömrü anlatıyor; Stagehand videosu ise “CDP tabanlı daha hızlı çekirdek + deterministic workflow” vurgusu yapıyor. Bu ikisi aynı ürünü değil, farklı lane'leri işaret ediyor.
- Net hüküm: **Her işi canlı exploratory browser agent'a bırakmak aptalca pahalı ve kırılgan.** Keşif modunu bir kez kullanıp sonra compile edilmiş deterministic akışa geçmek daha akıllı yol.
