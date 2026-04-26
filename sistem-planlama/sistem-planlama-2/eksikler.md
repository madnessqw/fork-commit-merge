# `nihai-planlama.md` Review — Eksikler, Sorunlar, Çözümler

## 1) Kısa hüküm
`nihai-planlama.md`, üç doküman içinde **en operasyonel ve en uygulanabilir** plan. Özellikle:
- mevcut sistemi ground-truth üzerinden okuması,
- rol matrisi ve görev dağılımını net yazması,
- `analysis/` tabanlı artifact-first haberleşmeyi koruması,
- Researcher / Strategist / Builder / Codex / GLM akışını somutlaştırması
güçlü.

Ama tek başına bırakılırsa hâlâ **eksik bir control plane** üretir.  
Ana sorun: doküman operasyonel akışı iyi tarif ediyor ama aşağıdaki production-grade katmanları tam kapatmıyor:
- yetki matrisi,
- queue/backpressure,
- effect/provenance,
- katmanlı memory,
- debate/arbiter,
- observability/SLO,
- protected action governance.

## 2) Korunması gereken güçlü yanlar
| Güçlü yan | Neden korunmalı | Kaynak |
|---|---|---|
| Ground-truth odaklı mevcut sistem okuması | Teorik plan değil, yaşayan sisteme yaslanıyor | `nihai-planlama.md` §1 |
| Rol matrisi | Kim ne yapar sorusuna operasyonel cevap veriyor | `nihai-planlama.md` §2 |
| Routing tablosu | Claude / Strategist / Researcher / Codex / GLM ayrımı pratik | `nihai-planlama.md` §3.1 |
| MD dosya protokolü | Düşük karmaşıklık, debug edilebilir artifact-first handoff | `nihai-planlama.md` §4 |
| Reconnect ve stale-team problemi | Gerçek operasyonel çürüme noktasını görüyor | `nihai-planlama.md` §5.1 |
| Araştırma agent operasyonel spec | Researcher rolünü belirsizlikten çıkarıyor | `nihai-planlama.md` §10 |

## 3) Kritik eksikler ve sorunlar
| Öncelik | Sorun | Neden problem | Önerilen çözüm | Kaynak / ilham |
|---|---|---|---|---|
| **P0** | **Deploy için human gate yok; QA PASS → autonomous deploy** | Bu, kullanıcının güncel ilkesiyle çelişiyor: deploy human gate olmadan geçemez | `deploy` ve `secret-impacting` aksiyonları **protected action** olarak işaretle; QA PASS sadece “deploy-ready” üretmeli | `nihai-planlama.md` §7.3 ile çelişki; kullanıcı ilkeleri; `sistem-planlamacodex.md` §13.3 |
| **P0** | **Capability Registry / Agent Card yok** | Rol tanımı var ama yetki sınırı, tool profili, concurrency, disallowed action yok | Her lane/agent için registry ekle: `allowed_tools`, `disallowed_actions`, `max_concurrency`, `verifier_profile`, `artifact_scope` | `sistem-planlamacodex.md` §12.3 |
| **P0** | **Effect Log + provenance receipt yok** | Run ledger var ama side-effect izlenmiyor; replay-safe değil | `file_write`, `memory_write`, `deploy`, `approval_request` için append-only effect log ekle | `sistem-planlamacodex.md` §13.3; ACP docs |
| **P0** | **Verifier çok dar** | Syntax + secret + state drift yeterli değil; regression/evidence/quality eksik | Verifier v2: code/research/policy task'leri için ayrı gate setleri tanımla | `nihai-planlama.md` §7 vs `sistem-planlama-sonnet4.6.plan.md` §6 |
| **P0** | **Protected action matrisi yok** | Hangi aksiyonun insana gideceği belirsiz | `deploy`, `prompt mutation`, `memory write`, `tool install`, `secret touch` için açık matrix ekle | `sistem-planlamacodex.md` §13.3, §17 |
| **P1** | **Queue / backpressure / concurrency policy yok** | Şu an loop/cycle var ama lane bazlı kapasite kontrolü yok | 4-lane queue + semaphore politikası ekle: `interactive-hot`, `build-repair`, `bulk-research`, `self-evolution` | `sistem-planlamacodex.md` §13.2 |
| **P1** | **Sandbox / isolation policy eksik** | `Builder` için worktree geçiyor ama tüm iş sınıfları için net değil | Research=readonly, build=owned-worktree, mutation=isolated-sandbox, external bridge=session-bound | `nihai-planlama.md` §2/§4/§5 ile kısmen var; tamamlayıcı: `sistem-planlamacodex.md` §13.4 |
| **P1** | **State machine eksik** | Failure recovery tablosu var ama lifecycle standardı yok | `proposed -> queued -> running -> blocked_* -> verifying -> passed/failed/escalated` akışını ekle | `sistem-planlama-sonnet4.6.plan.md` §9a |
| **P1** | **Memory mimarisi eksik** | `memory/daily_reports` var ama working/episodic/semantic/temporal ayrımı yok | 4 katmanlı memory plane ekle; `STATE.json` = temporal-portfolio current view olarak tanımla | `sistem-planlama-sonnet4.6.plan.md` §7; `sistem-planlamacodex.md` §11 |
| **P1** | **Observability / SLO / error budget eksik** | Run ledger tek başına yeterli değil; alarm ve operasyon yüzeyi yok | Metrikler, trace alanları, alarm eşikleri, SLO seti ve error budget ekle | `sistem-planlama-sonnet4.6.plan.md` §10; `sistem-planlamacodex.md` §14 |
| **P1** | **Debate / arbiter / early stopping policy yok** | QA/verifier dışında model ayrışması nasıl çözülecek belli değil | Debate sadece gerektiğinde; max 2 tur; stability score; arbiter = Claude supervisor | `sistem-planlamacodex.md` §13.5 |
| **P1** | **Topoloji siyaseti eksik** | Routing var ama hangi topoloji ne zaman default, net değil | `single-agent`, `sequential`, `iterative-loop`, `supervisor+fan-out`, `critic-reviewer`, `human-gated` sıralaması ekle | `sistem-planlama-sonnet4.6.plan.md` §3 |
| **P2** | **Provider abstraction ile control plane ayrımı yazılmamış** | PAL/MetaMCP gibi katmanlar yanlışlıkla orchestration brain'e dönüşebilir | “Gateway/tool fabric ≠ orchestration control plane” ilkesini açık ekle | `sistem-planlamacodex.md` §6, §12.2 |
| **P2** | **Bridge / ACP politikası yok** | CLI-to-CLI köprüler cazip ama asimetrik; çekirdek runtime yapılırsa kırılgan olur | Bridge/ACP yalnızca edge adapter olarak tanımlansın; core bus task/session/provenance üzerinden kalsın | `codex-claude-bridge`, `codex-weave`, ACP docs, `sistem-planlamacodex.md` §12.2 |

