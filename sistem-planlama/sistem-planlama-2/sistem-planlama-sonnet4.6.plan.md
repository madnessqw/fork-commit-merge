# UniverseCreator Swarm Planner — Sistem Geliştirme Planı
**Yazar:** Claude Sonnet 4.6 | **İlk Versiyon:** 2026-04-22 | **Son Güncelleme:** 2026-04-22 | **Versiyon:** 2.0  
**Durum:** PLAN (icra değil) | **v2 Değişiklikleri:** §14 Pattern Kütüphanesi eklendi, §3 Topoloji Matrix genişletildi (iterative-loop + competitive-planning), §12 anti-pattern listesi büyütüldü, §11 Faz 1 zenginleştirildi, §13 Açık Sorular güncellendi

---

## VARSAYIMLAR

1. Mevcut sistem tmux + cron bazlı; `codex_loop.sh`, `glm_loop.sh`, ve Claude CLI manuel/periyodik çalışıyor.
2. STATE.json bir portfolio state tutarken bireysel run yaşam döngüsü izlenmiyor.
3. Handoff'lar artifact-first değil; prompt/sohbet bazlı — bu context şişiriminin ana kaynağı.
4. Self-evolving subagent var ama promotion gate'siz; mutation'ların productiona direkt akması riski mevcut.
5. Routing kararı net değil: hangi iş Claude'a, hangi iş Codex'e, GLM'e gidiyor — yazılı kural yok.
6. Run bazlı cost, latency, retry, verifier result toplanmıyor — optimizer kör çalışıyor.
7. Kimi-k2.6 henüz entegre edilmemiş; uzun context ve multimodal lane boş.

---

## BOŞLUKLAR VE RİSKLER

| Boşluk | Risk | Kaynak |
|---|---|---|
| Run Ledger yok | Self-improvement kör; hangi run ne kadar tuttu bilinmiyor | `sistem-arastirma.md` §Run Ledger |
| Task Contract yok | Spawn öncesi amaç/kural belirsiz; "örtük anlaşma" ile çalışıyor | `sistem-arastirma.md` §Task Contract |
| Verifier Layer yok | Üretilen output kalitesi gözlemsiz; hata sessizce geçebilir | `sistem-arastirma.md` §Verifier Layer |
| Artifact-first handoff yok | Büyük context aktarımı, telefon oyunu etkisi, token israfı | `sistem-arastirma.md` §context sharing |
| Budget router yok | Her run benzer maliyet alıyor; ucuz lane yok | `sistem-arastirma.md` §budget routing |
| Checkpoint/replay yok | Side-effect çift çalışabilir; resume mantığı eksik | `sistem-arastirma.md` §rollback |
| Episodic memory zayıf | Run/failure tarihi kaydedilmiyor; aynı hata tekrarlanıyor | `sistem-arastirma.md` §memory |
| Human gate belirsiz | Deploy, self-mod, secret-impacting işlerde onay şartı net değil | `sistem-arastirma.md` §self-mod safety |
| Priority queue yok | Hot işler ile evolution işleri aynı kuyruğa düşüyor | `sistem-arastirma.md` §queueing |
| Observability dashboard yok | pass/fail, cost, retry oranları görülmüyor | `sistem-arastirma.md` §ops metrics |

---

## 1. KISA HÜKÜM: SİSTEMİN ANA DARBOĞAZI

> **Darboğaz zeka değil, orkestrasyon disiplini.**

Detay:
- `STATE.json` (cycle=1070, active=142, live=77) portfolio durumunu tutuyor; ama her **run/task'ın yaşam döngüsü kayıt altında değil**.
- `codex_loop.sh` + `tmux` iyi bir başlangıç ama **durable runtime değil** — replay-safe activity sınırı, effect log, idempotency key, checkpoint storage sınıfı eksik.
- Handoff'lar **raw transcript veya implicit**; artifact-first geçilmediği için her agent "her şeyi" bağlam olarak taşımak zorunda.
- Self-evolving subagent mutation önerileri doğrudan production'a akabilir durumdaydı — **promotion gate yok**.
- Yeni model ekleme (Kimi-k2.6) ancak net routing + budget policy ile değer yaratır; aksi halde sadece koordinasyon maliyetini büyütür.

Kaynak çıkarımı: `sistem-arastirma.md` §"Asıl bottleneck nerede?"

---

## 2. DOSYA BAZLI OKUMA ÖZETİ

| Dosya | Temsil ettiği | Kullanım amacı |
|---|---|---|
| `projeler.txt` | Fikir havuzu, araştırma backlog'u, tool/framework linkleri | İlham ve pattern zoo; direkt aksiyon değil |
| `sistem-arastirma.md` | Karar kaynağı, mimari tez, araştırma çıkarımları, önerilen şemalar | Bu planın temel ground truth'u |
| `proje-örnekler.txt` | Pattern zoo, örnek sistemler (TigrimOS, MoMoA, Engram, claude-swarm vs.) | Topoloji ve mimari inspirasyon |
| `STATE.json / STATE_SUMMARY.json` | Canlı portfolio state (cycle, ürün sayısı, deploy durumu) | Mevcut iş yükü gerçeği |
| `scripts/codex_loop.sh` | Codex için tmux-bazlı periyodik çalışma döngüsü | Mevcut otomasyon çekirdeği |
| `SOUL.md` | Sistemin kimlik ve evrim tiers tanımı | Amaç/hedef çerçevesi |
| Tarihsel tmux prompt | Eski otonom loop mantığı (5 subagent, team reconnect) | Tarihsel bağlam; yeni dosyalar çelişirse yeni kazanır |

### v2 Ek Kaynak Taraması (projeler.txt'ten araştırılan)

| Repo / Kaynak | Pattern | Alınan Ders |
|---|---|---|
| `cj-vana/claude-swarm` | MCP server tabanlı swarm, Ralph Loop, git worktree isolation, competitive planning | Fresh context per iteration; dosya tabanlı persistence; 2-worker rekabetçi planlama |
| `kingbootoshi/codex-orchestrator` | Claude → Codex tmux delegasyonu + CODEBASE_MAP.md | Codebase haritası her worker'a inject edilirse bağlam keşif maliyeti sıfıra düşer |
| `ComposioHQ/agent-orchestrator` | Agent-agnostic orchestrator, reaction loop (CI fail → agent), YAML policy | CI/review feedback otomatik worker'a routelanabilir; WORKFLOW.md versiyonlu policy fikri |
| `nicobailon/pi-messenger` | Daemon/server gerektirmeyen file-based A2A, task claim, file reservation | Sıfır altyapı koordinasyonu; dosya lock yeterli; presence tabanlı önleme |
| `AdviceNXT/sbp` | Stigmergic Blackboard Protocol: pheromone emit → sense → react | Tight coupling olmadan multi-agent koordinasyonu; decay sayesinde geçici gürültü erir |
| `openai/symphony` | Issue tracker → isolated workspace → agent run, WORKFLOW.md policy | Her issue kendi izole workspace'i = race condition yok; policy versiyonlanır |
| `wangziqi06/724-office` | 3500 satır saf Python, 26 araç, 3-katman bellek, 7/24 production | Framework bağımlılığı gerekmez; yalın Python yeterli; complexity earned not assumed |
| `meitarbe/cognetivy` | Open-source state layer: runs, events, collections | Run state'i agent'tan ayır; ayrı state store traceability'yi artırır |
| `musaceylan/looplens-mcp` | Retry loop ve iterasyon observability MCP'si | Döngü içi debug'a özel araç; genel observability'den ayrı tutulabilir |
| `ai-supervisor-foundry/foundry` | Persistent orchestration control-plane, minimal restart, multi-day | Codex_loop.sh'ın ihtiyacı olan persistence layer; context loss'u minimize et |
| `facebookresearch/Hyperagents` | Hyperagent: metacognitive self-modification | Self-modification mekanizmasını da modifiye etme kapısı; tehlikeli → human gate zorunlu |
| `agtx / fynnfluegge` | Multi-session AI coding terminal manager (Claude, Codex, Gemini, OpenCode) | Birden fazla CLI'yı tek tmux layout'ta koordine eden şef layer |

