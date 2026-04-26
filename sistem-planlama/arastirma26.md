# Araştırma #26 — AI-Powered Recruiting & HR Otomasyon (2026 doğrulama)
**Tarih:** 2026-04-21 20:17
**Konu:** AI-Powered Recruiting & HR Otomasyon — CV/resume screening, interview scheduling, candidate authenticity, compliance-first recruiter copilots
**Counter:** N=26 → konu indeksi `26 % 14 + 1 = 13`

**Kaynaklar / kullanılan katmanlar:**
- Yerel katalog: `projeler.txt` HR/recruiting keyword taraması
- ddgr: AI recruiting market, compliance, case study, LinkedIn Hiring Assistant, Greenhouse AI hiring raporu
- Reddit JSON API: r/recruiting, r/humanresources, r/recruitinghell, r/recruiters, r/AIAgents, r/SideProject
- GitHub CLI: resume parser/matcher/screening, open-source ATS ve multi-agent recruitment repos
- derin-arastirma: ArXiv MCP + MCPTube transcript araması + Jina Reader
- Seçici Jina: Workday/Paradox, Paradox MultiCare, HireVue Emirates NBD, Greenhouse/PRNewswire, NYC AEDT, EU AI Act, LinkedIn Hiring Assistant, Mordor, GitHub README'leri
- ProductHunt: Jina search denendi; güvenilir içerik düşük/blocked olduğu için karar sinyali olarak kullanılmadı.

## Özet Bulgular

1. **Pazar büyüyor ama “AI recruiter” söylemi zehirli.** Mordor, AI recruitment pazarını **2026 $640.99M → 2031 $920.91M** olarak veriyor; screening/assessment **2025 harcamasının %31.85**’i. Ama Reddit tarafında recruiter’lar generic sourcing botlarına sert tepki veriyor: sorun “profil bulmak” değil, doğru sinyal, güven, ilişki ve hiring-manager koordinasyonu.
2. **En güçlü ROI scheduling + candidate experience + high-volume hiring’de.** Paradox/Workday hattı; Workday Recruiting entegrasyonunda “up to 90% hiring process automation”, **190K+ candidate question**, **10K+ interview request**, **%89 application completion**, **%99 faster scheduling**, **%85 manual task reduction** iddia ediyor. MultiCare case: event cost **$4,000 → $1,000 (%75 düşüş)**, event hires **%25 artış**, cost-per-hire **%22 düşüş**.
3. **Video interview / skills validation enterprise ROI’si gerçek, ama compliance ve güven krizi ağır.** HireVue + Emirates NBD: **8,000 recruiter hour**, **$400K** tasarruf, **%80 time-to-offer düşüş**, **%100+ NPS uplift**, bazı roller için **8,000’e kadar başvuru**.
4. **2026 farkı: candidate fraud + prompt injection artık core problem.** Greenhouse 2025 AI in Hiring Report: **4,100+** job seeker/recruiter/hiring manager survey; ABD job seeker’larının **%41**’i prompt injection kullandığını söylüyor, **%52** kullanmayı düşünüyor; recruiter’ların **%91**’i candidate deception gördüğünü söylüyor; hiring manager’ların **%70**’i AI kararları hızlandırır/iyileştirir derken, job seeker’ların sadece **%8**’i AI screening’i adil buluyor.
5. **Regülasyon çıtası yükseldi.** NYC Local Law 144: AEDT kullanımı için son 1 yıl içinde bias audit, public summary ve aday/çalışan notice şartı. EU AI Act Annex III: işe alım/selection, job application analysis/filtering ve candidate evaluation için AI sistemlerini high-risk alanına koyuyor. “AI otomatik seçsin” fikri burada aptalca pahalı risk; doğru wedge **human-in-the-loop evidence pack + audit ledger + scheduling ops**.

## Gerçek Başarı Hikayeleri

### 1) Workday + Paradox: enterprise consolidation sinyali
- Workday, Paradox acquisition’ı **1 Ekim 2025**’te tamamladı.
- Workday açıklaması: Paradox + HiredScore + Workday Recruiting birleşince uçtan uca AI-powered talent acquisition suite.
- Workday Paradox Candidate Experience Agent: candidate engagement, instant responses, self-scheduling, 24/7 conversational support, application/scheduling/interview coordination.
- Workday müşteri tabanı açıklamasında **11,000+ organizations** ve Fortune 500’ün **%65+**’i geçiyor; yani enterprise tarafı ağır incumbent alanı.

