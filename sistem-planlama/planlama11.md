# Planlama #11 — Workflow Template Marketplace Uygulama Haritası
**Tarih:** 2026-04-21 09:14 +03
**Bağlı Araştırma:** arastirma11.md

## Swarm Agent ile Nasıl Uygulanır?
UniverseCreator için doğru tasarım **Workflow Template Foundry**: ham template pazarı değil, “bul → test et → iyileştir → paketle → outcome olarak sat → bakımını yap” hattı.

Önerilen mimari:
1. **Template Opportunity Scanner**
   - Giriş: n8nworkflows, n8n resmi templates, Make/Zapier templates, Reddit trendleri, GitHub repos, önceki `arastirma*.md`.
   - Çıkış: vertical template adayları: lead follow-up, support triage, content repurpose, meeting-to-CRM, weekly research report.
2. **Template QA Agent**
   - JSON parse, node listesi, credential placeholder, deprecated node, dangerous node, public webhook risk, version compatibility kontrolü.
   - “Import olur mu?” değil; “kurulunca gerçek kullanıcı bunu çalıştırabilir mi?” sorusuna cevap verir.
3. **Outcome Packager**
   - Template’i tekil JSON olarak değil, mini ürün olarak paketler:
     - workflow JSON
     - install guide
     - credential checklist
     - test data
     - demo video/screenshot
     - troubleshooting
     - ROI/usage claim
4. **Vertical Offer Designer**
   - Aynı template’i sektör/sonuç diliyle satar:
     - “n8n Gmail workflow” değil: “Missed lead follow-up autopilot”.
     - “RSS → social post” değil: “Weekly content repurposing system”.
5. **Distribution Agent**
   - Reddit/IndieHackers/GitHub/Neura/Gumroad/LemonSqueezy/Product Hunt alternatiflerini tarar.
   - İlk aşamada direct satış + case study; marketplace sadece distribution/backlink.
6. **Deployment / Maintenance Lane**
   - Paid customer’da setup support ve monthly maintenance retainer.
   - Template kırılırsa patch; API/provider fiyatı değişirse uyarı; execution hataları raporlanır.
7. **Learning Loop**
   - Support soruları → doküman güncellemesi.
   - En çok sorun çıkaran node → template kalite skoru düşer.
   - En çok kurulan template → high-ticket managed package’e evrilir.

## Gerekli Bileşenler
- **Script/Bot:**
  - template source scanner
  - n8n JSON validator / node inventory extractor
  - credential requirement extractor
  - QA checklist generator
  - install guide generator
  - demo data generator
  - pricing/ROI calculator
  - support issue logger
  - update/version monitor
- **MCP/Araç:**
  - `czlonkowski/n8n-mcp` ve `n8n-skills` yaklaşımı: workflow üretim/analiz yardımcısı
  - Jina/curl: docs, marketplace, Gumroad, Reddit okuma
  - GitHub CLI/API: repo/template kaynakları
  - Reddit JSON: community pain ve pricing sinyali
  - MCPTube: tutorial/transcript extraction
  - Playwright/chrome-devtools-axi: n8n/Make/Zapier UI doğrulama, gerektiğinde ekran kanıtı
- **API:**
  - n8n Cloud veya self-host n8n
  - Make API / scenario templates
  - Zapier templates / Zapier Tables/Forms/Agents stack
  - OpenAI/Anthropic/Gemini/OpenRouter gibi LLM provider’lar
  - Google Sheets/Drive, Slack, Gmail, HubSpot/Pipedrive, Airtable/Notion gibi sık connector’lar
  - ödeme: LemonSqueezy/Gumroad/Neura/iyzico uygun olan kanal
- **İnsan Müdahalesi:**
  - ilk vertical seçimi
  - template lisans/ownership kararı
  - müşteri credential bağlantıları
  - ilk 3 kurulumda canlı destek
  - refund/support sınırı ve fiyat onayı

## Workflow Haritası
Research signal
→ template adayı seçilir
→ JSON/source okunur
→ QA scan yapılır
→ risk/complexity skoru verilir
→ test workspace’te import/dry-run
→ credential checklist çıkarılır
→ vertical outcome copy yazılır
→ install guide + demo data + screenshot hazırlanır
→ landing / Gumroad / Neura draft
→ 10 hedef kullanıcıya veya community’ye gösterilir
→ feedback / satış / support sorusu toplanır
→ package revize edilir
→ maintenance retainer teklif edilir
→ başarılı olan package managed infra ürününe çıkarılır

Örnek ürün #1 — Lead Follow-up Kit:
Webhook/form/Google Sheet lead
→ lead score + enrichment optional
→ Gmail/Slack notification
→ 3-step follow-up sequence
→ CRM row update
→ weekly lead report
→ fiyat: $49 template / $300 setup / $200-$500 monthly maintenance

Örnek ürün #2 — Weekly Reddit Opportunity Report Kit:
10 subreddit
→ pain/frustration post scan
→ LLM clustering
→ Google Sheet + email digest
→ product/opportunity score
→ fiyat: $29 template / $99-$199 managed report

