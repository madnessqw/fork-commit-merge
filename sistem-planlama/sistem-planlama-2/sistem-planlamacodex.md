# UniverseCreator Swarm Plan

## 0) Kapsam
- Bu doküman **plan**dır.
- Kod/deploy/otomasyon önerileri uygulanacak iş olarak değil, fazlı teslim planı olarak yazıldı.
- Yeni dosyalar esas alındı; tarihsel not yalnızca topoloji bağlamı için kullanıldı.

## 1) Varsayımlar
| Varsayım | Durum | Kaynak |
|---|---|---|
| Mevcut gerçek mimari: **3 CLI = Claude + OpenCode + Codex** | Kabul | Kullanıcı talimatı |
| Claude altında **5 subagent** var | Kabul | Kullanıcı talimatı |
| OpenCode tarafında **GLM5.1 + kendi subagent'ları** çalışabiliyor | Kabul | Kullanıcı talimatı |
| Codex ayrı bir otonom worker lane olarak değerlendirilmeli | Kabul | Kullanıcı talimatı |
| Timeout ve cost cap değerleri aşağıda **ilk politika** olarak verildi; 2 haftalık telemetry ile kalibre edilmeli | Belirsiz ama gerekli | `sistem-arastirma.md` |
| Şu an görünür eksik: **per-run contract + run ledger + deterministic verifier + replay-safe runtime** | Güçlü sinyal | `sistem-arastirma.md` |

## 2) Boşluklar, çelişkiler, riskler
| Konu | Gözlem | Etki | Plan kararı | Kaynak |
|---|---|---|---|---|
| Run-level state eksik | Portfolio state var, ama task/run yaşam döngüsü zayıf | Context drift, provenance kaybı | `Run Ledger + Task Contract` zorunlu | `sistem-arastirma.md` |
| Handoff örtük | Tam sohbet/örtük bilgi ile iş devri olma riski var | Geri izlenebilirlik düşer | `artifact ref + delta summary + verify target` standardı | `sistem-arastirma.md` |
| Tarihsel prompt mutation | Eski notta prompt/MEMORY otomatik iyileşiyor | Human-gate ilkesine ters | Prompt/memory mutation artık gated | `claude tmux - sistem mimarisi prompt.txt` + kullanıcı ilkeleri |
| Kimi lane önerisi | Araştırma dökümanında Kimi lane öneriliyor ama mevcut mimari gerçeğinde aktif değil | Scope kayması | Kimi sadece geleceğe dönük opsiyon; baseline'a dahil değil | `sistem-arastirma.md` + kullanıcı talimatı |
| Tool/protocol bolluğu | `projeler.txt` çok fazla MCP/router/proxy/orchestrator örneği topluyor | Complexity creep | Yeni katman eklemeden önce mevcut ihtiyaç doğrulanacak | `projeler.txt` |

## 3) Kısa hüküm: ana darboğaz
**Ana darboğaz model kalitesi değil; uzun koşularda task kontratı, provenance, verifier ve replay disiplininin eksik olması.**

| Bulgular | Etki | Kaynak |
|---|---|---|
| Full-mesh yerine deterministic control plane öneriliyor | Koordinasyon maliyeti düşer | `sistem-arastirma.md` |
| En büyük eksik run/task yaşam döngüsü | Debug, retry, self-eval zorlaşıyor | `sistem-arastirma.md` |
| Tarihsel akış `tmux + STATE + prompt loop` ağırlıklı | Runtime var ama control plane sert değil | `claude tmux - sistem mimarisi prompt.txt` |

## 4) Dosya bazlı okuma özeti
| Dosya | Rolü | Planda nasıl kullanıldı |
|---|---|---|
| `projeler.txt` | Fikir havuzu / araştırma backlog'u / tool-pattern envanteri | Neleri **hemen kurmamamız** gerektiğini ve ekosistemdeki seçenek bolluğunu gösteriyor |
| `sistem-arastirma.md` | Karar kaynağı / mimari tez / çıkarım seti | Ana mimari kararların birincil kaynağı |
| `proje-örnekler.txt` | Pattern zoo / örnek sistemler / ilham | Açık workflow, tracing, version snapshot, memory ve visibility örnekleri için destekleyici kaynak |
| `claude tmux - sistem mimarisi prompt.txt` | Tarihsel topoloji notu | Eski sistemin `tmux + STATE + cycle loop + prompt mutation` doğasını anlamak için kullanıldı; yeni planın neden daha sert kontrol istediğini açıklıyor |

## 5) Hedef mimari
**Default hedef:** `deterministic control plane + uzman worker lane'leri + artifact-first handoff + sert verifier + append-only ledger + katmanlı memory + human gate`.

### 5.1 Hedef akış
`Intake -> Router -> Task Contract -> Topology seçimi -> Worker lane -> Artifact store -> Verifier -> Run Ledger -> Memory write -> Analyzer/Eval`

