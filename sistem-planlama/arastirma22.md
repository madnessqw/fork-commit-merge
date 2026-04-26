# Araştırma #22 — Multi-Agent Architecture Patterns
**Tarih:** 2026-04-21 17:19 +03
**Konu:** Production-grade multi-agent mimariler için 2. tur / 2026 doğrulama. Bu tur odak: hangi pattern gerçekten prod'da kazanıyor, framework kayması nereye gidiyor, coding swarm için hangi yapı uygulanabilir, observability/eval neden artık opsiyon değil.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma8.md` / `planlama8.md`, `STATE_SUMMARY.json`
- ddgr sorguları:
  - `multi agent architecture production case study 2025`
  - `llm multi agent framework comparison 2025`
  - `AI agents market size 2025 multi agent`
  - **Not:** Bu turda üçü de `[]` döndü; fallback olarak web/Jina/Reddit/GitHub/ArXiv/MCPTube kullanıldı.
- Resmî / pazar / dokümantasyon:
  - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  - https://openai.github.io/openai-agents-python/handoffs/
  - https://openai.github.io/openai-agents-js/guides/multi-agent/
  - https://learn.microsoft.com/en-us/agent-framework/overview/
  - https://github.com/microsoft/autogen
  - https://www.microsoft.com/en-us/research/project/autogen/
  - https://www.langchain.com/state-of-agent-engineering
  - https://www.langchain.com/langgraph
  - https://blog.langchain.com/command-a-new-tool-for-building-multi-agent-architectures-in-langgraph/
  - https://langchain-ai.github.io/langgraphjs/reference/modules/langgraph-supervisor.html
  - https://blog.langchain.com/langgraph-platform-ga
  - https://docs.crewai.com/
  - https://docs.crewai.com/en/concepts/collaboration
  - https://www.grandviewresearch.com/industry-analysis/ai-agents-market-report
  - https://www.deloitte.com/global/en/about/press-room/deloitte-globals-2025-predictions-report.html
  - https://www.capgemini.com/gb-en/news/press-releases/trust-and-human-ai-collaboration-set-to-define-the-next-era-of-agentic-ai-unlocking-450-billion-opportunity-by-2028/
- LangChain vaka çalışmaları:
  - https://blog.langchain.com/customers-klarna/
  - https://www.langchain.com/blog/customers-docentpro
  - https://www.langchain.com/blog/customers-tradestack
- Product Hunt / ürün sinyalleri:
  - https://www.producthunt.com/products/agentx
  - https://www.producthunt.com/posts/agent-development-kit
  - https://www.producthunt.com/posts/multi-agent-builder
  - https://www.producthunt.com/products/angy
  - https://www.producthunt.com/products/crewai-3
- Reddit JSON API:
  - https://reddit.com/r/LocalLLaMA/comments/1n6epwv/my_weekend_project_accidentally_beat_claude_code/
  - https://reddit.com/r/LocalLLaMA/comments/1qnjota/i_built_a_hive_mind_for_claude_code_7_agents/
  - https://reddit.com/r/LangChain/comments/1m8vo19/i_wrote_an_ai_agent_with_langgraph_that_works/
- GitHub:
  - https://github.com/FoundationAgents/MetaGPT
  - https://github.com/bytedance/deer-flow
  - https://github.com/microsoft/autogen
  - https://github.com/crewAIInc/crewAI
  - https://github.com/langchain-ai/langgraph
  - https://github.com/openai/openai-agents-python
  - https://github.com/ComposioHQ/agent-orchestrator
  - https://github.com/cj-vana/claude-swarm
  - https://github.com/kingbootoshi/codex-orchestrator
  - https://github.com/kayba-ai/agentic-context-engine
- ArXiv / akademik:
  - https://arxiv.org/abs/2408.09955
  - https://arxiv.org/abs/2412.05449
  - https://arxiv.org/abs/2408.15247
  - https://arxiv.org/abs/2601.07136
  - https://arxiv.org/abs/2308.00352
- YouTube / MCPTube:
  - https://www.youtube.com/watch?v=sWH0T4Zez6I
  - https://www.youtube.com/watch?v=4nZl32FwU-o
  - https://www.youtube.com/watch?v=8HqeY5v0ohM