Kaynaklar:
- https://newsroom.workday.com/2025-10-01-Workday-Completes-Acquisition-of-Paradox
- https://www.paradox.ai/partners/workday

### 2) Paradox / MultiCare Health System
- Odak: healthcare high-volume event hiring.
- Sonuçlar:
  - Event cost: **$4,000 → $1,000** (**%75** düşüş)
  - Event hires: **%25** artış
  - Cost-per-hire: **%22** düşüş
- Neden önemli: Bu, “resume parser” değil; scheduling + candidate communication + event workflow automation ROI’si.

Kaynak: https://www.paradox.ai/case-studies/multicare-health-system

### 3) HireVue / Emirates NBD
- Emirates NBD: **30,000+ employee**, 7 ülkede varlık; bazı roller için **8,000’e kadar application**.
- HireVue case sonucunda:
  - **8,000 recruiter hours** tasarruf
  - **$400,000** tasarruf
  - **%80** time-to-offer reduction
  - **%100+** NPS uplift
  - quality/performance artışı iddiası

Kaynak: https://www.hirevue.com/resources/video/emirates-nbd-uses-ai-and-skills-to-transform-volume-hiring

### 4) LinkedIn Hiring Assistant — agentic recruiter product
- LinkedIn product page, Ocak 2026 verisiyle:
  - **%81 fewer profiles viewed** to find a qualified match
  - **%66 higher InMail acceptance rates** vs traditional sourcing
  - **1.5 hours saved per role** identifying top-qualified applicants
- Engineering blog mimarisi: plan-and-execute supervisor agent, headless recruiter tools, async sourcing/evaluation, individualized memory, sub-agent/tool decomposition.
- Secondary HRD/HCA coverage: Certis tarafında LinkedIn Hiring Assistant + Talent Insights ile recruiter productivity **%60-70** artışı iddia ediliyor.

Kaynaklar:
- https://business.linkedin.com/hire/hiring-assistant
- https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant
- https://www.hcamag.com/asia/specialisation/hr-technology/hiring-supercharged-linkedins-first-ai-agent-boosts-recruiter-output-by-up-to-70/554403

### 5) No-code/n8n agency örnekleri — küçük oyuncu için uygulanabilir sinyal
MCPTube transcriptleri:
- `ppbXEab8334` — “AI Automation for Recruitment Agency That Saves 15 HOURS/WEEK (n8n workflow)”
  - JD → title mutation → Apollo/CRM search → dedupe → pre-score → full profile enrichment → detailed candidate assessment → personalized outreach.
  - İddia: **10-15 hours/week per recruiter**, **100+ positive replies/month**, testimonialda **80-100 meetings booked**.
  - Güçlü yan: service agency için satılabilir workflow.
  - Zayıf yan: LinkedIn/Apollo data provenance ve legal/compliance açıkları kapatılmazsa riskli.
- `LgAcdo91jt8` — “n8n for HR Teams: Automate Resume Screening, Emails & Candidate Scoring”
  - Jotform → resume PDF → parser/LlamaCloud → GPT-4o mini evaluation → strong/moderate/weak segmentation → candidate email → HR brief + interview questions.
  - İddia: 50-200 application, 20 dk/resume → **33 saatlik** manuel iş dakikalara iner.

Kaynaklar:
- https://www.youtube.com/watch?v=ppbXEab8334
- https://www.youtube.com/watch?v=LgAcdo91jt8
- https://www.youtube.com/watch?v=MiZNmjWHq1w

## Pazar Büyüklüğü & Fırsat

### Pazar verileri
- Mordor Intelligence:
  - AI recruitment market: **2026 $640.99M → 2031 $920.91M**
  - Software: **%64.12** of 2025 revenue
  - SME segment: **%10.05 CAGR**
  - Cloud solutions: **%77.94 share in 2025**, **%19.05 CAGR** through 2031
  - Screening/assessment: **%31.85** of 2025 expenditure
  - Healthcare: fastest-growing end-user with **%13.05 CAGR** through 2031
  - NLP: **%34.52** of 2025 revenue; RPA projected **%13.08/year**

