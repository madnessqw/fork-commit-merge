# Planlama #19 — White-label Otomasyon Ajansı Uygulama Haritası
**Tarih:** 2026-04-21 14:53 +03
**Bağlı Araştırma:** arastirma19.md

## Swarm Agent ile Nasıl Uygulanır?
Bu iş “automation agency” diye değil, **Delegated Ops Retainer** diye kurulmalı. Satılan şey workflow değil: kaçan geliri yakalayan, insan ekibi güçlendiren, haftalık ROI gösteren yönetilen operasyon sistemi.

1. **Vertical Scout Agent**
   - Home services/HVAC/roofing, dental/clinic, legal intake, med-aesthetics, recruitment, e-commerce ops gibi vertical’ları puanlar.
   - Kriterler: ticket büyüklüğü, lead kaçırma acısı, compliance riski, API/CRM erişimi, tekrar eden süreç, karar vericiye erişim.
2. **Leak Audit Agent**
   - Prospect website/form/call/booking/review/CRM görünürlüğünü inceler.
   - Çıktı: “missed revenue leak map” + estimated ROI + yapılacak ilk micro-automation.
3. **Offer Builder Agent**
   - AI replacement değil, delegation diliyle teklif üretir.
   - Örnek: “AI leads close eder” yasak; “AI ilgilileri ayıklar, ekibin sadece sıcak fırsatla konuşur” doğru.
4. **Demo Builder Agent**
   - n8n/GHL/Make/Zapier fark etmeksizin müşteriye görünen demo üretir: dashboard, inbox/handoff queue, weekly report mockup.
5. **Workflow Architect Agent**
   - İlk use case’i küçük tutar: missed-call recovery, speed-to-lead, database reactivation, invoice/chasing, support triage, review response support.
6. **QA & Compliance Agent**
   - Consent, opt-out, PII, role-based access, hallucination guard, escalation, failure alerts, call recording, KVKK/GDPR/TCPA checklist.
7. **Usage Margin Watcher**
   - GHL voice/AI/phone/email, n8n execution, Zapier tasks, Make credits, LLM/token maliyeti ve gross margin’i izler.
8. **Weekly ROI Reporter**
   - Müşteriye her hafta: kaç lead işlendi, kaç sıcak fırsat çıktı, kaç booking oldu, tahmini recovered revenue, hata/failure, insan müdahalesi, sonraki optimizasyon.
9. **Human Sales Gate**
   - İlk 10 müşteri için satış görüşmesi, fiyatlama, production onayı ve compliance kararı insan kapısında kalır.

## Gerekli Bileşenler
- **Script/Bot:**
  - vertical scoring sheet
  - prospect leak-audit generator
  - ROI calculator
  - demo/dashboard generator
  - onboarding questionnaire
  - workflow viability scorer
  - weekly ROI report generator
  - usage/margin calculator
  - QA/compliance checklist runner
  - churn-risk detector
- **MCP/Araç:**
  - Browser automation / `chrome-devtools-axi` / Playwright: prospect site, form, booking ve public funnel gözlemi
  - GitHub/gh: n8n/GHL template ve MCP repo araştırması
  - MCPTube: creator case study ve satış playbook extraction
  - ArXiv MCP: RPA/BPA/SMB AI adoption araştırma validasyonu
  - Jina Reader: pricing/docs/case study okuma
- **API:**
  - HighLevel: $497 Agency Pro hedef yol; $297 rebilling without markup; $97 starter sadece erken test için.
  - n8n: $20 Starter / $50 Pro / $800 Business; ilk IP kontrollü yol için Pro yeterli olabilir.
  - Stripe/Lemon/iyzico: abonelik + setup fee + usage overage.
  - Twilio/LC Phone/WhatsApp/SMTP/Google Calendar/Sheets/Airtable/Salesforce/HubSpot.
  - OpenAI/Claude/Gemini: triage, summarization, routing; voice varsa ayrı maliyet guardrail.
- **İnsan Müdahalesi:**
  - ilk vertical seçimi
  - ilk satış görüşmeleri
  - müşteri credential/onay toplama
  - production launch onayı
  - compliance sınırları
  - legal/medical/high-risk çıktıların son kararı

