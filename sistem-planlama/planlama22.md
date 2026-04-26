# Planlama #22 — Multi-Agent Architecture Patterns Uygulama Haritası
**Tarih:** 2026-04-21 17:19 +03
**Bağlı Araştırma:** arastirma22.md

## Swarm Agent ile Nasıl Uygulanır?
Buradaki doğru hamle yeni bir framework'e topluca göçmek değil. Doğru hamle:

**Hybrid Orchestration Kernel**
- Dış yüz: mevcut shell/tmux/file-first çalışma tarzı korunur.
- İnce orchestration: task contract + topology selector + state/checkpoint + verifier + trace.
- Framework kullanımı seçici olur:
  - **OpenAI Agents SDK:** hafif handoff / tool-as-agent / code-first supervisor işleri
  - **LangGraph:** long-running, checkpoint, human-in-the-loop ve net graph gereken işler
  - **CrewAI:** demo / hızlı PoC / delegasyon temelli akışlar; çekirdeğin dini olmaz
  - **Microsoft Agent Framework:** A2A/MCP/.NET/enterprise interop gerektiğinde değerlendirilir
  - **AutoGen:** yeni iş için başlangıç tabanı olmaz; maintenance mode

Önerilen çalışma topolojisi:
1. **Task Topology Classifier**
   - Her işi şu sınıflardan birine atar: `single-agent`, `supervisor`, `hierarchical`, `parallel committee`, `deterministic workflow`.
   - Basit işlere swarm açılmaz.
2. **Task Contract Planner**
   - Her run için aynı sözleşmeyi üretir: amaç, girişler, teslim tanımı, izinli araçlar, timeout, verify step, human gate.
3. **State / Checkpoint Keeper**
   - Run ID, artifact path, ownership, status, checkpoint, retry sayısı, final karar burada tutulur.
   - Başlangıçta file/SQLite yeter; sonra gerekirse Postgres.
4. **Runtime Router**
   - Hangi işin OpenAI Agents SDK, hangisinin LangGraph, hangisinin düz shell/tmux ile koşacağını seçer.
5. **Isolated Worker Layer**
   - Coding işi varsa worktree/sandbox ownership zorunlu olur.
   - Read-only explorer ile write-owner worker ayrılır.
6. **Verifier / Observer**
   - Trace, eval, lint/test/health-check, rubric ve rollback kararı burada.
7. **Human Approval Gate**
   - Deploy, ödeme, destructive edit, müşteri-facing metin ve yüksek riskli release burada durur.
8. **Learning Loop**
   - Hangi topology ne işte çalıştı, nerede patladı, hangi model ucuz/iyi çıktı; bunlar kalıcı hafızaya işlenir.

## Gerekli Bileşenler
- **Script/Bot:**
  - topology selector
  - task contract generator
  - run ledger writer
  - worktree / sandbox launcher
  - trace collector
  - eval / verify runner
  - retry / rollback helper
  - weekly orchestration scoreboard
- **MCP/Araç:**
  - mevcut browser/web araştırma stack'i
  - `gh-axi` / GitHub API
  - MCPTube / ArXiv / Jina araştırma katmanı
  - FWStack benzeri deterministic gate'ler (kod işleri için)
  - gerekirse LangSmith veya OpenTelemetry observability
- **API:**
  - kısa vadede şart değil; file-first ilerler
  - seçili akışlarda OpenAI Agents SDK
  - durable graph gereken yerde LangGraph
  - enterprise/protocol interop gerekiyorsa Microsoft Agent Framework
- **İnsan Müdahalesi:**
  - topology override
  - release/deploy onayı
  - kritik diff ve müşteri-facing copy onayı
  - eval rubric ayarı
  - üretim incident triage

## Workflow Haritası
Tetikleyici
→ görev gelir
→ classifier topolojiyi seçer
→ planner task contract üretir
→ state keeper run açar
→ router uygun runtime'ı seçer
→ worker(lar) izole bağlamda çalışır
→ verifier trace + rubric + test ile kontrol eder
→ başarısızsa retry / daraltılmış reroute / rollback
→ başarılıysa artifact ana sisteme alınır
→ reporter metrikleri yazar
→ learning loop kalıcı ders çıkarır

Topoloji bazlı branch'ler:
- **Single-agent:** kısa, deterministik, 1 domain, az araç
- **Supervisor:** research/planning, çok domain ama tek sentez noktası gereken işler
- **Hierarchical:** uzun görev + alt ekipler + checkpoint
- **Parallel committee:** riskli karar / karşılaştırma / review
- **Deterministic workflow:** release, monitoring, ödeme, compliance, product health

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** mevcut UniverseCreator için **task contract + topology matrix + run ledger** standardı koymak.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - mevcut file-first memory ve log sistemi
  - tmux/shell çalışma tarzı
  - Git + worktree
  - gh-axi / browser araştırma araçları
  - araştırma-planlama rutini zaten contract üretmeye çok yakın
- **Proof-of-concept için minimum gereksinimler neler?**
  - 1 sayfalık topology matrix
  - 1 JSON/YAML/Markdown run contract şablonu
  - 1 run ledger dosyası
  - 1 verify rubric
  - 1 pilot akış: `research → plan → verify`
  - 1 pilot coding akışı: `plan → isolated worker → review`
- **Tahmini kurulum süresi ve ilk gelir beklentisi?**
  - iç çekirdek POC: **4-7 gün**
  - traced pilot + review loop: **3-5 gün**
  - doğrudan dış gelir: **hemen değil**, ama orchestration audit/setup olarak paketlenirse **2-6 hafta** içinde **$1.5k-$5k** tek seferlik kurulum geliri makul bir tahmindir.
