# Sistem Geliştirme Araştırması — 2026-04-22

Kısa hüküm:
- UniverseCreator için doğru yön **full-mesh swarm** değil; **deterministik control plane + uzman worker'lar + artifact-first handoff + sert verifier**.
- En büyük darboğaz model kalitesi değil; **uzun koşularda context/provenance/verifier eksikliği**.
- Kimi-k2.6 eklenirse onu genel koordinatör yapma; **büyük context, multimodal triage, compression ve retry/repair** işlerine ver.

## Araştırılan Keyword'ler (senin eklediklerin dahil)

Zorunlu keyword'ler:
- multi agent orchestration patterns
- network topology for agent systems
- process management in autonomous agents
- system management multi-agent
- subagents management patterns
- context sharing between agents
- decision system design AI agents
- system analyzer autonomous loop
- best way to plan agent workflows
- supervisor worker pattern LLM
- agent state machine design
- deterministic vs stochastic orchestration
- agent memory architecture (episodic, semantic, working)
- inter-agent communication protocols (MCP, A2A, ACP)
- agent handoff patterns
- parallel agent execution patterns
- agent failure recovery and resilience
- self-evolving agent systems
- agent observability and tracing
- cost optimization multi-model swarm
- context window management strategies
- tool calling efficiency patterns
- agent specialization vs generalization tradeoffs

Kullanıcı ekleri:
- Topology Matrix
- Task Contract
- Run Ledger
- Verifier Layer
- Self-Evolving Loop

Sistemi okuyunca eklediğim eksik ama kritik başlıklar:
- budget-aware routing / model router
- artifact provenance & replay
- rollback / checkpoint / time-travel
- self-modification safety / governance

## Bulgular (keyword'e göre organize)

### Mevcut sistemden çıkan sinyal
- 2026-04-22 tarihli `STATE.json` sisteminizin **portfolio state** tuttuğunu gösteriyor: `cycle=1065`, `active_count=122`, `deploy_missing_or_bad_url=6`.
- `scripts/codex_loop.sh` + `tmux` + `scripts/refresh_codex_context.py` zaten **autonomous loop + context refresh** yapıyor.
- `PROMPT.txt` ve `SOUL.md` açıkça **state-first**, **evolve-first**, **multi-model** çalışma istiyor.
- Benim çıkarımım: sistemde eksik olan şey “bir agent daha” değil; **per-run contract, ledger, verifier, replay ve budget router**.

### multi agent orchestration patterns
- Anthropic’in production yazısı net: en iyi sonuçlar çoğunlukla framework fetişizminden değil, **basit composable pattern**’lardan geliyor: prompt chain, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- MAFBench çizgisi daha sert: orchestration framework tasarımı tek başına bile **latency’yi 100x+ şişirebiliyor**, planlama doğruluğunu düşürebiliyor ve koordinasyonu bozabiliyor.
- Vercel’in case study’si de aynı yumruğu vuruyor: fazla tool/soyutlama yerine daha yalın agent, **80%→100% başarı**, **3.5x hız**, **37% daha az token** verdi.
- Karar: UniverseCreator’da complexity varsayılan olmasın. **Complexity earned, not assumed.**

### network topology for agent systems
- “On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents” çalışmasında **hiyerarşik yapı** en dayanıklı topoloji çıktı; hatalı agent varken düşüş diğer topolojilere göre daha az.
- Cayley-graph topolojisi gibi araştırmalar, çok büyük agent ağlarında **seyrek ama düzenli bağlantıların** full mesh’ten daha iyi bilgi yayımı / yük dengesi verebildiğini gösteriyor.
- Benim çıkarımım: UniverseCreator ölçeğinde full-mesh gereksiz. **Star/hub + DAG** yeterli; çok sonra sparse peer mesh konuşulur.

### process management in autonomous agents
- `claude-swarm`, `agent-orchestrator` ve benzeri repo’larda pratik pattern aynı: **tmux/process isolation + worktree + dashboard + auto-retry + checkpoint**.
- AI Engineer konuşması da bunu distributed systems problemi diye çerçeveliyor: timeout, circuit breaker, compensation, immutable state versiyonları olmadan agent orkestrasyonu çamura saplanıyor.
- Karar: process lifecycle açık olmalı: `queued -> running -> blocked -> verifying -> passed/failed/escalated`.

### system management multi-agent
- Execution plane ile management plane ayrı olmalı. Agent’lar iş yapar; yönetim katmanı **quota, health, trace, retry, routing, policy** yönetir.
- Microsoft Agent Framework, LangGraph ve OpenAI Agents SDK’nın ortak noktası şu: production’da iş gören sistemler **checkpointing, tracing, human-in-the-loop ve observability** olmadan bırakılmıyor.
- Karar: UniverseCreator’a ayrı bir **orchestration control plane** lazım; mevcut loop bunun çekirdeği ama yönetim katmanı değil.

### subagents management patterns
- SPEAR çalışması smart contract denetiminde **planning agent + Contract Net Protocol + repair agent** kombinasyonunu kullanıyor. Yani subagent spawn işi “hadi dağılın” değil, **görev ilanı + yetenek eşleme + sonuç onayı**.
- `claude-swarm` benzeri repo’larda pre-spawn validation, file locking, dependency ordering ve post-completion review gibi sert kurallar var.
- Karar: her subagent spawn’ı öncesi en az şu sorular cevaplansın: **Neden ayrı agent? Hangi artifact’i üretecek? Ne ile doğrulanacak?**

### context sharing between agents
- Anthropic’in multi-agent research sistemi önemli bir dersi net söylüyor: subagent çıktısını dosya/artifact olarak dışarı yazmak, coordinator üzerinden her şeyi tekrar konuşturup “telephone game” oynamaktan daha iyi.
- A2A `contextId` + `taskId` yaklaşımı ve task immutability fikri, agent’lar arası bağlamı “sonsuz sohbet” değil **izlenebilir iş birimi** olarak ele alıyor.
- “The Complexity Trap” makalesi de aşırı summarization yerine bazen **observation masking / seçici görünürlük**’nün daha ucuz ve daha etkili olduğunu gösteriyor.
- Karar: agent’lar arasında **raw transcript paylaşma**; yalnızca **artifact ref + delta summary + verify target** paylaş.

### decision system design AI agents
- OpenAI’nin pratik kılavuzu sağlam bir prensip veriyor: önce en güçlü modelle baseline kur, sonra daha küçük modellere in.
- Difficulty-Aware Agentic Orchestration çizgisi de bunu destekliyor: query/task zorluğuna göre **workflow ve model router** değişmeli.
- Karar: routing kararı en az şu sinyallere bakmalı: **zorluk, risk, context boyutu, parallelizability, tool ihtiyacı, cost budget**.

### system analyzer autonomous loop
- En iyi self-improving sistemlerde builder agent tek başına kendi performansını okuyup karar vermiyor; ayrı bir **observer/analyzer** katmanı failure cluster, cost drift, retry hotspot ve verifier fail nedenlerini topluyor.
- OpenAI tracing, Microsoft OTEL ve workflow provenance mimarileri bu analyzer katmanını beslemek için var.
- Karar: UniverseCreator’da ayrı bir **Loop Analyzer** agent’ı olsun; günlük olarak ledger ve trace’lerden ilk 5 darboğazı çıkarsın.

