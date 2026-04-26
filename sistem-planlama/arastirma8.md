# Araştırma #8 — Multi-Agent Architecture Patterns
**Tarih:** 2026-04-21 07:21 +03
**Konu:** Production-grade multi-agent mimariler, framework farkları, gerçek implementasyon pattern'leri ve UniverseCreator için uygulanabilir orchestration modeli.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma0-7.md` / `planlama0-7.md`, `STATE_SUMMARY.json`
- LangGraph repo: https://github.com/langchain-ai/langgraph
- LangGraph multi-agent workflows: https://www.blog.langchain.com/langgraph-multi-agent-workflows/
- LangGraph `Command` / handoff yazısı: https://www.blog.langchain.com/command-a-new-tool-for-building-multi-agent-architectures-in-langgraph
- LangGraph Platform GA: https://blog.langchain.com/langgraph-platform-ga
- LangChain Vodafone case study: https://www.langchain.com/blog/customers-vodafone
- LangChain Kensho case study: https://www.langchain.com/blog/customers-kensho
- LangChain Minimal case study: https://www.langchain.com/blog/how-minimal-built-a-multi-agent-customer-support-system-with-langgraph-langsmith
- CrewAI repo: https://github.com/crewAIInc/crewAI
- CrewAI Flows: https://www.crewai.com/crewai-flows
- CrewAI Quickstart: https://docs.crewai.com/en/quickstart
- CrewAI OSS 1.0 GA: https://blog.crewai.com/crewai-oss-1-0-we-are-going-ga/
- CrewAI Gelato case study: https://www.crewai.com/case-studies/gelato-accelerates-fulfillment-via-agentic-integration
- CrewAI PwC case study: https://www.crewai.com/case-studies/pwc-accelerates-enterprise-scale-genai-adoption-with-crewai
- Microsoft AutoGen repo: https://github.com/microsoft/autogen
- Microsoft Agent Framework repo: https://github.com/microsoft/agent-framework
- OpenAI Swarm repo: https://github.com/openai/swarm
- OpenAI Agents SDK repo: https://github.com/openai/openai-agents-python
- GitHub repos: https://github.com/langchain-ai/open-swe , https://github.com/ComposioHQ/agent-orchestrator , https://github.com/cj-vana/claude-swarm , https://github.com/kingbootoshi/codex-orchestrator , https://github.com/kayba-ai/agentic-context-engine , https://github.com/paperclipai/paperclip , https://github.com/wshobson/agents , https://github.com/ruvnet/ruflo , https://github.com/simstudioai/sim
- Reddit: https://reddit.com/r/ClaudeCode/comments/1qbdcqx/update_claude_swarm_now_has_58_mcp_tools_protocol/ , https://reddit.com/r/SideProject/comments/1rl7q1j/i_built_an_open_source_command_center_for_ai/ , https://reddit.com/r/LangChain/comments/1mau9lx/anyone_actually_using_a_good_multi_agent_builder/ , https://reddit.com/r/LocalLLaMA/comments/1snp1r5/crewai_broke_my_agents_yesterday/
- ArXiv: https://arxiv.org/abs/2408.09955 , https://arxiv.org/abs/2408.15247 , https://arxiv.org/abs/2511.00628 , https://arxiv.org/abs/2601.03624
- ACL MegaAgent page: https://aclanthology.org/2025.findings-acl.259/
- YouTube/MCPTube: https://www.youtube.com/watch?v=4nZl32FwU-o , https://www.youtube.com/watch?v=sWH0T4Zez6I , https://www.youtube.com/watch?v=8HqeY5v0ohM

## Özet Bulgular
- **Production'da kazanan pattern serbest swarm değil.** LangChain'in resmi konsept videosu ve blog'u aynı yere geliyor: gevşek peer-to-peer ağlar demo'da havalı, prod'da ise pahalı ve güvenilmez. Kazanan yapı genelde **deterministik omurga + uzman alt ajanlar + açık handoff/state + güçlü gözlemlenebilirlik**.
- **Pazar geçen yıl ciddi biçimde ayrıştı.** 2026-04-21 itibarıyla GitHub'da AutoGen **57,252★** ama bakım modunda; Microsoft Agent Framework **9,646★** ile onun production-ready halefi. CrewAI **49,360★**, LangGraph **29,788★**, OpenAI Agents SDK **24,064★**. Swarm ise **21,357★** olsa da OpenAI README'sinde açıkça “educational/experimental” ve production için Agents SDK öneriliyor.
- **Gerçek prod sinyali var.** LangGraph ekibi 14 Mayıs 2025'te platformu beta'dan GA'ye geçirirken “beta'dan beri üretimde ajan deploy eden şirket sayısı neredeyse **400**” diyor. CrewAI Ekim 2025 GA yazısında **1.4B agentic execution**, **1.8M+ aylık indirme** ve **Fortune 500'ün %60+** kullanımını iddia ediyor. Bunlar vendor claim; ama kategorinin oyuncak olmadığını gösteriyor.
- **Araştırma cephesi tek şeyi bağırıyor:** büyük sistemler için yalnızca “çok ajan” yetmez; **dinamik decomposition + monitoring (MegaAgent)**, **rollback/branching (AgentGit)**, **görsel debug/eval (AutoGen Studio)** ve **formal governance/protocol (Architecting Agentic Communities)** gerekiyor.
- **Community tarafı da romantizmi kesmiş durumda.** Reddit ve modern code-agent repo'larında tekrar eden pattern şu: fazla soyut framework katmanı debugging'i öldürüyor. İnsanlar geri dönüp **JSON/file state + worktree isolation + ince bir orchestrator** kuruyor. Yani altyapı seçimi “en çok star kimde” oyunu değil; hata ayıklama ergonomisi oyunu.