## Özet Bulgular
- **Prod'da kazanan pattern serbest swarm değil.** OpenAI'nin pratik kılavuzu, Microsoft Agent Framework'in “agent vs workflow” ayrımı ve LangChain'in resmi multi-agent anlatısı aynı yere çıkıyor: açık uçlu işlerde ajan olabilir, ama kritik iş akışında **deterministik omurga + uzman alt ajanlar + açık handoff/state + insan kapıları** gerekiyor. “Ajanlar birbirine route etsin, bir şey olur” yaklaşımı pahalı ve gevşek.
- **Framework peyzajı ciddi biçimde kaydı.** `microsoft/autogen` hâlâ **57,285★**, ama repo açıkça maintenance mode diyor ve yeni projeleri Microsoft Agent Framework'e yönlendiriyor. Aynı anda `langchain-ai/langgraph` **29,860★**, `openai/openai-agents-python` **24,274★**, `crewAIInc/crewAI` **49,412★**. Yani pazar “ilk jenerasyon sohbet eden ajan topluluğu”ndan “kontrollü orchestration + tracing + deployment” eksenine kaymış durumda.
- **Observability artık opsiyon değil, giriş bileti.** LangChain'in 2026 survey'inde ajan kullanan ekiplerin **%57.3**'ü üretimde; **%89**'u observability kurmuş, **%62**'si detaylı tracing kullanıyor. En büyük blocker kalite (**%32**), sonra latency (**%20**). Enterprise'ta güvenlik ayrıca büyüyor. Kısacası trace yoksa prod da yok.
- **Gerçek iş sonuçları var; ama hepsi kontrol ve görünürlükle geliyor.** Klarna'nın AI assistant'ı **2.5M konuşma**, **700 FTE eşdeğeri** ve ortalama çözüm süresinde **%80 düşüş** raporluyor. DocentPro, modüler çok ajanlı seyahat sistemini LangGraph'a **2 günde** port edip **12 dil** destekli audio-guide zinciri kurmuş. Tradestack, **6 haftada** MVP çıkarıp supervisor node + LangSmith tracing ile **2 hafta** iç test süresi kazanmış.
- **Community tarafı hype'tan ayık.** Reddit'te “Claude Code'ı geçen weekend multi-agent coder” post'u 3 rollü mimariyle **%36.0 başarı** gördüğünü söylüyor; ama Sonnet-4 ile **93.2M token** yakmış. Başka bir postta 7 ajanlı “hive mind” kuran geliştirici, SQLite + FTS5 memory + message bus kurmasına rağmen debug'ın işkence olduğunu yazıyor. Ders net: koordinasyon var diye ekonomi otomatik düzelmiyor.
- **GitHub canlılığı çok yüksek ve yeni kuşak repo'lar doğrudan senin use-case'ine dokunuyor.** 2026-04-21 snapshot'ında `FoundationAgents/MetaGPT` **67,309★**, `bytedance/deer-flow` **63,182★**, `microsoft/autogen` **57,285★**, `crewAIInc/crewAI` **49,412★**, `langchain-ai/langgraph` **29,860★**, `openai/openai-agents-python` **24,274★**. Daha niş ama önemli katmanlar: `ComposioHQ/agent-orchestrator` **6,400★**, `kingbootoshi/codex-orchestrator` **273★**, `cj-vana/claude-swarm` **109★**. Büyük framework kadar “coding swarm harness” da ayrı ürün kategorisine dönüşmüş.

## Gerçek Başarı Hikayeleri
- **Klarna + LangGraph/LangSmith (resmî vaka):** Klarna'nın case study'si **85M aktif kullanıcı**, **2.5M günlük işlem**, **2.5M konuşma** ve yaklaşık **700 tam zamanlı çalışan eşdeğeri** operasyon yükünün AI assistant tarafından taşındığını söylüyor. Etki tarafında ortalama müşteri çözüm süresi **%80** kısalmış ve tekrarlı destek işlerinin yaklaşık **%70**'i otomasyona geçmiş.
- **DocentPro + LangGraph (resmî vaka):** DocentPro, gezi planlama için attractions/restaurants/hotels/activities şeklinde modüler ajanlar kurmuş. Aynı ajanlar hem itinerary hem sohbet kanalında tekrar kullanılıyor. Ayrıca audio-guide sistemini LangGraph'a **2 günde** taşıyıp **12 dil** destekli map-reduce zinciri kurmuşlar. Kritik ders: tekrar kullanılabilir ajan + trace/replay kombinasyonu prod hızını artırıyor.
- **Tradestack + LangGraph (resmî vaka):** WhatsApp tabanlı ajan MVP'si **6 haftada** çıkmış. Başlangıçta hierarchical multi-agent + supervisor node kullanmışlar; LangGraph Studio sayesinde flaw'ları erken görüp **2 hafta** iç test zamanı kazanmışlar. Node-level eval ile planning node için model seçimi bile optimize edilmiş.
- **Klarna dışında ikinci güçlü pattern: observability-first delivery.** Hem Klarna hem DocentPro hem Tradestack anlatılarında ortak nokta framework adı değil, trace ve eval döngüsü. Bu tekrar eden sinyal önemli; çünkü framework pazarlaması değil, prod davranışı anlatıyor.
- **Community self-report — TerminalBench multi-agent coder:** r/LocalLLaMA'daki self-report'a göre orchestrator + explorer + coder mimarisi Stanford TerminalBench'te **%36.0** başarıyla Claude Code'ın önüne geçmiş. Ama aynı post maliyet tarafında Sonnet-4 için **93.2M token** yaktığını da söylüyor. Yani başarı var, ama “ucuz ve kolay” değil.
- **Araştırma benchmark'ı — MegaAgent:** `MegaAgent` paper'ı Gobang oyununu **800 saniyede** üretip policy simulation'da **590 ajana** kadar ölçeklenmiş. Bu ticari vaka değil; ama SOP'suz dinamik ajan üretimi + paralel execution + monitoring kombinasyonunun ciddi bir yön işareti.