### 5.2 Katmanlar
| Katman | Sorumluluk | Not | Kaynak |
|---|---|---|---|
| Control plane | Routing, budget, permission, retry, escalation, topology | Deterministik olmalı | `sistem-arastirma.md` |
| Worker lanes | Claude subagent'ları, Codex, OpenCode/GLM5.1 worker'ları | Uzmanlık + tool profiline göre | `sistem-arastirma.md` |
| Artifact store | Dosya/artifact referansları, checksum, version | Transcript taşımaz | `sistem-arastirma.md`, `proje-örnekler.txt` |
| Verifier layer | Schema, secret, test, regression, evidence, quality | Deterministik kapı | `sistem-arastirma.md` |
| Run Ledger | Append-only run/task/artefact/cost/failure kaydı | Episodic memory çekirdeği | `sistem-arastirma.md` |
| Memory plane | Working, episodic, semantic, temporal-portfolio | `STATE.json` her şey olmamalı | `sistem-arastirma.md`, `proje-örnekler.txt` |
| Analyzer loop | Weekly insights, offline replay, online eval | Self-evolution'u besler, hot path'i değil | `sistem-arastirma.md` |

## 6) Kritik kararlar ve nedenleri
| Karar | Neden | Kaynak |
|---|---|---|
| **Full-mesh yok** | Gürültü, merge kaosu, debug zorluğu | `sistem-arastirma.md` |
| **Artifact-first handoff** | Transcript yerine izlenebilir iş birimi taşır | `sistem-arastirma.md` |
| **Task Contract olmadan spawn yok** | Örtük anlaşma üretim ortamında kaos üretir | `sistem-arastirma.md` |
| **Verifier ayrı katman** | Debate/review tek başına güvence değildir | `sistem-arastirma.md`, `proje-örnekler.txt` |
| **STATE.json = temporal-portfolio; her şey değil** | Tek store içine her şeyi yığmak context ve memory drift üretir | `sistem-arastirma.md`, tarihsel not |
| **Self-mod gated** | Tarihsel prompt mutation modeli artık güvenli değil | kullanıcı ilkeleri + tarihsel not |
| **Queue lane ayrımı** | Hot repair ile self-evolution aynı kuyruğa girmemeli | `sistem-arastirma.md` |
| **Sparse swarm** | Her worker herkesin her şeyini okumamalı | `sistem-arastirma.md` |
| **Provider abstraction ayrı, control plane ayrı** | PAL/MetaMCP yararlı olabilir; ama routing/budget/policy beynine dönüşürse complexity creep üretir | `projeler.txt` (PAL MCP, MetaMCP) + `sistem-arastirma.md` |
| **CLI-to-CLI bridge edge adapter olsun** | Bridge/relay faydalı ama asimetrik transport kısıtları core orchestration için zayıf temel | `projeler.txt` (codex-claude-bridge, codex-weave, ACP) |
| **Loop observability ayrı katman olsun** | Retry/thrashing analizi hot path içinde değil, analyzer/debug katmanında yapılmalı | `projeler.txt` (looplens-mcp) + `sistem-arastirma.md` |

## 7) Topology Matrix
> Timeout ve cost cap değerleri ilk politika önerisidir.

| Topoloji | Amaç | Input | Done tanımı | Allowed tools | Timeout | Cost cap | Ne zaman kullanılmalı | Ne zaman kullanılmamalı |
|---|---|---|---|---|---:|---:|---|---|
| `single-agent` | Tek artifact veya tek dosya setinde hızlı, ucuz çözüm | Tek contract + tek ownership alanı | Contract'taki tüm done maddeleri + verifier pass | Okuma, sınırlı yazma, lokal exec/test, artifact write | 15 dk | $0.75 | Varsayılan; düşük bağımlılık; tek owner yeterliyse | Bağımsız paralel dallar varsa; farklı uzmanlık net fayda veriyorsa |
| `supervisor` | Birden fazla worker'ı koordine etmek | Parent contract + alt task contract'ları + artifact listesi | Tüm child task'lar verifier sonrası merge edildi | Spawn/route/read artifact/merge; doğrudan geniş yazma yok | 25 dk | $1.20 | Birden çok bağımsız alt iş varsa | Tek iş için supervisor açmak token israfıysa |
| `sequential` | Sabit aşamalı, denetlenebilir akış | Fazlı contract: plan -> build -> verify -> publish-ready | Her faz checkpoint aldı; final verifier pass | Faz bazlı allowlist; her faz ayrı | 30 dk | $1.50 | Build/test/release benzeri ardışık işlerde | Fazlar bağımsız ise ve paralel kazanım yüksekse |
| `parallel fan-out` | Bağımsız araştırma/triage dallarında throughput | Aynı üst amaç, ayrı alt input kümeleri | Çakışmasız alt artefact'lar üretildi, supervisor merge etti | Varsayılan read-only; izole write sadece owned artifact'e | 10 dk/worker, 35 dk/run | $0.35/worker, $2.00/run | Research, market scan, log cluster, portfolio triage | Aynı dosya setine yazan build işlerinde; merge maliyeti işten pahalıysa |
| `critic-reviewer` | Taslak/artifact kalitesini bir tur daha yükseltmek | Builder artifact + verify hedefi | En fazla 2 tur içinde ya pass ya escalate | Critic read-only, reviewer annotate, verifier run | 15 dk | $0.60 | Hata maliyeti yüksek ama deterministic verifier tek başına yetmiyorsa | Verifier zaten net pass/fail veriyorsa; açık uçlu sonsuz loop riski varsa |
| `human-gated workflow` | Deploy, secret, self-mod, memory policy, tool ekleme gibi kritik işler | Contract + risk notu + evidence paketi + human gate nedeni | İnsan onayı alındıktan sonra aksiyon başlatıldı veya reddedildi | Approval request, read-only analysis; protected action gate sonrası | 24 saat bekleme penceresi, 10 dk compute | $0.40 pre-gate | Secret-impacting, deploy, permission, global policy değişimlerinde | Rutin düşük riskli, geri alınabilir işlerde |