### best way to plan agent workflows
- Anthropic’in önerdiği pattern’ler aslında şunu söylüyor: planı şiir gibi yazma; **iş akışı olarak yaz**.
- A2A task immutability de aynı tarafa basıyor: follow-up iş yeni task olsun, eskiyi yamama.
- Karar: workflow planı serbest metin değil, **DAG + task contract + dependency + verify rule** olsun.

### supervisor worker pattern LLM
- Anthropic Research sistemi, breadth-first araştırma işlerinde **lead agent + parallel subagents** modelinin güçlü olduğunu ve tek agent’e göre anlamlı üstünlük verdiğini raporluyor.
- Aynı yazı coding için uyarıyor: çok bağımlı, gerçek zamanlı koordinasyon isteyen işlerde multi-agent bugün hâlâ zor.
- Karar: bu pattern’i **araştırma, portfolio tarama, issue triage, rakip analizi** için kullan; sıkı bağlı code surgery için varsayılan yapma.

### agent state machine design
- A2A’nin `message/task`, `input-required`, `auth-required`, `completed`, `failed`, `canceled` gibi durumları production için sağlam bir iskelet veriyor.
- LangGraph ve Microsoft tarafında da durable execution / time-travel mantığı açık state machine olmadan çalışmıyor.
- Önerilen state machine:
  - `proposed`
  - `queued`
  - `running`
  - `blocked_input`
  - `blocked_auth`
  - `waiting_dependency`
  - `verifying`
  - `passed`
  - `failed_retryable`
  - `failed_terminal`
  - `escalated`
  - `archived`
- Karar: her run ve her task bu durum makinesinde yürüsün; gizli state olmasın.

### deterministic vs stochastic orchestration
- Anthropic, OpenAI ve pratik repo’ların ortak dersi: **yaratıcı/stochastic akıl yürütme** agent’ın içinde olabilir; ama orchestration katmanının sınırları deterministik olmalı.
- Full stochastic swarm dışarıdan havalı görünür ama debug edilmesi bok gibi zor olur.
- Karar: **topoloji seçimi, retry limiti, budget, verifier, escalation ve permission** deterministik olsun; modelin serbestliği görev kutusunun içinde kalsın.

### agent memory architecture (episodic, semantic, working)
- LightMem üç katmanı netleştiriyor: **working/short-term**, **mid-term consolidation**, **long-term memory**. Bu mimari düşük latency ve düşük storage baskısı sağlıyor.
- FadeMem adaptif forgetting ile gereksiz hafızayı buduyor; MAGMA semantic + temporal + causal + entity yönlü graph memory öneriyor.
- Karar:
  - **Working memory:** o run’ın scratchpad’i, task notes, current artifact refs.
  - **Episodic memory:** Run Ledger, trace, failure history, retry sonucu.
  - **Semantic memory:** kalıcı skill/policy/decision/prompt conventions.
- Benim çıkarımım: UniverseCreator bugün daha çok semantic + portfolio state tutuyor; **episodic run memory** zayıf.

### inter-agent communication protocols (MCP, A2A, ACP)
- **MCP:** modelin tool/resource/prompt erişimi için harika; ama tek başına peer agent task orchestration çözmüyor. Resmi mimari zaten “host-client-server” ve tool/resource/prompt katmanı üzerine kurulu.
- **A2A:** peer agent discovery, Agent Card, `contextId/taskId`, task lifecycle, SSE streaming ve webhook push notification veriyor. Yani uzun işler için daha uygun.
- **ACP:** IBM tarafında async-first, REST bazlı, offline discovery destekli ve scale-to-zero senaryolarına yakın tasarlanmış.
- Kısa karşılaştırma:

| Protokol | Asıl katman | Güçlü yanı | Zayıf yanı | UniverseCreator için rol |
|---|---|---|---|---|
| MCP | Model ↔ tool/context | Tool standardizasyonu, hızlı entegrasyon | Peer task lifecycle zayıf | Tool erişim standardı |
| A2A | Agent ↔ agent tasking | Discovery, task lifecycle, streaming, push | Daha ağır orchestration disiplini ister | Orta vadeli inter-agent bus ilhamı |
| ACP | Agent ↔ agent messaging | REST, async-first, offline discovery | Ekosistem/adoption daha sınırlı | Internal service-to-service messaging ilhamı |

- Karar: kısa vadede protocol savaşına girme. **İçeride A2A-benzeri task modeli + MCP tool layer** kurmak yeterli.

### agent handoff patterns
- OpenAI Agents SDK “handoff”u birinci sınıf kavram yapıyor; A2A ise bunu task lifecycle ile daha da netleştiriyor.
- Anthropic’in artifact-first yaklaşımı gösteriyor ki handoff, agent’ın bütün zihnini değil **iş birimini** taşımalı.
- Karar: handoff paketi şu 8 şeyi taşımalı: **amaç, input, done, allowed tools, timeout, cost cap, verify rule, escalation rule**. Geri kalan her şey opsiyonel.

### parallel agent execution patterns
- Anthropic açıkça söylüyor: parallel multi-agent özellikle **independent research branches** için iyi; coding’de paralelize edilecek gerçek bağımsız iş sayısı çoğu zaman az.
- `agent-orchestrator`, `claude-swarm` gibi repo’lar paralelliği genelde **worktree / isolated session / separate PR** ile güvenli hale getiriyor.
- Karar:
  - Coding için **3-5 worker** üst sınır mantıklı.
  - Research / market scan / portfolio triage için **5-8 worker** olabilir.
  - Aynı dosya setine çakışacak işler fan-out yapılmasın.

### agent failure recovery and resilience
- Resilience paper’ı ve Enforcement Agents çizgisi aynı şeyi söylüyor: hatalı agent’lar kaçınılmaz; önemli olan **topology + verifier + inspector/challenger** ile toparlamak.
- AI Engineer konuşmasındaki circuit breaker / saga / compensation yaklaşımı da agent orchestration için bayağı yerinde.
- Karar:
  - Retry sayısı sınırsız olmayacak.
  - `retryable` ve `terminal` fail ayrılacak.
  - Kritik aksiyonlarda compensation/rollback planı zorunlu olacak.

### self-evolving agent systems
- Self-evolving sistemler kağıt üstünde seksi; pratikte kolayca kendi çöplüğünü büyütür.
- SEVerA verified synthesis ile formal output contract kullanıp güvenli evrim öneriyor.
- “Zombie Agents” ve A-MemGuard çizgisi ise hafıza/memory mutation tarafının güvenlik açığı olabileceğini söylüyor.
- Karar: self-evolution doğrudan production prompt/skill edit hakkı almasın; önce **proposal -> replay -> canary -> promotion** hattından geçsin.

### agent observability and tracing
- OpenAI Agents SDK built-in tracing ile **LLM generation, tool call, handoff, guardrail** span’lerini topluyor.
- Microsoft Agent Framework OpenTelemetry ile distributed trace’i first-class yapıyor.
- `claude-swarm` ve `agent-orchestrator` dashboard yaklaşımı da operasyonda kör gitmemeyi sağlıyor.
- Karar: her run için en az şu telemetry olsun: **run_id, task_id, model, tool calls, token, cost, duration, verifier result, artifact refs, retry_count**.