Kaynak: https://www.mordorintelligence.com/industry-reports/ai-recruitment-market

### Opportunity wedge
Enterprise ATS/recruiting suite pazarı Workday, Greenhouse, HireVue, Paradox, LinkedIn, Eightfold, iCIMS, Lever, Ashby gibi devlerle dolu. UniverseCreator için direkt “ATS kuruyoruz” kötü fikir. Daha iyi wedge:

**Recruiting Ops Evidence Pack / Screening Triage Copilot**
- Auto-decision vermez.
- Adayı “eledi/seçti” demez.
- Her candidate için evidence-based brief üretir:
  - job criteria coverage
  - resume/profile evidence snippets
  - missing evidence
  - uncertainty/confidence
  - prompt-injection / AI-generated content risk
  - HR için interview focus questions
  - human approval checkbox
  - audit ledger
- Scheduling ve candidate communication ile gerçek admin yükünü azaltır.

Bu wedge hem Reddit’in “AI recruiter bullshit” itirazından kaçıyor hem de compliance çıtasına daha yakın.

## Rakipler & Boşluklar

### Büyük rakipler
- **Workday + Paradox + HiredScore:** enterprise suite, high-volume/frontline roles, scheduling + candidate conversation.
- **HireVue:** video interview, skill assessment, enterprise case studies.
- **LinkedIn Hiring Assistant:** LinkedIn network + Recruiter workflow içine gömülü agent.
- **Greenhouse:** ATS + structured hiring + AI principles + integration ecosystem.
- **Eightfold / Beamery / SeekOut / Gem / Findem:** talent intelligence ve sourcing.

### Open-source / GitHub sinyalleri
- `srbhr/Resume-Matcher`: **26.8K★ / 4.8K fork**, TypeScript+Python, job seeker tarafında resume-to-JD optimization commodity oldu.
- `xitanggg/open-resume`: **8.5K★**, resume builder/parser.
- `OmkarPathak/pyresparser`: **955★**, klasik resume parser.
- `JAIJANYANI/Automated-Resume-Screening-System`: **479★**, ML resume screening.
- `Hungreeee/Resume-Screening-RAG-Pipeline`: **178★**, RAG resume screening chatbot.
- `Ancastal/AI-Recruitment-Agent`: **38★**, AutoGen multi-agent recruitment assistant; resume screening, candidate evaluation, interview preparation.

Kaynaklar:
- https://github.com/srbhr/Resume-Matcher
- https://github.com/xitanggg/open-resume
- https://github.com/OmkarPathak/pyresparser
- https://github.com/JAIJANYANI/Automated-Resume-Screening-System
- https://github.com/Hungreeee/Resume-Screening-RAG-Pipeline
- https://github.com/Ancastal/AI-Recruitment-Agent

### Boşluklar
1. **Job seeker tools doymuş.** Resume optimizer/matcher çok; para ve compliance value employer tarafında.
2. **Recruiter workflow gerçekliği eksik.** Reddit sinyali: “profil bulmak” ana bottleneck değil; cevap almak, güven, hiring-manager speed, candidate quality ve ilişki yönetimi.
3. **Compliance-by-design az.** Çoğu n8n/demo workflow candidate ranking yapıyor ama audit, candidate notice, bias/validity test, data provenance yok.
4. **Candidate authenticity yeni pain.** Prompt injection, fake work samples, AI scripts, deepfake interview riski arttı. Bu, “AI screening”den daha satılabilir bir güvenlik/evidence layer olabilir.
5. **SMB/staffing agencies enterprise suite istemiyor.** Onların ihtiyacı: ATS export/Google Drive/Jotform/Sheets → hızlı triage → scheduling → weekly ROI report.

## Teknik Gereksinimler

