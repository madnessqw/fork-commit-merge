# Planlama #12 — AI-Powered Recruiting & HR Otomasyon Uygulama Haritası
**Tarih:** 2026-04-21 09:48
**Bağlı Araştırma:** arastirma12.md

## Swarm Agent ile Nasıl Uygulanır?

Bu alanda doğru ürün “otonom recruiter” değil. O fikir hem güven hem regülasyon tarafında mayın. Doğru ürün: **Human-in-the-loop Recruiting Ops Copilot**.

Mevcut Claude+Codex+GLM swarm şöyle kullanılabilir:

1. **Researcher agent**
   - HR/recruiting agency hedef listesi çıkarır.
   - Reddit/LinkedIn/Google Maps/agency directories üzerinden “manual screening, high-volume hiring, staffing agency, healthcare staffing” sinyallerini izler.
   - Rakip fiyat/özellik değişimini haftalık raporlar.

2. **Codex builder/research agent**
   - Uygulama değil, şimdilik plan ve workflow template hazırlar.
   - Müşteri bazlı gereksinimleri “input fields → decision rubric → outputs → human approval” şeklinde standartlaştırır.
   - ATS/API connector matrix çıkarır: Workable, Greenhouse, Ashby, Bullhorn, Google Sheets, Airtable.

3. **GLM analyst**
   - Toplanan workflow sonuçlarını skorlar: time saved, candidates processed, reply rate, drop-off, manual override rate.
   - Bias/compliance red flags için periyodik denetim raporu üretir.

4. **Human owner**
   - Final hiring kararları, rejection/advance approval ve legal-sensitive copy için onay verir.
   - İlk satış görüşmelerini yapar; AI sadece discovery brief ve demo script hazırlar.

## Gerekli Bileşenler

- **Script/Bot:**
  - Resume intake parser: PDF/DOCX → structured JSON.
  - Rubric scorer: JD + human criteria + candidate facts → evidence-based score.
  - Candidate brief generator: 1-page human-readable summary.
  - Interview kit generator: role-specific questions + risk areas.
  - Email/scheduling assistant: candidate status emails + calendar slots.
  - Audit logger: prompt/model/version/score/human override/reason code.

- **MCP/Araç:**
  - Browser automation: Workable/Greenhouse/Ashby/Bullhorn admin tasks API yoksa Playwright/chrome-devtools-axi.
  - Gmail/Calendar connector ileride gerekli olur; bu turda sadece plan.
  - Google Sheets/Airtable export.
  - ArXiv/web/reddit monitoring for compliance and product positioning.

- **API:**
  - LLM: OpenAI/Claude for extraction, scoring explanation, email draft.
  - Parser: LlamaParse/LlamaCloud veya open-source PDF extractor.
  - Optional enrichment: Apollo/Clay/Clearbit; LinkedIn scraping TOS riskli, dikkat.
  - Calendar: Google Calendar / Microsoft Graph.
  - Email: Gmail / SendGrid / customer SMTP.

- **İnsan Müdahalesi:**
  - Rubric onayı.
  - Shortlist approve/reject.
  - Sensitive rejection email onayı.
  - Bias/audit sampling review.
  - Legal/compliance localization: NYC, EU, KVKK/GDPR.

## Workflow Haritası

**MVP workflow:**

Trigger: New application / uploaded CV / form submission
→ Resume parser extracts facts
→ JD + role rubric loaded
→ AI creates structured candidate profile
→ AI maps evidence to rubric criteria
→ Score + confidence + missing-data flags generated
→ Human recruiter review queue
→ Recruiter approves next action
→ Candidate email draft generated
→ Calendar/scheduling link sent only after approval
→ ATS/Sheet row updated
→ Audit log stored
→ Weekly metrics report generated

**Agency sourcing workflow:**

Trigger: New role intake
→ JD parsed into title variants + must-have/nice-to-have criteria
→ Candidate source selected: CRM first, then Apollo/approved database
→ Candidate dedupe
→ Lightweight prequalification
→ Enrichment only for threshold-pass candidates
→ Human shortlist review
→ Personalized outreach draft
→ Multi-channel follow-up schedule
→ Reply tracking
→ Client-ready shortlist pack

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen uygulanabilir en iyi adım:** “Recruiting Workflow Audit + Resume Screening Copilot Template” hizmet paketini tanımlamak.
- **Satılacak şey:** AI hiring SaaS değil; küçük agency/SMB için **done-with-you automation setup**.
- **Minimum çıktı:**
  - 1 intake form taslağı.
  - 1 candidate summary schema.
  - 1 rubric scoring schema.
  - 1 Google Sheets/Airtable dashboard taslağı.
  - 1 compliance checklist: consent notice, bias audit readiness, human approval log.
  - 1 demo script: “CV upload → summary → recruiter review → email draft”.
