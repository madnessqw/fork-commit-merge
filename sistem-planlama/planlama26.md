# Planlama #26 — AI-Powered Recruiting & HR Otomasyon Uygulama Haritası
**Tarih:** 2026-04-21 20:17
**Bağlı Araştırma:** arastirma26.md

## Swarm Agent ile Nasıl Uygulanır?

Doğru ürün “AI recruiter” değil. O laf pazarda çürümüş. Doğru sistem:

**Recruiting Ops Evidence Pack / Candidate Triage Ledger**

Swarm rol dağılımı:
1. **Researcher Agent**
   - Dikey seçer: healthcare staffing, dental, BPO/call center, retail/frontline, local staffing agencies.
   - Reddit/Google/LinkedIn/agency directories üzerinden pain sinyali toplar: high-volume roles, manual screening, slow scheduling, spam applications, candidate ghosting.
2. **Intake Agent**
   - Job description → structured role scorecard çıkarır.
   - Must-have/nice-have kriterleri ayrıştırır.
   - Hiring manager onayı gerektirir; otomatik kriterle karar yok.
3. **Parser Agent**
   - Resume/CV/profile PDF/DOCX → normalized candidate profile.
   - File hash, parser version, source path ve timestamp kaydeder.
4. **Evidence Agent**
   - Her kriter için candidate evidence snippet çıkarır.
   - Eksik kanıtı açıkça işaretler.
   - “Candidate is good” yerine “şu kriter şu kanıtla destekleniyor” üretir.
5. **Risk & Compliance Agent**
   - Prompt injection, hidden text, impossible timeline, AI-scripted answer, data provenance ve PII retention riskini flag’ler.
   - NYC/EU gibi jurisdiction riskleri için audit checklist üretir.
6. **Scheduling Agent**
   - Human-approved candidate için email/calendar/SMS/WhatsApp akışını hazırlar.
   - Candidate communication templates’i legal-safe tutar.
7. **Verifier / GLM Critic**
   - Output’u bias, unsupported claim, hallucinated evidence ve auto-decision riskine karşı kontrol eder.
8. **Reporter Agent**
   - Weekly ROI report: resumes processed, recruiter hours saved, scheduling conversion, human overrides, false positives/negatives, candidate response time.

## Gerekli Bileşenler

- **Script/Bot:**
  - Resume batch intake + parser wrapper
  - JD → scorecard compiler
  - Evidence extraction + criteria coverage matrix
  - Candidate risk scanner
  - Human approval queue
  - Scheduling/email draft generator
  - Audit ledger writer
  - Weekly ROI report generator
- **MCP/Araç:**
  - Browser automation: ATS/export ekranlarından veri almak için Playwright/Chrome DevTools fallback
  - Gmail/Calendar connector: scheduling ve candidate comms
  - GitHub/local filesystem: audit ledger ve müşteri run kayıtları
  - Optional: MCP wrapper for ATS APIs later
- **API:**
  - LLM: OpenAI/Claude/Gemini veya local model; PII ve data retention şartları netleşmeden gerçek aday verisiyle kullanılmamalı.
  - Parser: LlamaParse/LlamaCloud veya self-hosted PDF parser; başlangıçta CSV/PDF sample yeterli.
  - ATS: Greenhouse/Lever/Workable/Ashby API veya export; ilk POC için CSV export.
  - Calendar/email: Google/Outlook.
  - Optional licensed sourcing: Apollo/LinkedIn Recruiter/CRM data; scraping yapma, data provenance riski var.
- **İnsan Müdahalesi:**
  - Role scorecard onayı
  - Candidate shortlist final decision
  - Rejection/next-step mesajı onayı
  - Bias/validity review
  - Customer-specific compliance approval

## Workflow Haritası

**Trigger:** müşteri yeni role/JD + resume batch yükler