### Minimum viable architecture
- **Input layer:** JD, role scorecard, must-have/nice-have criteria, candidate resumes/profiles, application form fields.
- **Parser:** PDF/DOCX → text/markdown; PII-aware extraction; file hash.
- **Criteria compiler:** JD’den otomatik scorecard çıkarır ama recruiter/hiring manager onayı ister.
- **Evidence extractor:** Candidate claim → source snippet mapping. “Bu aday güçlü” yerine “şu satır şu kritere kanıt” der.
- **Risk detector:** hidden prompt injection, AI-generated application artifacts, suspicious inconsistency, impossible timeline, missing evidence.
- **Human-in-loop queue:** accept/reject değil; “review needed / likely fit / missing evidence” gibi triage labels.
- **Communication/scheduling:** approved candidates için email/SMS/calendar workflow; rejected candidates için template ve legal-safe wording.
- **Audit ledger:** model/version, prompt hash, criteria, evidence, human decision, timestamps, notice status.
- **Metrics:** time saved, response time, schedule conversion, human override rate, false positive/negative feedback.

### Araçlar / API seçenekleri
- n8n / Make / Zapier: workflow orchestration. n8n resmi pricing sayfası güncel olarak Starter/Pro denemeleri ve execution-based fiyatlamayı gösteriyor; web index kaynakları aylık bandı kabaca **€24 monthly / €20 annual Starter**, **€60 monthly / €50 annual Pro** diye veriyor. Fiyat güncel kalmalı; satın almadan tekrar kontrol edilmeli.
- ATS/export: Greenhouse/Lever/Workable/Ashby API veya CSV export. Başlangıçta CSV/Google Drive/Sheets yeterli.
- Parsing: LlamaParse/LlamaCloud, self-hosted parser, `open-resume`/`pyresparser` benzeri OSS.
- LLM: OpenAI/Claude/Gemini + yerel model fallback; private candidate data için müşteri sözleşmesi ve retention policy şart.
- Calendar/email: Google Calendar/Gmail/Outlook, Twilio/WhatsApp opsiyonel.
- Compliance: bias/validity test harness, model output logging, candidate notice template, human approval gate.

## Regülasyon & Risk

### NYC Local Law 144
NYC DCWP sayfası AEDT kullanımında şunları şart koşuyor:
- tool son 1 yıl içinde bias audit’ten geçmeli,
- bias audit summary public olmalı,
- employee/job candidate notices verilmiş olmalı,
- DCWP şikayet kanalı var,
- presentation clarification: notice **10 business days** before AEDT use.

Kaynak: https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page

### EU AI Act
EU AI Act Annex III, employment/workers management alanında AI sistemlerini high-risk listesine alıyor:
- recruitment/selection,
- targeted job ads,
- job application analysis/filtering,
- candidate evaluation,
- promotion/termination/task allocation/performance monitoring.

Kaynaklar:
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3

### Akademik risk sinyalleri
- `2407.20371`: resume screening retrieval framework’ünde MTE modelleri White-associated names lehine **%85.1** vakada bias; Black males bazı koşullarda **%100** dezavantaj.
- `2401.08315`: LLM agent framework resume screening’i manuel yönteme göre **11x faster**, fine-tuned sentence classification F1 **%87.73**.
- `2504.02870`: context-aware explainable multi-agent RAG framework; extractor/evaluator/summarizer/score formatter agentleri.
- `2512.20164`: hidden adversarial instructions in resumes; certain attacks **>%80** success; combined defense **%26.3** attack reduction.
- `2602.18550`: LLM resume ranker’ların birçok durumda daha nitelikli CV’yi tutarlı seçemediği ve eşit adaylarda güvenilir abstain etmediği bulgusu.
- `2603.18390`: local/open-source LLM screening framework privacy avantajı ve bazı koşullarda GPT-5-nano/mini karşılaştırmaları.

Kaynaklar:
- https://arxiv.org/pdf/2407.20371v2
- https://arxiv.org/pdf/2401.08315v2
- https://arxiv.org/pdf/2504.02870v2
- https://arxiv.org/pdf/2512.20164v1
- https://arxiv.org/pdf/2602.18550v1
- https://arxiv.org/pdf/2603.18390v1

## Community Intelligence — Reddit