- **Mevcut araç/script avantajı:** UniverseCreator’da browser automation, workflow araştırma, agent coordination ve raporlama alışkanlığı var. Bu iş production kod yazmadan önce workflow tasarımıyla satılabilir.
- **Tahmini kurulum süresi:** 3–5 gün araştırma + şablon + teklif; 7–10 gün ilk client-specific POC.
- **İlk gelir beklentisi:**
  - Setup: **$499–$1,500**.
  - Monthly maintenance/reporting: **$99–$399/mo**.
  - Eğer agency için Apollo/ATS entegrasyonu yapılırsa setup **$2,000+** olabilir.
- **Bu hafta yapılacak POC sınırı:** Final decision yok; sadece summary + suggested next action + human approval.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda hedef sistem:**
  - 2-3 vertical için hazır paket:
    1. staffing/recruitment agency,
    2. healthcare/frontline/high-volume hiring,
    3. SMB founder hiring assistant.
  - Google Sheets/Airtable tabanlı working demo.
  - 5 gerçek workflow audit görüşmesi.
  - 1 pilot müşteri veya 1 ücretsiz case study.

- **Başarı metric’leri:**
  - Resume başına manual review süresi.
  - Shortlist creation time.
  - Human override rate.
  - Email reply rate.
  - Candidate drop-off.
  - Time-to-first-contact.
  - Recruiter admin hours saved/week.
  - Compliance completeness: notice, consent, audit log, versioning.

- **Paralel çalışabilecek adımlar:**
  - Researcher: target lead list + pain-point mining.
  - Codex: workflow templates + docs + checklist.
  - GLM: weekly metric dashboard design.
  - Human: 10 outreach + 3 discovery calls.

- **Ölçeklendirme için gerekenler:**
  - ATS connector library.
  - Client-specific prompt/rubric vault.
  - Data retention policy.
  - Audit export.
  - Simple onboarding checklist.
  - Case study izinleri.

- **Checkpoint’ler:**
  - Hafta 2: demo flow + sales one-pager hazır.
  - Hafta 4: 1 pilot workflow canlı.
  - Hafta 8: 3 müşteri discovery veya 1 paid client.
  - Hafta 12: repeatable offer + documented SOP.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:**
  - Sistem agency/SMB için recruitment ops layer olur: inbound applications, resume parsing, candidate scoring, interview briefs, scheduling, email drafts, audit logs.
  - İnsan hâlâ karar verir; swarm admin işini ve evidence packaging’i yapar.

- **Yeni gelir kolları:**
  - White-label recruiting copilot for agencies.
  - Compliance evidence pack subscription.
  - “AI hiring readiness audit” raporu.
  - ATS migration/automation consulting.
  - Vertical template marketplace: healthcare staffing, cleaning, logistics, hospitality.

- **Rakiplerin yapamadığı, swarm ile yapılabilecek şey:**
  - Tek bir tool değil, sürekli öğrenen ops loop: Reddit complaint mining → workflow improvement → client-specific prompt/rubric update → audit log → weekly ROI report.
  - Müşteri için “AI ne karar verdi?” değil, “hangi evidence hangi rubric maddesine bağlandı, insan neyi override etti?” raporu.

- **White-label / SaaS potansiyeli:**
  - White-label agency paketi daha erken satılır.
  - SaaS ancak 3-5 paid workflow’dan sonra mantıklı. Direkt SaaS’a atlamak, müşteri gerçeği yokken ürün gömmek olur; kötü fikir.

## Öncelik & Çaba Tahmini

- **Öncelik:** Orta-Yüksek.
- **Neden yüksek değil:** Regülasyon/güven riski yüksek; yanlış positioning markayı yakar.
- **Neden orta-yüksek:** Admin/task automation tarafı gerçek ROI üretiyor; agency modeli hızlı satılabilir.
- **Kurulum Süresi:**
  - Offer + demo docs: 3–5 gün.
  - İlk POC: 1–2 hafta.
  - Repeatable package: 1–3 ay.