Örnek ürün #3 — Content Repurposing Kit:
YouTube/RSS/blog input
→ platform-specific post drafts
→ approval queue
→ scheduler/Sheets tracking
→ weekly performance report
→ fiyat: $79 template / $500 setup / $300-$1,000 monthly retainer

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne HEMEN hayata geçirilebilir?**

- **Hemen yapılacak şey:** marketplace kurmaya kalkma. Bu aşamada marketplace inşa etmek gereksiz şişmanlık. İlk 1-2 haftada **tek vertical, tek çalışan paid kit** çıkarılmalı.
- **En düşük çaba / en yüksek çıktı adımı:** n8n/Make tabanlı **Weekly Reddit Opportunity Report Kit** veya **Lead Follow-up Kit**. UniverseCreator zaten Reddit JSON, Jina, araştırma ve rapor yazma kasına sahip.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - `ARASTIRMA_MODU` araştırma döngüsü
  - Reddit JSON komutları
  - Jina/curl
  - GitHub/MCPTube/arXiv araştırma akışı
  - mevcut product/health/report deneyimi
  - `projeler.txt` içindeki n8n-mcp / n8n-skills / workflow kaynakları
- **Proof-of-concept minimum gereksinimler:**
  - 1 workflow JSON veya pseudo-workflow tasarımı
  - 1 install guide
  - 1 demo output PDF/Markdown/Sheet
  - credential checklist
  - 5 dakikalık Loom/ekran görüntüsü veya metin demo
  - fiyat sayfası: template + setup + maintenance
  - 10 kişilik hedef alıcı listesi
- **Tahmini kurulum süresi:**
  - Araştırma + template seçimi: **1 gün**
  - QA + dokümantasyon: **1-2 gün**
  - demo çıktı + landing: **1-2 gün**
  - ilk outreach/community test: **2-5 gün**
- **İlk gelir beklentisi:**
  - Tek template satışında gerçekçi: **$0-$100**.
  - Setup + support ile gerçekçi: **$300-$1,000** ilk müşteri.
  - Maintenance ile ilk ay hedef: **$200-$500 MRR**.
- **Kısa vade hükmü:** “8,000 template satayım” fikri kötü. “1 tane çalıştığı kanıtlı, kurulumlu, niş outcome paketi satayım” doğru.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: Sistem nasıl olgunlaşır?**

- **1. ay sonunda sistem nasıl görünmeli?**
  - 3 tested vertical kit:
    1. Lead Follow-up Kit
    2. Weekly Opportunity Report Kit
    3. Content Repurposing Kit
  - Her kit için QA skoru, install guide, demo output, pricing, support sınırı.
  - En az 20 kişiyle feedback / 3-5 ciddi satış konuşması / 1 paid setup hedefi.
- **2-3 ay sonunda:**
  - 10 kaliteli template kit; her biri aynı standarda sahip.
  - Basit catalog: kategori, platform, fiyat, kurulum süresi, gereken credential’lar, demo output.
  - Paid support/retainer pipeline.
  - Neura/Gumroad/LemonSqueezy gibi dış distribution kanallarında test.
- **Hangi metric’ler başarıyı gösterir?**
  - template page views
  - demo download rate
  - install success rate
  - support minutes per install
  - paid conversion
  - refund rate
  - setup-to-retainer conversion
  - monthly recurring maintenance revenue
  - template breakage count
  - time-to-first-successful-run
- **Hangi adımlar paralel çalışabilir?**
  - source/template scouting
  - QA validator checklist
  - vertical copy/pricing
  - docs/demo creation
  - outreach list
  - platform listing
  - support FAQ
- **Ölçeklendirme için ne gerekiyor?**
  - reusable QA checklist
  - standard doc template
  - credential wizard/checklist
  - update/version monitor
  - customer issue log
  - legal/license review
  - small self-host n8n sandbox
  - payment + delivery automation
- **Checkpoint’ler ve başarı kriterleri:**
  1. Hafta 1: 1 packaged kit + demo + price
  2. Hafta 2: 10 kullanıcı/aday müşteri feedback
  3. Hafta 4: 1 paid setup veya net pivot
  4. Hafta 8: 3 paid kits veya 1 retainer
  5. Hafta 12: 10 kit catalog + 3 retainers veya high-ticket managed offer pivot

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator bir **AI Workflow Systems Studio** olur. Template catalog sadece frontend; arka tarafta QA, deployment, monitoring, support ve vertical outcome engine çalışır.
- **Evrim yolu:**
  1. Tek paid kit
  2. 3-kit mini catalog
  3. Setup + maintenance retainer
  4. White-label dashboard
  5. Client-specific deployment automation
  6. n8n custom template host / internal library API
  7. Agent-generated workflow + automatic QA
  8. Full marketplace ancak kalite standardı oturduktan sonra