## 8) Task Contract taslağı
### 8.1 Zorunlu alanlar
| Alan | Kural |
|---|---|
| `amaç` | Tek cümle, ölçülebilir hedef |
| `input` | Sadece artifact ref'leri + kısa delta summary + kısıtlar |
| `done` | Liste halinde, test edilebilir bitiş kriterleri |
| `allowed_tools` | Açık allowlist; varsayılan deny |
| `timeout` | Hard limit; aşıldığında escalate veya partial artifact |
| `cost_cap` | USD bazlı üst sınır |
| `verify_rule` | Makine/kuralla kontrol edilebilir kabul ölçütü |
| `escalation_rule` | Timeout, blocked, secret, auth, dependency, verifier fail davranışı |

### 8.2 Ek alanlar
`risk_tier`, `owner_lane`, `dependency_ids`, `artifact_owner`, `checkpoint_required`, `human_gate_required`.

### 8.3 Örnek sözleşme
```yaml
task_id: T-2026-04-22-001
parent_run_id: R-2026-04-22-014
topology: supervisor
owner_lane: claude-control-plane
amaç: "3 CLI swarm için deterministic routing policy taslağı üret"
input:
  artifacts:
    - file:///.../sistem-arastirma.md
    - file:///.../proje-örnekler.txt
  delta_summary: "Sadece control plane, routing ve handoff alanlarına bak"
  constraints:
    - "Raw transcript paylaşma"
    - "Human-gate gerektiren kararları işaretle"
done:
  - "Claude/Codex/OpenCode/GLM5.1 ayrımı tablo halinde yazıldı"
  - "Her lane için ne zaman kullanma maddesi var"
  - "Kaynak dosya adı belirtildi"
allowed_tools:
  - read
  - search
  - artifact_write
timeout: 900
cost_cap: 0.75
verify_rule:
  - "Tüm zorunlu bölümler mevcut"
  - "Her kritik karar en az bir kaynak dosya adına bağlı"
escalation_rule:
  - "Timeout -> partial artifact + supervisor'a dön"
  - "Secret/deploy/self-mod -> human gate"
```

## 9) Run Ledger şeması
### 9.1 Alanlar
| Alan | Tip | Kural |
|---|---|---|
| `run_id` | string | Global benzersiz, append-only |
| `topology` | enum | `single-agent`, `supervisor`, `sequential`, `parallel-fanout`, `critic-reviewer`, `human-gated` |
| `owner_model` | string | Run'ın kontrolünden sorumlu model/lane |
| `worker_list` | array | `task_id`, `model`, `role`, `status`, `cost` |
| `artifacts` | array | `artifact_id`, `path`, `sha256`, `producer`, `verify_status` |
| `retry_count` | integer | Toplam retry sayısı |
| `cost` | object | `input_tokens`, `output_tokens`, `usd` |
| `status` | enum | `queued`, `running`, `blocked`, `verifying`, `passed`, `failed_retryable`, `failed_terminal`, `escalated`, `archived` |
| `failure_class` | enum/null | `tool`, `model`, `schema`, `secret`, `test`, `regression`, `timeout`, `auth`, `dependency`, `policy`, `unknown` |
| `duration` | integer | ms cinsinden toplam süre |

### 9.2 Ek zorunlu alanlar
`parent_run_id`, `contract_hash`, `queue_delay_ms`, `checkpoint_id`, `human_gate_state`, `created_at`, `updated_at`.

### 9.3 Örnek JSON
```json
{
  "run_id": "R-2026-04-22-014",
  "parent_run_id": null,
  "topology": "supervisor",
  "owner_model": "claude-control-plane",
  "worker_list": [
    {"task_id": "T-1", "model": "codex", "role": "builder", "status": "passed", "cost_usd": 0.42},
    {"task_id": "T-2", "model": "glm5.1", "role": "classifier", "status": "passed", "cost_usd": 0.06}
  ],
  "artifacts": [
    {"artifact_id": "A-1", "path": "analysis/routing-policy.md", "sha256": "abc", "producer": "claude", "verify_status": "pass"}
  ],
  "retry_count": 1,
  "cost": {"input_tokens": 12000, "output_tokens": 4200, "usd": 0.88},
  "status": "passed",
  "failure_class": null,
  "duration": 182000,
  "contract_hash": "sha256:...",
  "queue_delay_ms": 4200,
  "checkpoint_id": "CP-009",
  "human_gate_state": "not_required"
}
```

## 10) Verifier Layer
### 10.1 Sıra
`schema -> secret scan -> test -> regression -> evidence -> quality`