1. JD alınır → role scorecard draft çıkarılır
2. Hiring manager/recruiter scorecard’ı onaylar
3. Resume/CV’ler parse edilir → normalized profiles
4. Her candidate için criteria coverage matrix oluşturulur
5. Evidence snippets + missing evidence + uncertainty çıkarılır
6. Risk scanner çalışır: prompt injection, hidden text, suspicious inconsistencies, unsupported claims
7. Verifier agent hallucination/unsupported scoring kontrol eder
8. Human queue:
   - “Review first”
   - “Likely fit, schedule after approval”
   - “Missing evidence, ask follow-up”
   - “Low fit, human confirm before rejection”
9. Approved candidate için email/calendar draft
10. Candidate communication gönderimi human gate sonrası
11. Audit ledger + weekly ROI report

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

**Hemen yapılabilir ürün:** `Application Flood Audit` — 1 role + 50-100 CV için evidence-based screening raporu.

- **En düşük çaba / en yüksek çıktı adımı:**
  - Gerçek ATS entegrasyonu kurmadan CSV/PDF upload üzerinden “candidate evidence pack” üretmek.
  - Output: role scorecard, top evidence, missing evidence, risk flags, interview questions, scheduling-ready shortlist.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - n8n/Make workflow mantığı; mevcut browser automation + filesystem + LLM çağrıları.
  - GitHub’daki `Resume-Matcher`, `pyresparser`, `AI-Recruitment-Agent` pattern’leri referans alınabilir ama bu turda kod yazılmayacak.
  - UniverseCreator’ın mevcut report-first ürün kası: GTIP/HS rapor mantığı gibi PDF/Markdown audit çıktısı.
- **Proof-of-concept minimum gereksinimler:**
  - 1 örnek JD
  - 20-50 anonim/sahte CV veya müşteri tarafından izinli sample
  - Role criteria rubric
  - Prompt-injection guard prompt + hidden text check
  - Human review checklist
  - Markdown/PDF report template
- **Tahmini kurulum süresi:** 3-5 gün planlama/prototip, 1 hafta demo + satış sayfası.
- **İlk gelir beklentisi:**
  - Tek seferlik audit: **$199-$499** başlangıç paketi.
  - Staffing/clinic/high-volume müşteri için setup: **$750-$2,500** tahmini.
  - Retainer: **$300-$1,500/mo**; ancak gerçek fiyat müşteri hacmine ve data/privacy yüküne göre.

### Kısa vade paket adı
**Hiring Signal QA — Application Flood Audit**

Paket vaadi:
- “AI karar vermez; recruiter’a kanıtlı triage listesi verir.”
- “Her önerinin kaynak satırı var.”
- “Prompt injection ve fake application riskleri flag’lenir.”
- “Aday iletişimi human approval’dan sonra gider.”

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

### 1. ay sonu hedef sistem
- 2 dikeyde pilot:
  1. healthcare/dental/frontline staffing
  2. local recruitment agency / BPO / call center hiring
- ATS export/import connector:
  - CSV/Google Drive first
  - Greenhouse/Lever/Workable API later
- Audit ledger:
  - candidate_id hash
  - role_id
  - criteria_version
  - model_version
  - evidence snippets
  - risk flags
  - human decision
  - timestamp
- Human review UI basit olabilir: Markdown/Sheets/Notion benzeri tablo.
- Weekly ROI dashboard:
  - resumes processed
  - recruiter minutes saved
  - schedule conversion
  - candidate reply time
  - human override rate
  - false positive/false negative feedback

### Metric’ler
- Per role recruiter admin time saved: hedef **5-10 saat** ilk ay.
- Manual review reduction: hedef **%30-50** ama “decision automation” değil, triage hızlanması.
- Candidate response time: hedef aynı gün / 24 saat içinde.
- Human override tracking: modelin kör kullanımı yasak; override oranı öğrenme sinyali.
- Evidence completeness: her shortlist recommendation için minimum 3 kaynak evidence snippet.
- Prompt-injection detection: hidden/irrelevant instruction flag’leri loglanır.

### Paralel çalışabilecek adımlar
- Researcher: müşteri dikeyleri + pain listeleri + outreach listeleri.
- Planner: role scorecard templates.
- Builder ileride: parser + ledger + report automation.
- Verifier: bias/validity and compliance checklist.
- Sales agent: one-page audit offer + cold outreach copy.

