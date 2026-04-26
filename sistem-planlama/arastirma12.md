# Araştırma #12 — AI-Powered Recruiting & HR Otomasyon
**Tarih:** 2026-04-21 09:48
**Konu:** AI-powered recruiting, resume screening, interview scheduling, onboarding ve compliance-first HR otomasyonu

**Kaynaklar:**
- Market.us — AI Hiring Software Market: https://market.us/report/ai-hiring-software-market/
- Mordor Intelligence — AI Recruitment Market: https://www.mordorintelligence.com/industry-reports/ai-recruitment-market
- NYC DCWP — Local Law 144 / AEDT: https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page
- EU AI Act Service Desk / Article 6: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6
- EU AI Act Annex III mirror: https://ai-act-law.eu/annex/3/
- Paradox MultiCare case study: https://www.paradox.ai/case-studies/multicare-health-system
- HireVue case studies: https://www.hirevue.com/case-studies
- Workday Paradox acquisition: https://investor.workday.com/news-and-events/press-releases/news-details/2025/Workday-Completes-Acquisition-of-Paradox-10-01-2025/default.aspx
- TechCrunch Mercor funding: https://techcrunch.com/2025/02/20/mercor-an-ai-recruiting-startup-founded-by-21-year-olds-raises-100m-at-2b-valuation/
- ProductHunt search snippets: Voxcruit, HireHunch/JusRecruit, hirebetter.io, HiveMind
- Reddit JSON: r/recruiting, r/humanresources, r/recruitinghell, r/SideProject, r/AIAgents
- GitHub CLI search: resume parser AI, AI recruiting automation, resume screening LLM, interview scheduler AI
- ArXiv MCP: 2407.20371, 2309.13933, 2401.08315, 2504.02870, 2512.20164, 2602.18550, 2603.18390
- MCPTube: `MiZNmjWHq1w`, `ppbXEab8334`, `LgAcdo91jt8`

## Özet Bulgular
- **En iyi fırsat “AI karar verici recruiter” değil; compliance-first recruiter copilot.** Recruiter topluluklarında AI sourcing/outreach spam’i ciddi tepki topluyor. Kalıcı kullanım alanı: transcript/özet, ATS alan doldurma, aday brief’i, interview question set, scheduling ve audit log.
- **Pazar büyüyor ama güven/regülasyon bariyeri sert.** Market.us, AI hiring software pazarını 2024’te **$1.8B**, 2025’te **$2.0B**, 2034’te **$5.4B** ve **%11.6 CAGR** olarak veriyor. Mordor daha dar tanımla 2026 değerini **$640.99M**, 2031’i **$920.91M** veriyor. Kapsam farkı büyük; tek rakama kör güvenmek aptallık olur.
- **Resume screening büyük segment ama riskli segment.** Market.us’a göre resume screening & matching kullanımın **%25.8**’i; Mordor’a göre screening/assessment 2025 harcamasının **%31.85**’i. Aynı alan EU AI Act ve NYC Local Law 144 altında en çok denetlenen alan.
- **Gerçek ROI yüksek hacimli/tekrarlı hiring’de.** Paradox/MultiCare: event cost **$4,000 → $1,000** (**%75 düşüş**), event hires **%25 artış**, cost-per-hire **%22 düşüş**. HireVue sayfasında Emirates NBD için **8,000 recruiter hour**, **$400K** tasarruf, time-to-offer **%80** düşüş iddiası var.
- **Open-source implementasyonlar zayıf sinyal veriyor.** GitHub’da çok sayıda yeni repo var ama star sayıları 0–6 bandında. Bu pazarın açık kaynak koddan değil, workflow + entegrasyon + güven + veri yönetişiminden para kazandığını gösteriyor.

## Gerçek Başarı Hikayeleri

### 1) Paradox / MultiCare Health System
- Sektör: Healthcare, ABD, **20,000** çalışan.
- Entegrasyon: Workday.
- Kullanım: Olivia AI assistant ile candidate registration, screening, scheduling.
- Sonuçlar:
  - Event cost: **$4,000 → $1,000**; **%75** düşüş.
  - Event hires: **%25** artış.
  - Cost per hire: **%22** düşüş.
- Not: Bu “insanı tamamen çıkarma” değil; AI registration/screening/scheduling admin yükünü alıyor.

Kaynak: https://www.paradox.ai/case-studies/multicare-health-system

### 2) HireVue case study havuzu
- Emirates NBD: HireVue sayfası, AI-driven video assessments ile **8,000 recruiter hour** ve **$400,000** tasarruf; time-to-offer **%80** düşüş; NPS **%100+** artış; quality-of-hire **%20** artış veriyor.
- APAC bank örneği: hiring time **%60** düşüş, CSAT **%25** artış, “millions of dollars” tasarruf iddiası.
- Swire Coca-Cola: chaos-to-clarity story; 18 gün time-to-fill kesintisi ve application-to-offer sürecinin **3.5 gün**e inmesi öne çıkarılmış.