### 10.2 Deterministik kurallar
| Gate | Input | PASS kuralı | FAIL kuralı | Sonraki aksiyon |
|---|---|---|---|---|
| Schema | Artifact + contract | Tüm zorunlu alanlar/bölümler mevcut, parse edilebilir | Eksik alan, parse hatası, format dışı çıktı | `failed_retryable` |
| Secret scan | Metin, diff, artifact | Yasak desen yok, secret path sızıntısı yok | API key/token/credential regex hit, gizli dosya içeriği sızıntısı | `failed_terminal` + human gate |
| Test | Çalıştırılabilir çıktı | Contract'ta tanımlı test/komutların tamamı 0 exit verir | Exit non-zero veya zorunlu test atlandı | `failed_retryable` |
| Regression | Baseline assertion + diff | Önceden geçen kritik assertion'lar korunur | Var olan kritik davranış bozuldu | `failed_retryable` |
| Evidence | İddia + kaynak/artifact | Kritik iddiaların %100'ü, geri kalan iddiaların >= %90'ı artifact/log/ref ile bağlı | Kanıtsız kritik iddia veya coverage eşiği altı | `failed_retryable` |
| Quality | Final çıktı | `done` maddelerinin tamamı karşılandı; `TODO/TBD` yok; çelişki yok | Done eksik, açık çelişki var, sonuç kullanılamaz | `failed_retryable` veya `escalated` |

### 10.3 Task sınıfına göre zorunlu set
| Task sınıfı | Zorunlu gate'ler |
|---|---|
| Kod/build/deploy-ready | Schema + Secret + Test + Regression + Evidence |
| Research/analysis/plan | Schema + Evidence + Quality |
| Memory/policy/self-mod proposal | Schema + Secret + Evidence + Quality + Human gate |

### 10.4 Ek kural
- Bir gate `skip` olabilir **yalnızca** task sınıfı bunu izinliyorsa.
- Kritik gate'lerde `skip` varsayılanı **fail** olmalı.

## 11) Memory mimarisi
| Katman | Amaç | Saklanan veri | Yazma kuralı | Okuma kuralı | Retention |
|---|---|---|---|---|---|
| `working` | O anki run scratchpad'i | geçici notlar, geçici plan, ara artifact ref'leri | Run içinde serbest; run bitince sil veya summarize et | Sadece current run ve owner worker | Saatlik / run sonu |
| `episodic` | Run geçmişi | Run Ledger, trace, retry, verifier sonucu, failure history | Append-only; mutation yok | Analyzer, supervisor, replay sistemi | Uzun süreli |
| `semantic` | Kalıcı politika/lesson/skill | kararlar, policy'ler, lesson learned, routing/verifier kuralları | Proposal -> verify -> human gate/promotion | Control plane ve planner | Kalıcı |
| `temporal-portfolio` | Ürün/sistem zaman çizgisi | deploy, incident, drift, health, product state event'leri | Event append + materialized current state | Portfolio/ops iş akışları | Kalıcı |

### 11.1 Net karar
- `STATE.json` tek başına memory sistemi değildir; **temporal-portfolio** katmanının güncel görünümü olmalı.
- `MEMORY.md`/lesson katmanı **semantic memory** sayılmalı.
- Replay ve self-eval için asıl eksik katman **episodic memory**.

## 12) Routing policy
| İş tipi | Primary owner | Secondary/Fallback | Neden | Ne zaman gitmemeli |
|---|---|---|---|---|
| Yüksek riskli planlama, orchestration, final karar, human-facing synthesis | **Claude** | Claude subagent veya insan | En güçlü kontrol/sentez lane'i olmalı | Ucuz triage veya basit bulk işlerde |
| Kod yazma/değiştirme, refactor, build repair, test odaklı artifact üretimi | **Codex** | Claude builder lane | Builder lane olarak ayrışmalı; deterministik verifier ile eşlenmeli | Saf araştırma, sınıflandırma, geniş context sentezi gereken işlerde |
| Ucuz classifier, ilk triage, bulk research, context compression, log clustering, düşük riskli taslak üretimi | **OpenCode / GLM5.1** | Claude veya Codex | Düşük maliyetli ön işleme ve paralel throughput için uygun | Son karar, deploy, secret, global policy işlerinde |
| Dar uzmanlık gerektiren bağımsız alt işler | **Subagent** | Parent supervisor | Ancak bağımsızlık/paralellik/kalite kazancı netse | Aynı artifact'e yazan çakışmalı işlerde |

### 12.1 Claude altındaki 5 subagent için önerilen çerçeve
| Rol tipi | İş |
|---|---|
| `planner-supervisor` | decomposition, routing, merge |
| `researcher` | evidence-heavy araştırma ve sentez |
| `critic` | çıktı inceleme, risk bulma |
| `verifier-runner` | deterministic gate'leri koordine etme |
| `analyst` | trace/ledger/failure cluster analizi |