### cost optimization multi-model swarm
- OpenAI: önce güçlü modelle baseline kur, sonra küçült.
- Anthropic multi-agent research: multi-agent güçlü ama pahalı; token kullanımı ana belirleyici.
- Vercel: tool pruning ciddi kazanç veriyor.
- Kimi resmi fiyatı da dikkate değer: `kimi-k2.6` yaklaşık **$0.95/MTok input**, **$4.00/MTok output**, cache hit **$0.16/MTok**.
- Karar: cost optimizasyonu sadece model downgrade değil; **tool azaltma + context azaltma + verifier ile erken durdurma**.

### context window management strategies
- Anthropic research sistemi planı memory’ye yazıyor; çünkü context çok uzarsa kesiliyor. Bu bayağı temel ama kritik ders.
- Aynı yazı fresh subagent + external memory + artifact refs kullanımını öneriyor.
- LightMem/FadeMem çizgisi de sürekli şişen context yerine **consolidation + forgetting** savunuyor.
- Karar:
  - Uzun run başında plan artifact’e yazılsın.
  - Her phase bitince delta summary çıkarılsın.
  - Context overflow yaklaşınca fresh worker spawn edilsin.

### tool calling efficiency patterns
- Anthropic tool engineering tavsiyesi çok net: tool formatı doğal olsun, örnek içersin, hata yapmayı zorlaştırsın; bazen prompt’tan çok tool tasarımı kritik.
- SWE-bench deneyimlerinde relative path yerine **absolute path** zorunluluğu gibi küçük tasarım farkları ciddi hata azaltıyor.
- Vercel’in dersi daha da sert: bazen özel tool setini azaltıp **filesystem + bash** vermek daha iyi.
- Karar: her agent için tool sayısını düşük tut; benzer tool çoğalması varsa kes.

### agent specialization vs generalization tradeoffs
- Anthropic routing pattern’i ve OpenAI’nin model seçimi rehberi specialization’ın ancak **doğru routing** varsa işe yaradığını söylüyor.
- OneFlow / Vercel / MAFBench çizgisi de güçlü bir single-agent baseline’ın hafife alınmaması gerektiğini gösteriyor.
- Karar: specialization’ı model adına göre değil, **artifact tipi + tool profili + verifier türü**ne göre yap.

### Topology Matrix

| Topoloji | Tipik owner | Ne zaman | Güçlü yanı | Ana risk | UniverseCreator kararı |
|---|---|---|---|---|---|
| single-agent | Codex veya Claude | Tek artifact, düşük bağımlılık, hızlı çözüm | En ucuz, en hızlı, en az koordinasyon | Paralel keşif yok | **Varsayılan** |
| supervisor | Claude | Birden fazla bağımsız alt iş var | Kontrol, görünürlük, merge yönetimi | Supervisor gereksiz konuşursa token yakar | **Varsayılan multi-agent** |
| sequential | Claude -> Builder -> Verifier | Sabit aşamalı işler | Predictable, audit kolay | Latency artar | Build/test/release akışında kullan |
| parallel fan-out | Claude supervisor + GLM/Kimi/Codex workers | Araştırma, portfolio tarama, log triage | Yüksek throughput | Merge kaosu, duplicate work | Sadece bağımsız dallarda |
| critic/reviewer loop | Builder + Critic + Verifier | Kod, doküman, strateji rafinesi | Hata yakalar, kaliteyi iteratif yükseltir | Sonsuz loop riski | Max 1-2 tur cap ile |
| human-gated workflow | İnsan + orchestrator | Deploy, ödeme, self-mod promotion, secret-impacting işler | Güvenlik ve hesap verebilirlik | Yavaşlık | **Zorunlu** kritik aksiyonlarda |

Benim çıkarımım: UniverseCreator için doğru default sıralama şu:
1. `single-agent`
2. Gerekirse `sequential`
3. Gerçek paralellik varsa `supervisor + parallel fan-out`
4. Sonda `critic/verifier`
5. Kritik yerde `human gate`

### Task Contract
Her görev şu alanlar olmadan spawn edilmemeli:
- amaç
- input
- done tanımı
- allowed tools
- timeout
- cost cap
- verify rule
- escalation rule

Önerilen şema:

```yaml
task_id: T-20260422-001
parent_run_id: R-20260422-014
topology: supervisor
owner_model: claude
purpose: "6 deploy_missing_or_bad_url item için neden analizi yap"
input:
  artifacts:
    - file:///home/gokhan/UniverseCreator/STATE.json
    - file:///home/gokhan/UniverseCreator/STATE_SUMMARY.json
  summary: "Sadece deploy drift ve URL problemi olan ürünlere bak"
done_definition:
  - "Her ürün için root cause sınıflandırıldı"
  - "Her ürün için önerilen aksiyon yazıldı"
  - "Çıktı markdown artifact olarak kaydedildi"
allowed_tools:
  - read_file
  - jq
  - grep
  - web_search
timeout_seconds: 900
cost_cap_usd: 0.75
verify_rule:
  - "Çıktı en az 6 ürünü kapsıyor"
  - "Her bulgu artifact veya URL ile destekleniyor"
escalation_rule:
  - "Timeout olursa summary artifact bırak ve supervisor'a dön"
  - "Secret / deploy / destructive action gerekirse insan onayı iste"
```

- Karar: Task Contract yoksa o iş spawn edilmesin. Aksi halde agent “örtük anlaşma” ile çalışır; bu da production’da kaostur.

### Run Ledger
Kullanıcı istediği alanlar doğru. Buna birkaç zorunlu alan daha eklemek lazım.

Asgari şema:
- run id
- topology
- owner model
- worker list
- artifacts
- cost
- pass/fail
- retry count

Önerilen geniş şema:

```json
{
  "run_id": "R-20260422-014",
  "parent_run_id": null,
  "topology": "supervisor_parallel",
  "owner_model": "claude",
  "workers": [
    {"task_id": "T-1", "model": "glm", "role": "market-scan"},
    {"task_id": "T-2", "model": "kimi-k2.6", "role": "context-compressor"}
  ],
  "artifacts": [
    {"id": "A-1", "path": "analysis/deploy-root-causes.md", "sha256": "..."}
  ],
  "token_usage": {"input": 0, "output": 0},
  "cost_usd": 1.42,
  "duration_ms": 182000,
  "verifier": {"schema": "pass", "evidence": "pass", "regression": "skip"},
  "status": "pass",
  "retry_count": 1,
  "failure_class": null,
  "created_at": "2026-04-22T12:00:00Z"
}
```

- Karar: Run Ledger append-only olsun. JSONL veya SQLite iş görür. Bu katman yoksa self-evolution körleşir.

### Verifier Layer
Kullanıcı verdiği katmanlar doğru; production için sıralamayı da netleştirmek lazım.

Önerilen sıra:
1. **schema gate** — output beklenen yapıda mı?
2. **secret scan** — secret/token/key sızıntısı var mı?
3. **test gate** — kod/komut/test davranışı geçti mi?
4. **regression gate** — daha önce kırılmayan şey bozuldu mu?
5. **evidence gate** — iddiaların artifact/URL/test/log desteği var mı?
6. **output quality gate** — son çıktı gerçekten iş görüyor mu?