Kaynak: https://www.hirevue.com/case-studies

### 3) Mercor
- TechCrunch: Mercor, Şubat 2025’te **$100M Series B** ve **$2B valuation** duyurdu; önceki valuation **$250M** idi.
- Forbes snippet’i: Mercor AI interviewer’ın **300,000** adayı vet ettiği; birkaç ayda **$1M revenue run-rate** ve **$80K profit** gördüğü bilgisi çıktı.
- Ders: Recruiting AI’da büyük para “HR için ATS eklentisi” kadar “talent marketplace + AI interview + expert matching” tarafında da var.

Kaynaklar:
- https://techcrunch.com/2025/02/20/mercor-an-ai-recruiting-startup-founded-by-21-year-olds-raises-100m-at-2b-valuation/
- https://www.forbes.com/sites/alexkonrad/2024/09/18/mercor-ai-interviewer-reaches-250-million-valuation/

### 4) Workday + Paradox konsolidasyonu
- Workday, 2025-10-01’de Paradox acquisition’ı tamamladı.
- Workday açıklaması: Paradox, HiredScore ve Workday Recruiting birleşince “end-to-end AI-powered talent acquisition suite” oluşuyor.
- Workday: **11,000+** organizasyon, Fortune 500’ün **%65+**’i.
- Ders: Büyük oyuncular AI recruiting’i tek modül olarak değil, sourcing → candidate conversation → scheduling → onboarding zinciri olarak paketliyor.

Kaynak: https://investor.workday.com/news-and-events/press-releases/news-details/2025/Workday-Completes-Acquisition-of-Paradox-10-01-2025/default.aspx

## Pazar Büyüklüğü & Fırsat

### Pazar verileri
- Market.us:
  - AI Hiring Software Market: **$1.8B** 2024, **$2.0B** 2025, **$5.4B** 2034.
  - CAGR: **%11.6**.
  - North America: **%41.8** share.
  - Software/platform: **%78.5**.
  - Cloud deployment: **%92.2**.
  - Large enterprise users: **%70.4**.
  - Resume screening & matching: **%25.8**.
  - IT & telecom: **%35.3**.
  - Adoption/efficiency iddiaları: time-to-hire **%50** düşebilir, cost-per-hire **%30** düşebilir, repetitive hiring tasks **%40** otomatikleşebilir, recruiter productivity **%60** artabilir.
- Mordor:
  - AI recruitment market: **$640.99M** 2026 → **$920.91M** 2031.
  - Cloud: **%77.94** share, **%19.05 CAGR**.
  - Screening/assessment: **%31.85** of 2025 expenditure.
  - Large orgs: **%57.22** spending in 2025.
  - SME segment: **%10.05 CAGR**.
  - Healthcare fastest end-user growth: **%13.05 CAGR**.

### Fırsat açısı
- **Enterprise pazar dolu ve ağır satış gerektiriyor.** Workday, Greenhouse, HireVue, Paradox, Bullhorn, Workable, Lever gibi oyuncular var.
- **SMB / agency pazarı hâlâ açık.** Reddit ve ProductHunt sinyalleri küçük ekiplerin enterprise ATS istemediğini, ama admin yükünden nefret ettiğini gösteriyor.
- **En düşük friction ürün:** ATS yerine “existing workflow üstüne HR ops copilot”: Google Sheets/Airtable/Workable/Greenhouse/Ashby/Bullhorn üstünden özet, score, email, scheduling, audit log.
- **Niche vertical önerisi:** Recruiting agency + high-volume roles: healthcare staffing, cleaning, logistics, hospitality, call center, construction/skilled trades. Niche/senior executive recruiting’de tam otomasyon ters teper.

## Rakipler & Boşluklar

### Büyük rakipler
- **Workday + Paradox + HiredScore:** full-suite, enterprise.
- **HireVue:** video interview, assessment, workflow automation, enterprise case study bolluğu.
- **Greenhouse:** ATS + sourcing/CRM + scheduling + reporting + Real Talent candidate matching; pricing açık değil.
- **Workable:** standard plan **$299/mo** başlangıç; ATS + sourcing + HR bundle.
- **Bullhorn + Textkernel:** staffing/recruiting agency tarafında semantic search / sourcing AI.
- **Mercor:** AI interview + talent marketplace; klasik ATS değil, marketplace model.

### ProductHunt yeni ürün sinyalleri
- **Voxcruit:** skill-based voice interviews; recruiter-defined skills/scoring/thresholds; 2026 launch, 21 review, 133 follower.
- **HireHunch / JusRecruit:** phone screens + first-round AI interviews; iddia: **10–15 gün** time-to-hire düşüş, **~20 recruiter hours per role** tasarruf.
- **hirebetter.io:** plug-and-play recruiting automation; job criteria → candidate summary → strengths/risks/recommendations.
- **HiveMind:** resume ranking, skill assessment, auto-routing, scheduling, interview copilot; özellikle solo recruiters/startups positioning.