### 12.2 `projeler.txt` keyword araştırmasından çıkan ek kararlar
| Referans | Alınacak ders | Alınmayacak şey | Plan kararı | Kaynak |
|---|---|---|---|---|
| `claude-octopus` | **Claude-native first, escalation on demand**, consensus gate, isolated worktree, tool pruning | 8 provider/32 persona/çok command default'ı | Çok model ancak escalation hattında; single-agent baseline korunacak | `projeler.txt` + `claude-octopus` README |
| `PAL MCP` | Provider abstraction, CLI subagent, disabled-by-default tool set, role specialization | "Full conversation continuity" varsayımı | PAL-benzeri katman varsa bile artifact-first ve deterministic control plane üstte kalacak | `projeler.txt` + `PAL MCP` README |
| `MetaMCP` | Namespace, middleware, tool override, traffic management, inspector | MCP aggregation'ı orchestration brain sanmak | MetaMCP-benzeri yapı yalnızca tool fabric/gateway rolünde düşünülmeli | `projeler.txt` + `MetaMCP` README |
| `agent-router` | Weighted routing, load/cost/latency/success scoring, fallback chain | Salt skora teslim tam otomatik routing | Router skoru yalnızca policy input'u; protected action'larda human/policy override kalır | `projeler.txt` + `agent-router` README |
| `looplens-mcp` | Loop detection, convergence scoring, eval export, redaction, session DB | Debug intelligence'ı genel memory yapmak | Retry/thrashing analizi için ayrı `iteration intelligence` katmanı planlanmalı | `projeler.txt` + `looplens-mcp` README |
| `codex-claude-bridge` / `codex-weave` / `ACP` | Gerçek hayatta bridge, room/session, queue+poll, background task ve provenance receipt gerekli | Raw transcript ile serbest peer chat | Inter-agent iletişim task/session temelli olacak; core bus için provenance receipt şart | `projeler.txt` + `codex-claude-bridge` README + ACP docs |
| `claude-code-monitor` | Hafif, file-based monitor ve ayrı TUI/mobile control surface faydalı | Operasyon yüzeyini ana loop'la karıştırmak | Run Ledger üstüne hafif bir ops yüzeyi kurmak yeterli; önce telemetry sonra dashboard | `projeler.txt` + `claude-code-monitor` README |

### 12.3 Capability Registry / Agent Card şeması
| Alan | Kural |
|---|---|
| `agent_id` | Benzersiz lane/worker kimliği |
| `runtime` | `claude`, `codex`, `opencode-glm`, `subagent`, `external-acp` |
| `role` | `planner`, `builder`, `critic`, `verifier`, `researcher`, `analyst` |
| `capabilities[]` | Yetkinlik adı + confidence değil, **izinli iş tipi** listesi |
| `allowed_topologies[]` | Hangi topolojilerde çalışabileceği |
| `allowed_tools[]` | Açık allowlist |
| `disallowed_actions[]` | Örn. `deploy`, `memory_mutation`, `secret_read`, `tool_install` |
| `max_concurrency` | Lane başına sert üst sınır |
| `cost_band` | `cheap`, `standard`, `premium` |
| `verifier_profile` | `research`, `build`, `policy`, `deploy-ready` |
| `artifact_scope` | Hangi path/artifact sınıfına yazabileceği |
| `cwd_policy` | `shared-readonly`, `owned-worktree`, `isolated-sandbox` |
| `requires_human_gate_for[]` | Korunan aksiyon listesi |

#### Deterministik kurallar
1. Registry'de olmayan agent spawn edilmez.
2. `disallowed_actions` ihlalinde run doğrudan `failed_terminal`.
3. `allowed_topologies` dışında çağrılan agent route edilmez.
4. `max_concurrency` aşılırsa queue'ya alınır; bypass yok.

## 13) Failure recovery
| Mekanizma | Deterministik kural |
|---|---|
| `retry` | Aynı contract ile en fazla **1 aynı-lane retry**; yalnızca `timeout`, `transient tool`, `provider saturation`, `non-deterministic output drift` için |
| `fallback` | Retry sonrası hala fail ise **1 alternate lane/model** dene; ör. GLM -> Claude, Codex -> Claude builder |
| `dead-letter` | `2 toplam deneme` sonrası veya `blocked > 2 saat` ise DLQ'ya taşı; `failure_class`, evidence ve next-action ile park et |
| `rollback` | Sadece reversible artifact/policy/memory promotion'larda otomatik; deploy/secret/global prompt rollback için human gate |
| `checkpoint` | Her faz sonunda ve her side-effect öncesi zorunlu; contract hash + artifact set + verifier durumu kaydedilir |
| `replay` | Son temiz checkpoint'ten, aynı contract hash ve aynı input artifact ref'leriyle yeniden oynatılır; side-effect'ler idempotency key ile korunur |

### 13.1 Fail sınıfları
`tool`, `model`, `schema`, `secret`, `test`, `regression`, `timeout`, `auth`, `dependency`, `policy`, `unknown`

### 13.2 Queue / backpressure / concurrency policy
| Lane | Tipik işler | Başlangıç concurrency | Sert kural |
|---|---|---:|---|
| `interactive-hot` | Kullanıcıya yakın kritik karar, kısa araştırma, orchestration | 1-2 | Başka lane aç bırakılamaz; self-evolution bu lane'i preempt edemez |
| `build-repair` | Kod değişikliği, test, verifier retry | 2-4 | Aynı artifact ownership setine iki writer verilmez |
| `bulk-research` | Pazar tarama, evidence toplama, log cluster | 4-8 | Read-only; queue doluysa degrade/örnekleme yapılır |
| `self-evolution` | Mutation proposal, replay, canary analiz | 1 | Hot lane aktifken throttle edilir; rollback oranı yüksekse otomatik freeze |

#### Semaphore kuralları
- Claude control plane: **global semaphore**
- Codex builder: **repo/file-ownership semaphore**
- OpenCode/GLM: **burst lane + max cost cap**
- External ACP/bridge worker: **session-bound semaphore**

### 13.3 Effect Log ve provenance receipt
Her side-effect öncesi append-only bir **effect log** kaydı üretilmeli.

