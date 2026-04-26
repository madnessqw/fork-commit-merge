# WORKFLOW.md — UniverseCreator Pipeline Kural Kitabı

> Her CLI (Claude, Codex, GLM) ve her subagent \*\*başlangıçta bu dosyayı okur\*\*.
> Politika koda gömülmez — buradan okunur.

\---

## 1\. Sistem Özeti

UniverseCreator, $500K hedefli otonom dijital fabrikadır. Üç döngü paralel çalışır:

* `universe\_loop.sh` (@reboot, 10dk) — Claude: Pure Orchestrator
* `codex\_loop.sh` (\*/35 cron) — Codex: Otonom Builder/Executor
* `glm\_loop.sh` (\*/20 cron) — GLM5.1: Analist/Monitor

**Human gate yok. QA gate autonomous karar verir. Onay bekleme.**

\---

## 2\. Pipeline Akış Şeması

```
GLM5.1 (Monitor)
  └─ sorun/öneri tespit → analysis/oneri.md
       └─ researcher\_needed? → .signals/researcher\_needed

Claude Orchestrator (10dk cycle)
  ├─ STATE.json oku → mevcut durumu anla
  ├─ sinyalleri tara (.signals/)
  ├─ STRATEGIST spawn → analysis/project\_decision.md
  ├─ PLANNER spawn → analysis/execution\_plan.md
  ├─ RESEARCHER spawn (30dk tetik) → research/YYYY-MM-DD.md
  ├─ BUILDER spawn → products/{slug}/spec.md
  └─ team\_status güncelle → analysis/team\_status.md

Codex (\*/35 cron)
  ├─ analysis/codex\_task.md oku → execute
  ├─ build tamamlandı → .signals/qa\_pending
  ├─ belirsizlik → SELF-PLAN modu
  └─ çözümsüz → STRATEGY modu → analysis/codex\_strategy\_input.md

QA-TESTER (qa\_pending sinyali)
  ├─ test et → analysis/qa\_result.md
  ├─ PASS → .signals/deploy\_ready → autonomous deploy
  └─ FAIL → analysis/sorun\_analizi.md → Codex'e geri döner
```

\---

## 3\. Agent Rolleri

|Agent|Sorumluluk|Çıktı|
|-|-|-|
|Claude (Orchestrator)|Koordinasyon, spawn kararı, döngü yönetimi|analysis/team\_status.md|
|STRATEGIST|Pazar/ROI analizi, proje kararı|analysis/project\_decision.md|
|PLANNER|Task breakdown, execution planı|analysis/execution\_plan.md|
|RESEARCHER|derin-arastirma skill, pazar/teknik araştırma|research/YYYY-MM-DD.md|
|BUILDER / BUILDER-2/3|Spec yazımı (paralel track mümkün)|products/{slug}/spec.md|
|CODEX|Kod execution, build, deploy hazırlık|analysis/codex\_result.md|
|QA-TESTER|Post-build test, deploy kararı|analysis/qa\_result.md|
|OPTIMIZER|SEO, kalite (haftalık)|analysis/optimizer\_report.md|
|ANALYST|Günlük raporlama|analysis/daily\_report.md|
|GLM5.1|Sağlık izleme, öneri|analysis/oneri.md|

\---

## 4\. Dosya Sahiplik Kuralları (Tek Writer Prensibi)

> Bir dosyanın \*\*tek yazarı\*\* vardır. Başka agent o dosyayı yalnızca okur.

|Dosya|Yazar|Okur|
|-|-|-|
|analysis/codex\_task.md|Claude / BUILDER|Codex|
|analysis/codex\_result.md|Codex|GLM, QA, Analyst|
|analysis/oneri.md|GLM5.1|Claude, Codex|
|analysis/sorun\_analizi.md|GLM, QA|Codex|
|analysis/qa\_result.md|QA-TESTER|Claude, Codex|
|analysis/project\_decision.md|STRATEGIST|PLANNER, BUILDER|
|analysis/execution\_plan.md|PLANNER|Codex, BUILDER|
|analysis/codex\_strategy\_input.md|Codex (strategy mode)|STRATEGIST|
|analysis/team\_status.md|Claude|Claude|
|research/YYYY-MM-DD.md|RESEARCHER|STRATEGIST, PLANNER|
|products/{slug}/spec.md|BUILDER|Codex, QA|
|STATE.json|Loop orchestrator|Tüm agentlar|

