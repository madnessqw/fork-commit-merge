# Planlama #25 — Workflow Template Marketplace Uygulama Haritası
**Tarih:** 2026-04-21 19:55 +03
**Bağlı Araştırma:** arastirma25.md

## Swarm Agent ile Nasıl Uygulanır?
Doğru ürün adı: **Workflow QA Foundry**.

Yanlış yol: “Binlerce n8n/Make/Zapier template’i scrape edip marketplace açalım.” Bu artık kalabalık ve güven problemi kokuyor. Daha akıllı yol: **template keşfi → lisans/attribution kontrolü → teknik QA → sandbox dry-run → vertical outcome paketi → kurulum desteği → bakım retainer**.

Mimari:
1. **Signal Scout**
   - n8n API, n8nworkflows, Make templates, Zapier templates, Reddit, GitHub ve mevcut `projeler.txt` tarar.
   - Çıktı: “lead follow-up”, “content repurpose”, “support triage”, “weekly research digest” gibi outcome adayları.
2. **License & Attribution Gate**
   - Original author, source URL, license, resale permission, platform ToS riski kontrol edilir.
   - Scrape edilmiş workflow’u attribution silerek satmak yok. O yol kısa ve aptalca.
3. **Template QA Agent**
   - JSON parse, node inventory, credential list, deprecated/community node, exposed secret, public webhook, plan/usage requirement, setup complexity skoru.
4. **Sandbox Runner**
   - Mock credentials + test data ile import/dry-run yapar.
   - “First successful run” kanıtı yoksa paid kit olmaz.
5. **Outcome Packager**
   - Workflow dosyası + install guide + credential checklist + test data + screenshot/GIF + troubleshooting + ROI calculator.
6. **Offer Builder**
   - Teknik isim değil, müşteri sonucu satar:
     - “Facebook Lead Ads → Gmail” değil: “5 dakikada ilk lead yanıtı”.
     - “RSS → LinkedIn post” değil: “haftalık content repurposing sistemi”.
7. **Sales/Support Lane**
   - Low-ticket template, setup paketi ve monthly maintenance ayrı fiyatlanır.
8. **Learning Loop**
   - Support soruları docs’a döner; kırılan node template skorunu düşürür; en çok talep gören kit managed infra’ya yükselir.

## Gerekli Bileşenler
- **Script/Bot:**
  - n8n API scanner (`totalWorkflows`, search query, purchaseUrl, views, category)
  - Make/Zapier template scraper/Jina reader
  - GitHub repo vetter: stars, forks, pushedAt, issues, license
  - Reddit pain/pricing scanner
  - n8n JSON node inventory + credential extractor
  - secret/public webhook scanner
  - template risk scorer
  - install guide generator
  - demo output generator
  - support/feedback logger
- **MCP/Araç:**
  - `gh-axi` / `gh` GitHub doğrulama
  - Jina/curl web okuma
  - Reddit JSON API
  - MCPTube transcript
  - ArXiv MCP
  - Playwright / chrome-devtools-axi: gerektiğinde marketplace veya template UI görsel doğrulama
  - İleri aşamada `czlonkowski/n8n-mcp` ve `n8n-skills` yaklaşımı
- **API:**
  - n8n API: `https://api.n8n.io/templates/search`
  - n8n self-host/cloud test instance
  - Google Sheets/Gmail/Slack/HubSpot/Airtable/OpenAI/Gemini gibi connector’lar
  - Make / Zapier hesapları sadece doğrulama ve demo için
  - ödeme: ilk aşamada Gumroad/LemonSqueezy/iyzico/Neura gibi dış kanal; kendi marketplace sonradan
- **İnsan Müdahalesi:**
  - lisans/attribution onayı
  - ilk 3 kit için vertical seçimi
  - fiyat ve refund sınırı
  - müşteri credential bağlantısı
  - satış metni ve demo onayı

## Workflow Haritası
n8n API / Reddit / GitHub signal
→ template adayı seçilir
→ original source + license kaydedilir
→ JSON/node/credential scan
→ risk skoru
→ sandbox import
→ mock data ile run
→ screenshot/GIF + demo output
→ vertical outcome copy
→ pricing ladder
→ 10 hedef kullanıcıya gösterim
→ ilk satış/setup
→ support soruları docs’a döner
→ kırılan template patch/version update
→ çalışan kit managed package’e çıkarılır

