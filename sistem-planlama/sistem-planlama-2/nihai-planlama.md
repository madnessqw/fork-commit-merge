# UniverseCreator Nihai Sistem Planı

**Versiyon:** 2.0 — 2026-04-22 (Autonomous Swarm + Strategist + QA Gate)  
**Durum:** Plan. Kod yok, deploy yok.  
**Referans planlar:**

* `sistem-planlama-sonnet4.6.plan.md` — tam mimari temel (altyapı, topoloji, memory, verifier)
* `sistem-planlamacodex.md` — Capability Registry, Effect Log, sandbox, 4-lane queue  
**Bu döküman ne değil:** Referans planların kopyası. Onlar zaten var, ayrıntılar oraya bakılır.  
**Bu döküman ne:** Kim ne yapar, ne sıklıkla, nereye yazar — **operasyonel görev dağılımı**.

\---

## 1\. Ground Truth: Mevcut Gerçek Sistem

|Katman|Araç|Tetik|Döngü süresi|Çıktı|
|-|-|-|-|-|
|Orkestratör|Claude (`universe\_loop.sh`)|`@reboot`, 10dk cycle|10 dk|Kararlar, `codex\_task.md`, inbox mesajları|
|Karar / Strategist|universe-prague/strategist (Claude subagent)|Claude spawn, `.signals/researcher\_done`|On-demand|`analysis/project\_decision.md`|
|Builder|Codex|Cron `\*/35 \* \* \* \*`|35 dk|`analysis/codex\_result.md`, git commit, deploy|
|Analist / Monitor|OpenCode/GLM5.1|Cron `\*/20 \* \* \* \*`|20 dk|`analysis/oneri.md`, Telegram alert|
|Subagentlar|universe-prague (8 üye)|Claude spawn veya sinyal|On-demand|Role bazlı (tanımlı — §2.2)|

**State (cycle 1072):** 142 aktif ürün, 77 live, 76 sağlıklı, 25 deploy gap, 33 spec-ready.  
**Team durumu:** universe-prague son reconnect cycle 773 (stale — 300 cycle geride).

### 1.1 Çalışan Pipeline (dokunma)

```
GLM  → analysis/oneri.md
         ↓ (Claude okur / subagent tetikler)
Claude → analysis/codex\_task.md
         ↓ (Codex okur)
Codex → analysis/codex\_result.md + git commit
         ↓ (GLM okur)
GLM  → oneri.md güncelle + Telegram
```

Bu pipeline **çalışıyor**. Temel haberleşme protokolü `analysis/` klasöründeki MD dosyaları. **Değiştirilmeyecek.**

### 1.1.1 Gerçek Döngü (güncel)

`universe\_loop.sh` — `@reboot` başlar, 10dk cycle, FACTORY.md oku, sinyaller kontrol et, team'i yönet.

```
\[10dk] Claude (universe\_loop) → FACTORY.md + sinyaller → team spawn/task → codex\_task.md
\[30dk tetik] Claude → researcher teammate'e prompt gönderir (her 3. 10dk cycle) → derin-arastirma → research/YYYY-MM-DD.md (append) → researcher_done sinyal
\[35dk] Codex                 → EXECUTION: codex\_task.md → build → qa\_pending sinyal
                               STRATEGY: research/ okur → codex\_strategy\_input.md → codex\_strategy\_ready sinyal
\[20dk] GLM                   → state sağlık → oneri.md → researcher sinyal (gerekirse)
\[on-demand] Strategist       → research/ + codex\_strategy\_input.md → project\_decision.md
\[on-demand] Builder          → project\_decision.md → products/spec.md + codex\_task.md
\[on-demand] QA-TESTER        → qa\_pending → codex\_result.md → qa\_result.md → deploy sinyal
```

### 1.2 Gerçek Darboğazlar

1. **Strategist eksik:** Kim proje kararı veriyor? Şu an belirsiz — Codex rastgele task alıyor.
2. **Researcher cadence yok:** Fırsat araştırması plansız ve tetik mekanizması tanımsız.
3. **Verifier yok:** Codex çıktısı QA'dan geçmeden deploy kuyruğuna giriyor.
4. **Task contract informal:** `codex\_task.md` yapısız — bazı cycleler stale, bazıları çakışan.
5. **Universe-prague stale:** 8 subagent var ama cycle 773'ten beri reconnect yok.
6. **Run ledger yok:** Ne yapıldı, başarı oranı, maliyet — hiçbiri izlenmiyor.
7. **Deploy pipeline kopuk:** 25 ürün deploy bekliyor; QA PASS → auto-deploy bağlantısı yok.

\---

## 2\. Rol Matrisi — Kim Ne Yapar

### 2.1 Claude Ana Session (Pure Orchestrator)

| Alan | Detay |
|---|---|
| **Ne yapar** | Teammate yönetimi: spawn, prompt gönder, kapat, durum kontrol, sinyal routing |
| **Ne okur** | `analysis/oneri.md`, `analysis/codex_result.md`, `STATE_SUMMARY.json`, `.signals/` |
| **Ne yazar** | `analysis/team_status.md`, `.signals/` (tetik sinyalleri), subagent inboxları |
| **Ne yazmaz** | **Kod yazmaz. Spec yazmaz. Build yapmaz. codex_task.md'ye direkt yazmaz.** |
| **Tetik** | `universe_loop.sh` — `@reboot`, 10dk cycle |
| **Tool** | Tümü (sadece yönetim işleri için) |

**Otonom çalışma kuralı:** Claude, `FACTORY.md` iron kuralına uyar:
> "ASLA onay bekleme. ASLA menü gösterme. STATE.json oku, karar ver, başla."

**Teammate yönetim döngüsü (her 10dk cycle):**
```
1. .signals/ tara → aktif tetik var mı?
2. team_status.md oku → kim meşgul, kim stale, prompt_count kaç?
3. Gerekli teammate'e prompt gönder
4. prompt_count[teammate] >= 2 → teammate kapat → yeniden aç (context reset)
5. STATE_SUMMARY.json + analysis/oneri.md oku → genel sağlık
6. team_status.md güncelle
```

**Context anti-bloat kuralı (kritik):**
- Her teammate için `prompt_count` takibi (`analysis/team_status.md`)
- **Max 2 prompt/session** → teammate kapat → aynı isimle yeniden başlat = temiz context
- Researcher: her 30dk'da 1 prompt (universe_loop.sh'in her 3. cycle'ında)
- Neden 2? Context şişmesi = hallüsinasyon + maliyet artışı + yavaşlama

**Claude ana ASLA:**
- Kod yazmaz
- `products/` altında dosya oluşturmaz  
- Codex'in, Builder'ın veya QA-TESTER'ın işini üstlenmez

