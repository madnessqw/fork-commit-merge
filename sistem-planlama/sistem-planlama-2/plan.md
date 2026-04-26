# Autonomous Swarm Implementation Plan

**nihai-planlama.md versiyonu:** 2.0 (721 satır) — bu plan onun implementasyon eşleniği.

## Temel Felsefe

Sistem: **detect → plan → execute → review → otomatik karar**  
İnsan onayı hiçbir adımda yok. QA/verifier katmanı karar verir.  
Sandbox yok. Tool kısıtlaması yok. FACTORY.md iron kuralları guardrail.

## Mevcut Eksikler (cycle 1072)

1. QA/verifier yok — Codex kodu doğrudan deploy ediyor, kalite gate yok
2. Run ledger yok — pattern analizi yapılamıyor
3. Task contract informal — `codex_task.md` yapısız, bazen stale
4. Researcher 30dk loop yok — tetik mekanizması tanımsız
5. Universe-prague team stale (cycle 773'ten beri reconnect yok)
6. WORKFLOW.md / CODEBASE_MAP.md yok
7. Codex strategy mode yok — boş cycle'da feasibility analizi yapamıyor
8. Strategist skill yok — project_decision.md üretilmiyor

## Yaklaşım

**En minimal değişiklik, en büyük fayda.** Çalışan şeylere dokunma:
- `universe_loop.sh` → çalışıyor, değiştirilmiyor
- `codex_loop.sh` → çalışıyor, değiştirilmiyor
- `glm_loop.sh` → çalışıyor, değiştirilmiyor
- `analysis/` MD haberleşmesi → çalışıyor, standartlaştırılıyor

**Felsefe değişikliği:**
> Old: `QA PASS → human decides → deploy`
> New: `QA PASS → Codex auto-deploy_product.sh`

QA verifier = autonomous decision gate. Insan değil.

## Dosyalar

### Yeni Oluşturulacak

| Dosya | Amaç |
|---|---|
| `WORKFLOW.md` | Pipeline kural kitabı — kim ne yazar/okur, sahiplik, tetik koşulları |
| `CODEBASE_MAP.md` | Klasör + anahtar dosya haritası — repo scan yerine bu okunur |
| `skills/agents/qa_tester.md` | QA agent skill — codex_result.md → qa_result.md → deploy sinyal |
| `skills/task_contract_template.md` | Standart task contract şablonu |
| `skills/agents/strategist.md` | Strategist skill — market/ROI kararı + codex_strategy_input okuma |
| `scripts/researcher_loop.sh` | Researcher 30dk cron loop — `*/30 * * * *`, derin-arastirma skill |

### Güncellenecek

| Dosya | Değişiklik |
|---|---|
| `skills/codex_skill.md` | +dual-mode (execution>strategy), +run_ledger, +qa_pending, +auto-deploy |
| `skills/glm_analyst.md` | +qa_result staleness kontrolü, +researcher_needed sinyal |
| `skills/agents/researcher.md` | +30dk cadence, +derin-arastirma skill, +full write access, +researcher_done sinyal |

### Sinyal Mekanizması (`.signals/`)

| Sinyal Dosyası | Kim Yazar | Kim Okur | Anlamı |
|---|---|---|---|
| `.signals/qa_pending` | Codex (her build sonrası) | QA-TESTER | Build bitti, QA bekliyor |
| `.signals/qa_result` | QA-TESTER | Codex | PASS/FAIL ve hangi ürün |
| `.signals/researcher_needed` | GLM | Claude/Researcher | Araştırma tetikle |
| `.signals/researcher_done` | Researcher | Claude + Strategist | Yeni araştırma hazır |
| `.signals/deploy_ready` | QA-TESTER (PASS) | Codex | Bu slug'ı deploy et |
| `.signals/codex_strategy_ready` | Codex (strategy mode) | Strategist | Feasibility inputu hazır |

## Todo Listesi (öncelik sıralı)

### Faz 0 — Bağımsız, paralel yapılabilir

1. `workflow-md` — WORKFLOW.md yaz
2. `codebase-map` — CODEBASE_MAP.md yaz
3. `qa-tester-skill` — skills/agents/qa_tester.md yaz
4. `task-contract-tpl` — skills/task_contract_template.md yaz
5. `strategist-skill` — skills/agents/strategist.md yaz (dual-input: market + codex)
6. `researcher-skill-update` — skills/agents/researcher.md güncelle (30dk, derin-arastirma, full write)

### Faz 1 — Faz 0 sonrası

7. `update-codex-skill` — skills/codex_skill.md güncelle (dual-mode + qa + run_ledger)
8. `update-glm-skill` — skills/glm_analyst.md güncelle
9. `researcher-loop-script` — scripts/researcher_loop.sh yaz (`*/30 * * * *`)

### Faz 2 — Faz 1 sonrası

10. `team-reconnect` — universe-prague reconnect protokolü (WORKFLOW.md'ye bağlı)
11. `run-ledger` — logs/run_ledger.jsonl aktivasyonu (codex_skill güncellemesine bağlı)

## Autonomous Swarm Loop (hedef durum)

```
researcher_loop.sh (30dk)
  Researcher → derin-arastirma → research/YYYY-MM-DD.md (append)
             → .signals/researcher_done yazar (Strategist tetiklenir)

universe_loop.sh (10dk)
  Claude → FACTORY.md + sinyaller → team spawn/task → codex_task.md
         → researcher_done varsa: Strategist spawn
         → codex_strategy_ready varsa: Strategist spawn (feasibility inputuyla)

Strategist (on-demand)
  → research/ + codex_strategy_input.md okur
  → analysis/project_decision.md yazar
  → Builder spawn

Builder (on-demand)
  → project_decision.md → products/{slug}/spec.md + codex_task.md

codex_loop.sh (35dk)
  Codex → EXECUTION MODE (codex_task.md varsa):
         build → .signals/qa_pending → codex_result.md + run_ledger
  Codex → STRATEGY MODE (execution yoksa):
         research/ okur → codex_strategy_input.md → .signals/codex_strategy_ready

QA-TESTER (sinyal tetikli)
  → .signals/qa_pending okur → codex_result.md analiz eder
  → qa_result.md yazar (PASS/FAIL)
  → PASS → .signals/deploy_ready → Codex deploy_product.sh

glm_loop.sh (20dk)
  GLM → STATE_SUMMARY + codex_result.md → oneri.md + Telegram
      → deploy_gap > 20 → .signals/researcher_needed
```

## Kararlar ve Gerekçeler

| Karar | Gerekçe |
|---|---|
| Human gate yok | FACTORY.md'nin temel felsefesi: "ASLA onay bekleme" |
| QA = autonomous gate | Broken deploy recovery > QA maliyeti; ama insanı bekleme |
| .signals/ mekanizması | universe_loop.sh zaten kullanıyor; genişletmek tutarlı |
| Run ledger JSONL | Minimal overhead; sorgulanabilir; disk ucuz |
| Researcher trigger via signal file | Cron eklemeye gerek yok; GLM zaten 20dk döngüsünde tetikleyebilir |

## Riskler

| Risk | Önlem |
|---|---|
| QA PASS ama prod broken | `products/{slug}/spec.md` done kriteri net tutulursa azalır |
| Auto-deploy bad code | syntax + secret scan mandatory; `bash -n` + `py_compile` zorunlu |
| Signal file accumulation | Sinyal işlendikten sonra sil |
| codex_task.md stale | GLM: task timestamp > 35dk ise warn + force-new-task sinyali |