- Kritik nokta: verifier mümkün olduğunca **deterministik** olsun. “Bence iyi görünüyor” production verifier’ı değil.
- Karar: code task’lerde `test + regression + secret scan` zorunlu; research task’lerde `schema + evidence + quality` zorunlu.

### Self-Evolving Loop
- Self-evolving loop’un doğru hali “kendini anında değiştiren agent” değildir. O yaklaşım hızlıca kendi prompt çöplüğünü üretir.
- Doğru loop şudur:
  1. **observe** — ledger/traces/failures topla
  2. **diagnose** — bottleneck hipotezi çıkar
  3. **propose** — versioned mutation önerisi üret
  4. **replay** — eski run’lar üzerinde test et
  5. **canary** — düşük trafikte dene
  6. **promote or rollback** — eşik geçerse yükselt, geçmezse sil
  7. **record lesson** — semantic memory’ye sonucu yaz
- Karar: self-evolution doğrudan skill kurma / MCP ekleme hakkı almamalı; promotion gate’siz bırakmak kumardır.

### budget-aware routing / model router
- Model router olmadan 4. model eklemek sadece faturayı kabartır.
- OpenAI’nin baseline yaklaşımı ve difficulty-aware orchestration araştırmaları aynı sonuca gidiyor: routing, task başında verilirse maliyet düşer.
- Önerilen policy:
  - **Cheap classifier lane:** GLM veya benzeri ucuz model -> task sınıflandırma
  - **Premium planner lane:** Claude -> high-stakes orchestration ve final merge
  - **Builder lane:** Codex -> code change üretimi
  - **Long-context / multimodal lane:** Kimi-k2.6 -> büyük input, görsel/log/video/doküman ağırlıklı işler
- Karar: her run `expected_value >= estimated_cost` kontrolü ile başlasın.

### artifact provenance & replay
- A2A task immutability ve workflow provenance mimarisi birlikte şunu söylüyor: artifact’ler versiyonlu ve referanslanabilir olmalı.
- Karar: her artifact şu formata yaklaşsın:
  - `artifact_id`
  - `run_id`
  - `task_id`
  - `producer_model`
  - `version`
  - `sha256`
  - `verify_status`
- Replay yoksa self-improvement lafı yarım kalır.

### rollback / checkpoint / time-travel
- LangGraph ve Microsoft Agent Framework açıkça checkpoint/time-travel vurguluyor.
- Karar: her kritik aşama sonunda snapshot alınsın:
  - input set
  - prompt/contract
  - artifacts
  - verifier result
  - state delta
- Böylece “neden bozuldu?” sorusu sezgiyle değil kayıtla cevaplanır.

### self-modification safety / governance
- Self-evolving sistemin en tehlikeli yanı model değil; **yetki sınırı**nın erimesi.
- Zombie Agents ve A-MemGuard çizgisi özellikle memory/prompt mutation tarafında saldırı yüzeyini büyütüyor.
- Karar:
  - Global prompt değişikliği -> human gate
  - Yeni MCP/tool kurulum önerisi -> sandbox replay + canary
  - Memory write -> policy-based validation
  - Self-mod budget -> günlük/haftalık cap

## Mevcut Sisteme Direkt Uygulama Önerileri

### Asıl bottleneck nerede?
En büyük darboğaz **uzun süreli koşularda koordinasyon ve context/provenance kaybı**.

Neden bunu söylüyorum:
- Mevcut sistemde `STATE.json` var ama bu daha çok **portfolio durumu**; tek tek run/task yaşam döngüsünü tutmuyor.
- `tmux` loop ve context refresh var ama handoff’lar hâlâ büyük ölçüde **örtük**.
- Self-evolving subagent var ama mutation’lar için henüz güçlü bir **replay + verifier + promotion gate** iskeleti görünmüyor.
- Çok model var; ama model/router/budget/authority kontratı net değilse her yeni model koordinasyon maliyetini büyütür.

Kısacası: darboğaz **zeka değil, orkestrasyon disiplini**.

### Hemen (1-2 hafta)
1. **Topology Matrix’i policy olarak kodla**
   - Default `single-agent`.
   - Yalnızca bağımsız dallarda `supervisor + fan-out`.
   - Deploy / self-mod / secret-impacting işlerde `human gate`.

2. **Task Contract zorunlu hale getir**
   - Spawn öncesi schema validation.
   - Contract’siz worker yok.

3. **Run Ledger v1 kur**
   - İlk sürüm JSONL yeter.
   - `run_id`, `task_id`, `owner`, `model`, `cost`, `artifact`, `status`, `retry_count` zorunlu olsun.

4. **Verifier Layer v1 kur**
   - Research için: `schema + evidence + quality`.
   - Code için: `schema + secret scan + tests + regression`.

5. **Artifact-first handoff’a geç**
   - Agent’lar tam sohbet dökümü taşımayacak.
   - Çıktılarını dosya/artifact bırakacak; supervisor sadece referans okuyacak.

6. **Tool pruning yap**
   - Her role için maksimum 3-7 gerçek tool bırak.
   - Tek işi aynı olan tool kümelerini kes.

7. **Budget router v1 ekle**
   - Run başında cost cap.
   - Worker başına timeout + token/cost sınırı.

8. **Self-evolving subagent için hard gate koy**
   - Proposal yazabilir.
   - Kendi önerisini direkt production’a itemez.

Beklenen etki: en hızlı kazanç burada. Çünkü bugünün problemini bugünün sistemine takıyorsun; yeni framework taşımıyorsun.

### Orta vadeli (1-3 ay)
1. **Episodic memory katmanı kur**
   - Run Ledger + trace store + failure taxonomy.
   - Bugün eksik olan hafıza katmanı bu.

2. **Analyzer loop ekle**
   - Günlük/haftalık olarak en pahalı 10 run, en sık fail eden 10 pattern, en çok retry isteyen 10 task tipi çıksın.

3. **Checkpoint / replay altyapısı kur**
   - Özellikle self-evolving önerileri historical run set üzerinde dene.

4. **Capability registry / internal agent card mantığı ekle**
   - Hangi model/worker ne iş alır, hangi tool’lara erişir, hangi verifier’dan geçer net olsun.

5. **Observability dashboard kur**
   - Run pass/fail, retry, cost, latency, verifier fail dağılımı.

6. **Kimi-k2.6 pilot lane aç**
   - Long-context analysis, multimodal triage ve compression işlerini gölgeden ölç.

7. **Parallel fan-out için dependency-aware scheduler ekle**
   - Aynı artifact setine çakışan işler aynı anda koşmasın.

### Uzun vadeli (3-6 ay)
1. **A2A-benzeri internal task bus kur**
   - `context_id`, `task_id`, immutable task, artifact refs, streaming updates.

2. **Graph/state-machine orchestration engine kur**
   - Supervisor kararı bile state machine üzerinden aksın.

3. **Verified self-evolving pipeline kur**
   - Proposal -> replay -> canary -> promote/rollback otomatik ama gated olsun.

4. **Cost/latency/success çok amaçlı scheduler kur**
   - Hangi topoloji hangi görevde daha kârlı, run ledger üzerinden öğrensin.

5. **Semantic + episodic + causal memory birleştir**
   - Basit vector dump yerine ilişki/olay tabanlı hafıza.

6. **Governed protocol layer kur**
   - Tool access, authority boundary, mutation budget, secret boundary hepsi policy ile yönetilsin.