\---

### 2.2 Universe-Prague Subagentler — Güncellenmiş Rol Tanımları

#### STRATEGIST ⭐ (Yeni Rol)

|Alan|Detay|
|-|-|
|**Ne yapar**|Pazar/ROI değerlendirme, proje seçimi, Codex feasibility inputuyla birleşik karar üretme|
|**Tetik**|`.signals/researcher\_done` VEYA `.signals/codex\_strategy\_ready` VEYA Claude spawn|
|**Ne okur**|`research/YYYY-MM-DD.md`, `STATE\_SUMMARY.json`, `analysis/oneri.md`, `analysis/codex\_strategy\_input.md` (varsa)|
|**Çıktı dosyası**|`analysis/project\_decision.md`|
|**Çıktı formatı**|`{"selected":"slug","rationale":"...","score":8.5,"risks":\["..."],"source":"research/...","cycle":N}`|
|**Done tanımı**|Seçilen proje netleşmiş, skor verilmiş, Builder handoff hazır|
|**Tool**|**Tümü**|

**İki katmanlı strateji:**

* Claude STRATEGIST: Pazar/ROI/iş kararı — büyük resim
* Codex STRATEGY MODE: Implementation feasibility — "bunu gerçekten yapabilir miyiz, ne kadar sürer?"
* Strategist ikisini okuyarak final `project\_decision.md`'yi yazar
* Codex strategy inputu yoksa sadece kendi analizine dayalı karar verir (daha hızlı ama daha az bilgili)

**Kritik not:** Strategist SADECE karar verir — kod yazmaz.


#### PLANNER ⭐ (Yeni Rol)

| Alan | Detay |
|---|---|
| **Ne yapar** | Strategist kararını alır → görevleri somut task contract'lara dönüştürür → hangi agent ne yapacak belirler → execution sırasını planlar |
| **Tetik** | `analysis/project_decision.md` güncellenince (Strategist çıktısı) |
| **Ne okur** | `analysis/project_decision.md`, `analysis/team_status.md`, `STATE_SUMMARY.json`, `WORKFLOW.md` |
| **Çıktı dosyası** | `analysis/execution_plan.md` — sıralı task listesi, hangi agent, hangi dosya, done kriteri |
| **Yapı** | `## Plan`, `## Task #1: {agent}`, `## Task #2: {agent}` ... her task için input/output/done |
| **Done tanımı** | Tüm task'lar atanmış, sıra netleşmiş, ilk task `codex_task.md`'ye veya ilgili agent'a yazılmış |
| **Tool** | File read/write (planlama yapıyor, build yapmıyor) |

**Planner vs Strategist farkı:**
- Strategist: "HANGI projeyi yapmalıyız? ROI ne? Pazar ne diyor?"
- Planner: "BU projeyi nasıl yapacağız? Hangi sırayla? Kim ne yapacak? Task #1, #2, #3..."

**Planner ASLA:**
- Kod yazmaz
- Strategy kararını değiştirmez
- Execution yapmaz — sadece plan yazar

#### RESEARCHER

|Alan|Detay|
|-|-|
|**Ne yapar**|Pazar araştırması, fırsat keşfi, rakip analizi, teknoloji radar — `derin-arastirma` skill kullanır|
|**Tetik**|Claude ana session — her 10dk cycle'ının her 3'üncüsünde (≈30dk) prompt gönderir; max 2 prompt → teammate reset|
|**Ne okur**|`analysis/oneri.md`, `research/` backlog, web (tüm kaynaklar)|
|**Çıktı dosyası**|`research/YYYY-MM-DD.md` — günlük dosyaya append, her run yeni bölüm ekler|
|**Yapı**|`## \[HH:MM] Araştırma`, `## Fırsatlar`, `## Riskler`, `## Aksiyon Önerisi`, `## Kaynaklar`|
|**Done tanımı**|En az 3 kaynakla desteklenmiş, aksiyon önerisi içeren bölüm; `.signals/researcher\_done` yazar|
|**Tool**|**Tümü** (`derin-arastirma` skill dahil — web search, deep research, GitHub API, dosya okuma/yazma)|

**Derin araştırma notu:** Researcher `derin-arastirma` skill'ini kullanır — içinde web search, URL okuma, kaynak sentezi var. Ayrı tool kurulması gerekmez.  
**Write access:** Tam — `research/` klasörüne serbestçe yazar. Sandbox yok.

#### ANALYST

|Alan|Detay|
|-|-|
|**Ne yapar**|Portföy sağlığı, run analizi, maliyet analizi, haftalık rapor|
|**Tetik**|Codex cycle'dan sonra (trigger: `analysis/codex\_result.md` yenilenince) VEYA günlük|
|**Ne okur**|`analysis/codex\_result.md`, `STATE\_SUMMARY.json`, `logs/codex\_loop.log`|
|**Çıktı dosyası**|`memory/daily\_reports/YYYY-MM-DD.md`, `analysis/weekly\_digest.md` (haftalık)|
|**Yapı**|Cycle özeti, başarı/başarısız, maliyet trend, önerilen sonraki task|
|**Done tanımı**|Sayısal özet + 1-3 actionable öneri içeren rapor|
|**Tool**|File read/write, bash (log analizi)|

#### BUILDER