### Boşluklar
- **Compliance + explainability default değil.** Çoğu küçük tool “AI ranks candidates” diyor ama audit trail, rubric versioning, consent, bias checks, human override log yok.
- **Recruiter workflow gerçekliği zayıf anlaşılmış.** Reddit’te 15–30 yıllık recruiter’lar “bottleneck profile bulmak değil, ilişki ve cevap almak” diyor.
- **Aday güveni kırılıyor.** AI screening call, AI-generated resumes, fake candidates, avatar/interview cheating ve automated rejections ciddi tepki yaratıyor.
- **ATS integration gap.** Küçük ekipler yeni ATS istemiyor; mevcut Workable/Greenhouse/Ashby/Bullhorn/Jira/Drive/Sheets akışına eklenen “thin layer” istiyor.

## Teknik Gereksinimler

### Minimum sistem bileşenleri
- **Input:** Job description, role rubric, application form, CV/PDF/DOCX, LinkedIn/profile URL, optional interview transcript.
- **Parsing:** LlamaParse/LlamaCloud, PDF extractor, OCR fallback, structured JSON schema.
- **Candidate model:** skills, experience, education, location, compensation, availability, red flags, positive signals, source, consent status.
- **Scoring:** human-defined rubric; “AI recommendation” değil “rubric-based evidence map”. Score tek başına karar olmamalı.
- **Human-in-the-loop:** shortlist approve/reject, reason code, override reason, audit trail.
- **Comms:** email templates, follow-up scheduling, calendar integration, candidate status updates.
- **Compliance:** consent notice, bias audit readiness, model/version log, prompt/version log, protected-class proxy control, explanation export.
- **Integrations:** Google Sheets/Airtable first; Gmail/Calendar; Workable/Greenhouse/Ashby/Bullhorn later; LinkedIn/Apollo only consent/TOS sınırıyla.

### ArXiv teknik bulguları
- **2401.08315 — LLM agents for resume screening:** LLM agent framework, resume screening’i manual method’a göre **11x faster** yapmış; resume sentence classification F1 **87.73%**.
- **2407.20371 — Bias in resume screening via language model retrieval:** MTE retrieval modelleri White-associated names lehine **%85.1** vakada bias göstermiş; female-associated names lehine yalnız **%11.1**; Black males bazı senaryolarda **%100** dezavantajlı.
- **2504.02870 — Multi-agent RAG resume screening:** extractor/evaluator/summarizer/score formatter agent’ları; RAG ile industry/certification/company-specific criteria ekliyor.
- **2512.20164 — adversarial resume instructions:** hidden instructions attack success bazı attack tiplerinde **%80+**; prompt defense attack’i **%10.1**, LoRA/FIDS **%15.4**, combined **%26.3** azaltmış ama false rejection artışı var.
- **2602.18550 — validity audits:** bazı LLM’lerin daha nitelikli adayı tutarlı seçemediği ve equal candidates durumunda güvenilir abstain edemediği vurgulanıyor.
- **2603.18390 — local resume screening:** open-source/local LLM tabanlı AutoScreen-FW, privacy riskini düşürme yönünde ilginç; ticari LLM bağımlılığını azaltabilir.

### MCPTube / n8n workflow bulguları
- **MiZNmjWHq1w:** n8n workflow: Form → Google Drive upload → PDF text extraction → AI extractor JSON schema → education/job/skills extraction → merge → MapReduce summarization, **1000 char chunk / 200 overlap** → AI score **1–10**, consideration, category → Google Sheet row → email confirmation. Video “single role resume screening average 23 hours” iddiasıyla başlıyor.
- **ppbXEab8334:** agency sourcing workflow: job title/description/location form → Airtable job/candidate DB → AI job-title mutation **5 titles** → Apollo/CRM/LinkedIn source → dedupe **50 → 43** sample → prequalification **0–5**, threshold **≥4** → profile enrichment → detailed fit/red-flag/positive-signal assessment → Claude-written email/LinkedIn message. İddia: **10–15 hours/week** saving ve **100+ positive replies/month**.
- **LgAcdo91jt8:** Jotform → resume download → LlamaCloud parsing → GPT-4o-mini HR analysis → strengths/concerns/relevant experience extraction → switch node strong/moderate/weak → candidate email + HR interview brief. Video “hundreds of applications × 20 min = 33 hours” iddiası veriyor.

## Regülasyon & Risk

### NYC Local Law 144
- Automated Employment Decision Tools için employers/employment agencies ancak:
  - son 1 yıl içinde bias audit yapılmışsa,
  - audit özeti public ise,
  - çalışan/adaya gerekli notice verilmişse kullanabilir.
