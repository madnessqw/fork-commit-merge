# Araştırma #13 — Swarm Agent Başarı Hikayeleri
**Tarih:** 2026-04-21 10:49
**Konu:** Swarm agent / multi-agent sistemlerin gerçek üretim başarıları, gelir örnekleri, production pattern'leri ve UniverseCreator için uygulanabilir dersler

**Kaynaklar:**
- Anthropic — The 2026 State of AI Agents Report: https://resources.anthropic.com/hubfs/The%202026%20State%20of%20AI%20Agents%20Report.pdf
- Grand View Research — AI Agents Market: https://www.grandviewresearch.com/industry-analysis/ai-agents-market-report
- Vercel — We removed 80% of our agent’s tools: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools
- AWS Prescriptive Guidance — CrewAI: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/crewai.html
- Kimi — Agent Swarm blog: https://www.kimi.com/blog/agent-swarm
- arXiv — MegaAgent: https://arxiv.org/abs/2408.09955
- arXiv — A Large-Scale Study on the Development and Issues of Multi-Agent AI Systems: https://arxiv.org/abs/2601.07136
- arXiv — An Outlook on the Opportunities and Challenges of Multi-Agent AI Systems: https://arxiv.org/abs/2505.18397
- Indie Hackers — RapidClaw $2K MRR story: https://www.indiehackers.com/post/we-hit-2k-mrr-letting-people-deploy-ai-agents-without-touching-a-terminal-45cfa83e06
- Reddit — OpenClaw 60 günde kâra geçen agent deneyi: https://reddit.com/r/SideProject/comments/1r1z42o/i_gave_an_ai_agent_60_days_and_50_bucks_to_build/
- Reddit — Cloudflare multi-agent build log: https://reddit.com/r/ClaudeAI/comments/1p6w71c/built_a_multiagent_system_on_cloudflare_workers/
- GitHub search snapshot — MetaGPT / CAMEL / MindSearch / Mission Control / Ruflo / ClawTeam / claude-swarm
- MCPTube — IBM Technology `sWH0T4Zez6I`, LangChain `4nZl32FwU-o`, Sam Witteveen `FfCqINSD8Tc`
- Yerel sinyal — `projeler.txt` içindeki Cloudflare multi-agent, claude-swarm, Vercel self-verifying agent, agent-to-agent/weave ve orchestration notları

## Özet Bulgular
- **Para kazanan şey “100 agent” demek değil; outcome paketlemek.** En güçlü gelir sinyalleri generic swarm framework'ten değil, deployment kolaylaştıran managed ürünlerden ve done-for-you hizmetten geliyor. RapidClaw, 2026-03-31 tarihli Indie Hackers postunda **~$2K MRR**, **68 paying customer**, **%4 churn** ve **$29/ay** fiyatla bunu açıkça gösteriyor.
- **Multi-agent zaten niş oyuncak değil ama hâlâ default da değil.** Anthropic’in 2026 raporunda organizasyonların **%57’si** agent’ları multi-stage workflow’larda, **%16’sı** ise cross-functional süreçlerde kullanıyor. Aynı raporda **%80** measurable ROI gördüğünü söylüyor. Talep gerçek; ama herkes swarm kurmuyor.
- **Production’da kazanan pattern “gevşek network” değil, kısıtlı supervisor/hierarchical + explicit state + verifier.** Vercel’in d0 örneğinde tool sayısını sert biçimde azaltmak başarıyı **%80 → %100** yaptı; ortalama süre **274.8s → 77.4s**, token tüketimi **~102K → ~61K** düştü. LangChain’in resmi multi-agent anlatımında da loose network’lerin prod’da pahalı ve güvenilmez olduğu açık söyleniyor.
- **Swarm’lerin en büyük düşmanı model zekâsı değil, koordinasyon vergisi.** 2026 arXiv büyük ölçekli çalışma, 8 framework’te **42K+ commit** ve **4.7K+ resolved issue** inceliyor; issue’ların **%22’si bug**, **%14’ü infra**, **%10’u coordination**. Yani sorun fikirde değil, bakımda.
- **Gerçek başarı hikâyelerinde ortak tema: trust layer.** OpenClaw deneyinde ürün ilk 12 günde sıfır satış yaptı; pivot sonrası bilgi satmak yerine “ben kurarım” demeye başlayınca **15. günde $600+** gelir geldi. İnsanlar swarm’in şiirini değil, çalışan sonucu satın alıyor.

## Gerçek Başarı Hikayeleri