|Alan|Detay|
|-|-|
|**Ne yapar**|Ürün spec yazımı, mimari tasarım, Codex'e task handoff|
|**Tetik**|Claude spawn talebi (yeni ürün veya major refactor)|
|**Ne okur**|`analysis/project\_decision.md`, `research/` son araştırma, `STATE\_SUMMARY.json`|
|**Çıktı dosyası**|`products/{slug}/spec.md` (ürün spec), `analysis/codex\_task.md` (Codex'e handoff)|
|**Yapı (spec)**|Hedef, kullanıcı akışı, tech stack, dosya listesi, test kriterleri|
|**Done tanımı**|Spec mevcut + `codex\_task.md` güncellenmiş|
|**Escalation**|Belirsiz req → Claude ana session'a sor, bekleme|
|**Tool**|Web search, file read/write|

#### BUILDER-2

|Alan|Detay|
|-|-|
|**Ne yapar**|Builder ile paralel izlerde çalışır; ikinci ürün spec veya mevcut ürün geliştirme|
|**Tetik**|Builder meşgulse ve ikinci track gerekiyorsa|
|**Sandbox**|Builder'dan bağımsız worktree — aynı `products/` dizini üzerine çift yazı yok|
|**Kural**|Builder'ın bitirmediği spec'i overwrite etmez; `products/{slug}-v2/` gibi izole çalışır|
|**Merge**|Otomatik — Builder'dan bağımsız track, çakışma yoksa merge|
|**Not** | Builder kapasitesi yeterliyse bu role gerek yok. ROI düşükse pasif tut. |

#### BUILDER-3 (isteğe bağlı, otonom geliştirici)

| Alan | Detay |
|---|---|
| **Ne yapar** | Codex'in devrettiği uzun süreli geliştirme görevleri — otonom çalışır, Claude'dan prompt beklemez |
| **Tetik** | `.signals/builder2_needed` veya Claude spawn talebi |
| **Ne okur** | `analysis/execution_plan.md`, `analysis/codex_block.md`, `products/{slug}/spec.md` |
| **Çıktı** | Kod değişiklikleri, commit, `analysis/builder3_result.md` |
| **Done tanımı** | Spec'teki tüm maddeler tamamlanmış, QA sinyal gönderilmiş |
| **Kural** | Builder-2 meşgulse aktif et. Her ikisi de meşgulse Claude'a escalate. |
| **Tool** | **Tümü** |

#### OPTIMIZER

|Alan|Detay|
|-|-|
|**Ne yapar**|SEO analizi, dönüşüm optimizasyonu, deploy sonrası ürün kalite skoru|
|**Tetik**|Haftalık (pazar sabahı) VEYA yeni deploy sonrası|
|**Ne okur**|`STATE\_SUMMARY.json`, `products/{slug}/spec.md`, vercel data|
|**Çıktı dosyası**|`analysis/seo\_report.md`, `products/{slug}/optimization.md`|
|**Done tanımı**|Her canlı ürün için skor + top-3 iyileştirme önerisi|
|**Tool**|Web search, file read/write, bash|

#### QA-TESTER

|Alan|Detay|
|-|-|
|**Ne yapar**|Codex çıktısını doğrular, hata tespiti, test koşturma|
|**Tetik**|`analysis/codex\_result.md` güncellendikten sonra (post-build hook)|
|**Ne okur**|`analysis/codex\_result.md`, `products/{slug}/spec.md`, git diff|
|**Çıktı dosyası**|`analysis/qa\_result.md` (PASS/FAIL + kanıt)|
|**Yapı**|`## Durum: PASS/FAIL`, `## Test Edilen`, `## Sorunlar`, `## Öneri`|
|**Done tanımı**|Her test edilebilir item için sonuç; FAIL ise `sorun\_analizi.md` güncellenmeli|
|**Escalation**|FAIL → `analysis/sorun\_analizi.md` yaz → Codex bir sonraki cycle'da okur|
|**Tool**|Bash, file read/write, python|

#### SKILL-WRITER

|Alan|Detay|
|-|-|
|**Ne yapar**|Skill dosyaları yaz, workflow dökümanları güncelle, ders çıkarımlarını kaydet|
|**Tetik**|Claude spawn talebi (yeni pattern öğrenilince, skill güncellemesi gerekince)|
|**Ne okur**|`skills/`, `memory/`, `analysis/codex\_result.md` (pattern mining)|
|**Çıktı dosyası**|`skills/{skill-name}.md`, `memory/lessons.md`|
|**Done tanımı**|Test edilebilir skill dosyası — en az 1 gerçek kullanım kanıtı ile|
|**Tool**|File read/write|

\---

### 2.3 Codex (Otonom Builder)

|Alan|Detay|
|-|-|
|**Ne yapar**|Kod değişikliği, otomasyon iyileştirme, git commit, test koşturma, QA PASS sonrası auto-deploy + **boştaysa strateji analizi**|
|**Tetik**|Cron `\*/35 \* \* \* \*` (`codex\_loop.sh`)|
|**Ne okur**|`skills/codex\_skill.md` → `analysis/codex\_task.md` → `analysis/oneri.md` + `STATE\_SUMMARY.json` + `.signals/qa\_result` + `research/` (strategy mode)|
|**Ne yazar**|`analysis/codex\_result.md`, `.signals/qa\_pending`, git commit; QA PASS sonrası `deploy\_product.sh`; boştaysa `analysis/codex\_strategy\_input.md`|
|**Bütçe**|Max 35 dk/cycle, max 1 saat/saat (flock korumalı)|
|**Autonomous deploy**|`qa\_result.md: PASS` → `./scripts/deploy\_product.sh {slug}` otomatik çalışır|
|**Tool**|**Tümü**|

**Codex çalışma modları (öncelik sırası):**

```
Codex cycle başlar
  ↓
1. EXECUTION MODE (en yüksek öncelik):
   codex_task.md'de bekleyen task var mı?
   → EVET: normal build/fix/deploy cycle
   → QA PASS → deploy_product.sh otomatik çağır

2. SELF-PLAN MODE (execution_plan.md varsa):
   analysis/execution_plan.md'de Codex'e atanmış task var mı?
   → EVET: kendi task'ını al, plan yap, execute et, sonucu yaz
   → Uzun süreli iş (>35dk tahmin) → analysis/codex_task.md'ye yaz + .signals/builder2_needed → Builder-2'ye devret
   → Küçük iyileştirme → .signals/optimizer_needed → Optimizer'a devret

3. STRATEGY MODE (fallback, execution/plan yoksa):
   research/ + project_decision.md'de yeni input var mı?
   → EVET: implementation feasibility analiz et
            "Bu ürünü yapabilir miyiz? Nasıl? Ne sürer?"
   → analysis/codex_strategy_input.md yazar
   → .signals/codex_strategy_ready yazar (Strategist tetiklenir)
   → HAYIR: oneri.md'ye bak, kendi teknik önerisini üret
```

**Codex self-routing kuralları:**

| Durum | Yönlendirme | Neden |
|---|---|---|
| Kısa görev (<35dk, net spec) | Kendisi execute eder | Hızlı, bağımsız |
| Uzun / multi-step görev | Builder-2'ye devret | Context limit + kendi loop'u 35dk |
| Küçük optimize görev | Optimizer'a devret | Optimizer bu işe özel, Codex builder'dır |
| Bilgi eksik, spec muğlak | `analysis/codex_block.md` yazar | Claude → Planner → netleştir |

**Neden dual/triple mode?**  
Codex codebase'i en iyi bilen agent. Pazar analizi yapamaz ama "bu ürünü yapabilir miyiz?" sorusuna doğru cevap verir. Claude Strategist pazar kararı alır; Codex implementasyon fizibilitesi katar. SELF-PLAN MODE ise Planner çıktısını alıp doğrudan uygulamasına olanak tanır — arada Claude koordinasyon gerektirmez.

**Geliştirilecek:** codex\_skill.md'ye dual-mode mantığı, run\_ledger append, qa\_pending sinyal üretimi eklenmeli.

\---

### 2.4 OpenCode / GLM5.1 (Analist + Monitor)

|Alan|Detay|
|-|-|
|**Ne yapar**|Portföy sağlık skoru, Codex auth kontrolü, öneri üretimi, Telegram alert|
|**Tetik**|Cron `\*/20 \* \* \* \*` (`glm\_loop.sh`)|
|**Ne okur**|`STATE\_SUMMARY.json`, `analysis/codex\_result.md`, `analysis/sorun\_analizi.md`|
|**Ne yazar**|`analysis/oneri.md`|
|**Bütçe**|Max 20 dk/cycle|
|**Escalation**|Kritik sorun → Telegram + `analysis/sorun\_analizi.md` (Codex'in okuması için)|
|**Ne yapamaz**|Kod değişikliği, deploy, spec yazımı|

**Ek görev (eklenecek):** `analysis/codex\_result.md` her güncellenince `qa\_result.md` varlığını kontrol et; yoksa `qa\_pending` flag koy → Claude'a bildir.

\---

## 3\. Görev Dağılımı — Karar Ağacı

```
Görev Geldi
    │
    ├── Pazar araştırması, fırsat keşfi
    │       → RESEARCHER (30dk loop, derin-arastirma skill)
    │       → Output: research/YYYY-MM-DD.md → .signals/researcher_done
    │
    ├── Proje / fırsat seçimi (pazar/ROI kararı)
    │       → STRATEGIST (Claude subagent)
    │       → Input: research/ + codex_strategy_input.md (varsa)
    │       → Output: analysis/project_decision.md
    │
    ├── Execution planlaması (kim ne yapacak, hangi sırayla)
    │       → PLANNER (Claude subagent)
    │       → Input: analysis/project_decision.md
    │       → Output: analysis/execution_plan.md
    │
    ├── Ürün spec / mimari tasarım
    │       → BUILDER (on-demand)
    │       → Input: analysis/execution_plan.md
    │       → Output: products/{slug}/spec.md + codex_task.md
    │
    ├── Paralel spec ihtiyacı
    │       → BUILDER-2 (Builder meşgulse)
    │       → BUILDER-3 (uzun süreli otonom görev)
    │
    ├── Kod implementasyonu (kısa/net görev <35dk)
    │       → Codex EXECUTION MODE (35dk loop, öncelik)
    │
    ├── Codex execution planı varsa
    │       → Codex SELF-PLAN MODE
    │       → Uzun görev → Builder-2/3'e devret
    │       → Küçük iyileştirme → Optimizer'a devret
    │
    ├── Implementasyon fizibilite analizi
    │       → Codex STRATEGY MODE (execution yoksa)
    │       → Output: codex_strategy_input.md → Strategist tetiklenir
    │
    ├── Portföy analizi, run raporu
    │       → ANALYST (günlük)
    │       → Output: memory/daily_reports/
    │
    ├── Ucuz analiz, sınıflandırma, sağlık skoru
    │       → GLM5.1 (20dk loop)
    │
    ├── Kalite doğrulama (post-build)
    │       → QA-TESTER → analysis/qa_result.md
    │       → PASS → .signals/deploy_ready → Codex auto-deploy
    │
    ├── SEO / optimizasyon
    │       → OPTIMIZER (haftalık / post-deploy)
    │
    └── Yüksek-çıta synthesis, escalation, team yönetimi
            → Claude Ana (Pure Orchestrator)
```

### 3.1 Hızlı Routing Tablosu

| Task türü | Claude Ana | Strategist | Planner | Researcher | Analyst | Builder | QA | Optimizer | Codex (exec) | Codex (strategy) | GLM5.1 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Pazar araştırması | — | — | — | ✅ | — | — | — | — | — | — | — |
| Proje seçimi (pazar/ROI) | — | ✅ | — | — | — | — | — | — | — | — | — |
| Execution plan (kim ne yapacak) | — | — | ✅ | — | — | — | — | — | — | — | — |
| Proje seçimi (fizibilite) | — | — | — | — | — | — | — | — | — | ✅ | — |
| Ürün spec yazımı | — | — | — | — | — | ✅ | — | — | — | — | — |
| Kod implementasyonu (kısa) | — | — | — | — | — | — | — | — | ✅ | — | — |
| Kod implementasyonu (uzun) | — | — | — | — | — | ✅(B-2/3) | — | — | devret | — | — |
| Portföy sağlık | — | — | — | — | ✅ | — | — | — | — | — | ✅ |
| Kalite gate | — | — | — | — | — | — | ✅ | — | — | — | — |
| Deploy (autonomous) | — | — | — | — | — | — | — | — | ✅ | — | — |
| SEO analizi | — | — | — | — | — | — | — | ✅ | — | — | ✅ |
| Skill/workflow yazımı | ✅(spawn) | — | — | — | — | — | — | — | — | — | — |
| Escalation / final | ✅ | — | — | — | — | — | — | — | — | — | — |

\---

## 4\. Context Management — MD Dosya Protokolü

### 4.1 Temel Kural

**MD dosya haberleşmesi çalışıyor. Doğrudan değiştirilmiyor.**  
`analysis/` klasörü CLI'lar arası haberleşme kanal olarak kalıyor.  
Tek değişiklik: **standart dosya isimleri + sahiplik kuralları**.

### 4.2 Standart Dosya Haritası

|Dosya|Kimin yazıyor|Kimin okuyor|Ne içeriyor|
|-|-|-|-|
|`analysis/codex\_task.md`|Claude ana / BUILDER|Codex|Mevcut cycle görevi|
|`analysis/codex\_result.md`|Codex|GLM, ANALYST, QA-TESTER|Son cycle çıktısı|
|`analysis/oneri.md`|GLM5.1|Claude ana, Codex|Portföy durumu + öneriler|
|`analysis/sorun\_analizi.md`|GLM, QA-TESTER|Codex|Aktif sorunlar|
|`analysis/qa\_result.md`|QA-TESTER|Claude ana, Codex|Son build kalite sonucu|
|`analysis/seo\_report.md`|OPTIMIZER|Claude ana|SEO durumu|
|`analysis/team\_status.md`|Claude ana|Claude ana|Subagent durumu özeti|
|`research/YYYY-MM-DD.md`|RESEARCHER|Claude ana, BUILDER|Araştırma bulguları|
|`products/{slug}/spec.md`|BUILDER|Codex, QA|Ürün spec'i|
|`products/{slug}/optimization.md`|OPTIMIZER|Claude ana|Ürün iyileştirme önerileri|
|`memory/daily\_reports/YYYY-MM-DD.md`|ANALYST|Claude ana|Günlük rapor|
|`STATE\_SUMMARY.json`|`update\_summary.py`|Hepsi|Portföy ground truth|

### 4.3 Sahiplik Kuralı (Çakışma Önleme)

* **Bir dosyaya tek writer.** Aynı dosyayı iki agent aynı anda düzenleyemez.
* `analysis/codex\_task.md` → sadece Claude ana/BUILDER yazar; Codex sadece okur.
* `analysis/codex\_result.md` → sadece Codex yazar; diğerleri sadece okur.
* `analysis/oneri.md` → sadece GLM5.1 yazar; diğerleri sadece okur.
* Çakışma riski → `.lock` dosyası (`/tmp/context\_{name}.lock`) kullan.

### 4.4 WORKFLOW.md (Eklenecek Yeni Dosya)

`/home/gokhan/UniverseCreator/WORKFLOW.md` — Sistemin kısa kural kitabı.  
İçereceği: pipeline özeti, kim ne yazar, sahiplik kuralları, escalation kuralları.  
Her CLI oturum başında okur. Bu dosya politikayı kodun içine gömmeyi önler.

### 4.5 CODEBASE\_MAP.md (Eklenecek Yeni Dosya)

`/home/gokhan/UniverseCreator/CODEBASE\_MAP.md` — Klasör yapısı + anahtar dosyalar özeti.  
Codex ve subagentler bu dosyayı okuyarak context kazanır; tam repo scan yerine.

### 4.6 Agent Knowledge Map — Kim Ne Okuyarak Başlar?

Her agent session başında hangi dosyaları okuduğu nettir. Bu bilgi hem skill prompt'larına hem WORKFLOW.md'ye girer.

| Agent | Zorunlu Başlangıç Dosyaları | Ek Okuma (koşullu) | Öğrendiği |
|---|---|---|---|
| **Claude Ana** | `FACTORY.md`, `STATE_SUMMARY.json`, `analysis/oneri.md`, `analysis/team_status.md`, `.signals/` (hepsi) | `analysis/qa_result.md` (sinyal varsa) | Mevcut sistem durumu, kim ne yapıyor, hangi sinyal var |
| **STRATEGIST** | `research/YYYY-MM-DD.md` (son), `STATE_SUMMARY.json`, `analysis/oneri.md` | `analysis/codex_strategy_input.md` (varsa) | Pazar trendi, portföy boşlukları, Codex fizibilite görüşü |
| **PLANNER** | `analysis/project_decision.md`, `analysis/team_status.md`, `STATE_SUMMARY.json`, `WORKFLOW.md` | `analysis/execution_plan.md` (önceki plan varsa) | Ne yapılacak, kim müsait, nasıl sıralanacak |
| **RESEARCHER** | `analysis/oneri.md`, `research/YYYY-MM-DD.md` (dün), `CODEBASE_MAP.md` | — | Araştırma geçmişi, boşluklar, odak alanlar |
| **BUILDER** | `analysis/project_decision.md`, `analysis/execution_plan.md`, `research/` (son), `STATE_SUMMARY.json` | `products/{slug}/spec.md` (refactor ise) | Proje kararı, pazar insight, mevcut kod yapısı |
| **BUILDER-2/3** | `analysis/execution_plan.md`, `products/{slug}/spec.md`, `CODEBASE_MAP.md` | `analysis/codex_block.md` (varsa) | Tam spec, dosya yapısı, görev detayı |
| **CODEX** | `skills/codex_skill.md`, `analysis/codex_task.md`, `analysis/oneri.md`, `STATE_SUMMARY.json` | `analysis/execution_plan.md`, `research/` (strategy mode) | Yapılacak iş, sistem durumu, kendi modu |
| **QA-TESTER** | `skills/agents/qa_tester.md`, `analysis/codex_result.md`, `products/{slug}/spec.md` | `analysis/sorun_analizi.md` (önceki fail varsa) | Build çıktısı, spec kriterleri, bilinen sorunlar |
| **OPTIMIZER** | `STATE_SUMMARY.json`, `products/{slug}/optimization.md` (varsa) | `analysis/seo_report.md` | Live ürün listesi, mevcut SEO durumu |
| **ANALYST** | `analysis/codex_result.md`, `STATE_SUMMARY.json`, `logs/codex_loop.log` | `analysis/qa_result.md` | Cycle performansı, cost trend |
| **GLM/OpenCode** | `skills/glm_analyst.md`, `STATE_SUMMARY.json`, `analysis/codex_result.md` | `analysis/sorun_analizi.md` | Portföy sağlığı, Codex son iş |

**MD Dosya Mimarisi Özeti:**
```
ÖĞRENME KATEGORİSİ       DOSYA                           OKUR
─────────────────────────────────────────────────────────────────
Sistem durumu (ground truth) → STATE_SUMMARY.json          Herkes
Kurallar / politika       → FACTORY.md, WORKFLOW.md        Claude, Codex, skill'ler
Repo haritası             → CODEBASE_MAP.md                Codex, Builder'lar
Skill talimatları         → skills/agents/{role}.md        İlgili agent
─────────────────────────────────────────────────────────────────
İŞ AKIŞI
Pazar araştırma           → research/YYYY-MM-DD.md         Strategist, Planner
Strateji kararı           → analysis/project_decision.md   Planner, Builder
Execution planı           → analysis/execution_plan.md     Codex, Builder'lar
Mevcut görev              → analysis/codex_task.md         Codex
Build sonucu              → analysis/codex_result.md       QA, GLM, Analyst
QA sonucu                 → analysis/qa_result.md          Claude, Codex
Optimizasyon              → analysis/seo_report.md         Optimizer, Claude
─────────────────────────────────────────────────────────────────
SİSTEM SAĞLIĞI
Agent durumu              → analysis/team_status.md        Claude
Öneriler                  → analysis/oneri.md              Claude, Codex, Planner
Sorun kaydı               → analysis/sorun_analizi.md      Codex, GLM
Sinyaller                 → .signals/*.signal              Herkes (poll)
```

\---

## 5\. Subagent Yönetim İyileştirmeleri

### 5.1 Reconnect Protokolü

**Şu an:** Claude ana session açıldığında team üyelerine reconnect mesajı gönderiliyor ama cycle 773'ten beri stale.

**İyileştirme:**

1. Claude ana session başladığında `\~/.claude/teams/universe-prague/inboxes/` tara.
2. Her inbox için son timestamp oku; 24h üstü stale.
3. Stale üyeye reconnect + güncel task mesajı gönder.
4. `analysis/team\_status.md`'ye son reconnect + task durumu yaz.

**Reconnect mesaj formatı (JSON inbox'a):**

```json
{
  "from": "team-lead",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "cycle": 1072,
  "type": "reconnect",
  "current\_state": "cycle 1072, 77 live, 25 deploy gap",
  "your\_task": "<role-specific task>",
  "output\_target": "<dosya yolu>",
  "done\_when": "<tamamlanma kriteri>"
}
```

### 5.2 Task Delegation Kuralı

Claude subagent\[teammate] spawn etmeden önce:

1. Task contract yaz (bkz. §6)
2. Ambiguity varsa önce resolve et; belirsiz task spawn etme
3. Done kriteri net olmadan spawn etme
4. Spawn sonrası bekleme süresi belirle; timeout'ta escalate

### 5.3 Builder-2 Kural

Builder-2 ancak aşağıdaki koşullarda aktif edilir:

* Builder aktif bir task'te meşgul (spawn bekliyor)
* Paralel spec gerekli (farklı ürün)
* Aynı `products/{slug}/spec.md` üzerine çift yazma riski yoksa

Aksi hâlde pasif tut. Gereksiz subagent = gürültü.

### 5.4 Skill-Writer Kural

Skill-writer yalnızca:

* Yeni bir pattern öğrenildiğinde ve `skills/` güncellenmesi gerektiğinde
* Mevcut skill'de hata bulunduğunda
* Kullanıcı döküman güncellemesi istediğinde

Rutin task için kullanılmaz. ROI düşük — sadece real knowledge capture için.

### 5.5 Context Anti-Bloat Kuralı (kritik)

Context şişmesi = hallüsinasyon + maliyet artışı + yavaşlama. Önleme:

**Kural:** Her teammate için `prompt_count` tutulur. `analysis/team_status.md` içinde:

```
teammate: researcher
last_prompt: 2024-01-15T14:30:00Z
prompt_count: 2
status: active
```

**Reset protokolü:**
```
prompt_count[teammate] >= 2
  → teammate kapat (session end)
  → aynı isimle yeni session başlat (temiz context)
  → prompt_count = 0
  → team_status.md güncelle
```

**Researcher cadence:**
- Claude her 3. 10dk cycle'da (≈30dk) researcher'a 1 prompt gönderir
- 2 prompt sonrası otomatik reset
- Yani her ~60dk tam bir researcher rotation döngüsü

**Genel kural:**
- Hiçbir teammate 2 prompt'tan fazla almaz (reset olmadan)
- Uzun task? Task daha küçük parçalara böl, her part için yeni session
- Context reset = fresh start = kalite korunur

\---

## 6\. Task Contract Formatı

Mevcut `analysis/codex\_task.md` iyi bir başlangıç. Aşağıdaki standart şablona uyarlanacak:

```markdown
# Task Contract — \[ID] \[YYYY-MM-DD HH:MM UTC]

## Amaç
<bir cümle — ne yapılacak>

## Input
- <dosya1 veya artifact>
- <dosya2>

## Done Kriteri
- \[ ] <ölçülebilir kriter 1>
- \[ ] <ölçülebilir kriter 2>

## Allowed Tools
<araç listesi veya "codex\_skill.md sınırları">

## Timeout
<35dk / 60dk / etc.>

## Cost Cap
<USD veya token limit>

## Verify Rule
<nasıl doğrulanır — örn: python3 -m py\_compile, bash -n>

## Escalation Rule
<ne zaman Claude ana'ya bildir>

## Out of Scope
<ne yapılmayacak — deploy, publish, etc.>
```

Bu şablon `skills/task\_contract\_template.md` olarak kaydedilmeli.

\---

## 7\. Verifier Katmanı (Basit, Hızlı)

**Mevcut:** Codex çıktısı doğrudan git'e gidiyor. Verifier yok.

**Hedef (basit v1):** QA-TESTER her Codex cycle sonrası `codex\_result.md`'yi okur; syntax + mantık kontrolü yapar; `qa\_result.md` yazar.

### 7.1 QA v1 Kuralları (Deterministik)

|Kural|Kontrol|Fail Durumu|
|-|-|-|
|Syntax|Python: `py\_compile`, Shell: `bash -n`|FAIL — `sorun\_analizi.md`'ye yaz|
|Secret scan|Regex: `(api\_key|secret|
|State drift|`STATE\_SUMMARY.json` last\_updated ≤ 5dk önce|WARN|
|Commit zorunlu|`git log --since="1 hour ago"` empty|WARN — task boş geçti|
|Out-of-scope write|Deploy config, vercel.json değiştirildi|FLAG — log, GLM'e bildir, cycle durdur|

### 7.2 QA v1 Akışı (Autonomous)

```
Codex → codex\_result.md yazar → .signals/qa\_pending yazar
QA-TESTER → .signals/qa\_pending okur → codex\_result.md analiz eder
           → qa\_result.md yazar (PASS/FAIL/WARN)
  PASS → .signals/deploy\_ready yazar
  FAIL → sorun\_analizi.md günceller
Codex (sonraki cycle) → .signals/deploy\_ready varsa → deploy\_product.sh çalıştırır
                      → .signals/qa\_result=FAIL → fix cycle başlatır
```

### 7.3 Autonomous Deploy Gate

**Kural:** QA PASS = Codex deploy eder. İnsan yok.  
**Mantık:** FACTORY.md iron kuralı "ASLA onay bekleme" — deploy kararını QA verifier'ı verir.  
`qa\_result.md: PASS` → `./scripts/deploy\_product.sh {slug}` → deploy.  
`qa\_result.md: FAIL` → `sorun\_analizi.md` güncellenir → Codex sonraki cycle'da okur → fix.

\---

## 8\. Run Ledger (Basit v1)

**Mevcut:** Log dosyaları var (`logs/codex\_loop.log`, `logs/glm\_loop.log`) ama sorgulanamıyor.

**Hedef:** JSONL tabanlı run ledger — `logs/run\_ledger.jsonl`.

```json
{
  "run\_id": "codex-2026-04-22-1430",
  "agent": "codex",
  "cycle": 1072,
  "started\_at": "2026-04-22T14:30:00Z",
  "ended\_at": "2026-04-22T14:58:22Z",
  "duration\_min": 28.4,
  "task\_contract\_id": "codex\_task-20260422",
  "artifacts\_in": \["analysis/codex\_task.md"],
  "artifacts\_out": \["analysis/codex\_result.md"],
  "commit\_sha": "abc123",
  "qa\_result": "PASS",
  "failure\_class": null,
  "retry\_count": 0,
  "cost\_usd": null
}
```

Her cycle sonunda Codex veya GLM bu satırı `run\_ledger.jsonl`'e append eder.  
ANALYST haftalık bu dosyayı okuyarak trend raporu çıkarır.

\---

## 9\. Failure Recovery

|Senaryo|Müdahale|Sorumluluk|
|-|-|-|
|Codex cycle başarısız|`codex\_result.md` yoksa GLM Telegram alert gönderir, sonraki cycle retry|GLM otomatik|
|Codex 3 cycle art arda fail|`analysis/sorun\_analizi.md`'ye yaz → Claude ana'ya Telegram|GLM|
|QA FAIL|`sorun\_analizi.md` güncelle, Codex sonraki cycle okur|QA-TESTER|
|Subagent timeout|Task FAIL olarak işaretle, Claude ana'ya bildir|Claude ana|
|Deploy bloğu (vercel auth)|Mevcut `codex\_auth\_switch.md` devreye girer|GLM|
|State drift|`update\_summary.py` yeniden çalıştır|Claude ana / GLM|
|Stale codex\_task.md|GLM cycle başında timestamp kontrol eder, stale ise warn|GLM|

\---

## 10\. Araştırma Agent Operasyonel Spec

Bu bölüm özellikle soruldu: **Researcher ne sıklıkla çalışır, nereye yazar?**

### 10.1 Tetik Koşulları

| Tetik | Açıklama |
|---|---|
| **Claude 30dk prompt** | **Ana tetik** — `universe_loop.sh` her ≈30dk'da Claude researcher teammate'e prompt gönderir (her 3. 10dk cycle = 30dk) |
| Fırsat boşluğu | `analysis/oneri.md` → `next_action: research_needed` → Claude anında researcher spawn |
| Deploy gap yüksek | `deploy_missing > 20` → GLM `.signals/researcher_needed` yazar → Claude tetiklenir |

**Researcher sürekli çalışır.** 30dk'da 1 kez prompt alır, 2 prompt sonrası teammate reset.

### 10.2 Araştırma Output Formatı

Dosya: `research/YYYY-MM-DD.md` — günlük tek dosya, her 30dk'lık run yeni bölüm ekler.

```markdown
# Araştırma — YYYY-MM-DD

## \[09:30] Araştırma — {konu}

### Fırsatlar
| Fırsat | Pazar | Rekabet | Güven | Kaynak |
|---|---|---|---|---|
| <isim> | <büyüklük> | <düşük/orta/yüksek> | <0-10> | <URL> |

### Teknoloji / Tool Radar
- <yeni tool veya pattern> — neden alakalı

### Riskler
- <tespit edilen risk>

### Aksiyon Önerisi
- \[ ] <somut önerilen aksiyon>

### Kaynaklar
- <URL1>
- <URL2>

---

## \[10:00] Araştırma — {konu2}
...
```

### 10.3 Araştırma → Pipeline Bağlantısı

```
RESEARCHER → research/YYYY-MM-DD.md
BUILDER okur → products/{slug}/spec.md oluşturur
Claude ana → codex\_task.md günceller
Codex → implement eder
```

Researcher araştırması `codex\_task.md`'yi doğrudan yazmaz. BUILDER aracılığıyla geçer.

\---

## 11\. Roadmap

### Faz 0 — Şimdi (Bu Hafta)

|#|Aksiyon|Sahip|Çıktı|Önce|
|-|-|-|-|-|
|F0.1|`WORKFLOW.md` yaz|Claude ana session|`WORKFLOW.md`|—|
|F0.2|`CODEBASE\_MAP.md` yaz|Claude ana session|`CODEBASE\_MAP.md`|—|
|F0.3|Universe-prague reconnect + task atama (Strategist dahil)|Claude ana session|`analysis/team\_status.md`|F0.1|
|F0.4|`skills/agents/qa\_tester.md` yaz|skill-writer|QA agent skill|F0.3|
|F0.5|`skills/task\_contract\_template.md` yaz|skill-writer|Task şablonu|F0.3|
|F0.6|`skills/agents/strategist.md` yaz (dual-input: market + codex)|skill-writer|Strategist agent skill|F0.3|
|F0.7|`skills/agents/researcher.md` güncelle (30dk cadence, derin-arastirma, full write)|skill-writer|Güncel researcher skill|F0.3|
|F0.8|`research/backlog.md` oluştur|Claude ana|Araştırma backlog|—|

### Faz 1 — 1-2 Hafta

|#|Aksiyon|Sahip|Çıktı|Önce|
|-|-|-|-|-|
|F1.1|`codex\_skill.md` güncelle|skill-writer|+dual-mode (execution>strategy), +run\_ledger, +qa\_pending, +auto-deploy|F0.4|
|F1.2|`glm\_analyst.md` güncelle|skill-writer|+qa\_result kontrolü, +researcher\_needed sinyal|F0.4|
|F1.3|`universe_loop.sh` araştırma cadence mantığı ekle|Claude/skill-writer|Her 3. cycle'da researcher teammate prompt gönderir, prompt_count>=2 → reset|F0.7|
|F1.4|Run Ledger v1 (`logs/run\_ledger.jsonl`) aktifleştir|Codex|Her cycle sonrası entry ekleniyor|F1.1|
|F1.5|Researcher → Strategist pipeline bağla (.signals/researcher\_done → strategist tetik)|Claude|project\_decision.md akıyor|F0.6|

### Faz 2 — 1-3 Ay

|#|Aksiyon|Sahip|Çıktı|Önce|
|-|-|-|-|-|
|F2.1|ANALYST haftalık digest otomasyon|ANALYST|`analysis/weekly\_digest.md` her pazartesi|F1.4|
|F2.2|Deploy gap sıfırla (25 ürün)|Codex autonomous|`deploy\_missing → 0`|F1.1|
|F2.3|Spec-ready pipeline (33 ürün)|BUILDER + Codex|Spec → deploy çevrim hızlanır|F0.5|
|F2.4|Observability (minimal)|ANALYST|`logs/run\_ledger.jsonl` üzerinden query|F1.4|

### Faz 3 — 3-6 Ay

|#|Aksiyon|Sahip|Çıktı|Önce|
|-|-|-|-|-|
|F3.1|Checkpoint + replay harness|Codex + Claude ana|Uzun koşu güvenli|F1.4|
|F3.2|Episodic memory olgunlaştır|ANALYST|Son 100 run sorgulanabilir|F3.1|
|F3.3|Provider-aware scheduler|Claude ana|Rate limit kaynaklı fail azalır|F2.1|
|F3.4|MiniMax / Kimi entegrasyonu|Claude ana|Yeni rol belirleme + routing|F1.4|

\---

## 12\. Anti-Pattern Listesi (Operasyonel)

|Anti-pattern|Risk|Önlem|
|-|-|-|
|Team stale tutmak|7 subagent atıl — potansiyel değer kaybı|Her oturum başı reconnect|
|Codex'e belirsiz task vermek|Stale task → boş cycle → maliyet|Task contract zorunlu|
|QA'sız deploy|Kırık kod production'a çıkar|Deploy = QA PASS şartı (autonomous)|
|`analysis/` üzerine çift yazı|Context bozulur|Dosya sahiplik kuralı|
|Tüm transcript handoff|Context şişmesi, maliyet patlaması|Artifact ref + delta summary|
|Builder-2'yi sürekli aktif tutmak|Gereksiz parallelism + çakışma|Sadece ihtiyaç anında|
|Researcher çıktısını direkt codex\_task'e koymak|Spec adımı atlandı|Pipeline: Researcher → Strategist → Builder → codex\_task|
|Her şeyi Claude'a sormak|Bottleneck oluşur|GLM/Codex/subagent önce dene|
|Deploy için insan onayı beklemek|Sistem durur, otonom döngü kırılır|FACTORY.md: "ASLA onay bekleme" — QA gate yeterli|
|skill-writer'ı rutin task için kullanmak|Gürültü|Sadece real knowledge capture|
|Codex'e hem stratejik karar hem kod ver|Context dilüsyon, iki rolde ortaüstü|Strategist karar verir, Codex uygular|

\---

## 13\. Tool Erişim Politikası (Full Access)

**Sandbox yok. Kısıtlama yok. Her agent tüm araçlara erişebilir.**

|Agent|Tool Erişimi|Not|
|-|-|-|
|Claude Ana|Tümü|Orkestratör|
|Strategist|Tümü|Karar verir; kod yazmaz (kural değil, görev tanımı)|
|Researcher|Tümü|`derin-arastirma` skill dahil|
|Builder|Tümü|Spec + codex\_task yazar|
|QA-TESTER|Tümü|bash, python, git dahil|
|Analyst|Tümü|Log analizi için bash gerekir|
|Optimizer|Tümü|Vercel API dahil|
|Skill-Writer|Tümü|skills/ dosyaları yazar|
|Codex|Tümü|Build + deploy + strategy|
|GLM5.1|Tümü (OpenCode izinleri)|Monitor + alert|

**Neden full access?**  
Kısıtlama = engel = cycle durur = deploy gap büyür. Güven sorunları agent yanlış konfigüre edilirse çözülür, tool kısıtlamasıyla değil. FACTORY.md iron kuralları yeterli guardrail.

**Referans çakışma notu:** `sistem-planlamacodex.md §13.4` "Research → yazma yetkisi Yok" diyordu. Bu geçersiz. Bu belge kazanır.

\---

## 14\. Açık Sorular

1. <b>~~Researcher için cron var mı?~~</b> **CEVAPLANDI:** Claude universe_loop.sh içinde her 3. cycle'da researcher teammate'e prompt gönderir. Ayrı script yok.
2. **QA-TESTER tetik mekanizması:** GLM `codex\_result.md` güncellenince nasıl haberdar edecek? (timestamp kontrolü yeterli mi?)
3. **ANALYST günlük rapor:** Her cycle sonra mı, sadece bir kez günde mi çalışsın?
4. **Builder + Codex handoff:** Codex task contract'ı Builder mı yazacak, Claude ana mı? İkisi çakışırsa?
5. **MiniMax / Kimi eklenince:** Hangi lane'e girecekler?
6. **Run ledger sahipliği:** Codex kendi entry'sini mi yazacak, yoksa GLM mi append edecek?
7. **Codex strategy mode çakışması:** Execution + strategy aynı anda tetiklenirse hangisi öncelik alır? (Cevap: Execution — ama belgelenmeli.)
8. **`research/` dosya boyutu:** 30dk'da 1 run, günde 48 bölüm — tek dosya mı, haftalık rotate mı?

\---

## 14\. Karar Gerekçeleri

|Karar|Gerekçe|Alternatif neden reddedildi|
|-|-|-|
|MD dosya haberleşmesi tutuldu|Çalışıyor, düşük maliyet, anlaşılır, debug edilebilir|DB veya message broker — overkill|
|Builder → Codex handoff (spec önce)|Spec olmadan Codex çalışırsa stale task risk artar|Direkt Codex'e research vermek — belirsizlik|
|Autonomous QA gate (insan yok)|FACTORY.md "ASLA onay bekleme" iron kuralı; ölçek için zorunlu|Human gate — sistem durur, deploy gap büyür|
|Full access (sandbox yok)|Kısıtlama = cycle durur = deploy gap büyür; guardrail = FACTORY.md kuralları|Sandbox — ek overhead, agent tıkanır|
|Researcher 30dk loop (derin-arastirma)|Sürekli araştırma = fırsat havuzu dolup taşmaz; günlük 1 araştırma yavaş|Günlük — yeterince hızlı değil|
|Codex dual-mode (execution > strategy)|Codex codebase'i bilen tek agent; feasibility inputu strateji kalitesini artırır|Sadece execution — stratejiye katkı 0|
|2-layer strateji (Claude + Codex)|Claude pazar/ROI; Codex fizibilite — farklı boyutlar, çakışma yok|Tek Strategist — fizibilite körü kalır|
|Builder-2 pasif default|ROI belirsiz; tek builder çoğu case'de yeterli|Her zaman aktif — gereksiz çakışma riski|
|Researcher ayrı role (GLM'de değil)|GLM 20dk loop'ta deep web araştırması için model gücü sınırlı|GLM'e araştırma ver — kalite düşük|
|Subagent task contract zorunlu|Belirsiz task → stale cycle → maliyet|Serbest çalışma — ölçümsüz|
|.signals/ mekanizması|universe\_loop.sh zaten kullanıyor; tutarlı, dosya tabanlı, zero-dep|Message queue — overkill|

\---

## 15\. Referans

* `sistem-planlama-sonnet4.6.plan.md` — Altyapı detayı: Topology Matrix, Run Ledger şeması, Verifier Layer, Memory mimarisi, Pattern Kütüphanesi
* `sistem-planlamacodex.md` — Capability Registry, Effect Log, sandbox policy, 4-lane queue, debate stability scorer
* `skills/codex\_skill.md` — Codex operasyonel kuralları
* `skills/glm\_analyst.md` — GLM operasyonel kuralları
* `scripts/codex\_loop.sh` — 35dk cron implementasyonu
* `scripts/glm\_loop.sh` — 20dk cron implementasyonu
* `STATE\_SUMMARY.json` — Portföy ground truth
* `\~/.claude/agents/team-coordination.md` — Team orchestration protokolü