## Kimi-k2.6 Entegrasyon Önerisi

Kimi resmi dökümanına göre `kimi-k2.6`:
- **256k context** veriyor
- **text/image/video** destekliyor
- **ToolCalls + JSON Mode + internet search + context caching** destekliyor
- instruction compliance ve self-correction tarafı güçlendirilmiş
- yaklaşık **$0.95/MTok input**, **$4.00/MTok output**

Bu profile göre Kimi’ye verilmesi gereken işler:

1. **Long-context analyst / compressor**
   - `STATE.json` delta analizi
   - uzun log yığınları
   - doküman + transcript + repo özetleme
   - supervisor’a task contract taslağı çıkarma

2. **Multimodal verifier / triage worker**
   - screenshot, video, UI bug, görsel doküman, OCR benzeri işler
   - GLM’den daha ağır, Claude’dan daha ucuz bir lane olarak konumlanabilir

3. **Retry / repair specialist**
   - İlk worker fail ettiyse, bounded ikinci deneme yapan self-corrector rolü
   - Özellikle “neden fail oldu + nasıl düzeltirim” görevlerinde iyi aday

4. **Research fan-out worker**
   - web search + uzun kaynak okuma + sentez
   - supervisor için evidence-heavy briefing üretme

5. **Self-evolving evaluator shadow lane**
   - Mutation proposal’larını historical replay set’inde puanlama

Kimi’ye **vermemeni** önerdiğim işler:
- Final deploy kararı
- Global orchestration sahibi olmak
- Unrestricted self-modification
- Secret-sensitive policy mutation

Benim önerim:
- **GLM** ucuz classifier / hızlı ilk triage olarak kalsın.
- **Kimi** yüksek context ve multimodal lane’i alsın.
- **Claude** orchestrator ve final high-stakes judge olarak kalsın.
- **Codex** builder lane’in ana sahibi olsun.

## Self-Evolving Sistem Güçlendirme

Self-evolving subagent’ı daha akıllı yapmak için gereken şey “daha özgür bırakmak” değil; **daha iyi veriyle, daha dar mutation yüzeyiyle ve daha sert promotion gate’leriyle** çalıştırmak.

Önerdiğim tasarım:

1. **3 rolü ayır**
   - **Observer:** ledger/traces/failure pattern okur
   - **Proposer:** mutation önerisi üretir
   - **Promoter:** replay/canary sonucuna göre kabul veya red verir

2. **Mutation template’leri sınırla**
   - prompt tweak
   - tool description düzeltmesi
   - routing threshold değişimi
   - verifier rule ekleme
   - yeni skill/tool önerisi
   - bunların dışında serbest mutasyon verme

3. **Her mutation proposal şu alanları içersin**
   - problem tanımı
   - hedef metric (`success`, `cost`, `latency`, `retry_rate`)
   - etkilenen dosyalar
   - risk seviyesi
   - rollback planı
   - gerekli eval seti

4. **Historical replay zorunlu olsun**
   - Son 50-100 benzer run üstünde test etmeden promotion yok.

5. **Canary rollout uygula**
   - Başta %5-%10 run’da dene.
   - Başarı artmıyorsa veya maliyet patlıyorsa otomatik rollback.

6. **Memory write’ları doğrula**
   - A-MemGuard çizgisindeki gibi memory’ye her dersi kör yazma.
   - Consensus veya en az verifier destekli kabul kullan.

7. **Mutation budget koy**
   - Günde kaç öneri?
   - Haftada kaç promotion?
   - Aynı alana kaç tekrar deneme?

8. **Cooldown ve blast-radius koy**
   - Global prompt / orchestrator policy / tool permission değişiklikleri için yavaş hat.

9. **Başarı ölçümünü tek metric’e bağlama**
   - Sadece success rate artışı yetmez.
   - `success ↑`, `cost ↔/↓`, `latency ↔/↓`, `retry ↓`, `verifier_pass ↑` birlikte bak.

10. **Self-evolution’u production loop’un dışında tut**
   - Ana loop para kazansın.
   - Evolution loop operasyonu bozmasın.

Kısa versiyon: self-evolving agent’ı “kafasına göre kurcalayan usta” değil, **hipotez kuran ve deneyle kanıtlayan mühendis**e çevir.

## Kaynaklar (URL + tarih)

### Yerel sistem artefact'leri
- 2026-04-22 — `file:///home/gokhan/UniverseCreator/STATE.json`
- 2026-04-22 — `file:///home/gokhan/UniverseCreator/PROMPT.txt`
- 2026-04-22 — `file:///home/gokhan/UniverseCreator/SOUL.md`
- 2026-04-22 — `file:///home/gokhan/UniverseCreator/scripts/codex_loop.sh`
- 2026-04-22 — `file:///home/gokhan/UniverseCreator/scripts/refresh_codex_context.py`
- 2026-04-22 — `file:///home/gokhan/UniverseCreator/sistem-planlama/sentez28.md`

### Resmi dokümanlar / case study / vendor docs
- 2026-04-22 — Anthropic, *Building Effective Agents* — https://www.anthropic.com/engineering/building-effective-agents
- 2026-04-22 — Anthropic, *How we built our multi-agent research system* — https://www.anthropic.com/engineering/multi-agent-research-system
- 2026-04-22 — OpenAI, *A practical guide to building agents* — https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- 2026-04-22 — OpenAI, *New tools for building agents* — https://openai.com/index/new-tools-for-building-agents/
- 2026-04-22 — OpenAI Agents SDK, *Tracing* — https://openai.github.io/openai-agents-python/tracing/
- 2026-04-22 — OpenAI Agents SDK, *Guardrails* — https://openai.github.io/openai-agents-python/guardrails/
- 2026-04-22 — Model Context Protocol, *Architecture overview* — https://modelcontextprotocol.io/docs/learn/architecture
- 2026-04-22 — A2A Protocol, *What is A2A?* — https://a2a-protocol.org/dev/
- 2026-04-22 — A2A Protocol, *Agent Discovery* — https://a2a-protocol.org/dev/topics/agent-discovery/
- 2026-04-22 — A2A Protocol, *Life of a Task* — https://a2a-protocol.org/dev/topics/life-of-a-task/
- 2026-04-22 — A2A Protocol, *Streaming & Asynchronous Operations* — https://a2a-protocol.org/dev/topics/streaming-and-async/
- 2026-04-22 — IBM, *What is Agent Communication Protocol (ACP)?* — https://www.ibm.com/think/topics/agent-communication-protocol
- 2026-04-22 — Vercel, *We removed 80% of our agent’s tools* — https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools
- 2026-04-22 — Kimi API Platform, *Kimi K2.6 Pricing* — https://platform.kimi.ai/docs/pricing/chat-k26
- 2026-04-22 — Kimi API Platform, *Platform Overview* — https://platform.kimi.ai/
- 2026-04-22 — Microsoft Agent Framework Overview — https://learn.microsoft.com/en-us/agent-framework/overview/