| Alan | Amaç |
|---|---|
| `effect_id` | Tekil effect kimliği |
| `run_id`, `task_id` | Hangi run/task üretti |
| `effect_type` | `file_write`, `git`, `network`, `memory_write`, `deploy`, `approval_request` |
| `target_ref` | Hedef path/resource/session |
| `idempotency_key` | Replay-safe tekrar koruması |
| `requested_by` | Agent/lane |
| `requested_at`, `applied_at` | Zaman bilgisi |
| `before_ref`, `after_ref` | Önce/sonra artifact checksum veya ref |
| `verify_ref` | Hangi verifier sonucu ile bağlandı |
| `human_gate_ref` | Onay gerekiyorsa receipt kimliği |
| `status` | `planned`, `applied`, `rolled_back`, `rejected` |

#### Kural
- Effect log kaydı olmayan side-effect **policy ihlali** sayılır.
- `deploy`, `memory_write`, `tool_install`, `prompt_mutation`, `secret_touch` effect türlerinde `human_gate_ref` boş olamaz.

### 13.4 Sandbox / isolation policy
| İş sınıfı | Çalışma alanı | Yazma yetkisi | Ağ yetkisi | Not |
|---|---|---|---|---|
| Research / triage | `shared-readonly` | Yok | Kısıtlı/izinli kaynaklar | Artifact ref üretir |
| Build / repair | `owned-worktree` | Sadece owned scope | Gerektiğinde | Çakışma önlenir |
| Memory mutation proposal | `isolated-sandbox` | Sadece proposal artifact | Gerekmez | Production memory'ye direkt yazmaz |
| External ACP bridge session | `session-bound workspace` | Sözleşmedeki scope kadar | Runtime'a bağlı | Receipt ve session binding zorunlu |

### 13.5 Debate / arbiter / early stopping policy
- Debate **default değil**, yalnızca şu koşullarda açılır:
  1. Deterministik verifier tek başına karar veremiyor.
  2. Karar riski `medium` veya `high`.
  3. En az iki **gerçekten farklı** lane/model var.
- `critic-reviewer` döngüsü maksimum **2 tur**.
- **Stability score >= 0.85** veya yeni kanıt yoksa döngü durur.
- Arbiter varsayılanı **Claude planner-supervisor**.
- 2 tur sonunda ayrışma sürüyorsa:
  - protected action ise `human gate`
  - değilse `escalated` + alternatif topoloji önerisi

## 14) Observability planı
### 14.1 Metrikler
| Metrik | Amaç |
|---|---|
| `task_success_rate` | Genel teslim başarısı |
| `verifier_pass_rate` | Verifier kalitesi ve lane sağlığı |
| `p95_latency_by_lane` | Her lane için operasyonel gecikme |
| `p95_cost_by_lane` | Lane başına maliyet disiplini |
| `retry_depth_avg` | Tekrarlı başarısızlık sinyali |
| `dead_letter_rate` | Kurtarılamayan iş oranı |
| `handoff_loss_rate` | Handoff sonrası done/evidence kaybı |
| `context_compaction_rate` | Context baskısı ve kompresyon ihtiyacı |
| `cache_hit_rate` | Cache-aware orchestration başarısı |
| `queue_wait_p95` | Backpressure görünürlüğü |
| `memory_write_revert_rate` | Self-evolution / memory governance sağlığı |

### 14.2 Trace alanları
| Alan | Not |
|---|---|
| `run_id`, `parent_run_id`, `task_id` | Zincirlenebilir kimlik |
| `topology`, `lane`, `owner_model`, `worker_model` | Routing ve topoloji analizi |
| `contract_hash`, `prompt_family_id` | Replay ve cache ailesi |
| `artifact_in[]`, `artifact_out[]` | Handoff görünürlüğü |
| `queued_at`, `started_at`, `ended_at` | Queue ve duration ölçümü |
| `tool_calls[]` | Tool yoğunluğu ve hata noktaları |
| `token_usage`, `cost_usd` | Bütçe |
| `verifier_results` | Gate bazlı sonuç |
| `retry_count`, `failure_class` | Recovery analizi |
| `human_gate_state` | Korunan aksiyonların izi |
| `checkpoint_id` | Replay entrypoint |

### 14.3 Alarm eşikleri
| Alarm | Eşik | Aksiyon |
|---|---|---|
| Hot lane latency | `p95 > 60s` (30 dk pencere) | Lane throttling + queue inceleme |
| Build verifier düşüşü | `verifier_pass_rate < 85%` (son 20 run) | Builder lane review |
| Research evidence düşüşü | `evidence_coverage < 90%` (son 20 run) | Research contract tightening |
| DLQ artışı | `dead_letter_rate > 5%` günlük | Root-cause review, yeni spawn freeze |
| Handoff kaybı | `handoff_loss_rate > 2%` günlük | Artifact/handoff contract audit |
| Memory revert artışı | `memory_write_revert_rate > 1%` haftalık | Self-mod freeze |
| Cost drift | `cost_per_passed_run +30%` haftalık | Routing policy review |

### 14.4 Gözlem yüzeyleri
| Yüzey | Amaç | İlk sürüm |
|---|---|---|
| Ledger query / CLI | Operasyon ekibi için ham gerçek | Zorunlu |
| Minimal dashboard | Lane sağlığı, queue, verifier, cost | Orta vadede |
| Mobile/TUI monitor | Canlı session görünürlüğü | Ops konforu; çekirdek değil |
| Weekly insights report | Analyzer çıktısı, top failure clusters | Zorunlu |