## Pazar Büyüklüğü & Fırsat
- **Pazar hızla büyüyor, ama rakamlar analist tahmini.** Grand View Research'e göre global AI agents pazarı **2025'te $7.63B**, **2033'te $182.97B** ve **%49.6 CAGR**. Bu sayılar vendor/analist estimate; ama kategori büyüklüğünü kabaca gösteriyor.
- **Kurumsal adoption da kâğıt üstünde değil.** Deloitte'nin 2025 öngörüsü, GenAI kullanan enterprise'ların **%25**'inin 2025 içinde AI agents deploy edeceğini, bunun **2027'de %50**'ye çıkacağını söylüyor.
- **Ekonomik fırsat büyük, ama trust açığı da büyüyor.** Capgemini, 2028'e kadar AI agents için **$450B** ekonomik değer potansiyeli görüyor. Aynı sayfa, fully autonomous agents'a güvenin son bir yılda **%43'ten %27'ye** düştüğünü ve etkili human-agent collaboration'ın yüksek değerli işlere ayrılan insan zamanını **%65** artırabileceğini söylüyor. Yani market fırsatı var, ama “tam otonom bırak gitsin” güvenmiyor.
- **Prod tarafı artık niş değil.** LangChain'in 2026 survey'inde üretimde ajan kullanan oran **%57.3**. 10k+ çalışanlı şirketlerde bu oran **%67**. En yaygın kullanım customer service (**%26.5**) ve research/data analysis (**%24.4**). Bu, UniverseCreator'ın hem iç research-planning hattı hem dış agent-ops ürünü için doğrudan alakalı.
- **Product Hunt tarafı da kategoriye para kokusu geldiğini gösteriyor.** AgentX 2.0, **16 Haziran 2025** lansmanında haftanın **#3**, günün **#2** ürünü olmuş. Google ADK 2025'te “multi-agent systems” için ayrı hunt almış. Credal'ın Multi-Agent Builder lansmanı **20 Mart 2025**'te günün **#5**'i. 2026 tarafında Angy, çok ajanlı coding pipeline'ını ayrı ürün diliyle satıyor. Framework → orchestration product dönüşümü net.
- **UniverseCreator iç fırsatı da küçümsenmemeli.** `STATE_SUMMARY.json` 2026-04-21 snapshot'ında **113 aktif ürün** ve **99 live ürün** gösteriyor. Bu ölçekten sonra orchestration artık lüks değil; kalite, sağlık ve shipping hızı için iç çarpan.