- **Hangi yan ürünler / gelir kolları çıkabilir?**
  - $29-$99 template kits
  - $300-$1,500 setup packages
  - $200-$1,000/ay maintenance retainers
  - $1,500-$10,000/ay managed AI infrastructure
  - n8n/Make/Zapier audit service
  - “broken workflow repair” service
  - white-label automation portal
  - vertical SOP + workflow bundles
  - n8n credential/security checklist product
- **Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek nedir?**
  - Reddit/GitHub/YouTube/docs sinyaliyle hangi workflow talep görüyor hızlı bulunur.
  - Codex template QA/doküman standardını uygular.
  - Browser tools gerçek import/setup ekranını doğrular.
  - Research agent fiyat ve community reaksiyonunu sürekli ölçer.
  - Analyst hangi kitin support yükü/revenue oranı iyi görüyor.
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet; ama ilk gün SaaS değil.
  - 3 ay: “managed workflow kit + client portal” white-label olarak satılabilir.
  - 6 ay: en çok tekrarlanan kit, küçük dashboard/SaaS’a çevrilebilir.
  - 12 ay: kendi template catalog + QA badge + installer + support subscription.
- **Uzun vade ana fikir:** statik marketplace değil, **workflow reliability layer**. Alıcı “workflow dosyası” değil, “bu iş her hafta çalışıyor” satın alır.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** ilk kit **5-10 gün**, 3 kit catalog **3-5 hafta**, 10 kit + retainer sistemi **2-3 ay**
- **Aylık İşletme Maliyeti:**
  - n8n Cloud Starter: **€20/ay**, 2,500 execution, 5 concurrent execution
  - n8n Pro: **€50/ay** başlangıç bandı
  - self-host VPS: yaklaşık **$5-$25/ay** düşük başlangıç, ama bakım/security yükü var
  - Make Core: **$9/ay** / 10K credits; Pro **$16/ay**; Teams **$29/ay**
  - Zapier Pro: **$19.99/ay** / 750 tasks; Team **$69/ay**
  - Activepieces: free/standard modelde 10 free active flows, sonra **$5/active flow/month** iddiası
  - LLM/API maliyeti: **$10-$100/ay** başlangıç; usage’a bağlı artar
- **Potansiyel Gelir:**
  - one-off kit: **$29-$99**
  - premium bundle: **$99-$299**
  - setup: **$300-$1,500**
  - maintenance: **$200-$1,000/ay**
  - managed infra: **$1,500-$10,000/ay**
- **ROI Beklentisi:**
  - Low-cost kit tek başına zayıf; 10 satış bile support yükü yaratabilir.
  - Setup + retainer ile 1 müşteri maliyeti kapatır.
  - Break-even hedefi: ilk paid setup veya 2-3 maintenance müşteri.

## Mevcut Sistemle Entegrasyon
- Araştırma/planlama döngüsü her konu sonunda “workflow kit’e dönüşür mü?” sorusunu ekleyebilir.
- Mevcut ürün portföyündeki health/checkout/report scriptleri template kit için demo olabilir: “Vercel product health monitor”, “checkout evidence reporter”, “weekly product status digest”.
- Önceki araştırmalardan doğal kit adayları:
  - Lead Generation Automation → lead scrape/enrich/follow-up kit
  - Content Factory + SEO → content repurpose/schedule kit
  - Local Business Automation → missed-call / review / booking follow-up kit
  - Browser Agent → portal QA / checkout proof kit
  - Micro-SaaS API → API usage/report kit
- Swarm rolleri:
  - Research: pazar + template kaynakları
  - Codex: QA checklist + docs + packaging
  - Browser automation: import/setup doğrulama
  - Analyst: pricing/revenue/support hesabı
  - Operator: müşteri demo/support handoff

## Riskler & Dikkat Edilecekler
- **Race to bottom:** 4,000 template $4.99 ise ham bundle satmak zaman kaybı.
- **Broken templates:** eksik node, eski version, credential karmaşası, community node bağımlılığı.
- **Security:** API key leakage, public webhook, execution log’da PII, self-host patching.
- **License/ownership:** official/community template’i aynen yeniden satmak riskli. Kendi modifikasyon, attribution, lisans kontrolü şart.
- **Support yükü:** low-ticket ürün support’u kârlılığı yer. Support sınırı net yazılmalı.
- **Platform drift:** n8n/Make/Zapier node veya pricing değişince workflow kırılır.
- **Fake revenue stories:** Reddit/YouTube gelir rakamları self-report; karar verirken “kanıtlanmış gelir” değil, hipotez sinyali sayılmalı.
- **Marketplace dependency:** Neura/Gumroad/ProductHunt discovery verir ama customer ownership zayıf kalabilir.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek vertical seç:** “Weekly Reddit Opportunity Report Kit” veya “Lead Follow-up Kit”. İkisini aynı anda yapma; o klasik scope bataklığı.
2. **Package spec yaz:** workflow adımları, input/output, credential checklist, demo output, QA checklist, fiyat: template/setup/retainer.
3. **10 kişilik feedback listesi çıkar:** n8n/automation/SideProject/agency community’den hedef alıcı; satış değil önce “bunu kurar mıydın, neye para verirdin?” doğrulaması.