### Recruiter tarafı
- r/recruiting “These AI recruitment companies are pissing me off”: 13+ yıllık recruiter, AI vendor demolarının generic questions/video review ile zaman kazandırmadığını, recruiting gerçekliğini anlamadığını söylüyor. Yorumlarda ortak tema: tool’lar recruiter tarafından tasarlanmadıysa işe yaramıyor.
- r/recruiting “AI recruiting is going nowhere”: 15+ yıllık corporate recruiter, bottleneck’in profil bulmak olmadığını; doğru adaydan gerçek cevap almak, ilişki kurmak ve hiring manager’ı yönetmek olduğunu vurguluyor. Bir yorumda, kısa ve organik LinkedIn mesajlarının AI slop içinde daha çok öne çıktığı; response rate’in 2025’te **%53**’e çıktığı self-report edilmiş.
- r/humanresources “great at applying, terrible at doing”: keyword/parser odaklı screening’in keyword gaming yapanları öne çıkarıp gerçek yetkinliği kaçırdığı şikayeti.
- r/humanresources “LinkedIn wrappers”: AI hiring platformlarının çoğu LinkedIn/data-broker wrapper; data provenance ve scraping riski kullanıcıların aklında.

Kaynaklar:
- https://reddit.com/r/recruiting/comments/1nxapg9/these_ai_recruitment_companies_are_pissing_me_off/
- https://reddit.com/r/recruiting/comments/1ph6qhq/ai_recruiting_is_going_nowhere/
- https://reddit.com/r/humanresources/comments/1oe8him/im_tired_of_interviewing_people_who_are_great_at/
- https://reddit.com/r/humanresources/comments/1nxbcss/f_these_linkedin_wrappers_na/

### Net çıkarım
AI recruiting satılacaksa “ben recruiter’ı değiştiriyorum” değil, **recruiter’ın admin yükünü ve riskini azaltıyorum** denmeli. Candidate relationship tarafında insanı büyüten copilot; decision tarafında audit-friendly evidence pack.

## GitHub Implementasyon Bulguları

### Kullanılabilir yapı taşları
- Resume parsing/matching OSS bol; MVP için sıfırdan parser yazmak gereksiz.
- Multi-agent recruitment agent örnekleri var ama yıldız sayıları düşük; production pattern henüz olgun değil.
- En güçlü public traction job seeker tarafında; employer/recruiter compliance ops boşluğu daha ticari.

### Mimari öğrenim
- LinkedIn Hiring Assistant mimarisi UniverseCreator swarm için iyi pattern: supervisor agent + sub-tools + async task queue + memory + feedback loop.
- AutoGen multi-agent recruitment agent küçük ama doğru iş bölümünü gösteriyor: parser/extractor, evaluator, interviewer/prep, formatter.
- Bizim farkımız “AI score” değil: evidence, audit, human approval, weekly ROI report.

## Ham Notlar

- `projeler.txt` HR/recruiting için zayıf sinyal verdi; doğrudan recruiting ürün fikri yok, generic browser/agent automation linkleri çıktı. Bu iyi: UniverseCreator portföyünde konu henüz temsil edilmiyor.
- ddgr çalıştı ve Forbes/Humanly/MiHCM gibi vendor içerikleri de verdi; fakat karar için vendor bloglarını ikinci sınıf tuttum, resmi/case/legal/academic kaynaklara ağırlık verdim.
- ProductHunt Jina search güvenilir extract vermedi; bu turda PH sinyali “blocked/low value” diye notlandı.
- En tehlikeli ürün adı: “AI Resume Screener”. Bu doğrudan legal/bias risk kutusuna giriyor. Daha iyi ad: **Recruiting Ops Evidence Pack**, **Candidate Triage Ledger**, **Hiring Signal QA**, **Application Flood Audit**.
- İlk müşteri için en mantıklı dikeyler: staffing agencies, healthcare staffing, dental/clinic chains, retail/frontline hiring, call center/BPO hiring. Tech recruiting’de AI slop ve candidate fraud daha yüksek; risk fazla.
- Satış mesajı: “%80 daha hızlı işe alım” gibi abartı değil; “her role için 10 saat admin yükü çıkarıyoruz, karar sizde kalıyor, her öneri kanıtlı ve loglu.”