## Rakipler & Boşluklar
- **LangGraph:** En büyük gücü state, graph ve long-running durability. Hierarchical supervisor, memory, checkpoint ve human-in-the-loop ihtiyaçlarında güçlü. Zayıf yanı: rahat ama gevşek değil; biraz mühendislik disiplini istiyor.
- **OpenAI Agents SDK:** Hafif, code-first, handoff/tool pattern'leri net. OpenAI'nin kendi kılavuzu da code orchestration'ın LLM orchestration'a göre hız/maliyet/tahmin edilebilirlik açısından daha deterministik olduğunu söylüyor. İnce orchestration katmanı için güçlü aday.
- **CrewAI:** Ergonomik ve hızlı başlatıyor; collaboration sayfası delegasyonu çok görünür kılıyor. Ama dokümanında bile “agents not collaborating” başlığı var ve `allow_delegation=True` şart. Yani prod'da yine discipline gerekiyor; sihirli takım oyunu yok.
- **Microsoft Agent Framework:** AutoGen + Semantic Kernel derslerini birleştiren enterprise successor. Workflows, checkpointing, middleware, telemetry ve MCP/A2A uyumu güçlü. Ama UniverseCreator için hemen default olmak zorunda değil; .NET/Azure/enterprise interop tarafı ağırsa anlamlı.
- **AutoGen:** Yeni çekirdek için yanlış taban. Repo'nun kendisi maintenance mode diyor. AutoGen geçmişte öncüydü; şimdi lesson-learned statüsünde.
- **deer-flow / MetaGPT / coding orchestrator'lar:** `deer-flow` ve `MetaGPT` büyük ölçekli “superagent company” yönünü temsil ederken `agent-orchestrator`, `codex-orchestrator`, `claude-swarm` gibi repo'lar gerçek üretim ihtiyacını daha dürüst anlatıyor: task planning, parallel workers, CI fix, merge conflicts, persistent state, worktree isolation.
- **Asıl boşluk:** çoğu çözüm ya fazla soyut framework dini, ya da fazla ham shell script. Eksik olan şey **ince ama sert orchestration katmanı**: task contract + topology seçimi + shared state/checkpoint + eval/rollback + maliyet/latency guardrail.
- **İkinci boşluk:** “Her işe multi-agent” safsatasını kıran task matrix'i az ekip yapıyor. Oysa Microsoft açıkça “fonksiyon yazabiliyorsan agent kurma” diyor; LangChain videosu da tek ajan için **5-10 tool** üstünün bozulduğunu anlatıyor. Task-classification matrix olmayan swarm, token sobasıdır.

## Teknik Gereksinimler
- **Task-topology matrix:** her işi önce sınıflandırmak şart. `single-agent`, `supervisor`, `hierarchical`, `parallel committee`, `deterministic workflow` ayrımı olmadan herkes her işe ajan salıyor.
- **Açık görev sözleşmesi:** `goal`, `inputs`, `definition_of_done`, `allowed_tools`, `timeout`, `verify gate`, `human escalation rule` alanları zorunlu olmalı.
- **State / checkpoint disiplini:** LangGraph supervisor docs, Microsoft workflow yaklaşımı ve akademik çalışma aynı şeyi söylüyor: checkpoint yoksa uzun görevlerde yeniden başlama maliyeti patlıyor.
- **Mesaj geçmişi bütçesi:** LangGraph supervisor docs'ta `full_history` ve `last_message` ayrımı boşuna değil. Her ajan iç monoloğunu ortak konteks'e dökmek aptalca; mümkün olduğunda ortak state'e yalnızca final sonuçlar yazılmalı.
- **Araç bütçesi ve uzmanlaşma:** LangChain'in resmi multi-agent videosu tek ajan için yaklaşık **5-10 tool** bandını tatlı nokta diye veriyor. Tool seti büyüdükçe routing kararı bozuluyor; ajan bölmek o yüzden mantıklı hale geliyor.
- **Observability + eval:** trace, node latency, reroute rate, tool failure rate, token/run, human intervention rate, rollback rate, pass/fail rubric. LangChain survey'deki **%89 observability** ve **%52.4 eval** oranı tesadüf değil.
- **Coding swarm için izolasyon:** worktree/sandbox ownership şart. Niş coding orchestrator repo'larının neredeyse hepsi bu yöne kaymış. Aksi halde ajanlar birbirinin üstüne yazar, diff okunmaz, blame imkânsız olur.
- **HITL, güvenlik ve governance:** Capgemini güven düşüşünü, `2601.07136` paper'ı da issue'ların **%22 bug**, **%14 infra**, **%10 coordination** olduğunu gösteriyor. İnsan kapıları, rollback ve audit trail olmadan büyük sistem güven vermez.
- **Multi-model / multi-provider routing:** LangChain survey'de ekiplerin üçte ikisinden fazlası OpenAI kullansa da tek modele kilitlenen az. Prod'da complexity/cost/latency bazlı model seçimi norm olmuş durumda.

## Ham Notlar
- `ddgr` bu turda yine boş döndü. Formal step'i uyguladım; sonuç yok. Araştırmayı kilitlemek yerine fallback'lerle devam ettim.
- Product Hunt, Jina üzerinden Cloudflare/403 verdi. Buna rağmen indekslenmiş Product Hunt sayfaları üzerinden sinyal toplamak mümkün oldu.
- ArXiv `search_papers` bir noktada rate-limit yedi; hedef paper ID'leri `get_abstract` ile okuyup devam etmek daha verimli oldu.
- MCPTube tarafında bir video ingest listede görünmedi; iki ana video + mevcut comparison videosuyla transcript sentezini tamamladım.
- Net hüküm: **UniverseCreator'ın ihtiyacı daha fazla ajan değil; daha iyi orchestration disiplini.** Framework fanboyluğu yerine hybrid kernel gerekir.