## Gerçek Başarı Hikayeleri
- **LangGraph + Vodafone:** Vodafone, 340M+ müşterili telekom ölçeğinde iki iç AI asistanını LangChain/LangGraph ile kurmuş. Çok ajanlı tarafta modüler subgraph'lar, API entegrasyonu ve workflow doğrulaması kullanmış; sonuç olarak kritik veri sorularında time-to-insight düşmüş ve yeni domain eklemek kolaylaşmış.
- **LangGraph + Kensho / S&P Global:** Kensho çok parçalı veri erişimini “Grounding router + specialized data retrieval agents” mimarisiyle toplamış. Kritik fikir yalnızca routing değil; ajanların birbirine konuştuğu **custom data retrieval protocol**. Bu sayede farklı veri ekipleri arasında güvenilir ve tek formatlı alışveriş sağlanmış.
- **CrewAI + Gelato:** Resmî vaka çalışmasına göre yeni bir carrier entegrasyonu **5 günden 10 dakikaya** inmiş, SKU mapping süreleri **>%90** kısalmış, carrier integration eforu da yaklaşık **%99** azalmış. Bu, “multi-agent sadece chat bot” masalını öldürüyor.
- **CrewAI + PwC:** PwC, CrewAI ile code-generation accuracy'nin yaklaşık **%10'dan %70+** seviyesine çıktığını söylüyor. Buradaki önemli ders accuracy artışı kadar monitoring/ROI görünürlüğü; ekip özellikle observability katmanını satın alma sebebi olarak anlatıyor.
- **MegaAgent (paper + ACL 2025):** MegaAgent, Gobang oyununu **800 saniye** içinde üretiyor ve policy simulation'da **590 ajana** kadar ölçekleniyor. Her production takımı 590 ajan kurmaz; ama “predefined SOP olmadan dinamik ajan üretimi + paralellik + monitoring” pattern'i önemli bir yön işareti.

## Pazar Büyüklüğü & Fırsat
- **Talep proxy'si olarak açık kaynak çekişi çok yüksek.** 2026-04-21 snapshot'ında `microsoft/autogen` **57.3k★**, `paperclipai/paperclip` **56.9k★**, `crewAIInc/crewAI` **49.4k★**, `wshobson/agents` **34.0k★**, `ruvnet/ruflo` **32.6k★**, `langchain-ai/langgraph` **29.8k★**, `simstudioai/sim` **27.8k★**, `openai/openai-agents-python` **24.1k★**. Yani “orchestration layer” artık niş değil, doğrudan ürün kategorisi.
- **LangGraph tarafında prod adoption açık.** 14 Mayıs 2025 GA duyurusunda beta'dan beri **yaklaşık 400 şirket** agent deploy etmiş görünüyor. Ayrıca platform seviyesinde 1-click deploy, **30 API endpoint**, persistence layer ve horizontal scaling vurgusu var.
- **CrewAI tarafında enterprise positioning agresif.** 20 Ekim 2025 GA post'u **1.4B execution**, **1.8M+/ay download**, **%60+ Fortune 500** ve “thousands of engineers” kullanımını öne çıkarıyor. Pazarlama dozu yüksek ama kategoriye kurumsal bütçe girdiği net.
- **Kod ajanı orkestrasyonu ayrı alt pazar oldu.** `open-swe`, `agent-orchestrator`, `claude-swarm`, `codex-orchestrator`, `paperclip`, `wshobson/agents` gibi repo'lar 2025-2026'da patladı. Bu da şunu söylüyor: insanlar yalnızca “AI ajan” değil, **ajanları yöneten yönetim katmanını** satın alıyor/yapıyor.
- **UniverseCreator için fırsat dış pazar kadar iç pazar.** `STATE_SUMMARY.json` 2026-04-21 snapshot'ında **113 aktif**, **86 live**, **23 healthy** gösteriyor. Bu kadar düşük health ile daha fazla paralellik kör takviye olur. Doğru orchestration burada doğrudan gelir çarpanı; bozuk üretim hattını büyütmek aptallık.