## 15) Roadmap
### 15.1 1-2 hafta
| ID | Öneri | Beklenen fayda | Maliyet | Risk | Bağımlılık | Doğrulama kriteri | Kaynak |
|---|---|---|---|---|---|---|---|
| S1 | `Topology Matrix`'i policy haline getir | Gereksiz swarm azalır | Düşük | Yanlış sınıflandırma | Yok | Multi-agent run oranı düşerken success sabit/artar | `sistem-arastirma.md` |
| S2 | `Task Contract` zorunlu olsun | Örtük task azalır | Düşük | Başta yavaşlatır | S1 | Contractsiz spawn = 0 | `sistem-arastirma.md` |
| S3 | `Run Ledger v1` (JSONL/SQLite) kur | Episodic hafıza başlar | Düşük-Orta | Eksik alanla başlama | S2 | Her run ledger entry üretiyor | `sistem-arastirma.md` |
| S4 | `Verifier Layer v1` kur | Debate yerine gerçek gate gelir | Orta | Fazla katılık | S2 | Pass/fail nedeni gate bazlı görülebiliyor | `sistem-arastirma.md`, `proje-örnekler.txt` |
| S5 | `Artifact-first handoff` standardına geç | Context şişmesi düşer | Düşük | İlk başta ek belge yükü | S2 | Raw transcript handoff = 0 | `sistem-arastirma.md` |
| S6 | Queue'yu `interactive-hot / build-repair / bulk-research / self-evolution` diye ayır | Backpressure kontrolü gelir | Orta | Operasyonel ayar ihtiyacı | S3 | Hot lane bekleme süresi düşer | `sistem-arastirma.md` |
| S7 | Self-mod için hard human gate koy | Güvenlik artar | Düşük | Öğrenme hızı düşer | S3/S4 | Gated olmayan prompt/memory mutation = 0 | kullanıcı ilkeleri + tarihsel not |
| S8 | `Capability Registry / Agent Card v1` kur | Kimin neyi yapacağı netleşir | Düşük-Orta | Başlangıçta fazla kural yazımı | S1/S2 | Registry dışı agent/action = 0 | `projeler.txt` + `agent-router` + `sistem-arastirma.md` |
| S9 | `Effect Log + provenance receipt v1` kur | Replay-safe side-effect görünürlüğü gelir | Orta | Ek operasyon yükü | S3/S4 | Protected effect'lerin %100'ünde receipt var | `projeler.txt` + ACP docs + `sistem-arastirma.md` |
| S10 | `Sandbox / ownership policy` tanımla | Parallel worker çakışması düşer | Düşük-Orta | İlk başta katı gelebilir | S2/S8 | Aynı artifact setine çift writer = 0 | `projeler.txt` + `sistem-arastirma.md` |

### 15.2 1-3 ay
| ID | Öneri | Beklenen fayda | Maliyet | Risk | Bağımlılık | Doğrulama kriteri | Kaynak |
|---|---|---|---|---|---|---|---|
| M1 | `Episodic memory` katmanını olgunlaştır | Replay ve analyzer çalışır | Orta | Storage/bakım yükü | S3 | Son 100 run sorgulanabilir | `sistem-arastirma.md` |
| M2 | `Analyzer loop` ekle | En pahalı/fail pattern görünür olur | Orta | Gürültülü öneriler | M1 | Haftalık top-10 bottleneck raporu çıkıyor | `sistem-arastirma.md` |
| M3 | `Checkpoint + replay harness` kur | Uzun koşu güvenliği ve self-eval artar | Orta-Yüksek | İdempotency zor | S3/S4 | En az 1 run checkpoint'ten replay edilebiliyor | `sistem-arastirma.md` |
| M4 | `Capability registry / Agent Card` mantığı ekle | Kimin ne iş aldığı netleşir | Orta | Yönetim overhead | S1/S2 | Her lane'in tool ve yetki profili kayıtlı | `sistem-arastirma.md`, `proje-örnekler.txt` |
| M5 | `Observability dashboard` kur | Ops körlüğü azalır | Orta | Yanlış metrik seçimi | S3/M2 | p95, cost, verifier, DLQ görünür | `sistem-arastirma.md`, `projeler.txt` |
| M6 | `Provider-aware scheduler` ekle | RPM/TPM/concurrency boğulmaları azalır | Orta | Yanlış throttle | S6 | Rate-limit kaynaklı fail azalır | `sistem-arastirma.md` |
| M7 | `LoopLens-benzeri retry intelligence` ekle | Thrashing ve tekrar eden başarısızlıklar görünür olur | Orta | Fazla telemetry gürültüsü | S3/M2 | Loop detection ile aynı fail döngüleri sınıflanıyor | `projeler.txt` + `looplens-mcp` |
| M8 | `Debate stability scorer + arbiter policy` ekle | Gereksiz tartışma kesilir | Orta | Yanlış erken durdurma | S4 | Critic loop ortalama tur sayısı düşer, kalite korunur | `sistem-arastirma.md` + `projeler.txt` |