---

## 3. TOPOLOGY MATRIX

### 3a. Topoloji Detayları

| Topoloji | Amaç | Input | Done Tanımı | Allowed Tools | Timeout | Cost Cap | Ne zaman kullan | Ne zaman kullanma |
|---|---|---|---|---|---|---|---|---|
| **single-agent** | Tek artifact üretmek, hızlı sorguya cevap vermek | Artifact ref + task contract | Artifact dosyada, verifier geçti | 3-7 araç | 300s | $0.50 | Default; tek bağımlılık, düşük risk | Paralel bağımsız dallar varsa |
| **supervisor** | Birden fazla bağımsız alt iş koordinasyonu | Task listesi, artifact refs | Alt task'lar tamamlandı, merge yapıldı | read, write, spawn | 900s | $2.00 | Multi-worker araştırma, portfolio triage | Supervisor gereksiz konuşup token yakarsa; sıkı bağımlı işlerde |
| **sequential** | Sabit aşamalı iş (plan→build→test→verify) | Çıktı artifact'i önceki aşamadan | Son aşama verifier'dan geçti | her aşama için ayrı set | 1800s | $3.00 | Build/test/release hattı, audit akışı | Aşamalar gerçekten sıralı değilse |
| **parallel fan-out** | Bağımsız dallarda yüksek throughput | Bölünebilir task listesi | Her branch artifact bıraktı, merge tamamlandı | read-only + search + write kendi branch'ine | 600s/worker | $0.75/worker | Market scan, portfolio triage, SEO batch | Aynı artifact setine yazan çakışan işlerde |
| **critic-reviewer** | Kalite rafinesi, hata yakalama | Builder çıktısı, review rubric | Critic pass/fail verdi; max 2 tur sonra son karar | read, lint, test, comment | 600s/tur | $1.00/tur | Kod review, doküman kalitesi, strateji onayı | Deterministik verifier yeterliyse; fixed loop count yeter sanılırsa |
| **human-gated** | Kritik karar noktası | Tüm bağlam + öneri + risk özeti | İnsan onayladı veya reddi açıkladı | sadece okuma ve bildirim | async | N/A | Deploy, ödeme, self-mod promotion, secret-impact | Geri dönüşü olmayan düşük riskli işlerde |
| **iterative-loop** | Uzun çalışma seansı; her iterasyon fresh context | `progress.md` + git diff + hedef kriterleri | Hedef kriter karşılandı veya max iterasyon aşıldı | read, write, search (iterasyon başına dar set) | per iter: 600s | $0.50/iter | Uzun araştırma döngüleri, autoresearch, multi-day build | Tek iterasyonla bitecek işlerde; context rot sorun değilse |
| **competitive-planning** | Karmaşık özellik için 2 farklı yaklaşım → en iyisi seçilir | Özellik spec, codebase map | Orchestrator 2 planı karşılaştırdı; birini seçti | plan-phase: read/glob/grep/write only | 900s/plan | $1.00 toplam | Yüksek karmaşıklık özellikleri (score ≥30), mimari karar | Basit işlerde; ikinci plan ek değer yaratmıyorsa |

### 3b. UniverseCreator Varsayılan Sıralaması

```
1. single-agent          (default)
2. sequential            (aşamalı işlerde)
3. iterative-loop        (uzun çalışma, fresh context per iter)
4. supervisor + fan-out  (gerçek bağımsızlık varsa)
5. competitive-planning  (yüksek karmaşıklık, score≥30)
6. critic-reviewer       (2 tur cap ile)
7. human-gated           (kritik yerlerde ZORUNLU)
```

---

## 4. TASK CONTRACT TASLAĞU

Her görev bu şema olmadan spawn edilmeyecek.

```yaml
task_contract:
  task_id: "T-YYYYMMDD-NNN"
  parent_run_id: "R-YYYYMMDD-NNN"
  topology: "single-agent | supervisor | sequential | parallel_fan_out | critic_reviewer | human_gated"
  owner_model: "claude | codex | glm | kimi"
  
  purpose: "[1-2 cümle: ne yapılacak, neden]"
  
  input:
    artifacts:
      - "file:///path/to/artifact.md"
    summary: "[Max 200 token: context özetı, dikkat edilecek nokta]"
  
  done_definition:
    - "[Madde 1: somut, ölçülebilir, doğrulanabilir]"
    - "[Madde 2: ...]"
  
  allowed_tools:
    - "[tool_1]"
    - "[tool_2]"
    # Max 7 araç. Fazlası kesilir.
  
  timeout_seconds: 900
  cost_cap_usd: 1.00
  
  verify_rule:
    - "[Deterministik kural 1]"
    - "[Deterministik kural 2]"
  
  escalation_rule:
    - "Timeout olursa: partial artifact bırak, supervisor'a sinyal gönder"
    - "Secret / deploy / destructive action: STOP, insan onayı iste"
    - "3. retryde fail: dead-letter queue'ya at, supervisor escalate et"
    - "Cost cap aşılırsa: STOP, mevcut çıktıyı kaydet"
```

**Kural:** Contract yoksa spawn yok.

---

## 5. RUN LEDGER ŞEMASI

Append-only. Başlangıç için JSONL; orta vadede SQLite.