## Workflow Haritası
Tetikleyici: yeni vertical seçimi
→ 50 prospect listesi
→ public funnel audit
→ leak score + ROI estimate
→ 5 demo adayı seç
→ demo Loom + 1 sayfa audit
→ warm outreach / referral / lokal kanal
→ discovery call
→ küçük paid pilot scope
→ onboarding form + credential checklist
→ workflow kurulum planı
→ QA/compliance test
→ pilot launch
→ weekly ROI report
→ retainer upgrade / referral / second automation

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen uygulanabilir şey:** Tek vertical ve tek offer seç: **Missed Revenue Recovery OS**.
  - İlk önerilen vertical: HVAC/roofing/home services veya dental/clinic.
  - Mesaj: “kaçan leadleri yakala, ekibi sadece sıcak fırsatla konuştur, haftalık recovered revenue raporu al.”
- **En düşük çaba / en yüksek çıktı:** 20 prospect için public leak audit üretmek. Kod/deploy gerekmez; browser gözlem + manuel not + ROI calculator yeter.
- **Mevcut araç/script katkısı:** araştırma döngüsü, `projeler.txt` n8n/MCP kaynakları, browser gözlem araçları, GitHub template katalogları, mevcut 113 sağlıklı ürün portföyü demo/landing/dash fikirleri için kullanılabilir.
- **Minimum POC gereksinimleri:**
  - 1 vertical
  - 1 teklif adı
  - 1 audit checklist
  - 1 ROI hesaplama formülü
  - 1 demo dashboard mockup
  - 1 fiyat kartı
  - 1 compliance checklist
- **Tahmini kurulum süresi:** 3-5 gün offer/audit/pitch materyali; 5-10 gün ilk demo/pilot görüşmeleri.
- **İlk gelir beklentisi:** gerçekçi pilot hedefi **$500-$2,000 setup** + **$500-$1,500/mo retainer**. Daha yüksek mümkün ama ilk iki haftada $10K MRR hedeflemek yine YouTube sarhoşluğu.
- **İlk paket önerisi:**
  - Audit Sprint: $250-$500 tek seferlik — leak map + ROI estimate + demo Loom.
  - Starter Retainer: $750/mo — 1 workflow + weekly report + usage cap.
  - Growth Retainer: $1,500-$3,500/mo — multi-step handoff + dashboard + support + optimization.
  - Premium: $4,000+/mo + upside — high-volume lead recovery / legal / dental / HVAC.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **Ay 1 hedef görüntü:**
  - 1 vertical seçilmiş
  - 50-100 prospect audit yapılmış
  - 10 kişiselleştirilmiş demo/audit gönderilmiş
  - 3-5 discovery call
  - 1-2 paid pilot veya net reddedilme paterni
  - onboarding + QA + weekly report şablonu hazır
- **Başarı metrikleri:**
  - audit → call: %5-15
  - call → paid audit/pilot: %20-30
  - pilot launch süresi: <7 gün
  - onboarding süresi: <60 dk
  - workflow failure alert süresi: <15 dk
  - gross margin: %60+
  - churn riski: weekly report okunmuyorsa kırmızı bayrak
- **Paralel çalışabilecek adımlar:**
  - Researcher: vertical pain ve prospect listesi
  - Analyst: ROI/margin modeli
  - Builder: demo dashboard / workflow prototype planı
  - QA: failure/compliance cases
  - Skill-writer: onboarding SOP + sales script
  - Reporter: weekly ROI report formatı
- **Ölçeklendirme gereksinimleri:**
  - client portal / permission layer
  - template versioning
  - credentials vault
  - run logs + incident dashboard
  - usage-based billing guardrails
  - support queue
- **Checkpoint’ler:**
  - Hafta 2: offer + 20 audit + 1 demo
  - Hafta 4: 3-5 call + 1 pilot
  - Hafta 8: 2 aktif müşteri veya vertical pivot kararı
  - Hafta 12: repeatable template + onboarding <45 dk + 2 case-study adayı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** Ajans “workflow yapan freelancer” olmaktan çıkar; vertical-specific managed automation OS olur. Her müşteri aynı çekirdek: lead intake, triage, human handoff, dashboard, report, optimization.
- **Yan ürünler / yeni gelir kolları:**
  - paid leak audit report
  - vertical ROI calculator
  - n8n/GHL template pack
  - white-label client portal
  - agency partner program
  - onboarding sprint
  - usage markup
  - compliance checklist product
  - weekly reporting SaaS