- **Aylık İşletme Maliyeti:**
  - MVP: **$30–$150/mo** LLM + parser + Sheets/Airtable.
  - Client workflow: **$100–$500/mo** API/enrichment/ATS connector kullanımına göre.
- **Potansiyel Gelir:**
  - Starter audit/setup: **$499–$1,500**.
  - Managed automation: **$199–$999/mo**.
  - Agency/enterprise connector setup: **$2,000–$10,000** project fee.
- **ROI Beklentisi:**
  - Eğer müşteri 10+ saat/hafta recruiter admin yükü azaltıyorsa, $300/mo fee kolay savunulur.
  - Break-even: düşük maliyetli setup ile 1. müşteri; custom entegrasyon varsa 2-3 müşteri.

## Mevcut Sistemle Entegrasyon

Mevcut UniverseCreator sistemi ürün fabrikası gibi çalışıyor; HR automation için execution değil, önce **offer factory** kurulmalı:

1. `sistem-planlama` içinde vertical research devam eder.
2. Research output’tan “HR Ops Automation Offer” çıkarılır.
3. Product değil service-first paket yazılır.
4. Swarm agent’lar satış öncesi discovery brief ve workflow map üretir.
5. İlk müşteri olmadan SaaS kodu yazılmaz.
6. İlk 1-3 müşteri sonrası ortak pattern varsa micro-SaaS/white-label düşünülür.

Mevcut 113 ürün/Vercel hattıyla birleşme:
- Bu fikir, tek seferlik “free web tool” portföyünden çok **B2B workflow service** tarafına daha uygun.
- Vercel ürünleri lead magnet olabilir: “Free Resume Screening Risk Checklist”, “Time-to-Hire ROI Calculator”, “AI Hiring Compliance Checklist”.
- Asıl para checkout’lu micro-tool’dan değil, setup + monthly service’den gelir.

## Riskler & Dikkat Edilecekler

- **Legal risk:** EU AI Act ve NYC Local Law 144 nedeniyle AI candidate ranking/selection hassas. İnsan onayı ve audit log şart.
- **Bias risk:** ArXiv bulguları LLM/retrieval modellerinde isim/cinsiyet/ırk proxy bias’ının gerçek olduğunu gösteriyor.
- **Candidate trust risk:** AI call/interview kötü uygulanırsa aday markayı çöpe atar.
- **Spam risk:** AI outreach hacmi artırır ama cevap oranını ve marka güvenini düşürebilir.
- **TOS risk:** LinkedIn scraping/sourcing otomasyonu dikkat ister; resmi API veya müşteri CRM daha güvenli.
- **Data privacy:** CV, phone, email, employment history, interview notes PII içerir; retention ve access control gerekir.
- **Bad positioning:** “AI replaces recruiters” deme. Satış cümlesi: “Recruiters spend less time on admin, more time on people.”

## Önce Yapılacak 3 Adım (Bu Hafta)

1. **Offer dokümanı hazırla:** “Recruiting Admin Copilot Setup — CV summary, interview brief, scheduling draft, audit log” şeklinde tek sayfalık teklif.
2. **Demo workflow tasarla:** Kod yazmadan, form alanları + output schema + dashboard kolonları + approval states dokümanı çıkar.
3. **10 hedef müşteri listesi çıkar:** staffing agencies, healthcare staffing, local service businesses, SMB founders; her biri için “haftada kaç CV, kaç screening call, kaç saat admin?” discovery soruları yaz.

## Zorunlu 3 Soruya Net Cevap

### Kısa vade (1-2 hafta): Bu bulgudan ne HEMEN hayata geçirilebilir?
Human-in-the-loop resume summary + candidate brief + email draft workflow’u. Bunu SaaS gibi değil, **consulting/setup paketi** gibi sat. İlk hafta demo ve satış dokümanı; ikinci hafta pilot müşteri görüşmesi.

### Orta vade (1-3 ay): Sistem nasıl olgunlaşır?
ATS/Sheets/Airtable entegrasyonlu, metric takipli ve audit-log’lu repeatable workflow paketine dönüşür. 3 vertical template, 1 paid pilot, weekly ROI report ve compliance checklist ile güven kazanır.

### Uzun vade (3-12 ay): Bu sistem nasıl evrilebilir, büyüyebilir?
White-label recruiting ops copilot’a evrilir: agency’ler kendi markasıyla kullanır, swarm arkada sourcing/review/reporting döngüsünü işletir. SaaS ancak gerçek müşteri pattern’i tekrarlandığında yapılır; aksi hâlde pahalı oyuncak olur.