- **Kısa vade net kararı:** önce kalite ve kontrol katmanı. Büyük framework migrasyonu şu aşamada vakit israfı.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda ideal görünüm:**
  - her önemli görev run contract ile açılıyor
  - topology otomatik veya yarı otomatik seçiliyor
  - araştırma/planning/coding akışlarında trace var
  - retry/rollback mantığı tanımlı
  - düşük riskli coding işleri worktree isolation ile çalışıyor
- **2-3 ay sonunda olgun görünüm:**
  - OpenAI Agents SDK veya benzeri hafif bir supervisor katmanı seçili işlerde devrede
  - LangGraph sadece durable/human-in-loop işler için pilotta
  - node-level eval ve maliyet raporu çıkıyor
  - failure taxonomy oluşmuş
  - weekly orchestration review ritmi yerleşmiş
- **Hangi metric'ler başarıyı gösterir?**
  - completion rate
  - verify pass rate
  - reroute / retry / rollback rate
  - average token per run
  - mean time to recovery
  - human intervention rate
  - node latency / queue time
  - failed handoff count
- **Hangi adımlar paralel çalışabilir?**
  - topology matrix tasarımı
  - run ledger + contract standardı
  - worktree isolation
  - observability / dashboard
  - eval rubricleri
  - model routing denemeleri
- **Ölçeklendirme için ne gerekiyor (insan, araç, bütçe)?**
  - 1 operatör gözü (weekly review)
  - 1 builder sahibi (kernel / tooling)
  - başlangıçta **$50-$300/ay** iç operasyon maliyeti
  - hosted tracing / dashboard / ek runner'larla **$300-$1,000/ay** bandına çıkabilir
- **Checkpoint'ler ve başarı kriterleri?**
  1. Hafta: topology matrix + contract şablonu
  2. Hafta: ilk traced pilot run'lar
  4. Hafta: retry/rollback + scoreboard
  8-12. Hafta: isolated coding lane + eval seti + provider routing

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator araştırma, planlama, coding, QA, health-check ve shipping öncesi gate'leri yöneten gerçek bir orchestration kernel'e dönüşür. Ajanlar roleplay yapmaz; ölçülen üretim birimleri olur.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - orchestration audit / setup service
  - managed coding swarm
  - agent observability + eval dashboard
  - template/topology marketplace
  - white-label agent ops kit
- **Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?**
  - multi-model ama tek contract standardı
  - research + planning + coding + QA + product ops'u tek disiplin altında koşturmak
  - her run'dan ders çıkaran file-first memory katmanı
  - işe göre topology seçmek; herkese aynı swarm şablonunu dayatmamak
- **White-label veya SaaS olarak satılabilir mi?**
  - **Evet**, ama ilk faz iç kalite altyapısı olmalı.
  - ikinci faz: danışmanlık / kurulum paketi
  - üçüncü faz: dashboard + run ledger + eval katmanı ürünleşmesi
  - dördüncü faz: “Agent Ops OS” veya “Swarm Control Plane” tarzı SaaS
- **Uzun vade evrim sırası:**
  1. iç kalite ve tracing
  2. tekrar edilebilir contract + topology seçimi
  3. worktree/sandbox + rollback + eval
  4. dış müşteriye paketlenebilir orchestration offering
  5. ürünleşmiş control-plane

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** 1-2 hafta ilk kontrol katmanı, 1-3 ay olgunlaştırma
- **Aylık İşletme Maliyeti:** iç kullanımda yaklaşık **$50-$300**, observability/hosted runner genişlerse **$300-$1,000**
- **Potansiyel Gelir:** dışarıya paketlenirse yaklaşık **$1.5k-$5k** setup + **$500-$2.5k/ay** managed service (**tahmin**)
- **ROI Beklentisi:** iç tarafta zaman/kalite kazancı **ilk 2-6 hafta** içinde hissedilir; dış satış düşünülürse ilk müşteriyle **1-2 ay** içinde break-even mümkün olabilir (**tahmin**)

## Mevcut Sistemle Entegrasyon
- `STATE_SUMMARY.json`'daki **113 aktif / 99 live ürün** seviyesi, orchestration disiplinini doğrudan operasyonel ihtiyaç yapıyor.
- Mevcut araştırma döngüsü (`ARASTIRMA_MODU`) zaten supervisor pattern'e uygun; bunun üstüne contract + trace eklemek düşük maliyetli.
- Vercel health triage, ürün kalite kontrolleri, içerik güncellemeleri ve bugfix işleri aynı kernel altında farklı topology ile koşabilir.
- Voice/runtime/browser gibi domain-specific işler framework içinde gömülmek zorunda değil; kernel sadece koordinasyon ve doğrulama katmanı olur.
- Kod yazma işi için worktree isolation, içerik/research işi için shared artifact/state, release işi için deterministic gate kullanılmalı.

## Riskler & Dikkat Edilecekler
- framework dini geliştirmek
- her işe multi-agent salmak
- trace/eval olmadan üretime güvenmek
- context şişmesi ve message-history çöpü
- worktree/sandbox ownership net olmadan paralellik açmak
- maliyet görünürlüğü olmadan uzun koşular başlatmak
- HITL kapıları koymadan kritik aksiyon otomatize etmek
- AutoGen maintenance modunu görmezden gelip eski dünyaya yatırım yapmak

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Topology matrix'i yaz:** hangi iş single-agent, hangisi supervisor, hangisi deterministic workflow olacak netleşsin.
2. **Run contract + ledger standardını sabitle:** her araştırma/coding run'ı aynı şema ile açılsın; trace ve verify zorunlu olsun.
3. **Tek pilot lane seç:** düşük riskli bir repo veya görevde worktree-isolated worker + reviewer + verify döngüsünü dene; sonra sonucu ölç.