### 1) Vercel d0 — daha az tool ile daha iyi agent
- Vercel, 2025-12-22 tarihli resmi blogunda internal text-to-SQL agent’ı için tool setini sert biçimde sadeleştirdi.
- Sonuçlar:
  - Başarı: **4/5 (%80) → 5/5 (%100)**
  - Ortalama süre: **274.8s → 77.4s** (**3.5x hızlı**)
  - Ortalama token: **~102K → ~61K** (**%37 düşüş**)
  - En kötü senaryo: eski akış **724 saniye**, **145,463 token** yakıp fail; yeni akış **141 saniye**, **67,483 token** ile success.
- Ders: iyi swarm mimarisi bazen daha fazla agent/tool değil, daha az karar yüzeyi demek.

### 2) AWS + CrewAI — enterprise pilotlarda ölçülebilir operasyon kazancı
- AWS Prescriptive Guidance, CrewAI ile Bedrock üzerinde kurulan pilotları resmi örnek olarak veriyor.
- Erken pilot sonuçları:
  - büyük code modernization projesinde **%70 daha hızlı execution**
  - CPG back-office akışında yaklaşık **%90 processing time reduction**
- Ek sinyal: observability stack (CloudWatch, AgentOps, LangFuse) ve compliance guardrails özellikle vurgulanıyor.
- Ders: multi-agent satışının anahtarı framework değil; enterprise-grade traceability + guardrail + template.

### 3) Kimi Agent Swarm — paralel araştırma için ürünleşmiş performans vaadi
- Kimi’nin resmi blogu Agent Swarm’ın:
  - **100 sub-agent**'a kadar paralel çalışabildiğini,
  - **1,500+ tool call** yürütebildiğini,
  - sequential execution’a göre **4.5x daha hızlı** sonuç verdiğini söylüyor.
- Verilen örnekler: 100 niş YouTube alanı için creator avı, **200+** Paul Graham essay derleme, **40 PDF**'den **100 sayfalık** literature review.
- Ders: swarm özellikle broad research, batch processing, multi-perspective synthesis ve long-form üretimde parlıyor.
- Not: bu bir vendor-owned benchmark; gerçek maliyet ve failure rate sayıları açıklanmıyor.

### 4) RapidClaw — swarm/deployment karmaşasını ürün yapan managed servis
- 2026-03-31 tarihli Indie Hackers postu:
  - **~$2K MRR**
  - **68 paying customer**
  - **%4 monthly churn**
  - fiyat: **$29/mo** ve plana **$10 AI token** dahil
  - signupların **~%30**'u tek bir pratik blog postundan geliyor.
- Kurucunun şaşırtıcı bulduğu asıl kullanıcı kitlesi developer değil; **küçük ajans sahipleri**.
- Ders: “agent kurma” acısını çözmek, “en zeki swarm runtime” satmaktan daha kolay para kazanıyor.

### 5) OpenClaw / Idiogen deneyi — kurs değil, kurulum sat
- Reddit’te paylaşılan 60 günlük deneyde agent:
  - ilk 12 günde **0 satış** gördü,
  - **400+ unique visitor** aldı,
  - pivot sonrası bir günde **695 pageview** yakaladı,
  - **15. günde $600+** revenue üretti.
- Kritik pivot: 58,000 kelimelik guide satmaya çalışmak yerine “done-for-you AI agent setup service”e geçiş.
- Aynı postta sistemin **4 sub-agent**’a bölündüğü yazıyor: social, analytics, customer monitoring, creative.
- Ders: info product güven vermiyor; DFY kurulum, support ve ownership verince dönüşüm geliyor.

### 6) Cloudflare multi-agent community build — güçlü POC, düşük default trust
- Reddit / GitHub örneğinde kurucu, Claude Code ile **16 AI agent**, **4 team**, **4 worker**, **387 passing test**, yaklaşık **4,500 satır TypeScript** + **3,000 satır React/JS** ürettiğini ve bunun için **$1,000 Claude Code credits** harcadığını paylaşıyor.
- Teknik olarak etkileyici; topluluk tepkisi ise sert: yorumlarda “yolo mode”, “janky UI” ve güven eksikliği baskın.
- Ders: teknik throughput tek başına satış yaratmaz. Güven, polish, scope sınırı ve observability olmazsa swarm demosu kolayca “şov” gibi algılanıyor.