## 4) `nihai-planlama.md` içindeki belirgin çelişkiler
| Çelişki | Neden sorun | Öneri |
|---|---|---|
| `QA PASS = deploy eder. İnsan yok.` | Güncel kullanıcı ilkesiyle doğrudan çelişiyor | `QA PASS -> deploy_ready artifact`; deploy için human approval receipt |
| Artifact-first yaklaşım var ama effect/provenance yok | Handoff var, ama yan etki izi yok | Artifact store + effect log birlikte tanımlanmalı |
| MD dosya protokolü iyi ama memory plane tanımsız | Çalışan dosya iletişimi ile kalıcı hafıza karışıyor | `analysis/` iletişim, `memory/` semantic, `ledger/` episodic diye ayır |
| Run ledger var ama observability yok | Veri toplanır ama yönetim kör kalır | Ledger üstüne metrics+alarms+weekly insights ekle |

## 5) Eklenmesi gereken yeni bölümler
| Yeni bölüm | Ne ekler | Hangi dokümandan alınmalı |
|---|---|---|
| **Topology Matrix + default order** | Hangi işte hangi topoloji kullanılacak | `sistem-planlama-sonnet4.6.plan.md` §3 |
| **Capability Registry / Agent Card** | Yetki sınırı, tool profili, concurrency | `sistem-planlamacodex.md` §12.3 |
| **Layered Memory Architecture** | Working / episodic / semantic / temporal | `sistem-planlama-sonnet4.6.plan.md` §7 + `sistem-planlamacodex.md` §11 |
| **Queue / Backpressure / Semaphore Policy** | Lane bazlı kapasite yönetimi | `sistem-planlamacodex.md` §13.2 |
| **Effect Log + Provenance Receipt** | Replay-safe side-effect yönetimi | `sistem-planlamacodex.md` §13.3 |
| **Sandbox / Isolation Policy** | Çakışma ve blast-radius kontrolü | `sistem-planlamacodex.md` §13.4 |
| **Debate / Arbiter / Early Stop** | Çok-model ayrışmasında disiplin | `sistem-planlamacodex.md` §13.5 |
| **Observability / SLO / Alarm Eşikleri** | Operasyonel görünürlük | `sistem-planlama-sonnet4.6.plan.md` §10 + `sistem-planlamacodex.md` §14 |
| **Protected Action Matrix** | Human gate kapsamı | `sistem-planlamacodex.md` §13.3, §17 |
| **Gateway vs Control Plane Boundary** | MetaMCP/PAL misuse önleme | `sistem-planlamacodex.md` §12.2 |

