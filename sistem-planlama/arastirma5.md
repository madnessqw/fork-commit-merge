# Araştırma #5 — White-label Otomasyon Ajansı
**Tarih:** 2026-04-21 05:15 +03
**Konu:** White-label otomasyon ajansı kurup aylık abonelikli hizmet satmak: hangi paketler, hangi tool stack, hangi vertical'lar, hangi müşteri edinme modeli?
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma0-4.md` / `planlama0-4.md`
- HighLevel Pricing & Billing: https://help.gohighlevel.com/support/solutions/articles/155000001156-highlevel-pricing-guide
- HighLevel AI Employee overview: https://help.gohighlevel.com/support/solutions/articles/155000003906-ai-employee-overview
- HighLevel AI product pricing update: https://help.gohighlevel.com/support/solutions/articles/155000006652-ai-product-pricing
- HighLevel Conversation AI pricing: https://help.gohighlevel.com/support/solutions/articles/155000001357-pricing-and-rebilling-conversation-ai
- HighLevel Workflow AI pricing: https://help.gohighlevel.com/support/solutions/articles/155000000169-how-to-enable-and-rebill-workflow-ai-
- n8n pricing: https://n8n.io/pricing
- Make pricing: https://www.make.com/en/pricing
- Make credits docs: https://help.make.com/introducing-credits-new-billing-unit-live-in-make
- Zapier pricing: https://zapier.com/pricing
- U.S. Chamber 2025 SMB AI report: https://www.uschamber.com/technology/artificial-intelligence/u-s-chambers-latest-empowering-small-business-report-shows-majority-of-businesses-in-all-50-states-are-embracing-ai
- SBA 2025 Small Business Profile PDF: https://advocacy.sba.gov/wp-content/uploads/2025/06/United_States_2025-State-Profile.pdf
- U.S. Census BTOS AI use among small businesses: https://www.census.gov/newsroom/blogs/research-matters/2024/12/ai-use-small-businesses.html
- Grand View Research — Marketing Automation: https://www.grandviewresearch.com/industry-analysis/marketing-automation-software-market
- Grand View Research — Robotic Process Automation: https://www.grandviewresearch.com/industry-analysis/robotic-process-automation-rpa-market
- Product Hunt AI Workflow Automation category: https://www.producthunt.com/categories/ai-workflow-automation
- Reddit r/gohighlevel: https://reddit.com/r/gohighlevel/comments/1ltmtwg/how_to_get_your_first_monthly_ghl_client_in_7/ , https://reddit.com/r/gohighlevel/comments/1sb9x13/ghl_has_completely_changed_my_business/ , https://reddit.com/r/gohighlevel/comments/1riynzm/what_services_justify_1000month_on_gohighlevel/ , https://reddit.com/r/gohighlevel/comments/1o17vir/i_learned_ai_automations_in_6_months_with_no_code/ , https://reddit.com/r/gohighlevel/comments/1id5l1w/white_label_saas_agency/
- Reddit r/Entrepreneur: https://reddit.com/r/Entrepreneur/comments/1rnfgee/the_real_ai_gold_rush_isnt_in_building_its_in/
- GitHub: https://github.com/FlowEngine-cloud/flowengine , https://github.com/nusquama/n8nworkflows.xyz , https://github.com/tosodo/Real-Estate-AI-Automation-N8N-AgencyTemplate
- ArXiv: https://arxiv.org/abs/2001.03543 , https://arxiv.org/abs/2407.04472 , https://arxiv.org/abs/2401.06801
- YouTube/MCPTube: https://www.youtube.com/watch?v=vjuGcWrOf1Q , https://www.youtube.com/watch?v=GKCBpj9FQXU , https://www.youtube.com/watch?v=r5yL8PW8Kyc

## Özet Bulgular
- Bu işin para kazanan versiyonu “n8n workflow satmak” değil, **sonuç + görünürlük + yönetilen hizmet** satmak. Toplam teklif; audit, kurulum, portal/dashboard, haftalık ROI raporu ve gerektiğinde usage-based faturalama olmalı. Ham workflow satan çok, beyaz eldiven deneyim satan az.
- HighLevel tarafında gerçek white-label marjı için kritik eşik **$497 Agency Pro**. Resmi pricing guide'a göre markup ile rebilling sadece bu planda açılıyor; $297 Unlimited plan maliyet geri alma için yeterli ama agresif marj/white-label oyununda eksik kalıyor.
- En temiz ilk müşteri profili mikro KOBİ değil; **geliri olan, lead kaçırma acısı yaşayan, ticket'ı yüksek, karar vericisi hızlı** işletmeler. Roofing/HVAC/home services ve beauty/med-aesthetics gibi vertical'lar topluluk örneklerinde tekrar tekrar çıkıyor.
- Müşteri edinmede en iyi pattern “genel AI danışmanlığı” değil; **vertical audit + bedava demo + düşük riskli pilot**. Chris Koerner'ın roofing testinde 96 teslim edilen SMS → 15 yanıt → 3 warm lead çıkması, volume-based cold outbound'ın kaba ama işe yarar olduğunu gösteriyor. Oran muhteşem değil, ama matematiği net.
- Tool pazarı hızla kalabalıklaşıyor. Product Hunt AI workflow automation kategorisinde Gumloop, Airtop, Trace gibi ürünler öne çıkıyor; GitHub'da n8nworkflows.xyz 2,294 star'a ulaşmış. Yani tool artık edge değil. Edge; template kütüphanesi, onboarding, raporlama, support ve doğru vertical seçimi.

## Gerçek Başarı Hikayeleri
- **Ethan Nelson / “AI infrastructure” yaklaşımı:** Videoda son 8 ayda **$80K+ automation systems** sattığını söylüyor ve tekil Make/n8n workflow satmanın acı verdiğini, dashboard + uygulama + görünürlük paketinin çok daha yüksek fiyatlandığını anlatıyor. Onun argümanı net: müşteri “100 node'lu workflow” değil, “çalışan sistem + görünür dashboard” istiyor. Bu creator beyanı; denetlenmiş finansal tablo değil.
- **Chris Koerner / roofing outreach deneyi:** 96 başarılı SMS tesliminden **15 yanıt** ve **3 warm lead** üretiyor; videonun sonunda bu matematikle $1,000/mo paket için yaklaşık 1,000 prospect'ten $10K MRR çıkarılabileceğini söylüyor. Bu da creator math; ama acquisition funnel'ı çıplak haliyle gösterdiği için değerli. Ayrıca niche seçiminde roofing'i, yüksek ticket ve yüksek pazarlama alışkanlığı nedeniyle tercih ediyor.
- **Andrew George / HighLevel voice AI paketleme:** Videoda 30 günlük deneme sonrası **$97/mo** taban fiyatın, usage markup ile birlikte çok daha kârlı hale geldiğini söylüyor. HighLevel voice maliyetinin yaklaşık **$0.13-$0.14/dk** bandında olduğunu, 1.5x–3x markup ve günde 3–5 çağrı ile aylık **$400-$500 profit/client** üretilebileceğini iddia ediyor. Bu da creator claim; ama resmi HighLevel pricing mantığıyla uyumlu.
- **Reddit r/gohighlevel — $1K+ paket sinyali:** “What services justify $1,000+/month on GoHighLevel?” thread'inde bir kullanıcı **full lead gen + ads + nurture + pipeline** için **$1.5K-$2.5K/mo** bandını normal buluyor; başka biri **AI calls + website + social + payments + pipeline** kombinasyonunu **$1,000/mo**'ya sattığını söylüyor. Tamamı self-report, ama çıplak tool değil paket sattıklarında fiyat yükseliyor.
- **Reddit r/gohighlevel — beauty / med-aesthetics örneği:** “GHL has completely changed my business” post'unda ads agency sahibi, lead teslim etmek yerine **ads → booking → nurture → conversion → retention** hattını kontrol etmeye başlayınca iş modelinin değiştiğini anlatıyor. Ders basit: sadece lead üretip kaçmak churn doğuruyor; kapanan geliri sahiplenmek retention yaratıyor.

## Pazar Büyüklüğü & Fırsat
- **Adreslenebilir müşteri tabanı çok büyük:** SBA 2025 profiline göre ABD'de **36.2 milyon** küçük işletme var; bunlar tüm işletmelerin **%99.9**'unu ve çalışanların **%45.9**'unu oluşturuyor. White-label otomasyon ajansı için müşteri havuzu “niş ama küçük” değil; devasa ama dağınık.
- **AI ilgisi yüksek, gerçek operasyon entegrasyonu hâlâ düşük-orta:** U.S. Chamber 2025 raporunda küçük işletmelerin **%58'i generative AI kullandığını**, **%96'sı emerging tech benimsemeyi planladığını** söylüyor. Ama Census BTOS verisi daha ayık bir resim gösteriyor: 2023–2024 döneminde 1–4 çalışanlı firmalarda AI use rate **%4.6 → %5.8**, 250+ çalışanlı firmalarda **%5.2 → %7.8**. Bu çelişki önemli: talep var, derin uygulama hâlâ seyrek. Ajansın fırsatı burada.
- **Komşu pazarlar büyüyor:** Grand View'e göre marketing automation pazarı **$6.65B (2024)**'ten **$15.58B (2030)**'a gidiyor; RPA pazarı **$4.68B (2025)**'ten **$35.84B (2033)**'e projekte ediliyor. White-label ajans bunların ikisinin kesişiminde duruyor: CRM + communication + workflow + reporting.
- **Template ekonomisi zaten oluşmuş durumda:** `nusquama/n8nworkflows.xyz` repo'su **2,294 GitHub star**'a çıkmış. Bu, “hazır otomasyon reçetesi” talebinin gerçek olduğunu gösteriyor. Ama template tek başına para etmiyor; delivery, onboarding ve support eklenince iş modele dönüşüyor.
- **Tool maliyeti erken aşamada öldürücü değil:** n8n Starter **$20/mo**, Pro **$50/mo**. Zapier Professional **$19.99/mo**, Team **$69/mo**. GHL tarafında giriş **$97/$297/$497** merdiveni var. Yani bottleneck teknoloji maliyeti değil; hangi offer'ı, kime, nasıl kanıtla sattığın.

## Rakipler & Boşluklar
- **HighLevel:** White-label ajans kurmak için en hazır ticari omurga. Resmi pricing guide'a göre rebilling without markup **$297 Unlimited**, markup'lı rebilling ise sadece **$497 Agency Pro** planında var. Ayrıca AI Employee tarafında sub-account başına **$97/mo unlimited** seçeneği mevcut; ancak resmi overview, bazı ürünlerde (özellikle Voice AI / AI Agents gibi) ürün-spesifik pricing istisnalarını ayrıca kontrol etmen gerektiğini söylüyor. Güçlü yanı: SaaS Mode, billing, CRM, phone, funnel aynı yerde. Zayıf yanı: gerçek “agency to agencies to SMBs” black-label kurgusu bulanık; toplulukta bunun straight-forward olmadığını söyleyen kullanıcılar var.
- **n8n:** Esnek, açık, ucuz ve agentic workflow için güçlü. Ama müşteri-facing shell, seat billing, brand management, permissions ve support katmanını senin kurman gerekiyor. Bu yüzden n8n tek başına ajans ürünü değil; motor.
- **Make:** 2025 sonlarında operasyon bazlı modelden **credits** modeline geçti. Resmi dokümana göre non-AI kullanımda 1 operation ≈ 1 credit, fakat AI özelliklerinde kredi kullanımı token/işlem bazlı dinamik hale geldi. Yani satış fiyatını sabit, maliyeti kontrolsüz bırakırsan marj saçma şekilde eriyebilir.
- **Zapier:** 8,000+ app ekosistemi hâlâ güçlü. Ama task ekonomisi ve MCP call başına **2 task** tüketimi, yüksek hacimli agentic use case'lerde maliyeti hızlı şişirebilir. İlk POC iyi, white-label ölçek için pahalılaşabilir.
- **FlowEngine:** Açık kaynak ve doğrudan bu probleme vuruyor: n8n tabanlı otomasyon ajansları için white-label client portal, template import, credential yönetimi, Stripe billing. Bu repo'nun varlığı tek başına şu gerçeği kanıtlıyor: insanlar “workflow var ama müşteri-facing katman yok” boşluğunu yaşıyor.
- **Vertical starter kit'ler:** Real Estate AI Automation N8N AgencyTemplate gibi küçük ama odaklı repo'lar gösteriyor ki vertical-specific automation pack satışı gerçek bir pattern. Genelci ajans yerine dar dikey + tekrar eden onboarding daha mantıklı.

## Teknik Gereksinimler
- **Temel ürün katmanları:**
  1. Prospect audit raporu
  2. Branded portal / dashboard
  3. Template library + one-click import/update
  4. Credential vault / OAuth onboarding
  5. Billing + seat + usage + markup motoru
  6. Weekly ROI / activity reporting
  7. Support / escalation / human handoff akışı
- **Stack seçenekleri:**
  - **Hızlı ticari yol:** HighLevel $497 + LC Phone/Twilio + AI Employee + premium workflow rebilling
  - **Ucuz ve esnek yol:** n8n Pro $50 + self-host + FlowEngine benzeri portal + Stripe + custom dashboard
  - **Karma yol:** Make/Zapier sadece glue layer; müşteri-facing katman ayrı
- **Minimum veri modeli:** client, sub-account, template, workflow run, lead, appointment, message volume, AI usage, margin, SLA, support ticket, ROI snapshot.
- **Agent rolleri:** niche scout, audit builder, demo generator, onboarding interviewer, QA tester, billing/usage monitor, weekly reporter, churn detector.
- **Metrikler:** lead response rate, warm lead rate, demo-to-close, onboarding time, template reuse %, monthly gross margin, support tickets/account, churn, payback period.
- **İnsan müdahalesi gereken yerler:** satış, fiyat görüşmesi, compliance onayı, credentials doğrulama, riskli otomasyonların onayı, müşteri itiraz yönetimi.

## Ham Notlar
- Product Hunt'in AI workflow automation kategorisi yeni launch'larla dolu. Bu iyi haber değil; bu, generic automation agency pitch'inin emtia olmaya başladığı anlamına geliyor.
- ArXiv `2407.04472` (EventChat) SME bağlamında LLM-driven conversational system'in **85.5% recommendation accuracy** yakaladığını ama **median $0.04/interaction** ve **5.7s latency** yüzünden iş tarafında hâlâ cost/latency baskısı olduğunu gösteriyor. Yani “çalışıyor” ile “kârlı biçimde ölçekleniyor” aynı şey değil.
- ArXiv `2001.03543` business process automation için proactive conversational assistant framework'ü savunuyor; ana fikir bugünkü ajans dünyasına çok uyuyor: business user'ın kontrol, gözlem ve özelleştirme ihtiyacı var. Siyah kutu ajan değil, kontrol paneli lazım.
- Reddit yorumlarında tekrar eden tema şu: **müşteri AI istemiyor, müşteri sonuç istiyor.** “Lead gen, nurture, booking, payments, reporting” diye konuşunca bütçe açılıyor; “bot, agent, automation” diye açınca şüphe artıyor.
- GHL topluluğunda review gating uyarısı önemli. Review automation satarken platform policy'yi ihlal edecek hack'ler uzun vadede müşteriyi de seni de yakar.
- En mantıklı erken teklif: setup fee + monthly retainer + usage cap. Sadece usage bazlı model ilk müşteride kolay görünür ama nakit akışını zayıflatır; sadece retainer da düşük kullanımda “bu para neye gidiyor?” krizine döner. Hibrit daha mantıklı.