### 15.3 3-6 ay
| ID | Öneri | Beklenen fayda | Maliyet | Risk | Bağımlılık | Doğrulama kriteri | Kaynak |
|---|---|---|---|---|---|---|---|
| L1 | A2A-benzeri internal task bus kur | Daha temiz task lifecycle | Yüksek | Over-engineering | M3/M4 | Task lifecycle event'leri unify oldu | `sistem-arastirma.md` |
| L2 | Graph/state-machine orchestration engine kur | Replay-safe runtime | Yüksek | Karmaşıklık | M3 | State drift azalır, resume güvenilir | `sistem-arastirma.md` |
| L3 | Offline replay + online eval flywheel kur | Sürekli kalite ve maliyet optimizasyonu | Yüksek | Eval gürültüsü | M2/M3 | Yeni değişiklikler önce replay'de ölçülüyor | `sistem-arastirma.md` |
| L4 | Verified self-evolution pipeline kur | Güvenli iyileştirme | Yüksek | Yanlış promotion | S7/M3/L3 | Proposal -> replay -> canary -> promote/rollback hattı çalışıyor | `sistem-arastirma.md` |
| L5 | Temporal-portfolio + semantic + episodic entegrasyonu tamamla | Hafıza katmanları net ayrılır | Orta-Yüksek | Konsolidasyon zorluğu | M1/L2 | `STATE` ve lesson katmanları çakışmıyor | `sistem-arastirma.md`, `proje-örnekler.txt` |

## 16) Risks ve anti-pattern'ler
| Anti-pattern | Neden kötü | Önleyici kontrol | Kaynak |
|---|---|---|---|
| Dense all-to-all swarm | Gürültü, duplicate work, merge kaosu | Star/hub + DAG + sparse communication | `sistem-arastirma.md` |
| Context şişirme | Cost/latency patlar, drift artar | Artifact-first handoff, delta summary, fresh worker | `sistem-arastirma.md` |
| Checkpoint'siz uzun koşu | Resume güvenilmez, side-effect iki kez çalışır | Checkpoint + effect log + idempotency key | `sistem-arastirma.md` |
| Verifier'siz debate | Tartışma var ama güvence yok | Debate ancak verifier'dan sonra veya gerekirse | `sistem-arastirma.md` |
| Human-gate'siz self-mod | Prompt/memory/tool drift ve güvenlik riski | Hard human gate + replay + canary | kullanıcı ilkeleri + `sistem-arastirma.md` |
| Hot lane ile evolution aynı kuyruk | Kritik işler aç kalır | Lane ayrımı + quota | `sistem-arastirma.md` |
| Her worker'a tüm transcript'i vermek | Context ve gizlilik yüzeyi büyür | Raw transcript yasağı | kullanıcı ilkeleri + `sistem-arastirma.md` |
| Prompt ailesini sürekli değiştirmek | Cache verimi düşer | Stable prompt family + versioned prefix | `sistem-arastirma.md` |
| Aynı artifact üstünde paralel writer | Yarış durumu, overwrite | File/worktree ownership | `sistem-arastirma.md`, `proje-örnekler.txt` |
| Tool sayısını şişirmek | Hata yüzeyi ve seçim maliyeti artar | Tool pruning, role-based allowlist | `sistem-arastirma.md`, `projeler.txt` |
| MCP aggregator'ı control plane sanmak | Tool fabric ile orchestration policy birbirine karışır | Gateway ile control plane'i ayır | `projeler.txt` + `MetaMCP` |
| Bridge/proxy üstüne core runtime kurmak | Transport asimetrisi ve poll/push sınırı sistemi kilitler | Bridge'i edge adapter olarak tut | `projeler.txt` + `codex-claude-bridge` + `codex-weave` |
| Autonomous merge / publish | Verifier/human gate olmadan zincirleme hata üretir | Publish/deploy her zaman protected action | `projeler.txt` + `continuous-claude` satırı + kullanıcı ilkeleri |

## 17) Açık sorular
1. Claude altındaki mevcut 5 subagent'ın tam rol listesi ve tool boundary nedir?
2. OpenCode tarafındaki subagent envanteri ve GLM5.1 dışı modeller var mı?
3. Codex hangi seviyeye kadar otonom yazabilir; verifier ve merge ayrı lane mi kalacak?
4. Human gate hangi kanal üzerinden işletilecek ve bekleme SLA'si nedir?
5. Mevcut run/trace arşivi nerede; replay seti için son 50-100 kritik run erişilebilir mi?
6. Cost cap ve provider concurrency limitleri model bazında nedir?
7. Artifact store formatı ne olacak: dosya tabanlı JSONL mi, SQLite mı, git-backed mi?
8. Secret scan policy'si hangi regex/path sınıflarını kapsayacak?
9. Temporal-portfolio memory için `STATE.json` dışında canonical event store var mı?
10. Hangi iş sınıfları için parallel fan-out fiilen ROI veriyor; ölçüm baseline'ı var mı?
11. Protected action inventory tam olarak hangi komut/path/resource kümelerini içeriyor?
12. Human gate approval receipt nerede saklanacak ve nasıl referanslanacak?

## 18) Sonuç
**Önerilen sade plan:** önce yeni ajan ekleme değil; `Topology Matrix + Task Contract + Run Ledger + Verifier + Artifact-first handoff + queue lane ayrımı + human-gated self-mod` kur.  
Bu set gelmeden daha fazla model, daha fazla MCP, daha fazla swarm topolojisi sadece gürültü üretir.