```json
{
  "run_id": "R-20260422-014",
  "parent_run_id": null,
  "topology": "supervisor_parallel",
  "owner_model": "claude",
  "workers": [
    {"task_id": "T-20260422-041", "model": "glm", "role": "market-scan", "status": "passed"},
    {"task_id": "T-20260422-042", "model": "kimi", "role": "context-compressor", "status": "passed"},
    {"task_id": "T-20260422-043", "model": "codex", "role": "builder", "status": "failed_retryable"}
  ],
  "artifacts": [
    {"id": "A-001", "path": "analysis/deploy-root-causes.md", "sha256": "abc123...", "verify_status": "passed"},
    {"id": "A-002", "path": "products/uuid-generator/spec.md", "sha256": "def456...", "verify_status": "passed"}
  ],
  "token_usage": {
    "input_tokens": 42000,
    "output_tokens": 8500
  },
  "cost_usd": 1.42,
  "duration_ms": 182000,
  "verifier": {
    "schema": "pass",
    "secret_scan": "pass",
    "test": "skip",
    "regression": "skip",
    "evidence": "pass",
    "quality": "pass"
  },
  "status": "passed",
  "retry_count": 1,
  "failure_class": null,
  "created_at": "2026-04-22T12:00:00Z",
  "completed_at": "2026-04-22T12:03:02Z",
  "notes": ""
}
```

**failure_class değerleri:** `timeout | cost_exceeded | verifier_fail | tool_error | context_overflow | secret_leak | human_rejected | unknown`

---

## 6. VERIFIER LAYER

Her kural deterministik. "Bence iyi görünüyor" verifier değildir.

### 6a. Code Task Verifier (zorunlu sırayla)