### GitHub repo analizi
- 2026-04-22 — LangGraph — https://github.com/langchain-ai/langgraph
- 2026-04-22 — OpenAI Agents Python — https://github.com/openai/openai-agents-python
- 2026-04-22 — Microsoft Agent Framework — https://github.com/microsoft/agent-framework
- 2026-04-22 — Agent Orchestrator — https://github.com/ComposioHQ/agent-orchestrator
- 2026-04-22 — Claude Swarm — https://github.com/cj-vana/claude-swarm
- 2026-04-22 — DeerFlow — https://github.com/bytedance/deer-flow
- 2026-04-22 — MetaGPT — https://github.com/FoundationAgents/MetaGPT
- 2026-04-22 — Codex Orchestrator — https://github.com/kingbootoshi/codex-orchestrator

### Akademik makaleler / arXiv
- 2026-04-22 — *SPEAR: An Engineering Case Study of Multi-Agent Coordination for Smart Contract Auditing* — https://arxiv.org/abs/2602.04418
- 2026-04-22 — *Towards Effective GenAI Multi-Agent Collaboration* — https://arxiv.org/abs/2412.05449
- 2026-04-22 — *Understanding Multi-Agent LLM Frameworks / MAFBench* — https://arxiv.org/abs/2602.03128
- 2026-04-22 — *Difficulty-Aware Agentic Orchestration* — https://arxiv.org/abs/2509.11079
- 2026-04-22 — *MAGMA* — https://arxiv.org/abs/2601.03236
- 2026-04-22 — *Graph-based Agent Memory Survey* — https://arxiv.org/abs/2602.05665
- 2026-04-22 — *FadeMem* — https://arxiv.org/abs/2601.18642
- 2026-04-22 — *LightMem* — https://arxiv.org/abs/2604.07798
- 2026-04-22 — *The Complexity Trap* — https://arxiv.org/abs/2508.21433
- 2026-04-22 — *Persistent Q4 KV Cache* — https://arxiv.org/abs/2603.04428
- 2026-04-22 — *SEVerA: Verified Synthesis of Self-Evolving Agents* — https://arxiv.org/abs/2603.25111
- 2026-04-22 — *Adaptive Orchestration: Scalable Self-Evolving Multi-Agent Systems* — https://arxiv.org/abs/2601.09742
- 2026-04-22 — *Zombie Agents* — https://arxiv.org/abs/2602.15654
- 2026-04-22 — *A-MemGuard* — https://arxiv.org/abs/2510.02373
- 2026-04-22 — *REMAC* — https://arxiv.org/abs/2503.22122
- 2026-04-22 — *On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents* — https://arxiv.org/abs/2408.00989
- 2026-04-22 — *Enforcement Agents* — https://arxiv.org/abs/2504.04070
- 2026-04-22 — *Workflow provenance reference architecture* — https://arxiv.org/abs/2509.13978
- 2026-04-22 — *Communication + verifier improves trust/comprehension* — https://arxiv.org/abs/2510.25595
- 2026-04-22 — *AutoML-Agent with multi-stage verification* — https://arxiv.org/abs/2410.02958
- 2026-04-22 — *OneFlow / strong single-agent baseline* — https://arxiv.org/abs/2601.12307
- 2026-04-22 — *Cayley graph communication topology* — https://arxiv.org/abs/2604.09703

### Video / transcript kaynakları
- 2026-04-22 — AI Engineer, *From Chaos to Choreography: Multi-Agent Orchestration Patterns That Actually Work* — https://www.youtube.com/watch?v=2czYyrTzILg
- 2026-04-22 — LangChain, *Conceptual Guide: Multi Agent Architectures* — https://www.youtube.com/watch?v=4nZl32FwU-o
- 2026-04-22 — IBM Technology, *Multi Agent Systems Explained* — https://www.youtube.com/watch?v=sWH0T4Zez6I
- 2026-04-22 — Microsoft Developer, *AI powered automation & multi-agent orchestration in Foundry* — https://www.youtube.com/watch?v=v1Q7rEE3StM

---

## Ek Araştırma — Tekrarsız Devam (2026-04-22 / 2. Tur)

Bu bölüm ilk araştırmada özellikle derinleşmeyen ama production'da sistemi ya uçuran ya da yere seren işletme katmanlarını ekler: **queue/backpressure, durable runtime, eval flywheel, memory implementation, sparse swarm, isolation, ops metrikleri**.

### Queueing, Backpressure ve Concurrency Control
- İlk md'de cost cap vardı; bu yetmez. Production swarm’larda gerçek limit çoğu zaman **para değil eşzamanlılık**. Kimi resmi limit dokümanı çağrıları `Concurrency`, `RPM`, `TPM`, `TPD` olarak ayırıyor. Bu, scheduler’ın sadece “bu run kaç dolar?” değil, “bu dakika hangi model hattı boğuluyor?” diye bakması gerektiğini gösteriyor.
- OpenAI background mode da aynı fikri API seviyesinde doğruluyor: işler `queued` ve `in_progress` gibi durumlarda kalabiliyor; polling, cancel ve stream-resume destekleniyor. Yani orchestration state machine’in provider-native async durumlarla hizalanması lazım.
- Kimi Batch API ayrıca ilginç: resmi fiyat sayfasına göre batch çağrılar standart fiyatın **%60 maliyetine** çalışıyor ve **real-time concurrency limitine takılmıyor**. Bulk işler için bu bayağı güçlü bir ayrı lane demek.
- Benim çıkarımım: UniverseCreator tek kuyrukla devam etmemeli. En az 4 lane lazım:
  1. **interactive-hot** — anlık kritik işler, düşük latency
  2. **build-repair** — code/change/test işleri
  3. **bulk-research** — portfolio tarama, SEO, pazar araştırması
  4. **self-evolution** — asla hot lane’i aç bırakmayan arka plan kuyruk
- Direkt uygulanabilir kural:
  - Claude orchestration için **global semaphore**
  - Codex builder için **repo/file-ownership bazlı semaphore**
  - Kimi research/compression için **TPM-aware semaphore**
  - GLM triage için **cheap burst lane**
- Ayrıca bir **dead-letter queue** şart. Retry sayısını aşan task kaybolmayacak; `dlq/` benzeri bir yerde root-cause etiketiyle park edecek. Bu kısım kaynaklardan türetilmiş bir sistem çıkarımı; vendor dokümanları queue ismini vermiyor ama runtime semantiği oraya çıkıyor.

### Async Runtime ve Durable Execution: "Loop" Yetmez, Replay-Safe Runtime Gerekir
- LangGraph durable execution dokümanı çok net: uzun işler, human-in-the-loop ve timeout’lu LLM çağrıları için ilerleme **kalıcı store**’a yazılmalı; resume edildiğinde önceki iş tekrar edilmemeli. Bunun için side-effect ve non-deterministic işlemler task içine alınmalı, mümkünse idempotent yapılmalı.
- Microsoft Agent Framework checkpoint dokümanı daha da operasyonel: checkpoint bütün workflow durumunu saklıyor — **executor state**, **pending messages**, **pending requests/responses**, **shared states**. Yani resume mantığı sadece “nerede kalmıştık?” değil, “hangi mesajlar sıradaydı?” sorusunu da koruyor.
- Temporal’ın AI sayfası meseleyi daha çıplak anlatıyor: agent’lar güvenilmez; runtime ise state, retry ve failure yönetimini otomatik üstlenmeli. OpenAI Agents SDK entegrasyonu çıkarmaları da bu yüzden anlamlı.
- UniverseCreator için sonuç: tmux loop iyi bir başlangıç ama **durable runtime değildir**. Şunlar eksik:
  - replay-safe activity sınırı
  - effect log
  - idempotency key
  - checkpoint storage sınıfı