- **Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek şey:**
  - Her prospect’e hızlı audit çıkarma
  - demo’yu vertical’a otomatik uyarlama
  - müşteri başına weekly ROI raporu üretme
  - workflow failure ve margin izleme
  - vertical playbook’u her müşteriyle güncelleme
  - 113 ürün portföyünü demo/mini-tool/landing varlığı olarak kullanma
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet, ama önce managed service. Salt SaaS’a erken kaçmak kötü fikir. Pattern kanıtlandıktan sonra FlowEngine benzeri portal + n8n/GHL connector + reporting katmanı white-label lisansa dönebilir.
- **12 ay hedefi:**
  - 5-10 retainer müşteri veya 2 agency partner
  - 2 vertical template
  - müşteri başı onboarding <45 dk
  - support yükü müşteri başı <3 kritik ticket/ay
  - MRR hedefi: **$5K-$25K** gerçekçi; **$50K+** ancak acquisition kanalı ve case study oluşursa.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek. AI calling, lead gen, browser automation, n8n/MCP ve local market bulgularını tek gelir modelinde birleştiriyor.
- **Kurulum Süresi:** 1-2 hafta offer/audit/demo; 1-3 ay ilk müşteri ve templateleşme; 3-12 ay portal/white-label.
- **Aylık İşletme Maliyeti:**
  - Lean n8n yolu: $50-$150/mo + LLM/hosting.
  - GHL yolu: $497/mo + AI Employee/voice/SMS/email/WhatsApp usage.
  - POC Zapier/Make yolu: $20-$100+ ama hacim artınca task/credit maliyeti izlenmeli.
- **Potansiyel Gelir:**
  - İlk pilot: $500-$2,000 setup + $500-$1,500 MRR.
  - 1-3 ay: $2K-$10K MRR.
  - 3-12 ay: $5K-$25K MRR; iyi vertical + case study ile üstü mümkün.
- **ROI Beklentisi:**
  - Lean n8n yolu 1 müşteriyle break-even.
  - GHL Pro yolu için 1 Growth müşteri veya 2 Starter müşteri gerekir.
  - En hızlı break-even: paid audit + starter retainer; en iyi long-term: portal + reusable template.

## Mevcut Sistemle Entegrasyon
- UniverseCreator mevcut durumda **113 active / 113 healthy** ürün ve güçlü araştırma/loglama disipliniyle çalışıyor. Bu direkt olarak müşteri-facing “weekly ops report” formatına çevrilebilir.
- `projeler.txt` n8n/MCP ağırlıklı; bu sistemin n8n backend + MCP workflow builder kası hızlı kurulabilir.
- Mevcut browser automation stack public site/funnel audit için kullanılabilir.
- Vercel portföyü client audit landing, ROI calculator, report demo ve mini dashboard prototipleri için yüzey sağlayabilir; bu araştırma modunda kod/deploy yok.
- Swarm rollerini gelir modeline çevir: researcher=vertical scout, analyst=ROI/margin, builder=demo plan, qa=compliance/failure, skill-writer=SOP/report.

## Riskler & Dikkat Edilecekler
- **AI slop / outreach zehirlenmesi:** Küçük işletmeler otomatik AI mesajlarından bıkmış. Generic cold outreach spam bu kategoriyi öldürür.
- **Replacement pitch:** “AI çalışanı değiştirir” dersen direnç doğar. “Ucuz tekrarı AI yapar, pahalı insan daha çok kazanır” dili şart.
- **Compliance:** legal/dental/medical para öder ama PII/HIPAA/KVKK/TCPA yanlış yapılırsa büyük risk.
- **One-off trap:** $5K build güzel görünür ama retainer yoksa her ay yeniden satış cehennemi.
- **Tool lock-in:** GHL hızlı ama vendor bağımlı. n8n esnek ama ops yükü fazla. Paket baştan migration opsiyonuyla tasarlanmalı.
- **Margin leakage:** voice minute, LLM token, Zapier task, Make credit, GHL AI/phone usage cap’siz bırakılırsa kâr erir.
- **Support cehennemi:** Çok custom iş + düşük fiyat = ölüm. Aynı vertical, aynı workflow ailesi, aynı rapor standardı şart.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek offer seç ve isimlendir:** “Missed Revenue Recovery OS” — HVAC/roofing veya dental için kaçan lead/call/form recovery.
2. **20 prospect leak audit çıkar:** site formu, call/booking akışı, review/Google Business, speed-to-lead sinyali, ROI estimate. Outreach yoksa bile audit arşivi yarın satış varlığı olur.
3. **1 demo + fiyat kartı hazırla:** Starter/Growth/Premium; setup fee + retainer + usage cap + weekly report. Tool adı değil, sonuç dili kullan.
