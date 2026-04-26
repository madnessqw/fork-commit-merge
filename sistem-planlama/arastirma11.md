# Araştırma #11 — Workflow Template Marketplace
**Tarih:** 2026-04-21 09:14 +03
**Konu:** n8n / Make / Zapier workflow template satışı, marketplace ekonomisi, template kütüphanesi, kalite/QA boşluğu ve swarm ile ürünleştirme.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma10.md` / `planlama10.md` formatı.
- `projeler.txt` sinyalleri: `n8n-openai-bridge`, `czlonkowski/n8n-mcp`, `czlonkowski/n8n-skills`, `nusquama/n8nworkflows.xyz`, `vercel/workflow`, Flowise, browser/automation workflow projeleri.
- ddgr: komut çalıştırıldı ama bu ortamda sonuç boş döndü; kaynak keşfi web/Jina/Reddit/GitHub fallback ile tamamlandı.
- n8n resmi pricing: https://n8n.io/pricing/
- n8n resmi workflow templates: https://n8n.io/workflows/
- n8n template docs / custom library API: https://docs.n8n.io/workflows/templates/
- n8nworkflows catalog: https://n8nworkflows.xyz/ , GitHub: https://github.com/nusquama/n8nworkflows.xyz
- Neura Market: https://www.neura.market/
- Make templates/pricing: https://www.make.com/en/templates , https://www.make.com/en/pricing
- Zapier templates/pricing blog: https://zapier.com/templates , https://zapier.com/blog/zapier-pricing
- Activepieces pricing/GitHub: https://www.activepieces.com/pricing , https://github.com/activepieces/activepieces
- Gumroad examples: https://dzdigitals.gumroad.com/l/n8n-templates , https://aipromptsworld.gumroad.com/l/6000-n8n-workflow-automation-template , https://openworksheet.gumroad.com/l/2000-n8nAIWorkflowInstantNo-CodeAutomations
- Reddit JSON: https://reddit.com/r/n8n/comments/1qci0g7/ , https://reddit.com/r/n8n/comments/1owt1z5/ , https://reddit.com/r/n8n/comments/1ltsocy/ , https://reddit.com/r/automation/comments/1neplv2/ , https://reddit.com/r/zapier/comments/1ovhrhz/ , https://reddit.com/r/n8n_ai_agents/comments/1s0wt7c/ , https://reddit.com/r/automation/comments/1m2zx4f/ , https://reddit.com/r/SideProject/comments/1pm8yxr/
- GitHub snapshot: `n8n-io/n8n`, `czlonkowski/n8n-mcp`, `czlonkowski/n8n-skills`, `nusquama/n8nworkflows.xyz`, `ritik-prog/n8n-automation-templates-5000`, `harshit-exe/FlowKit`, `activepieces/activepieces`, `huginn/huginn`.
- ArXiv: https://arxiv.org/abs/2506.10991 , https://arxiv.org/abs/2001.03543
- MCPTube / YouTube: https://www.youtube.com/watch?v=_ZpGQ8PpzaE , https://www.youtube.com/watch?v=GKCBpj9FQXU
- Market reports: https://www.grandviewresearch.com/industry-analysis/robotic-process-automation-rpa-market , https://www.globalgrowthinsights.com/market-reports/workflow-automation-market-120836

## Özet Bulgular
- **Template pazarı var ama ham JSON pazarı çöplüğe dönmüş durumda.** n8n resmi sayfası **9,297 workflow automation template** gösteriyor; n8nworkflows.xyz ise 2026-04-14 güncellemesiyle **9,514 workflow**, bunun **8,347 free / 1,167 paid** olduğunu listeliyor. Bu arz bolluğu iyi haber değil: tekil template satışı commodity.
- **Para ham template’te değil, “çalışan outcome paketi + kurulum + bakım + dashboard” tarafında.** Reddit ve MCPTube sinyali aynı yere çıkıyor: $15 JSON dosyası yarışında marj yok; müşterinin ödediği şey follow-up kaçmasın, lead aksın, içerik çıksın, rapor gelsin. Community’de açıkça “$200/ay follow-up derdi yaşamamak için ödenir” çizgisi var.
- **Marketplace boşluğu kalite/QA.** r/n8n’de 1,000+ template inceleyen post, çoğunun yarım, kırık, eksik node’lu veya bug’lı olduğunu söylüyor. n8nworkflows yorumlarında da template’lerin 1:1 değil, daha çok referans/inspiration olduğu vurgulanıyor. Buradaki fırsat: “tested, maintained, credential-safe, docs’lu, vertical kit”.
- **Mevcut platformlar template discovery’yi büyütüyor.** Make resmi template library **8,167 sonuç** gösteriyor. Zapier kendi template sayfasında AI agents, forms, zaps, tables, CRM, HR, lead, content gibi yüzlerce çözüm listeliyor. Neura Market kendi iddiasına göre **5,000+ workflow**, platform kırılımında **2,100 n8n + 1,800 Make + 1,500 Zapier + 600 Pipedream + 400 Activepieces** ve satıcıya **%90** gelir payı sunuyor.
- **AI workflow builder dalgası templates’i öldürmüyor, template’in rolünü değiştiriyor.** n8n docs “creator program” ve template marketplace’in geliştirilmekte olduğunu söylüyor; n8n-mcp ve n8n-skills GitHub traction’ı AI ile workflow üretiminin büyüdüğünü gösteriyor. Bu, statik template yerine “template + skill + validator + deployment guide” paketini değerli yapıyor.

## Gerçek Başarı Hikayeleri
- **n8nworkflows.xyz — discovery/aggregation ürünü.** Site 2026-04-14 itibarıyla **9,514 workflow** gösteriyor; GitHub repo snapshot’ı **2,294★ / 603 fork**. r/n8n post’u **491 score / 40 comments** seviyesinde ilgi aldı. En değerli yorumlar template’lerin doğrudan kopya değil, başkalarının problem çözme yaklaşımını görmek için iyi referans olduğunu söylüyor. Bu, “workflow search + categorization + quality layer” talebini doğruluyor.
- **Neura Market — çok-platformlu paid marketplace iddiası.** Site “5,000+ prebuilt workflows”, “sell workflows, blueprints, agents”, “keep 90% of sales” diyor. Rakamlar platformun kendi marketing iddiası; bağımsız doğrulama yok. Yine de model açık: tek template değil, workflow + blueprint + agent + SOP paketleri.
- **Gumroad bundle ekonomisi — race to bottom kanıtı.** Canlı Gumroad sayfasında **4,000+ n8n automation templates** paketi **$4.99** görünüyor; başka Gumroad sonuçlarında **2,000 template $35**, **6,000 template $19.99**, **80 sales workflows $17.99** gibi fiyatlar var. Bu, ham JSON dosyasının fiyat çıpasını aşağı çekiyor. “Bir template yapıp pasif gelir” fikri zayıf; iyi satış için niş outcome ve güven gerekiyor.
- **FlowKit — hızlı adoption, sıfır monetizasyon.** r/SideProject postunda FlowKit 7 günde **1,000+ user**, **4,000+ downloads**, **$0 revenue**, **$0 cost** anlattı. Bu güzel bir top-of-funnel göstergesi: ücretsiz curated library büyür; paraya çevirmek için premium install/support/vertical kit gerekir.
- **n8n template video — zaman tasarrufu ve $500/ay algısı.** MCPTube `_ZpGQ8PpzaE` videosunda binlerce template’in tek tık import edilebildiği, bazı karmaşık otomasyonlar için insanların **$500+/ay** ücret aldığı iddia ediliyor. Aynı videoda n8n cloud starter **€20/ay**, **2,500 execution**, **5 concurrent execution** olarak anlatılıyor; self-host seçeneği maliyet avantajı veriyor. Bu claim creator self-report; yine de alıcının gördüğü value prop “bir gün sürecek workflow’u dakikaya indirmek”.
- **AI infrastructure video — high-ticket model.** MCPTube `GKCBpj9FQXU` videosu ham n8n workflow satmak yerine “AI infrastructure + frontend dashboard + white-glove experience” satmayı savunuyor. Self-report’a göre hedef müşteri **25-50+ headcount** veya **$100K+/ay recurring revenue** olan şirket; teklif **2 haftada launch**, custom dashboard, sonuç bazlı anlatım; fiyat **$5K-$10K/ay** bandına çıkabiliyor. Bu, template marketplace’in üst segment yolu: template → managed system → infra retainer.
- **Reddit monetization tavsiyesi — recurring bakım.** r/n8n_ai_agents postunda community sinyali net: tek seferlik template satışı fiyat kırar; asıl para aynı sistemi aynı nişte 10 müşteriye bakım/optimizasyonla satmak. r/automation postunda da ilk müşteri için ücretsiz case study, sonra outcome-based monthly retainer öneriliyor.

## Pazar Büyüklüğü & Fırsat
- **Automation TAM büyüyor ama burada TAM satmıyoruz.** Grand View Research, RPA pazarını **2025’te $4.68B**, **2033’te $35.84B**, **%29 CAGR** olarak tahmin ediyor. GlobalGrowthInsights ise workflow automation market için **2024 $7.89B**, **2025 $8.95B**, **2034 $27.75B**, **%13.4 CAGR** veriyor. Raporlar arası fark büyük; bu yüzden TAM’i karar değil, talep yönü sinyali olarak kullanmak lazım.
- **Platformların template inventory’si çok büyük:** n8n **9K+**, Make **8K+**, Neura **5K+**, Zapier yüzlerce/ binlerce solution template. Bu pazarın commodity tarafı doygun; fakat aynı doygunluk iyi bir arama/QA/kurulum layer’ı için veri havuzu demek.
- **Satıcı için en iyi fiyat çıpası iki katmanlı:**
  - Low-ticket: $19-$99 tek seferlik vertical kit / mini bundle.
  - Mid-ticket: $200-$500/ay bakım + küçük özelleştirme.
  - High-ticket: $1.5K-$10K/ay outcome + dashboard + managed infra.
- **En iyi ilk vertical’lar:** lead capture/follow-up, content repurposing, support inbox triage, meeting/call summary → CRM, weekly market/reddit opportunity reports, product/checkout monitoring. Bunlar UniverseCreator’ın önceki araştırmaları ve mevcut product health mantığıyla uyumlu.
- **AI agent trendi template değerini artırabilir:** n8nworkflows node sayımında `agent` **3,251**, `lmChatOpenAi` **2,301**, `outputParserStructured` **1,589**, `mcpTrigger` **313**, `mcpClientTool` **129** görünüyor. AI/MCP nodes artık niche değil; template marketplace agent-compatible olmak zorunda.

## Rakipler & Boşluklar
- **n8n resmi template library:** Güçlü dağıtım, creator hub, community. Boşluk: kalite garantisi, bakım SLA’sı, vertical outcome packaging, installation support.
- **n8nworkflows.xyz:** Büyük searchable catalog, ücretsiz/paid filtre, node bazlı istatistikler. Boşluk: güven/QA/“bu çalışıyor mu?” katmanı, credential guide, version compatibility.
- **Make/Zapier official templates:** Devasa discovery ve güven. Boşluk: çok genel; müşteri “benim sektörümde hemen çalışan paket” istiyor. Ayrıca platform içi template çoğu zaman full service değil.
- **Neura Market:** Paid marketplace pozisyonlaması iyi; workflow/agent/blueprint kombinasyonu doğru yönde. Boşluk: kalite sinyali, gerçek satış verisi ve bağımsız başarı hikayesi belirsiz.
- **Gumroad bundle seller’ları:** Fiyat çok düşük, hacim iddiası yüksek. Boşluk: güven, güncellik, kurulum, support, API key güvenliği, lisans/ownership netliği.
- **n8n-mcp / n8n-skills:** AI ile workflow üretimi için güçlü araçlar; `czlonkowski/n8n-mcp` **18,525★**, `n8n-skills` **4,501★**. Boşluk: bunlar marketplace değil, builder tooling. UniverseCreator burada “AI-generated workflow QA + packaged kits” layer’ı kurabilir.
- **Activepieces/Huginn/open-source alternatives:** Activepieces **21,795★**, Huginn **49,151★**. Boşluk: multi-platform template portability ve client deployment playbook.

## Teknik Gereksinimler
- **Template inventory layer:** Kaynak, platform, kategori, node listesi, son güncelleme, complexity, credential ihtiyacı, paid/free, lisans, author, import URL.
- **QA harness:** JSON parse, node existence check, deprecated node check, credential placeholders, dangerous node scan, webhook/form exposure scan, minimum dry-run/sandbox test.
- **Credential abstraction:** “OpenAI key”, “Google Sheets OAuth”, “Slack bot token” gibi gereksinimleri açık wizard’a çevirmek; secret asla template dosyasına gömülmemeli.
- **Version compatibility:** n8n version, node version, community node install listesi, Make/Zapier plan gereksinimleri.
- **Outcome packaging:** Her template için “hangi işi çözer, kim alır, kaç dakika/saat kazandırır, output örneği ne, kurulum ne kadar sürer?” alanları.
- **Documentation:** 1 sayfa install guide, screenshot/GIF, test checklist, rollback, known limitations, troubleshooting.
- **Support model:** Free template = no support; paid kit = 7 gün install support; retainer = bakım + güncelleme + metric raporu.
- **Marketplace / storefront:** İlk aşamada Gumroad/LemonSqueezy/Neura gibi dış ödeme; sonra kendi catalog. Kendi catalog için search/filter, download, license, update notifications.
- **Security:** Public webhook riskleri, exposed credentials, untrusted community nodes, self-host n8n patching, execution logs’ta PII/secret leakage.
- **Swarm QA:** Research agent template bulur; Codex JSON/doküman/QA planını çıkarır; Browser/Playwright kurulum ekranlarını doğrular; analyst fiyat/ROI hesaplar.

## Ham Notlar
- ddgr komutları çalıştı ama JSON sonuç üretmedi. Boş sonucu “kaynak yok” diye yorumlamak aptalca olurdu; web/Jina fallback kullanıldı.
- ProductHunt Jina araması CAPTCHA uyarısında kaldı; bu turda ProductHunt’tan güvenilir sinyal çıkarılmadı.
- GitHub CLI JSON alanı `stargazerCount` değil `stargazersCount`; ilk parse boştu, düzeltildi.
- MCPTube `parallel_add.py` 5 video için başarı döndürdü ama kütüphanede yalnız bazıları göründü; `_ZpGQ8PpzaE` MCP ile tekil eklendi ve transcript okundu.
- Neura Market ve Gumroad rakamları satıcı/platform iddiası; bağımsız gelir kanıtı değil. Araştırmada “kanıtlanmış revenue” diye değil, pazar davranışı ve fiyat çıpası diye kullanılmalı.
- Net hüküm: **UniverseCreator workflow template marketplace’e “binlerce JSON satıcı” olarak girmemeli. İlk wedge: tested vertical workflow kits + setup docs + maintenance retainer. Marketplace sonradan gelir; önce güven ve outcome.**