### Ölçeklendirme gereksinimleri
- **İnsan:** 1 domain reviewer / recruiter danışmanı gerekir; HR workflow’u bilmeyen tool bok gibi olur.
- **Araç:** n8n/Make, LLM API, parser, email/calendar, encrypted storage.
- **Bütçe:** küçük POC $20-$100/mo tool/API; pilotta $100-$300/mo; gerçek PII/compliance varsa hukuki danışmanlık maliyeti doğar.
- **Güvenlik:** PII retention, deletion policy, customer DPA, audit logs.

### Checkpoint’ler
- Hafta 2: 1 demo report + 1 landing/offer + 20 prospect listesi.
- Ay 1: 1 ücretli audit veya 3 ücretsiz pilot call.
- Ay 2: 2 pilot müşteri, 5+ role processed.
- Ay 3: repeatable vertical playbook + retainer dönüşümü.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo
Sistem bir **compliance-aware hiring ops layer** olur:
- ATS’lerin üstünde çalışır.
- Candidate communication + scheduling + evidence pack + audit ledger sağlar.
- Recruiter kararını değiştirmez; karar kalitesini ve hızını artırır.
- Her role için öğrenen scorecard library tutar.

### Yan ürünler / yeni gelir kolları
1. **Candidate Authenticity Check API**
   - hidden prompt injection, suspicious AI-script, document inconsistency, duplicate application risk.
2. **Hiring Bias/Validity Audit Kit**
   - synthetic resume test sets, demographic signal perturbation, model stability report.
3. **Interview Question Generator + Evidence Map**
   - her soruyu candidate evidence/missing evidence ile bağlar.
4. **Scheduling Recovery Bot**
   - candidate no-show, reschedule, reminder, timezone handling.
5. **White-label Recruitment Agency Ops Kit**
   - agencies kendi markasıyla müşterilere “screening evidence pack” satar.
6. **MCP/Agent-ready ATS connector pack**
   - Greenhouse/Lever/Workable/Ashby read-only connectors + audit-safe operations.

### Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek şey
- Tek LLM skoru yerine multi-agent cross-check:
  - extractor ayrı,
  - evaluator ayrı,
  - risk scanner ayrı,
  - verifier ayrı,
  - compliance ledger ayrı.
- Her output kanıt satırıyla gelir.
- Weekly ROI + error-learning loop otomatik.
- Candidate fraud/prompt injection + recruiter workflow pain tek pakette.

### White-label veya SaaS olarak satılabilir mi?
Evet, ama SaaS’a hemen atlamak kötü fikir. Doğru sıra:
1. Report-first paid audit
2. Done-for-you workflow implementation
3. Retainer + monthly hiring ops QA
4. White-label agency kit
5. SaaS / API / MCP layer

SaaS ancak 3-5 pilotta aynı workflow tekrar ediyorsa mantıklı.

## Öncelik & Çaba Tahmini

- **Öncelik:** Yüksek — çünkü ROI case’leri güçlü, ama direct auto-screening riskli. Evidence/compliance wedge ile oynanırsa iyi.
- **Kurulum Süresi:**
  - Audit-only POC: 3-5 gün
  - Pilot workflow: 2-4 hafta
  - ATS connector + compliance ledger: 6-10 hafta
- **Aylık İşletme Maliyeti:**
  - POC: **$20-$100/mo** tahmini
  - Pilot: **$100-$300/mo** tahmini
  - Compliance-heavy müşteri: hukuk/güvenlik dahil çok değişir
- **Potansiyel Gelir:**
  - Audit: **$199-$499** tek sefer
  - Setup: **$750-$2,500**
  - Retainer: **$300-$1,500/mo**
  - Agency/healthcare high-volume için daha yüksek olabilir, ama önce kanıt gerekir.