\---

## 5\. Sinyal Mekanizması (.signals/)

Sinyaller boş dosyalardır. Varlıkları tetikleyicidir; okunduktan sonra **silinir**.

|Sinyal|Yazar|Okur|Tetikler|
|-|-|-|-|
|.signals/qa\_pending|Codex|QA-TESTER|QA döngüsü başlar|
|.signals/deploy\_ready|QA-TESTER|Codex|Autonomous deploy|
|.signals/researcher\_done|RESEARCHER|Claude, STRATEGIST|Araştırma tüketti|
|.signals/codex\_strategy\_ready|Codex (strategy)|STRATEGIST|Strateji re-eval|
|.signals/researcher\_needed|GLM|Claude|RESEARCHER spawn|
|.signals/builder2\_needed|Codex|Claude|BUILDER-2 spawn|
|.signals/optimizer\_needed|Codex|Claude|OPTIMIZER spawn|

```bash
# Sinyal oluştur
touch .signals/qa\_pending

# Sinyal oku ve sil
\[ -f .signals/qa\_pending ] \&\& rm .signals/qa\_pending \&\& echo "triggered"
```

\---

## 6\. Context Anti-Bloat Kuralı

* Bir teammate conversation'ı **max 2 prompt** alır.
* 2 prompttan sonra sonuç gelmezse veya context şişerse → `teammate close` → yeni `teammate open`.
* Uzun araştırma görevleri için `derin-arastirma` skill kullan — native conversation değil.
* Her cycle sonunda STATE.json güncelle, eski context'i taşıma.

\---

## 7\. Codex Routing Modları

|Mod|Tetik|Davranış|
|-|-|-|
|**EXECUTE**|codex\_task.md + net spec|Direk build et|
|**SELF-PLAN**|Task var ama spec eksik|Kendi planını yaz → execute|
|**STRATEGY**|Blocker, mimari karar gerekli|codex\_strategy\_input.md yaz → .signals/codex\_strategy\_ready|
|**IDLE** |Task yok|Mevcut codebase'i optimize et / teknik borç öde|
|<br />**EVOLVE - SİSTEMİ GELİŞTİRME-READY SYSTEM ARCHITECTURE** |||

\---

## 8\. Escalation Kuralları

```
QA FAIL × 2  →  Codex STRATEGY modu
Codex STRATEGY  →  STRATEGIST re-eval
STRATEGIST değişiklik  →  PLANNER yeniden plan
GLM researcher\_needed  →  Claude RESEARCHER spawn (bir sonraki cycle)
Build > 3 cycle tamamlanmadı  →  ANALYST rapor + STRATEGIST gözden geçir
```

\---

## 9\. Anti-Patterns — Asla Yapma

|❌ Yapma|✅ Yap|
|-|-|
|Onay bekleme|Karar ver, başla|
|Kullanıcıya soru sor|STATE.json / dosyaları oku, çıkar|
|Menü veya seçenek listesi göster|Tek doğru aksiyonu al|
|Aynı dosyaya iki agent yaz|Tek writer prensibine uy|
|Context'i büyütmek için gereksiz okuma|Sadece ihtiyaç duyulan dosyayı oku|
|Sinyal dosyasını silmeden bırak|Oku → sil → işle|
|Spec olmadan build et|Spec yoksa SELF-PLAN yaz|
|Hard-code politika|Bu dosyayı güncelle|

\---

## 10\. Glossary

|Terim|Anlam|
|-|-|
|Cycle|universe\_loop.sh'ın bir 10dk turu|
|Sinyal|.signals/ altında boş tetikleyici dosya|
|Teammate|Claude'un başlattığı subagent (open/prompt/close)|
|Pure Orchestrator|Claude'un rolü: sadece koordine eder, kod yazmaz|
|SELF-PLAN|Codex'in task'ı kendi planladığı mod|
|STRATEGY mode|Codex'in çözümsüz kaldığında STRATEGIST'e eskalettiği mod|
|Gate|Otonom karar noktası — insan onayı gerektirmez|
|Anti-bloat|Context şişmesini önleme kuralları|
|spec.md|Bir ürün için Codex'in okuyacağı teknik şartname|