- Önerilen execution modeli:
  - **Reasoning step** -> saf karar
  - **Action plan step** -> yapılacak effect’ler listesi
  - **Effect executor** -> her effect için idempotency key + result log
  - **Checkpoint commit** -> state + pending work + artifacts
- Bu ayrım yapılmazsa aynı task resume olduğunda deploy, dosya yazma, memory mutation gibi side-effect’ler çift çalışır. Klasik sessiz felaket.

### Evaluation Flywheel: Offline Replay + Online Evals + Trace Mining
- LangSmith’in evaluation akışı production için bayağı öğretici: dataset kaynağı olarak **manuel test**, **historical production traces** ve **synthetic data** birlikte kullanılabiliyor. Evaluator türleri de tek değil: **human review**, **code rules**, **LLM-as-judge**, **pairwise**.
- Aynı doküman deney koşusunda **repetitions, concurrency ve caching** ayarlanabildiğini söylüyor. Bu önemli; çünkü aynı workflow’u tek sefer ölçmek çoğu zaman istatistik değil, anekdot.
- OpenAI trace grading de siyah kutu final-output puanlamasından daha faydalı: trace içindeki kararlar, tool call’lar ve reasoning adımları etiketlenebildiği için sistem neden patladı daha net görünür hale geliyor. OpenAI bunu özellikle resilience için kritik diye çerçeveliyor.
- AgentKit lansmanındaki Carlyle örneği de boş laf değil: eval platformu ile multi-agent due diligence framework’ünde **geliştirme süresini %50+** kısaltıp **accuracy’yi %30** artırdıklarını söylüyorlar.
- LangSmith Insights Agent ayrıca binlerce trace’i tek tek okumadan usage pattern, failure mode ve kategori dağılımı çıkarıyor. Dokümana göre 1,000 thread civarı analiz OpenAI modelleriyle kabaca **$1-$2** seviyesinde.
- Benim çıkarımım: UniverseCreator’ın Analyzer loop’u prompt yazan bir danışman değil, şu 3 katmandan beslenen bir eval flywheel olmalı:
  1. **Offline replay set** — son 100 başarısız + pahalı + kritik run
  2. **Online evaluators** — production trace üstünde schema/safety/quality alarmı
  3. **Insights clustering** — haftalık failure taxonomy çıkarımı
- Shadow mode burada doğrudan kaynakta isim olarak geçmiyor ama çıkan pattern şu: yeni topoloji/model/prompt önce **historical traces** üzerinde koşturulmalı, sonra küçük oranda gerçek trafikte denenmeli. Ben bunu doğrudan öneriyorum.

### Prompt Prefix Engineering ve Cache-Aware Orchestration
- OpenAI prompt caching dokümanı pratik tarafta çok önemli bir ayrıntı ekliyor: cache hit sadece **exact prefix match** ile oluyor. Statik içerik başa, değişken içerik sona konmalı. 1024+ token prompt’larda caching aktifleşiyor ve doğru kurulumla **latency %80’e**, input maliyeti **%90’a** kadar düşebiliyor.
- Aynı dökümanda `prompt_cache_key` ile routing iyileştirilebildiği, ama aynı prefix kombinasyonunun yaklaşık **15 request/minute** üstünde cache etkinliğini düşürebildiği yazıyor.
- Önceki md’de context küçültmeden bahsetmiştim; burada yeni eklediğim nokta şu: orchestrator prompt’larını sadece kısa değil, **cacheable** tasarlamak gerekiyor.
- UniverseCreator için bu şu anlama geliyor:
  - Claude supervisor sabit policy prefix kullanmalı
  - role-specific tool açıklamaları stabil olmalı
  - per-task değişken özetler prompt’un sonuna eklenmeli
  - model/router aynı prefix family’lerini yeniden kullanmalı
- Kısacası context management sadece token azaltma işi değil; **cache topology engineering** işi.

### Memory Uygulama Desenleri: Tek Store Yerine Katmanlı Hafıza
- LangGraph memory dokümanı önceki teorik çerçeveyi uygulamaya indiriyor: short-term memory thread/checkpoint tabanlı; long-term memory ise custom namespace altında saklanıyor. Ayrıca procedural memory’yi doğrudan instruction/prompt güncelleme üzerinden modelleyebiliyorlar.
- Aynı doküman memory write için iki ayrı yol veriyor:
  - **hot path**: cevap üretirken anında memory yaz
  - **background**: ayrı task ile sonra yaz
  Bu ayrım kritik; çünkü self-evolving sistemlerde her şeyi hot path’e yazarsan latency şişer ve agent hem cevap verip hem hafıza küratörlüğü yapmaya çalışır.
- Letta Memory tarafı daha da ilginç: hafıza **git-backed markdown repository** olarak tutuluyor. `system/` altı pinned; diğer hafızalar ağaçta görünür ama tam içerik zorunlu değil. Dahası memory subagent’lar **git worktree** ile paralel memory değişikliği yapabiliyor. Bu, self-evolving hafıza için bayağı sağlam bir pattern.
- Graphiti ise farklı bir kulvar: dinamik veri için temporal graph. Resmi dokümanları özellikle **Temporal Awareness**, **Episodic Processing**, **data provenance** ve tipik **sub-second latency** vurguluyor. Bu, portfolio ve ürün durumunun zaman içinde nasıl değiştiğini izlemek için düz vector memory’den daha mantıklı.
- Mem0 kendi research sayfasında vendor-reported benchmark olarak LOCOMO üstünde **%26 accuracy artışı**, **%91 daha düşük p95 latency**, **%90 daha az token** raporluyor. Bunu “kanıtlandı” diye değil, **memory-layer pazarının gittiği yön** diye okuyorum.
- UniverseCreator için önerdiğim hafıza bölünmesi:
  1. **Run Memory / Episodic Log** — append-only, immutable, replay için
  2. **Semantic Policy Memory** — kurallar, lessons learned, agent contracts
  3. **Temporal Portfolio Memory** — ürün, deploy, drift, incident timeline
  4. **Working Scratchpads** — run bitince çöp veya summarize
- Tek hata: bunların hepsini `STATE.json` veya tek markdown havuzuna yığmak. Bu aptalca olur.

### Sparse Swarm, Arbiter ve Debate: Herkes Herkesi Okumasın
- Mixture-of-Agents çalışması katmanlı, çok-agent’lı sentezin bazı benchmark’larda güçlü sonuçlar verebildiğini ve kendi raporlarına göre GPT-4 Omni’yi geçtiğini gösteriyor.
- Ama SMoA tam burada daha faydalı bir ders veriyor: dense all-to-all iletişim verimliliği ve çeşitliliği bozuyor; bunun yerine **Response Selection** ve **Early Stopping** ile sparse bilgi akışı kurmak daha mantıklı.
- Daha yeni debate çalışmaları da aynı damara basıyor. Controlled study sonuçlarına göre debate başarısını asıl artıran şey debate order veya confidence visibility değil; **intrinsic reasoning strength** ve **group diversity**. Yani aynı modelden üç tane koyup tartıştırmak çoğu zaman gösteri.
- Adaptive Stability Detection paper’ı da önemli: fixed-round debate yerine, consensus kararlı hale geldiğinde tartışmayı erken kesmek daha verimli.
- UniverseCreator için doğrudan anlamı:
  - critic/reviewer loop sabit 3 tur çalışmasın
  - **stability score** artsa loop bitsin
  - eğer verifier deterministik pass/fail verebiliyorsa debate hiç başlamasın
  - multi-model swarm’da yeni model eklemek için şart: **gerçek çeşitlilik** getirmeli