| Adım | Kural | Pass Kriteri | Fail Aksiyonu |
|---|---|---|---|
| 1. Schema Gate | Output beklenen yapıda mı? | JSON/YAML parse edilebilir, zorunlu alanlar var | STOP, kontrat eksikliğini logla |
| 2. Secret Scan | Hardcoded key/token/password var mı? | regex + truffleHog pattern — 0 bulgu | STOP, human escalate, artifact karantinaya al |
| 3. Test Gate | Testler çalışıyor ve geçiyor mu? | `exit 0` + 0 fail | STOP, retry eligibility'e bak |
| 4. Regression Gate | Daha önce geçen testler bozuldu mu? | Baseline geçmiş test suite'i pass | STOP, rollback trig |
| 5. Evidence Gate | İddialar artifact/URL/test/log ile destekli mi? | Her ana iddia için ≥1 referans | Warn (code'da critical değil) |
| 6. Quality Gate | Lint/format/syntax clean mi? | 0 error (warning opsiyonel) | Fail sayılır veya warn, policy'e göre |

### 6b. Research Task Verifier (zorunlu sırayla)

| Adım | Kural | Pass Kriteri | Fail Aksiyonu |
|---|---|---|---|
| 1. Schema Gate | Markdown/JSON yapısı doğru mu? | Parse edilebilir, bölümler tam | Retry |
| 2. Evidence Gate | Her ana iddia kaynaklandırılmış mı? | ≥%80 iddia için kaynak var | Retry, eksik bölümü doldur |
| 3. Quality Gate | Çıktı task contract done_definition'ı karşılıyor mu? | Tüm done maddeler işaretli | Escalate supervisor'a |
| 4. Completeness Gate | Kapsam eksiği var mı? | İstenen alt başlıklar mevcut | Partial pass, eksikler not edildi |

### 6c. Self-Evolving Mutation Verifier (ek)

| Adım | Kural |
|---|---|
| Replay Gate | Son 50+ benzer run üzerinde test geçmeden promotion yok |
| Regression Gate | Mevcut başarı oranı düşmüyor |
| Blast-Radius Gate | Değişiklik global prompt veya orchestrator policy'yi etkiliyorsa → human gate |
| Budget Gate | Günlük mutation quota aşılmamış |
| Canary Gate | %5-%10 gerçek trafik denemesi başarılı |

---

## 7. MEMORY MİMARİSİ

4 katman. Tek store'a yığma.

### 7a. Working Memory (per-run scratchpad)

- **Ne:** Aktif run'ın notları, intermediate artifact refs, current task state
- **Nerede:** `/tmp/run-{run_id}/` veya tmux pane env
- **Yaşam süresi:** Run bitince ya çöp, ya delta summary olarak episodic'e yazılır
- **Kim yazar:** Owner model (sadece kendi run'ı)
- **Kim okur:** Run aktifken sadece o run'ın agent'ları

### 7b. Episodic Memory (run history)

- **Ne:** Run Ledger + trace + failure taxonomy + retry sonuçları
- **Nerede:** `logs/run_ledger.jsonl` (append-only)
- **Yaşam süresi:** Kalıcı; arşiv rotasyonu isteğe bağlı
- **Kim yazar:** Orchestrator (run bitince otomatik commit)
- **Kim okur:** Analyzer loop, debug, self-evolution proposer
- **Bugünkü eksiklik:** `sistem-arastirma.md` §Asıl bottleneck — "episodic run memory zayıf"

### 7c. Semantic Memory (policy & lessons)

- **Ne:** Routing kuralları, verifier kuralları, agent kontratları, lessons learned, skill açıklamaları
- **Nerede:** `memory/policy.md`, `memory/lessons.md`, `skills/` dizini
- **Yaşam süresi:** Kalıcı; versiyon kontrolünde
- **Kim yazar:** Analyzer loop önerisi → human gate → commit
- **Kim okur:** Her run başında orchestrator system prompt'una enjekte edilir

### 7d. Temporal Portfolio Memory

- **Ne:** Ürün/deploy/drift/incident timeline; `STATE.json` tarihsel hali
- **Nerede:** `STATE_SUMMARY.json` + `logs/state_timeline.jsonl`
- **Yaşam süresi:** Kalıcı; append-only
- **Kim yazar:** `scripts/product_state_sync.py` + orchestrator
- **Kim okur:** Supervisor, analyzer, Kimi (uzun context okuma)

---

## 8. ROUTING POLICY

Routing kararı şu sinyallere bakacak: **task tipi, risk seviyesi, context boyutu, parallelizability, tool ihtiyacı, cost budget, model rate-limit durumu**.

### 8a. Model Routing Tablosu

| Görev Tipi | Birincil Model | Neden | Uyarı |
|---|---|---|---|
| Orchestration, final merge, high-stakes karar | **Claude** | En güçlü planner + verifier judge | Pahalı; sadece gerektiğinde |
| Code generation, PR, refactor, build | **Codex** | Builder lane sahibi; isolated execution | Self-mod + deploy yetkisi yok |
| Cheap triage, fast classify, first-pass research | **GLM5.1** | Ucuz burst lane; hızlı ilk eleme | Düşük accuracy kabul; doğrulama gerekebilir |
| Long-context analysis, log/doc/transcript özeti | **Kimi-k2.6** | 256K context, çok ucuz bulk işlerde (batch %60) | Multimodal ama orchestrator rolü verme |
| Paralel araştırma, market scan, portfolio triage | **GLM fan-out veya Kimi fan-out** | Ucuz + yüksek throughput | Çıktıları supervisor'da merge et |
| Kritik deploy, secret, self-mod promotion | **Human gate** | Güvenlik + hesap verebilirlik | Otomatize etme |
| Mutation replay, canary eval | **Kimi shadow lane** | Historical run analizi, ucuz batch | Doğrudan production'a dokunmaz |

### 8b. Subagent Routing

5 Claude subagent:
- `planner` → Cycle önceliklendirme, task breakdown → **sequential** topoloji girişi
- `researcher` → Market araştırması, opportunity scan → **parallel fan-out** ile GLM/Kimi worker
- `writer` → İçerik, pitch, SEO → **single-agent** veya **sequential**
- `executor` → Code, API, deploy → **Codex'e handoff** (builder lane) + human gate deploy'da
- `monitor` → Balance, PR status, health → **single-agent**, periyodik

### 8c. Routing Karar Ağacı (sözde kod)

```
IF task.risk == "critical" OR task.type in ["deploy", "secret", "self_mod"]:
    → human_gate()
ELIF task.context_tokens > 100K:
    → kimi_lane()
ELIF task.type == "code_change":
    → codex_lane()
ELIF task.type in ["research", "triage"] AND task.parallelizable:
    → glm_fan_out() OR kimi_fan_out()
ELIF task.cost_estimate > $1.00:
    → claude_supervisor_with_cheaper_workers()
ELSE:
    → single_agent(default_model)
```

---

## 9. FAILURE RECOVERY

### 9a. State Machine

```
proposed → queued → running → verifying → passed
                 ↓                    ↓
           blocked_input        failed_retryable → retry(n<max) → running
           blocked_auth         failed_terminal → dead_letter
           waiting_dependency   escalated → human_review
```

### 9b. Failure Recovery Tablosu

| Senaryo | Aksiyon | Limit | Kayıt |
|---|---|---|---|
| **Retry** | Aynı task, aynı model, yeni context | Max 2 retry (code), Max 1 retry (research) | `run_ledger.jsonl` retry_count++ |
| **Fallback** | Farklı model veya farklı topoloji | Tek seferlik; orchestrator kararı | Failure class: `fallback_triggered` |
| **Dead-letter** | Max retry aşıldı; park et | Sınırsız park; analiz için | `dlq/{task_id}.json` |
| **Rollback** | Artifact veya state değişikliği geri al | Checkpoint'ten restore | `checkpoints/{run_id}/` |
| **Checkpoint** | Her kritik aşama sonunda snapshot | Input, prompt, artifacts, state delta | `checkpoints/` |
| **Replay** | Eski run'u yeni model/topoloji ile tekrar çalıştır | Self-evolution öncesi zorunlu | Replay harness scripti |

### 9c. Kritik Kurallar

- Retry sınırsız değil. `failed_terminal` ayrımı zorunlu.
- DLQ'daki task'lar minimum haftada bir gözden geçirilir.
- Checkpoint olmadan uzun run başlamaz (>5 dakika veya >$0.50 tahmini maliyet).
- Rollback sadece checkpoint'e döner; "uydurma geri al" yok.

---

## 10. OBSERVABILITY PLANI

### 10a. Toplanacak Metrikler

| Metrik | Tanım | Alarm Eşiği |
|---|---|---|
| `task_success_rate` | pass / (pass + fail) | < %80 → alert |
| `verifier_pass_rate` | verifier geçen / toplam | < %75 → investigate |
| `p95_latency_hot` | Hot lane 95. yüzdelik gecikme | > 60s → alert |
| `p95_cost_per_task` | Task başına 95. yüzdelik maliyet | > $2.00 → investigate |
| `retry_depth_avg` | Ortalama retry sayısı | > 1.5 → investigate |
| `dead_letter_rate` | DLQ'ya düşen / toplam | > %5 → alert |
| `handoff_loss_rate` | Handoff sonrası artifact eksikliği | > 0 → bug |
| `context_compaction_rate` | Context overflow → fresh spawn oranı | > %20 → investigate |
| `cache_hit_rate` | Prompt cache isabet oranı | < %30 → prefix tasarımına bak |
| `memory_write_revert_rate` | Geri alınan memory write | > %10 → policy sıkılaştır |
| `cost_per_cycle_usd` | Toplam cycle maliyeti | > $5.00/gün → optimize |

### 10b. Trace Alanları (her run için)

```json
{
  "run_id", "task_id", "parent_run_id",
  "model", "topology",
  "input_token_count", "output_token_count",
  "tool_calls": [{"name", "duration_ms", "result_size_bytes"}],
  "cost_usd",
  "duration_ms",
  "verifier_result": {"schema", "secret_scan", "test", "regression", "evidence", "quality"},
  "artifact_refs": [{"id", "path", "sha256"}],
  "retry_count",
  "failure_class",
  "escalation_triggered",
  "cache_hit"
}
```

### 10c. Alarm Eşikleri (özet)

- **Kırmızı (STOP):** secret_scan=fail, human_gate_bypassed, cost > 2x cap
- **Sarı (INVESTIGATE):** task_success_rate < %80, dead_letter_rate > %5, retry_depth > 1.5
- **Mavi (MONITOR):** cache_hit_rate < %30, context_compaction_rate > %20

### 10d. SLO Seti

| Lane | SLO |
|---|---|
| Hot lane | p95 latency < 60s |
| Build lane | verifier_pass_rate > %85 |
| Research lane | evidence_coverage > %90 |
| Self-evolution lane | promotion_success > rollback oran |

---

## 11. ROADMAP

### Faz 1: Temel Disiplin (1–2 hafta)

**Öncelik:** Mevcut sisteme minimum disiplin ekle; framework değiştirme yok.

| Aksiyon | Beklenen Fayda | Maliyet | Risk | Bağımlılık | Doğrulama Kriteri |
|---|---|---|---|---|---|
| **Task Contract şemasını yaz + spawn validation ekle** | Örtük anlaşma ortadan kalkar; hangi iş neden çalıştığı netleşir | Düşük (1-2 saat) | Düşük | Yok | Her spawn'da contract.yaml var mı? |
| **Run Ledger v1 kur** (JSONL) | Self-improvement için data üretmeye başla | Düşük (2-3 saat) | Düşük | Yok | `logs/run_ledger.jsonl` yazılıyor mu? |
| **Verifier Layer v1** (research: schema+evidence+quality; code: schema+secret+test) | Sessiz hata oranı düşer | Orta (3-5 saat) | Orta (false positive olabilir) | Run Ledger | Verifier sonucu ledger'da kayıtlı mı? |
| **Artifact-first handoff** (raw transcript taşıma, sadece ref+delta) | Token kullanımı azalır; context şişmesi durur | Orta | Orta (eski prompt'lar bozulabilir) | Task Contract | Handoff paketi transcript yerine artifact ref mi taşıyor? |
| **Budget router v1** (run başında cost cap; worker timeout) | Runaway maliyet önlenir | Düşük | Düşük | Run Ledger | Her run cost_cap_usd aşıldığında stop oluyor mu? |
| **Tool pruning** (her role ≤7 gerçek tool) | Latency düşer; model routing iyileşir | Düşük | Düşük | Yok | Rol başına araç sayısı ≤7 mi? |
| **Self-evolving hard gate** (proposal yaz, direkt production'a gitme) | Mutation riskı ortadan kalkar | Düşük | Düşük | Yok | Mutation direkt production'a akıyor mu? (Hayır olmalı) |
| **4-lane queue** (hot, build, research, evolution) | Hot işler evolution'dan etkilenmiyor | Düşük-Orta | Düşük | Yok | Evolution işi hot lane'i engelliyor mu? (Hayır olmalı) |
| **CODEBASE_MAP.md oluştur** (projeler, product dizin yapısı, modül sınırları) | Her new worker oturumu keşif maliyeti sıfıra yaklaşır; agent fumbling biter | Düşük (2-3 saat) | Düşük | Yok | Worker prompt'una `--map` flag ile harita inject ediliyor mu? |
| **WORKFLOW.md policy belgesini yaz** (versiyon kontrollü; task contract şeması, routing kuralları, verifier kuralları) | Policy tek kaynaktan yönetilir; prompt versiyonları çakışmaz | Düşük (1-2 saat) | Düşük | Yok | WORKFLOW.md git'te versiyonlanıyor mu? |
| **File-based A2A coordination** (task claim dosyası + file reservation lock) | Daemon/server olmadan agent-to-agent koordinasyonu; sıfır ek altyapı | Düşük (1-2 saat) | Düşük | Yok | Çakışan artifact yazımı aynı anda olabilir mi? (Hayır olmalı) |

### Faz 2: Episodic Memory + Analyzer (1–3 ay)

**Öncelik:** Sistemi kendi hakkında düşünebilir yap.

| Aksiyon | Beklenen Fayda | Maliyet | Risk | Bağımlılık | Doğrulama Kriteri |
|---|---|---|---|---|---|
| **Episodic memory katmanı** (Run Ledger + trace store + failure taxonomy) | Sistemin hafızası oluşur; analyzer için ham data | Orta (5-8 saat) | Orta | Run Ledger v1 | Son 30 günlük run tarihçesi sorgulanabiliyor mu? |
| **Loop Analyzer** (haftalık: top 10 pahalı run, top 10 fail pattern) | Bottleneck otomatik tespit | Orta | Düşük | Episodic memory | Haftalık analyzer raporu üretiliyor mu? |
| **Checkpoint / replay altyapısı** | Durable execution; hata sonrası devam | Yüksek (8-12 saat) | Yüksek (idempotency hatası olabilir) | Run Ledger | Run kesintisi sonrası checkpoint'ten devam ediliyor mu? |
| **Capability registry** (internal agent card) | Hangi model ne iş alır — yazılı kural | Düşük-Orta | Düşük | Task Contract | Her model için capability.yaml mevcut mu? |
| **Observability dashboard** (basit CLI veya markdown rapor) | run pass/fail, retry, cost, latency görünür | Orta | Düşük | Run Ledger | Günlük dashboard raporu üretiliyor mu? |
| **Kimi-k2.6 pilot lane** (long-context + batch) | Uzun log okuma maliyeti düşer | Orta | Orta (yeni entegrasyon) | Budget router | Kimi lane maliyet/kalite karşılaştırması raporlanmış mı? |
| **Dependency-aware scheduler** (çakışan artifact'ler aynı anda koşmuyor) | Race condition'lar ortadan kalkar | Orta | Orta | 4-lane queue | Aynı dosyaya iki worker aynı anda yazabiliyor mu? (Hayır olmalı) |

### Faz 3: Verified Self-Evolution (3–6 ay)

**Öncelik:** Sistemi kendi kendini geliştirebilir yap — ama kontrollü.

| Aksiyon | Beklenen Fayda | Maliyet | Risk | Bağımlılık | Doğrulama Kriteri |
|---|---|---|---|---|---|
| **A2A-benzeri internal task bus** (contextId, taskId, immutable task, artifact refs) | Agent iletişimi standartlaşır | Yüksek (10-15 saat) | Yüksek | Checkpoint, Capability Registry | task bus üzerinden mesaj kaybı 0 mı? |
| **Graph/state-machine orchestration engine** | Supervisor kararı izlenebilir; gizli state yok | Yüksek | Yüksek | Task Bus | Her state geçişi loglanıyor mu? |
| **Verified self-evolving pipeline** (proposal → replay → canary → promote/rollback) | Self-improvement güvenli ve ölçülebilir | Yüksek (15-20 saat) | Yüksek | Episodic memory, Checkpoint, Canary infra | Mutation sonrası başarı oranı arttı mı? Rollback sayısı azaldı mı? |
| **Multi-objective scheduler** (cost/latency/success trade-off) | Optimal topoloji/model seçimi otomatik | Yüksek | Yüksek | Run Ledger (6+ ay veri) | Scheduler recommendation accuracy > %70 mi? |
| **Semantic + episodic + causal memory** birleşimi | İlişki/olay tabanlı hafıza; daha akıllı recall | Çok yüksek | Çok yüksek | Faz 2 complete | memory recall accuracy baseline'ı geçiyor mu? |
| **Governed protocol layer** (tool access, authority, mutation budget, secret boundary) | Policy yazılı ve enforce ediliyor | Yüksek | Orta | Tüm Faz 1-2 | Policy ihlali caught rate %100 mı? |

---

## 12. RİSKLER VE ANTİ-PATTERN'LER

### 12a. Anti-Pattern Listesi

| Anti-Pattern | Neden Tehlikeli | Kaynak | Önleme |
|---|---|---|---|
| **Dense all-to-all swarm** | Her agent her transcript'i okur; O(n²) token; Debug edilemez | `sistem-arastirma.md` §Sparse Swarm | Sparse communication policy; artifact-first handoff |
| **Context şişirme** | Token maliyet patlar; model quality düşer; context overflow | `sistem-arastirma.md` §context window | Delta summary; artifact ref; fresh worker spawn |
| **Checkpoint'siz uzun koşu** | Side-effect çift çalışır; crash sonrası sıfırdan başla | `sistem-arastirma.md` §durable execution | Her kritik aşama sonunda checkpoint commit |
| **Verifier'sız debate** | Sonsuz döngü; görüşler konsensüs gibi görünür ama boş | `sistem-arastirma.md` §critic-reviewer | Max 2 tur cap; deterministik verifier varsa debate başlatma |
| **Human-gate'siz self-mod** | Model kendi kurallarını değiştirir; güvenlik çöker | `sistem-arastirma.md` §self-mod safety | Global prompt / tool permission değişikliği → human gate |
| **Aynı prompt ailesini sürekli değiştirme** | Cache ölür; her seferinde tam token ücret | `sistem-arastirma.md` §cache-aware | Statik prefix → sona değişken içerik |
| **Tüm worker'lara tüm transcript'i yedirme** | Token patlar; model context çöpe gider | `sistem-arastirma.md` §handoff | Sadece artifact ref + delta summary |
| **Self-evolving agent'a hot path memory write** | Latency şişer; hem cevap hem kürasyon yapıyor | `sistem-arastirma.md` §memory | Background memory write lane ayır |
| **Bulk research ile hot repair aynı kuyrukta** | Hot işler bulk bekler; latency SLO aşılır | `sistem-arastirma.md` §queueing | 4-lane queue; ayrı semaphore |
| **"Daha fazla agent = daha akıllı"** | Gereksiz koordinasyon maliyeti; gürültü | `sistem-arastirma.md` §specialization | Her agent spawn öncesi: "Neden? Hangi artifact? Nasıl doğrulanır?" |
| **Critic loop'u verifier varsa döndürme** | Deterministik sonuç varsa debate zaman kaybı | `sistem-arastirma.md` §Sparse Swarm | Verifier pass/fail verebiliyorsa debate başlatma |
| **Fixed-round debate** | Konsensüs oluşmuşsa da devam eder; kaynak israfı | `sistem-arastirma.md` §adaptive stability | Stability score izle; kararlı olunca durdur |
| **Context rot — tek uzun oturumda çalışma** | Token birikir; giderek artan bağlam noise'u model kalitesini düşürür; context overflow | `claude-swarm` Ralph Loop; `karpathy/autoresearch` | İterative-loop topolojisi: fresh session per iteration; state dosyaya persist et |
| **Worker'a codebase haritası vermeden başlatmak** | Agent keşfe token yakar; ne nerede bilinmez; tahmin ederek çalışır | `codex-orchestrator` CODEBASE_MAP | Faz 1: `docs/CODEBASE_MAP.md` üret; her worker spawn'ına inject et |
| **Policy'yi promptlara göm, dosyaya yazma** | Farklı session'lar farklı kural; sürüm çakışması; "hangi kural geçerli?" belirsizliği | `symphony` WORKFLOW.md; `agent-orchestrator` YAML | Tüm kurallar `WORKFLOW.md`'de versiyon kontrollü; prompt sadece referans eder |
| **Agent çakışması — aynı dosyaya birden fazla worker** | Veri kayıpları; corrupt artifact; race condition | `pi-messenger` file reservation; `claude-swarm` file-based task locking | File reservation sistemi: bir worker dosyayı claim edince diğerleri bloklanır |
| **Metacognitive self-mod (modifikasyon mekanizmasını değiştirmek)** | Self-improvement loop'u değil, self-improvement mekanizmasını değiştirme = unpredictable; geri alınamaz sistem kayması | `facebookresearch/Hyperagents`; `sistem-arastirma.md` §self-mod safety | Sadece task-level mutation; orchestration/routing/memory policy = human gate |
| **Workspace izolasyonu olmadan paralel build** | Aynı branch üzerinde çakışan commit; file system yarışı; merge cehennem | `ComposioHQ/agent-orchestrator`; `claude-swarm` git worktree isolation | Faz 2: Her worker için ayrı git worktree veya isolated dizin |

### 12b. Risk Özeti

| Risk | Olasılık | Etki | Azaltma |
|---|---|---|---|
| Self-mod promotion gate'i atlanır | Orta | Çok Yüksek | Hard gate; human approval mandatory |
| Kimi-k2.6 entegrasyonu routing karmaşası yaratır | Orta | Orta | Routing policy önce yazıldıktan sonra entegrasyon |
| Run Ledger büyür, analiz yavaşlar | Yüksek | Düşük | Log rotasyonu; SQLite sorgu indeksi |
| Verifier false positive ile iş durur | Orta | Orta | Verifier kuralları önce staging'de test edilmeli |
| DLQ birikir, gözden kaçar | Orta | Orta | Haftalık DLQ review zorunlu |

---

## 13. AÇIK SORULAR

Bu sorular dosyalarda net cevabı olmayan; planı uygulamadan önce netleştirilmeli.

1. **Checkpoint storage sınıfı ne olacak?**  
   Şu an dosya tabanlı yeterli mi, yoksa SQLite/Redis hemen mi gerekiyor? Cevap altyapı karmaşıklığını etkiliyor.

2. **4-lane queue nasıl implemente edilecek?**  
   Mevcut tmux + cron üzerine shell semaphore yeterli mi, yoksa gerçek bir job queue (Redis, SQLite-backed) şart mı?

3. **Kimi-k2.6 API key ve rate limit durumu nedir?**  
   Batch lane için fatura limiti ne? `sistem-arastirma.md`'de fiyat var ama aktif kullanım için quota onayı gerekiyor mu?

4. **GLM5.1'in mevcut entegrasyon derinliği nedir?**  
   `glm_loop.sh` ne kadar aktif? Tool profili nedir? Routing policy yazılmadan önce mevcut yetenekleri belgelenmiş mi?

5. **Artifact-first handoff geçişi mevcut prompt'ları ne kadar bozuyor?**  
   Büyük bir rewrite mi, yoksa ekleme mi? Prompt uyumluluğu testi yapılacak mı?

6. **Observer / Proposer / Promoter rolleri mevcut subagent'lara mı yükleniyor, yoksa yeni spawn mı?**  
   Bu karar Faz 1 maliyetini doğrudan etkiliyor. Mevcut `monitor` subagent'ı observer rolünü üstlenebilir mi?

7. **Run Ledger'ın erişim modeli nedir?**  
   Sadece Analyzer loop mu okuyacak, yoksa her agent kendi run'ını okuyabilecek mi? Yetki sınırı belirsiz.

8. **Self-evolving subagent günlük mutation quota'sı ne olmalı?**  
   `sistem-arastirma.md` "günlük cap" öneriyor ama sayı belirsiz. Bu, risktolerance kararı — insan belirlemeli.

9. **Canary rollout %5-%10 hangi ölçekte anlamlı?**  
   Günde kaç run çalışıyor? Cycle=1070 ama run sayısı/gün belli değil. Canary için minimum trafik gerekiyor.

10. **Stability score nasıl hesaplanacak (critic-reviewer loop için)?**  
    Bu kararın deterministik bir formülü var mı, yoksa LLM yargısı mı? LLM yargısı ise verifier saflığı bozulur.

11. **CODEBASE_MAP.md kimin sorumluluğu ve ne zaman güncelleniyor?**  
    Her ürün için ayrı harita mı? Günlük otomatik yenileme mi? Harita staleness'i agent'ı yanlış yönlendiriyorsa ne olur?

12. **File-based A2A için lock granülaritesi ne olmalı?**  
    Dosya bazlı mı (her dosya için bir lock), dizin bazlı mı, yoksa task-id bazlı mı? Yanlış granülarite ya false contention ya da data corruption yaratır.

13. **Iterative-loop için stopping condition kim tanımlıyor?**  
    Zaman limiti mi, başarı kriteri mi, max iterasyon sayısı mı? LLM kendi döngüsünü ne zaman durduracağını bilmiyor; dışarıdan kontrol şart.

14. **SBP (Stigmergic Blackboard) için pheromone decay süresi ne kadar?**  
    Çok hızlı decay → sinyal kaybolur. Çok yavaş → eski sinyaller yanıltır. UniverseCreator'ın cycle hızı (35 dakika) ile uyumlu ne olmalı?

15. **git worktree isolation Faz 2'de mevcut `codex_loop.sh` ile uyumlu mu?**  
    `codex_loop.sh` tek repo'da singleton çalışıyor. Paralel worker'lar için worktree altyapısı hangi script'te tanımlanacak?

---

## KARAR LOG (Bu Planın Aldığı Kararlar ve Gerekçeleri)

| Karar | Gerekçe | Alternatif | Neden Reddedildi |
|---|---|---|---|
| Default topoloji: single-agent | MAFBench: fazla soyutlama latency'yi 100x+ şişirebilir; Vercel: tek agent %80→%100 başarı | Full-mesh swarm | ROI düşük, debug impossible |
| Routing model bazlı değil, artifact tipi + risk bazlı | Specialization sadece doğru routing ile değer yaratır | Model bazlı sabit routing | Görev tipi değişince routing kırılır |
| Run Ledger JSONL ile başla | Yeterince basit, anında kullanılabilir, SQLite'ye migrate kolay | Direkt SQLite | Faz 1'de ek bağımlılık istemiyoruz |
| Self-evolving gate zorunlu | A-MemGuard, Zombie Agents çizgisi: memory mutation = saldırı yüzeyi | Özgür self-evolution | Kendi çöplüğünü büyütür, geri dönüşü zor |
| Critic-reviewer max 2 tur | SMoA + adaptive stability: fixed round debate verimli değil | Fixed 3 tur | Token israfı; diversity yoksa debate anlamsız |
| Kimi orchestrator değil, worker | Büyük context + ucuz batch lane — orchestrator rolü Claude'da kalsın | Kimi genel koordinatör | `sistem-arastirma.md` açıkça "genel koordinatör yapma" diyor |
| 4-lane queue | Hot işler evolution'dan etkilenmiyor | Tek kuyruk | SLO ihlali riski; hot lane bloklanabilir |
| Cache-aware prompt tasarımı | Prompt caching: exact prefix match; 15 req/min üstünde etkinlik düşüyor | Her seferinde farklı prompt | Token maliyeti %90'a kadar yükselir |
| Iterative-loop topolojisi eklendi (v2) | `claude-swarm` Ralph Loop ve `karpathy/autoresearch`: context rot'u fresh session ile çöz | Tek uzun oturum | Context şişmesi, model quality düşüşü |
| CODEBASE_MAP.md zorunlu (v2) | `codex-orchestrator`: haritasız agent fumbling; harita ile agent direkt execute eder | Her session codebase keşfi | N×token keşif maliyeti; tahmin hatası |
| File-based A2A lock (v2) | `pi-messenger`: sıfır altyapı, daemon yok, server yok; shell lock yeterli | Merkezi message broker | Faz 1'de ek servis istemiyoruz |

---

*Bu plan icra için değil, bir sonraki fazın giriş noktası olarak hazırlanmıştır. Uygulamaya başlamadan önce §13 Açık Sorular'ı gözden geçir.*

---

## 14. PATTERN KÜTÜPHANESİ (v2 Eklentisi)

> Bu bölüm `projeler.txt` araştırmasından damıtılmış. Her pattern için: ne, neden, ne zaman uygula, ne zaman kullanma.

---

### 14a. Ralph Loop — Fresh Context Per Iteration

**Kaynak:** `cj-vana/claude-swarm`, `karpathy/autoresearch`

**Ne:** Uzun çalışma süresi gerektiren görevlerde her iterasyon yeni (fresh) bir agent oturumu açar. State dosya sistemine persist edilir. Bir sonraki iterasyon önceki git diff + progress.md'yi okuyarak devam eder.

**Mekanizma:**
```
LOOP:
  1. Yeni agent oturumu aç (sıfır context, fresh)
  2. progress.md + son git diff'i prompt'a inject et
  3. Agent çalışır, artifact üretir, .done marker yazar
  4. Git commit + checkpoint
  5. Stopping condition var mı? → Evet: STOP | Hayır: LOOP
```

**Ne zaman uygula:**
- 30+ dakikadan uzun sürecek çalışmalar
- Multi-day build veya research
- Context rot riski varsa (çok uzun conversation)
- `autoresearch` loop: modify → verify → keep/discard → repeat

**Ne zaman kullanma:**
- Tek iterasyonla biten işler (bu overhead'e değmez)
- Conversation state'in korunması kritikse

**Stopping Conditions (dışarıdan kontrol — agent değil):**
- `goal_achieved.done` dosyası var → STOP
- Max iterations aşıldı → STOP
- Cost cap aşıldı → STOP + partial result kaydet
- Human cancel signal → STOP

**UniverseCreator uygulaması:** `codex_loop.sh` hali hazırda tmux + 35dk periyodik ile çalışıyor. Ralph Loop, bu döngüye `progress.md` + `run_id` ekleyerek kolayca implemente edilebilir.

---

### 14b. SBP — Stigmergic Blackboard Protocol

**Kaynak:** `AdviceNXT/sbp`

**Ne:** Ajanlar birbirini doğrudan çağırmaz. Paylaşılan bir "blackboard"a pheromone sinyali bırakır. Diğer ajanlar bu sinyali algılar ve threshold'a göre tepki verir. MCP'yi tamamlar; MCP = tool invocation, SBP = agent-to-agent coordination.

**Mekanizma:**
```
Agent A: pheromone.emit("deploy-ready", intensity=0.8, decay=600s)
Agent B: pheromone.sense(type="deploy-ready") → intensity > 0.7 → trigger verifier
Agent C: pheromone.sense(type="deploy-ready", verifier-pass) → intensity > 0.9 → human_gate_notify
```

**Ne zaman uygula:**
- Multi-agent pipeline'da tight coupling yerine
- Birden fazla monitor/worker'ın ortak tetikleyiciye bağlanması gerektiğinde
- Transient sinyaller (bir kez geçip giden olaylar) için
- Örnek: 5 GLM worker araştırma bitirince synthesis agent otomatik uyanır

**Ne zaman kullanma:**
- Deterministik sıralı pipeline'da (sıra önemli → sequential topoloji daha iyi)
- Gerçek zamanlı event (pheromone decay latency'si varsa)
- Henüz Faz 1'de — bu Faz 2/3 pattern'ı

**UniverseCreator için minimal SBP:** `logs/blackboard.jsonl` — her agent pheromone yazar; poller script sinyalleri okur; threshold aşınca action tetikler. Server gerekmez.

```json
{"type": "research-complete", "agent": "glm-worker-3", "intensity": 0.9, 
 "expires_at": "2026-04-22T13:35:00Z", "artifact_ref": "analysis/cycle-1071.md"}
```

---

### 14c. File-Based A2A Coordination

**Kaynak:** `nicobailon/pi-messenger`

**Ne:** Daemon, server veya message broker olmadan agent-to-agent koordinasyonu. Paylaşılan dizin + dosya lock. Ajanlar isim alır, task claim eder, dosya rezerve eder.

**Mekanizma:**
```
CLAIM:
  .locks/task-{id}.lock dosyası oluştur (atomic)
  Başka agent aynı lock'ı görürse: bekle veya başka task al

MESSAGE:
  .messages/{to_agent}/{timestamp}.json yaz
  Alıcı agent döngüde .messages/ dizinini poll eder

RELEASE:
  .locks/task-{id}.lock sil
  Diğer ajanlar artık o task'ı alabilir
```

**Ne zaman uygula:**
- Paralel fan-out sırasında aynı dosyaya çakışma riski varsa
- İnfra eklememek istiyorsan ama koordinasyon gerekiyorsa
- Basit task marketplace: worker gelir, boş task alır, claim eder, bitirir

**Faz 1'de uygulama:** `run_locks/` dizini → her task spawn'ında `task-{id}.lock` yaz; duplicate spawn önle; `scripts/claim_task.sh` script'i yeterli.

---

### 14d. CODEBASE_MAP.md Injection Pattern

**Kaynak:** `kingbootoshi/codex-orchestrator`, `kingbootoshi/cartographer`

**Ne:** Her worker spawn edilmeden önce projenin/ürünün kaynak haritası prompt'a enjekte edilir. Modüller, dosya amaçları, veri akışları, bağımlılıklar — tek belgede.

**Etki:** Haritasız agent ≈ keşif modunda; haritası olan agent ≈ direkt execute modunda.

**UniverseCreator formatı:**
```markdown
# CODEBASE_MAP.md

## Dizin Yapısı
- `scripts/` — Otomasyon loop'ları (codex_loop, glm_loop, refresh_codex)
- `engine/` — Core business logic
- `products/` — 142 aktif ürün dizini
- `logs/` — Run ledger, blackboard, state timeline
- `memory/` — Policy, lessons, semantic store

## Kritik Dosyalar
- `STATE.json` — Portfolio state (okuma; yazmak için update_state.py)
- `WORKFLOW.md` — Tüm routing, verifier, task contract kuralları
- `logs/run_ledger.jsonl` — Append-only run history

## Veri Akışı
codex_loop.sh → [task contract] → [run ledger] → [verifier] → [artifact]
                                                               ↓
                                                      logs/run_ledger.jsonl
```

**Güncelleme politikası:** Dizin yapısı değiştiğinde insan günceller. Otomatik güncelleme önerilmez (stale harita, yanlış haritadan daha tehlikeli).

---

### 14e. WORKFLOW.md — Versiyonlu Policy Belgesi

**Kaynak:** `openai/symphony`, `ComposioHQ/agent-orchestrator`

**Ne:** Tüm orkestrasyon politikası (routing kuralları, verifier kuralları, task contract şeması, tool kısıtlamaları, timeout'lar, cost cap'ler) tek bir `WORKFLOW.md` dosyasında tutulur ve git'te versiyonlanır.

**Avantajları:**
- Farklı session'lar aynı politikayı okur → tutarlılık
- Değişiklik tarihi görünür
- Agent "hangi kural geçerli" sorusunu sormak zorunda değil
- Debate yerine referans

**YAML front matter + Markdown body:**
```yaml
---
version: "1.0"
routing:
  code_change: codex
  long_context_gt_100k: kimi
  critical_or_deploy: human_gate
verifier:
  code: [schema, secret_scan, test, regression, evidence, quality]
  research: [schema, evidence, quality, completeness]
cost_caps:
  single_agent: 0.50
  supervisor: 2.00
  fan_out_per_worker: 0.75
timeouts:
  single_agent_s: 300
  supervisor_s: 900
---
# WORKFLOW POLICY
[Markdown açıklamalar buraya]
```

**UniverseCreator için:** `WORKFLOW.md` hali hazırda yoksa Faz 1'in en düşük maliyetli ama en yüksek getirili aksiyonu. Tüm kuralları tek yere toparlamak, 10+ dağınık prompt dosyasından daha güvenli.

---

### 14f. Reaction Loop — CI/Review Feedback → Agent

**Kaynak:** `ComposioHQ/agent-orchestrator`, `openai/symphony`

**Ne:** CI başarısız olduğunda veya PR review comment geldiğinde, agent otomatik olarak log/feedback'i alır ve düzeltmeye girişir. İnsan sadece merge/reject kararı verir.

**Mekanizma:**
```
CI_FAIL → reaction trigger → agent'a: "CI log şu, düzelt" → agent PR'ı günceller
REVIEW_COMMENT → reaction trigger → agent'a: "reviewer şunu istedi" → agent adresledi
APPROVED+GREEN → human notification → human: merge veya reject
```

**Kısıtlar:**
- Max retry: 2 (reaction da dahil)
- Eskalasyon: 2 denemede düzelmiyorsa → human review

**UniverseCreator için:** PR gönderen Codex/executor subagent döngüsüne CI status check eklenirse Faz 2'de implemente edilebilir.

---

### 14g. Competitive Planning — 2 Worker Yaklaşımı

**Kaynak:** `cj-vana/claude-swarm` (Worker Plan Mode, complexity≥30)

**Ne:** Yüksek karmaşıklıklı task'larda (karmaşıklık skoru ≥30) aynı spec için iki farklı worker ayrı plan üretir. Orchestrator planları test strategy, risk assessment, dosya özgüllüğü ve adım sayısına göre puanlar. En yüksek skoru alan plan uygulamaya girer.

**Puanlama kriterleri:**
1. Test stratejisi (açık mı?)
2. Risk değerlendirmesi (edge case'ler görülmüş mü?)
3. Dosya özgüllüğü (hangi dosya, hangi değişiklik?)
4. Adım sayısı ve net sıra (yürütülebilir mi?)

**Ne zaman uygula:**
- Mimari karar içeren özellikler
- Refactor veya büyük entegrasyon
- Birden fazla yaklaşım gerçekten mümkün olduğunda

**Ne zaman kullanma:**
- Routine fix, tek-dosya değişiklik
- Spesifikasyon zaten tek yol gösteriyorsa
- Budget dar olduğunda (2× plan maliyeti)

---

### 14h. Isolated Workspace Per Task

**Kaynak:** `openai/symphony`, `ComposioHQ/agent-orchestrator`, `claude-swarm`

**Ne:** Her issue/task için ayrı bir workspace dizini (veya git worktree). Worker komutları yalnızca kendi workspace içinde çalışır. Farklı worker'ların dosya sistemi çakışması imkânsız hale gelir.

**Mekanizma:**
```
issue_id → workspace_path = ~/.workspaces/{sanitized_issue_id}/
git worktree add workspace_path --detach
```

**UniverseCreator için:** Faz 2. `codex_loop.sh` şu an tek repo. Paralel Codex worker'ları için `run_workspaces/run-{run_id}/` dizin izolasyonu minimum gereksinim. Tam git worktree Faz 3.

---

*§14 sonu. Tüm pattern'lar `projeler.txt` araştırmasından damıtılmış; mevcut sisteme artımlı uygulanabilir.*