- Enforcement: **2023-07-05**.
- Ürün tasarım dersi: audit export ve notice workflow “sonradan eklenir” değil, MVP çekirdeği olmalı.

Kaynak: https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page

### EU AI Act
- Article 6: Annex III sistemleri high-risk sayılır.
- Annex III employment category: recruitment/selection, targeted job ads, job applications filtering, candidate evaluation high-risk kapsamına girer.
- Ürün tasarım dersi: final karar AI’da olmamalı; human oversight, logging, documentation, transparency ve risk management şart.

Kaynaklar:
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6
- https://ai-act-law.eu/annex/3/

## Community Intelligence — Reddit

### Recruiter tarafı
- r/recruiting “AI recruiting is going nowhere”: 15+ yıllık recruiter OP’nin ana fikri: bottleneck aday profili bulmak değil, doğru adaydan marka yıkmadan cevap almak. Top comment: relationship/selling işi hâlâ recruiter’da.
- Aynı thread’de 30+ yıl tecrübeli commenter: AI sourcing tool’larının kendi ekibinden iyi aday bulmadığını, hâlâ “şit ton of profiles” gerektiğini söylüyor.
- “Anyone actually cut hiring costs using AI?” thread: Somut işe yarayanlar olarak interview transcript → summary → MPC profile, ATS field filling, email campaigns ve Clay/automation geçiyor. Tam otomatik interview/screening için özellikle senior/niche rollerde tepki yüksek.
- High-volume blue-collar/mass labor için calls/scheduling/interview/credential verification işe yarıyor; Coinbase gibi AI first screening tool deneyimlerinde kötü candidate feedback uyarısı var.

### HR tarafı
- r/humanresources “What HR tasks are you actually using AI for?”: işe yarayan kullanım: job description draft, mass email draft, Excel formula/math, compliance search, exit interview notes theme summary, manager feedback phrasing. Güçlü direnç: confidential HRIS data, portal-heavy workflows, vendor spam.

### Candidate tarafı
- r/recruitinghell ve r/SideProject sinyali: applicant-side agents yükseliyor. Bir kullanıcı **516 evaluations / 66 applications / zero manual screening** job-search automation anlattı. Yorumlarda “my agent applying to your agent” distopyası konuşuluyor.
- Bu karşı taraf otomasyonu, employer-side tool için bot/fraud/spam detection ve candidate authenticity layer ihtiyacını büyütüyor.

## GitHub Implementasyon Bulguları

GitHub araması açık kaynak pazar olgunluğunun zayıf olduğunu gösterdi:
- `rahulapjs/ResumeParserAI` — Streamlit + Google Gemini; PDF resume parse, structured data, summaries; **4 star**, 2026 update.
- `codewave-ansuman/resume-parser-ai` — PDF/DOCX resume extraction, skills/education/work/contact analysis; **1 star**, 2025 update.
- `arushjasuja/ai-recruiting-platform` — job descriptions + candidate matching; CrewAI + LangChain + AutoGen; **0 star**, 2025 update.
- `kapooraditi79/Resume-Ranker-Agent` — PDF parse, Gemini embeddings, ChromaDB rank, Gmail notifications/interview scheduling; **0 star**, 2025 update.
- `SupriyaKamatagi/interview-scheduler-aiagent` — Google ADK, Composio, Cloud Run, credential management; **1 star**, 2026 update.
- `satyaswaminadhyedida0703/smart-hiring-system` — resume screening, matching, AI interviews, fairness auditing; **0 star**, 2026 update.

Ders: Teknik MVP zor değil; güvenilir entegrasyon, compliance ve müşteri workflow’u zor.

## Ham Notlar
- `projeler.txt` doğrudan HR/recruiting projesi açısından zayıf; mevcut katalogda browser agent, workflow, Twilio/voice, MCP ve automation pattern’leri var. HR ürünü bu mevcut agent/browser/automation altyapısıyla eklenebilir.
- `ddgr` çalıştırıldı ama bu turda boş sonuç verdi. Web araması + Jina + Reddit JSON + GitHub CLI ile açık kapatıldı.
- ProductHunt Jina 403/Cloudflare döndürdü; fallback web search ProductHunt snippets ile Voxcruit, HireHunch/JusRecruit, hirebetter.io, HiveMind, InCruiter bulundu.
- En güçlü positioning: “AI recruiter” değil, **Recruiter Admin Copilot + Compliance Evidence Pack**.
- En zayıf fikir: “CV’yi at, AI otomatik reject etsin.” Bu hukuki, etik ve marka açısından mayın tarlası.
- En satılabilir paket: “2 haftada HR ops automation audit + one workflow + dashboard + audit log” — setup fee + monthly maintenance.