## Pazar Büyüklüğü & Fırsat
- Grand View Research’e göre global AI agents pazarı **2025’te $7.63B**, **2026’da $10.91B**, **2033’te $182.97B** ve **%49.6 CAGR**. Bu büyüme gerçek ama önemli detay şu: **single-agent systems 2025’te %59.24 revenue share** ile hâlâ baskın.
- Aynı rapor multi-agent sistemlerin “significant growth” göreceğini söylüyor. Yani pazar swarm’a gidiyor ama henüz “her iş çok agentlı” noktada değil.
- Anthropic raporunda:
  - **%57** multi-stage workflow kullanımı
  - **%16** cross-functional / end-to-end kullanım
  - **%80** measurable economic impact
  - en büyük bariyerler: **%46 integration**, **%42 data quality**, **%43 implementation cost**
- Çıkan net fırsat: “genel swarm platformu” satmak zor. **Narrow ROI lane** satmak kolay. Yani research swarm, browser QA swarm, lead-intelligence swarm, deployment/setup service gibi net output’lar daha mantıklı.

## Rakipler & Boşluklar

### Framework ve tooling tarafı kalabalık
- GitHub search snapshot’ında:
  - **MetaGPT** yaklaşık **67.3K★**
  - **CAMEL** yaklaşık **16.7K★**
  - **MindSearch** yaklaşık **6.8K★**
  - orchestration tarafında **mission-control** yaklaşık **4.2K★**
  - swarm tarafında **ruflo** yaklaşık **32.6K★**, **ClawTeam** yaklaşık **4.9K★**
- Sonuç: framework kıtlığı yok. Yeni bir generic swarm runtime daha çıkarmak neredeyse kesin olarak yanlış savaş.

### Boşluklar
- **Boşluk #1 — trust/governance wrapper:** insanlar raw agent değil; approval, log, rollback, observability ve “kim ne yaptı?” cevabı istiyor.
- **Boşluk #2 — deployment simplicity:** RapidClaw örneği gösteriyor ki asıl acı orchestration teorisi değil, ayakta tutma işi.
- **Boşluk #3 — verticalized outcome packs:** “AI agent platform” yerine “HS code report swarm”, “local business leak audit swarm”, “browser QA swarm” gibi net deliverable daha satılabilir.
- **Boşluk #4 — hybrid human gate:** yorumlar ve enterprise guidance aynı şeyi söylüyor: para, public output, customer-facing actions ve compliance tarafında insan kapısı şart.

## Teknik Gereksinimler
- **Task router:** her iş swarm’a gitmemeli. Single-agent / supervisor / hierarchical / deterministic workflow ayrımı şart.
- **Kısıtlı tool yüzeyi:** LangChain videosunda tek agent için **5-10 tool** sweet spot olarak anılıyor. Tool patlaması hem maliyet hem saçmalık üretir.
- **Shared state + artifact store:** agent’lar ya ortak state üzerinden ya da tool-call parametreleriyle haberleşmeli; “herkes her şeyi biliyor” modeli çürük.
- **Verifier / critic layer:** diğer agent çıktısını kontrol eden QA/verifier olmadan swarm hızlı ama kör olur.
- **Observability:** token, latency, retry, failure reason, run graph, human override log.
- **Budget guardrail:** Kimi ve Cloudflare örnekleri gösteriyor ki parallelism güzel ama cüzdan yakar.
- **Public-action gate:** email, post, ödeme, deployment, destructive command gibi aksiyonlar insan onayı görmeli.
- **Content/trust assets:** demo, case study, audit raporu, guide, onboarding dokümanı. Satış motoru bunlar.

## Ham Notlar
- `projeler.txt` içindeki en değerli yerel sinyal, doğrudan “Claude Code ile 16 agent / 4 team” deneyimi ve Vercel self-verifying agent notları oldu; yani bu repo zaten teori değil, pratik swarm damarına bakıyor.
- Reddit/Indie Hackers katmanı çok net bir şey söyledi: **swarm ürün değil, arka mutfak.** Müşteri ön tarafta hız, kurulum, sonuç ve support görüyor.
- IBM ve LangChain anlatımlarında multi-agent’ın güçlü olduğu alanlar aynı: domain specialization, long-horizon tasks, parallel research, multi-perspective evaluation.
- LangChain tarafında gevşek agent network’lerine prod için soğuk durulması önemli. Bu, UniverseCreator’ın gelecekte “open-ended swarm” değil, **router + supervisor + verifier** çizgisine gitmesi gerektiğini doğruluyor.
- Şaşırtıcı ama mantıklı sonuç: bazen en iyi swarm tasarımı, daha az tool, daha az agent, daha net rol ve daha iyi log.