**Örnek Kit #1 — Lead Response Kit**
Facebook Lead Ads / form webhook
→ normalize + score
→ Google Sheets / CRM kayıt
→ Gmail/WhatsApp/Slack notification
→ 3-step follow-up
→ weekly lead report
→ fiyat: **$49 template / $300 setup / $200–$500 monthly maintenance**

**Örnek Kit #2 — Weekly Opportunity Report Kit**
subreddit/source list
→ pain posts scan
→ LLM clustering
→ opportunity score
→ Markdown/PDF/Sheet report
→ fiyat: **$29 template / $99 managed report / $300–$750 monthly niche monitoring**

**Örnek Kit #3 — Content Repurpose Kit**
RSS/YouTube/blog input
→ multi-platform post drafts
→ approval queue
→ scheduler/Sheet tracking
→ weekly content report
→ fiyat: **$79 template / $500 setup / $300–$1,000 monthly retainer**

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne HEMEN hayata geçirilebilir?**

- **Hemen yapılacak şey:** marketplace değil, **1 tane QA’lı vertical kit**. Marketplace şimdi yapılırsa dikkat dağıtır; en kötü ürünleşme refleksi bu olur.
- **En düşük çaba / en yüksek çıktı:** UniverseCreator’ın mevcut araştırma kasıyla **Weekly Opportunity Report Kit** veya **Lead Response Kit**.
- **Mevcut araç/script avantajı:**
  - `ARASTIRMA_MODU` zaten Reddit/Jina/GitHub/ArXiv/MCPTube tarıyor.
  - UniverseCreator zaten rapor formatı ve ürün health/audit disiplinine sahip.
  - `projeler.txt` içinde n8n-mcp, n8n-skills, n8nworkflows gibi kaynaklar var.
- **PoC minimum gereksinimler:**
  - 1 workflow/pseudo-workflow JSON veya n8n taslağı
  - 1 sample input + 1 sample output
  - credential checklist
  - import/setup guide
  - risk/QA checklist
  - 1 sayfa satış metni
  - 10 potansiyel alıcı listesi
- **Kurulum süresi:**
  - kaynak/template seçimi: **0.5–1 gün**
  - QA checklist + docs: **1–2 gün**
  - demo output + landing/satış sayfası: **1–2 gün**
  - outreach/community test: **3–5 gün**
- **İlk gelir beklentisi:**
  - ham template: **$0–$99** ve ağır commodity.
  - setup ile: **$300–$1,000** ilk müşteri daha gerçekçi.
  - maintenance: **$200–$500 MRR** ilk ay hedeflenebilir.
- **Bu hafta yapılacak en mantıklı PoC:** n8n API’den `lead`, `content`, `support` query’leriyle 30 template çıkar; 3 tanesini QA skorla; 1 tanesini vertical kit’e paketle.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: Sistem nasıl olgunlaşır?**

- **1. ay sonunda sistem görünümü:**
  - 3 QA’lı vertical kit: Lead Response, Weekly Opportunity Report, Content Repurpose.
  - Her kit için demo output, setup guide, credential list, risk score, fiyat sayfası.
  - 20 outreach / 5 call / 1 paid setup hedefi.
- **2-3 ay sonunda:**
  - 10 kitlik küçük catalog.
  - Her kit için install success rate ve support minutes ölçümü.
  - Basit “trusted workflow kits” landing.
  - Dış distribution: Neura / n8n Markets / Gumroad / Reddit / GitHub repo.
  - 2 managed retainer müşteri hedefi.
- **Başarı metric’leri:**
  - first successful run time
  - install success rate
  - support minutes/install
  - demo download → paid conversion
  - refund rate
  - activation rate
  - monthly template breakage
  - setup-to-retainer conversion
  - monthly recurring maintenance revenue
- **Paralel çalışabilecek adımlar:**
  - source scanner
  - QA scanner
  - docs template
  - sales copy
  - pricing ladder
  - outreach list
  - sandbox instance
  - demo output gallery
- **Ölçeklendirme gereksinimi:**
  - reusable QA schema
  - n8n sandbox otomasyonu
  - connector credential playbook
  - license/attribution policy
  - support issue taxonomy
  - version update monitor

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** Workflow QA Foundry, public template çöplüğünü alır ve “çalıştığı kanıtlı business automation kitleri”ne çevirir. Template marketplace değil, **automation trust layer** olur.
- **Yan ürünler:**
  - Workflow QA score API
  - n8n template compatibility scanner
  - credential wizard generator
  - vertical workflow catalog
  - managed n8n hosting/setup service
  - “workflow insurance” / maintenance retainer
  - internal company template library for teams