- **ROI Beklentisi:**
  - Eğer 1 recruiter haftada 5-10 saat admin kazanırsa, $30-$50/saat loaded cost ile aylık değer **$600-$2,000** bandı eder.
  - Bu yüzden $500-$1,500/mo retainer savunulabilir; ama sadece gerçek time-saved ölçülürse.

## Mevcut Sistemle Entegrasyon

UniverseCreator mevcut yapısı:
- Research → plan → report-first output kası güçlü.
- Çok sayıda Vercel ürün var; ama HR recruiting için yeni SaaS açmak şimdilik gereksiz.
- Swarm zaten Claude+Codex+GLM gibi farklı rollerle çalışıyor; bu konu multi-agent verification’a doğal uyuyor.

Entegrasyon yolu:
1. `sistem-planlama` içinde vertical offer ve audit template hazırlanır.
2. İlk çıktı bir PDF/Markdown audit ürünü olur, production app değil.
3. Mevcut browser automation stack ile ATS/export işlemleri araştırılır.
4. Mevcut report automation mantığı candidate evidence pack’e uyarlanır.
5. İleride MCP connector olarak ATS read-only layer yazılabilir.

## Riskler & Dikkat Edilecekler

- **Legal / compliance:** EU AI Act ve NYC AEDT nedeniyle candidate filtering/ranking high-risk. Auto-reject yasak gibi davran; human gate şart.
- **Bias:** ArXiv bias bulguları ağır; demographic proxy ve name bias audit olmadan “fair AI” iddiası yapılmaz.
- **Validity:** Model doğru adayı seçemeyebilir; “score” yerine “evidence + uncertainty” tasarımı şart.
- **Prompt injection:** Resume içine hidden instruction koyma gerçek risk; Greenhouse ve ArXiv bunu doğruluyor.
- **Data privacy:** CV/PII hassas veri. Retention/deletion/DPA olmadan gerçek müşteri verisiyle oynamak olmaz.
- **Recruiter backlash:** “AI recruiter replaces you” mesajı satış öldürür. “Admin load off, recruiter in control” mesajı kullanılmalı.
- **Data provenance:** LinkedIn scraping / data broker kaynakları lawsuit ve ToS riskine açık. Owned CRM/ATS data ve licensed APIs tercih edilmeli.
- **False confidence:** Tek model skoru tehlikeli; verifier + human override + feedback loop zorunlu.

## Önce Yapılacak 3 Adım (Bu Hafta)

1. **Offer dosyası hazırla:** `Hiring Signal QA — Application Flood Audit` için 1 sayfalık teklif: problem, çıktı örneği, fiyat bandı, compliance stance.
2. **Demo veri seti seç:** 1 public/sample JD + 20-30 synthetic/anonymized resumes ile evidence pack örneği üretilecek şekilde tasarla. Gerçek PII kullanma.
3. **Pilot müşteri listesi çıkar:** 30 staffing/healthcare/dental/BPO recruitment target; mesaj: “AI karar vermez, 1 role için candidate evidence audit çıkarırız.”

## Zorunlu 3 Soruya Net Cevap

### Kısa vade (1-2 hafta): Bu bulgudan ne HEMEN hayata geçirilebilir?
**Application Flood Audit** hemen hayata geçirilebilir: 1 role + 50 CV için evidence-based triage report. Kod/SaaS gerekmez; report-first hizmet satılır. En düşük riskli gelir yolu bu.

### Orta vade (1-3 ay): Sistem nasıl olgunlaşır?
ATS export/import, parser, audit ledger, human approval queue, scheduling draft, weekly ROI report ve bias/validity test harness ile tekrarlanabilir “Recruiting Ops Copilot” hizmetine dönüşür. Başarı metriği model accuracy değil; recruiter hours saved + schedule conversion + human override kalitesi.

### Uzun vade (3-12 ay): Bu sistem nasıl evrilebilir, büyüyebilir?
Compliance-aware hiring ops layer / white-label agency kit / MCP-ready ATS connector pack’e evrilir. En büyük büyüme alanı “AI screener” değil; **candidate authenticity + evidence ledger + audit-ready human-in-loop hiring workflows**.