- Kimi-k2.6 bu yüzden değerli olabilir; çünkü diversity ekseni “Claude ama biraz farklı” değil, **uzun context + multimodal + self-correction**.

### Sandbox ve İzolasyon: Parallelism, Aynı Workspace'te Kavga Etmesin
- OpenAI Codex cloud dökümanı, görevlerin arka planda ve paralel kendi cloud environment’larında yürüyebildiğini söylüyor. Bu pattern’in özü şu: **task-local environment**.
- Letta memory subagent’larının git worktree kullanması ve `agent-orchestrator`/`claude-swarm` çizgisiyle birleşince ortaya çıkan ders basit: paralel worker varsa izolasyon da olmalı.
- UniverseCreator’da ayrım net olmalı:
  - **Read-heavy research workers** -> ortak read-only artifact store
  - **Write-heavy build workers** -> worktree / file ownership / isolated branch
  - **Memory mutation workers** -> ayrı memory workspace + promotion gate
- Aynı dosya üstünde iki builder’ı aynı anda koşturmak “swarm” değil, **gereksiz kavga**.

### Ops Metrikleri, SLO ve Error Budget (Kaynak Türetilmiş Uygulama Katmanı)
Bu alt başlık doğrudan tek bir vendor dokümanında yok; ama tracing + eval + checkpoint + queue kaynaklarının doğal sonucu.

Ölçülmesi gereken asgari metrikler:
- `task_success_rate`
- `verifier_pass_rate`
- `p95_latency_by_lane`
- `p95_cost_by_lane`
- `retry_depth_avg`
- `dead_letter_rate`
- `handoff_loss_rate`
- `context_compaction_rate`
- `cache_hit_rate`
- `memory_write_revert_rate`

Önerilen SLO seti:
- Hot lane: `p95 < 60s`
- Build lane: `verifier_pass_rate > %85`
- Research lane: `evidence_coverage > %90`
- Self-evolution lane: `promotion_success > rollback_success` değilse lane throttling

Error budget mantığı:
- Aynı gün içinde self-evolution rollback oranı belli eşiği aşarsa otomatik freeze
- Aynı model lane’i retry/dead-letter patlatıyorsa scheduler ağırlığı düşsün
- Aynı task sınıfı 3 kere art arda fail ederse otomatik supervisor escalation

### UniverseCreator için Ek Mimari Kararlar (Bu Turun Çıktısı)
1. **Provider-aware scheduler** yaz
   - cost değil sadece concurrency/RPM/TPM/TPD de görsün.

2. **Priority queue + dead-letter queue** ekle
   - hot işlerle evolution işi aynı kuyruğa düşmesin.

3. **Checkpoint store** kur
   - en kötü dosya tabanlı; idealde SQLite/DB-backed.

4. **Effect log** kur
   - side-effect yapan her iş idempotency key ile kaydolacak.

5. **Replay harness** kur
   - topoloji/model/prompt değişimi önce eski run’larda ölçülecek.

6. **Online eval + weekly insights** katmanı ekle
   - sadece son output değil, trace davranışı puanlansın.

7. **Sparse communication policy** koy
   - her worker her artifact’i okumayacak.

8. **Stability-based critic stop** uygula
   - fixed loop count yerine stop score.

9. **Memory write policy** ayır
   - run memory, semantic memory, portfolio memory farklı akacak.

10. **Kimi batch lane** aç
   - bulk/offline research ve low-urgency compression işlerini batch’e kaydır.

### Bu Turda Netleşen Yeni Anti-Pattern'lar
- Aynı prompt ailesini sürekli değiştirip cache’i öldürmek
- Bütün worker’lara bütün transcript’i yedirmek
- Self-evolving agent’a hot path memory write yetkisi vermek
- Bulk research ile hot repair işlerini aynı kuyruğa atmak
- Critic loop’u verifier varken yine de döndürmek
- Dense all-to-all swarm’ı “zeki” sanmak
- Checkpoint olmadan uzun iş koşturmak

### Yeni Kaynaklar (ek)
- 2026-04-22 — LangGraph Durable Execution — https://docs.langchain.com/oss/javascript/langgraph/durable-execution
- 2026-04-22 — LangGraph Memory Overview — https://docs.langchain.com/oss/javascript/langgraph/memory
- 2026-04-22 — Letta Code Memory / MemFS — https://docs.letta.com/letta-code/memory/
- 2026-04-22 — Graphiti Overview — https://help.getzep.com/graphiti/getting-started/overview
- 2026-04-22 — LangSmith Evaluation — https://docs.langchain.com/langsmith/evaluation
- 2026-04-22 — LangSmith Insights — https://docs.langchain.com/langsmith/insights
- 2026-04-22 — OpenAI Trace Grading — https://developers.openai.com/api/docs/guides/trace-grading
- 2026-04-22 — OpenAI Prompt Caching — https://developers.openai.com/api/docs/guides/prompt-caching
- 2026-04-22 — OpenAI Background Mode — https://developers.openai.com/api/docs/guides/background
- 2026-04-22 — OpenAI AgentKit — https://openai.com/index/introducing-agentkit/
- 2026-04-22 — OpenAI Codex Cloud — https://developers.openai.com/codex/cloud
- 2026-04-22 — Kimi Rate Limits — https://platform.kimi.ai/docs/pricing/limits
- 2026-04-22 — Kimi Batch Pricing — https://platform.kimi.ai/docs/pricing/batch
- 2026-04-22 — Temporal AI Overview — https://ai.temporal.io/
- 2026-04-22 — Temporal OpenAI Agents SDK Integration — https://temporal.io/change-log/open-ai-agents-sdk-integration-pp
- 2026-04-22 — Microsoft Agent Framework Overview — https://learn.microsoft.com/en-us/agent-framework/overview/
- 2026-04-22 — Microsoft Agent Framework Checkpoints — https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints
- 2026-04-22 — Microsoft Agent Framework DevUI Tracing — https://learn.microsoft.com/en-us/agent-framework/devui/tracing
- 2026-04-22 — Mem0 Research — https://mem0.ai/research
- 2026-04-22 — arXiv: Assessing and Enhancing the Robustness of LLM-based Multi-Agent Systems Through Chaos Engineering — https://arxiv.org/abs/2505.03096
- 2026-04-22 — arXiv: Mixture-of-Agents Enhances Large Language Model Capabilities — https://arxiv.org/abs/2406.04692
- 2026-04-22 — arXiv: SMoA: Improving Multi-agent Large Language Models with Sparse Mixture-of-Agents — https://arxiv.org/abs/2411.03284
- 2026-04-22 — arXiv: Multi-Agent Debate for LLM Judges with Adaptive Stability Detection — https://arxiv.org/abs/2510.12697
- 2026-04-22 — arXiv: Can LLM Agents Really Debate? A Controlled Study of Multi-Agent Debate in Logical Reasoning — https://arxiv.org/abs/2511.07784