## Rakipler & Boşluklar
- **LangGraph:** En güçlü tarafı state ve transition kontrolü. Custom cognitive architecture isteyenler için iyi. Zayıf tarafı: ilk kurulumda daha fazla mühendislik disiplini istiyor.
- **CrewAI:** Hızlı başlamak için çekici; resmi dokümantasyon bile production için “Flows owns state/execution order, agents work inside” diyor. Yani CrewAI'nin kendisi bile aslında gevşek swarm değil, **dışta deterministik flow** öneriyor.
- **OpenAI Agents SDK:** Hafif, güçlü, handoff/guardrail/HITL/tracing/MCP uyumlu. Swarm'dan production'a geçiş için mantıklı. Özellikle ağır graph framework istemeyen ekipler için iyi default.
- **Microsoft Agent Framework:** AutoGen'in lessons learned versiyonu gibi. .NET + Python, A2A + MCP, middleware ve OpenTelemetry ile enterprise yönelimli. Yeni işte AutoGen başlamak pek akıllıca görünmüyor.
- **Code-agent orchestrator'lar:** Composio Agent Orchestrator, Claude Swarm, Codex Orchestrator, Open-SWE, Paperclip vb. tarafında pattern aynı: **git worktree isolation, CI/review loops, dashboard, persistent state**. Bu dünya iş akışı otomasyonuna değil, “paralel üretim”e optimize.
- **Büyük boşluk:** pek çok çözüm ya aşırı soyut ya da aşırı ham. Eksik olan şey **ince ama disiplinli orchestration layer**: task contract + state/checkpoint + worktree isolation + eval/rollback + learning loop. Çoğu takım burada kendi çözümünü yazıyor.
- **İkinci boşluk:** framework seçmek yerine **task-classification matrix** kuran ekip az. Halbuki her işe multi-agent gerekmez. Basit işleri tek ajan, orta işleri supervisor, yüksek riskli işleri deterministic workflow + isolated worker ile çözmek daha mantıklı.

## Teknik Gereksinimler
- **Açık görev sözleşmesi:** her run için `goal`, `inputs`, `definition_of_done`, `allowed_tools`, `timeout`, `verify step` zorunlu olmalı.
- **Kalıcı state/checkpoint:** LangGraph persistence, CrewAI flows state, AgentGit rollback, claude-swarm persistent state — hepsi aynı şeyi söylüyor. Bellek yoksa tekrar tekrar duvara toslarsın.
- **İletişim modeli seçimi:** shared scratchpad mi, tool-call parametresi mi, yoksa explicit handoff mu? Bunu baştan belirlemek şart. “Ajanlar konuşsun bakarız” prod tasarımı değil.
- **Araç sınırı ve uzmanlaşma:** LangChain'in resmi multi-agent videosu tek ajana **5-10 araç** civarının üstünü riskli görüyor. Araç seti büyüdükçe routing kalitesi düşüyor.
- **Observability + eval:** tracing, node latency, routing accuracy, tool failure rate, rollback rate, token/run, human intervention rate. Bunlar yoksa sistem çalışıyor sanırsın; aslında çürüyor olur.
- **Rollback ve branching:** AgentGit'in ana katkısı önemli: hata anında commit/revert/branch yoksa büyük swarm'lar hata biriktirir. Coding tarafında git worktree bunun pratik karşılığı.
- **Human-in-the-loop ve governance:** IBM videosu ve `Architecting Agentic Communities` paper'ı daha fazla ajan = daha fazla unpredictability diyor. İnsan onay kapıları, policy/protocol ve audit izi zorunlu.
- **Heterogeneous runtime desteği:** model/provider/tool bağımsızlığı önemli. OpenAI Agents SDK, Microsoft Agent Framework ve modern orchestration repo'larının çoğu provider-agnostic veya multi-provider gidiyor.

## Ham Notlar
- `ddgr` bu cycle'da yine boş döndü (`[]`). Formal step'i uyguladım ama sonuç yok; asıl bilgi Jina/web, GitHub API, Reddit JSON, ArXiv abstraktları ve MCPTube'dan geldi.
- `gh search repos` burada fiilen boş çıktı. GitHub araştırmasını `gh api search/repositories` fallback'i ile tamamladım. Aynı işi farklı kabukla yapıp devam ettim; boş bakıp durmadım.
- `mcp__arxiv__search_papers` rate-limit yedi ama `get_abstract` ile hedef paper ID'lerde devam etmek mümkün oldu. Yani arayüz kırıldı diye araştırma bitmiyor.
- Product Hunt Jina üzerinden **403 / security verification** verdi. Denedim; kapı duvar. Bu cycle için kritik kayıp değil.
- MCPTube `parallel_add.py` başarılı döndü ama yeni videolar MCP library listesinde görünmedi; bu yüzden transcript işi için `add_video` tool'unu ayrıca kullandım. İnce ama gerçek bir entegrasyon sürtünmesi.
- Net hüküm: **UniverseCreator'ın ihtiyacı “daha fazla ajan” değil; daha iyi orchestration disiplini.** Serbest konuşan ajan kalabalığı değil, ölçülen ve geri alınabilen görev akışı lazım.