## 6) `nihai-planlama.md` için önerilen geliştirme planı
### Faz A — Kritik düzeltmeler
| Aksiyon | Fayda | Maliyet | Risk | Bağımlılık |
|---|---|---|---|---|
| Autonomous deploy kararını human-gated deploy-ready modeline çevir | En kritik policy çelişkisi kapanır | Düşük | Düşük | Yok |
| Verifier v1'i verifier v2'ye genişlet | Sessiz hata riski düşer | Orta | Orta | Run ledger |
| Protected action matrix ekle | Yetki sınırı netleşir | Düşük | Düşük | Yok |
| State machine ekle | Recovery deterministik olur | Düşük | Düşük | Yok |

### Faz B — Kontrol düzlemini tamamlama
| Aksiyon | Fayda | Maliyet | Risk | Bağımlılık |
|---|---|---|---|---|
| Capability Registry v1 ekle | Kimin neyi yapacağı netleşir | Düşük-Orta | Düşük | Faz A |
| Queue/backpressure policy ekle | Cycle çakışmaları ve starvation azalır | Orta | Düşük | Registry |
| Effect Log + provenance receipt ekle | Replay-safe operasyon başlar | Orta | Orta | Run ledger |
| Sandbox policy ekle | Paralel task güvenliği artar | Düşük-Orta | Düşük | Registry |

### Faz C — Gelişmiş operasyon
| Aksiyon | Fayda | Maliyet | Risk | Bağımlılık |
|---|---|---|---|---|
| Layered memory mimarisini ekle | Memory drift düşer | Orta | Orta | Ledger |
| Observability + SLO + weekly insights ekle | Sistem yönetilebilir hale gelir | Orta | Düşük | Ledger |
| Debate/arbiter/stability scorer ekle | Gereksiz tartışma azalır | Orta | Orta | Verifier v2 |
| Bridge/ACP edge-adapter policy yaz | Gelecek entegrasyonlarda mimari drift önlenir | Düşük | Düşük | Yok |

## 7) Eklenebilecekler
| Ek | Ne sağlar | Ne zaman |
|---|---|---|
| `WORKFLOW.md`'yi sadece kural kitabı değil, versioned policy front-matter ile kullanmak | Routing/verifier/cost cap tek kaynaktan yönetilir | Hemen |
| `CODEBASE_MAP.md` injection pattern | Yeni session keşif maliyetini azaltır | Hemen |
| File-based A2A claim lock | Duplicate spawn ve çakışan writer riskini azaltır | Hemen |
| LoopLens-benzeri retry intelligence | Thrashing / retry loop görünürlüğü | Orta vade |
| Weekly insights digest | En pahalı/fail patternleri haftalık çıkarır | Orta vade |
| Gateway/tool fabric boundary notu | MCP araç zenginliğinin control plane'e taşmasını engeller | Hemen |
| ACP provenance receipt | Dış runtime/bridge entegrasyonunu izlenebilir yapar | Orta vade |

## 8) Ne alınmalı, ne alınmamalı
| Kaynak plan | Alınmalı | Alınmamalı |
|---|---|---|
| `sistem-planlama-sonnet4.6.plan.md` | Topology Matrix, layered memory, state machine, SLO/error budget, pattern library | Kimi lane'ini mevcut gerçekmiş gibi erken merkeze koymak |
| `sistem-planlamacodex.md` | Capability Registry, 4-lane queue, effect log, sandbox, debate/arbiter, provider abstraction boundary | Faz 1'e gereğinden fazla policy karmaşıklığı yüklemek |

## 9) Net öneri
**`nihai-planlama.md` ana baz olarak korunmalı.**  
Ama “nihai” olabilmesi için aşağıdaki 6 şey eklenmeden bırakılmamalı:

1. **Protected action matrix + deploy human gate**
2. **Capability Registry / Agent Card**
3. **Effect Log + provenance receipt**
4. **Queue/backpressure/semaphore policy**
5. **Layered memory + observability/SLO**
6. **Debate/arbiter/early stopping policy**

Bu altı katman eklenirse `nihai-planlama.md` gerçekten operasyonel + güvenli + replay-safe bir control plane taslağına dönüşür.