- **Swarm farkı:** Rakipler template listeler; UniverseCreator swarm template’i test eder, belgeler, riskini çıkarır, vertical offer’a çevirir ve bakım döngüsünü tutar. İşte burada para var.
- **White-label/SaaS potansiyeli:**
  - Ajanslara white-label “tested workflow kit library”.
  - n8n consultants için QA badge / validator.
  - KOBİ’lere managed monthly automation ops.
  - İleri aşamada SaaS: “Upload workflow → risk score + docs + credential checklist + demo test”.
- **Uzun vade gelir modeli:**
  - Low-ticket catalog: **$19–$99**
  - Setup: **$300–$1,500**
  - Retainer: **$200–$1,000/ay** küçük müşteriler
  - Managed infra/dashboard: **$1.5K–$10K/ay** mid-market
  - QA API/SaaS: **$29–$199/ay** builder/agency segmenti

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek, ama marketplace olarak değil; QA’lı vertical kit olarak.
- **Kurulum Süresi:** PoC **5–7 gün**, ilk 3 kit **3–4 hafta**, retainer lane **6–10 hafta**.
- **Aylık İşletme Maliyeti:**
  - n8n self-host/VPS: **$5–$30**
  - n8n Cloud opsiyon: **$20–$50+**
  - Make test: **$9–$29+**
  - Zapier test: **$19.99–$69+**
  - LLM/API/misc: **$20–$100** başlangıç
  - toplam PoC: **$50–$200/ay**
- **Potansiyel Gelir:**
  - 1. ay: **$300–$1,000** setup hedefi
  - 3. ay: **$1K–$3K MRR** bakım/setup karışık
  - 6-12 ay: **$5K–$15K MRR** eğer 10+ kit ve 5+ retainer yakalanırsa
- **ROI Beklentisi:** İlk paid setup ile break-even; tekil template satışına bel bağlanırsa ROI zayıf.

## Mevcut Sistemle Entegrasyon
- `universe_loop.sh` mantığına “research → QA → package → plan” lane’i eklenebilir ama bu turda kod yazılmayacak.
- `sistem-planlama` araştırmaları template vertical seçiminde veri kaynağı olur.
- 113+ ürün portföyü için de workflow kit çıkarılabilir:
  - product health monitor kit
  - checkout monitoring kit
  - SEO/content repurpose kit
  - support/lead response kit
- Mevcut Claude+Codex+GLM swarm rolleri:
  - Claude: offer/positioning/docs
  - Codex: JSON/risk/QA/checklist
  - GLM/analyst: fiyat, pazar, metric
  - Browser agent: kurulum ekranı/screenshot doğrulama

## Riskler & Dikkat Edilecekler
- **Attribution/lisans riski:** Public workflow’u indirip author silerek satmak çöp hamle. Kısa vadede hızlı görünür, uzun vadede güveni yakar.
- **Commodity risk:** 5,000 template bundle’lar bedava/ucuz; ham JSON için yüksek fiyat yok.
- **Support riski:** Müşteri credential bağlayamazsa template değil destek satıyorsun. Bunu fiyatlamazsan zarar.
- **Platform maliyeti:** Zapier task, Make credits, n8n executions/concurrency açık yazılmalı.
- **Security:** embedded token, public webhook, customer PII, execution logs, OAuth scope.
- **Quality drift:** n8n node güncellenir, template kırılır; version monitor şart.
- **Fake metric riski:** download/view sayılarını şişirmek yerine first successful run ve refund rate gösterilmeli.
- **Sales riski:** AI automation space’te “çok para kazanırsın” gürültüsü var. Müşteri workflow değil sonuç ve güven satın alır.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **n8n API scanner spec’i yaz:** `lead`, `content`, `support`, `crm`, `agent` sorguları için workflow count, views, purchaseUrl, verified creator, category çıkaran araştırma artefact’i tasarla.
2. **3 aday kit seç ve QA checklist uygula:** Lead Response, Weekly Opportunity Report, Content Repurpose. Her biri için credential, node, license, setup complexity, expected output yaz.
3. **Tek landing/demo paketi hazırla:** Ham marketplace değil; “Tested Workflow Kit + Setup Support + Maintenance” fiyat merdiveniyle 10 hedef kullanıcıya gösterilecek tek sayfa.
