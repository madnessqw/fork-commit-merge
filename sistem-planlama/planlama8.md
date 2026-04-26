# Planlama #8 — Multi-Agent Architecture Patterns Uygulama Haritası
**Tarih:** 2026-04-21 07:21 +03
**Bağlı Araştırma:** arastirma8.md

## Swarm Agent ile Nasıl Uygulanır?
En kritik karar şu: **UniverseCreator yeni bir framework'e kör atlamamalı.** İlk hedef LangGraph/CrewAI/MAF fanboyluğu değil; mevcut tmux + dosya + shell swarm'ının üstüne **ince ama sert bir orchestration omurgası** koymak.

Önerilen hedef mimari:
1. **Intake / Task Classifier**
   - Her işi `single-agent`, `supervisor`, `hierarchical`, `parallel committee`, `deterministic workflow` diye sınıflar.
   - Basit işlere multi-agent açılmaz. Gereksiz ajan açmak token yakma makinesi.
2. **Planner / Task Contract Agent**
   - Her run için tek tip contract üretir: amaç, girişler, done kriteri, izinli araçlar, timeout, verify command.
3. **State Keeper**
   - Run ledger, checkpoint, artifact path, ownership, status ve rollback noktalarını tutar.
   - File-first başlayabilir; sonra SQLite/Postgres'e geçebilir.
4. **Worker Launcher**
   - Ajanları izole worktree / sandbox / tmux context'inde çalıştırır.
   - Coding işi varsa write-set ownership zorunlu olur.
5. **Router / Handoff Layer**
   - Shared state mi geçilecek, tool parametresi mi, explicit handoff mu — bunu kontrol eder.
   - Supervisor kafasına göre değil, protokole göre route eder.
6. **Verifier / Eval Agent**
   - Test, lint, health check, content rubric, diff review, regression gate.
   - “Çalışıyor gibi” ile “gerçekten çalışıyor” arasındaki fark burada.
7. **Memory / Learning Agent**
   - Hata pattern'lerini, başarılı çözüm yollarını ve run sonrası lesson'ları kalıcılaştırır.
   - ACE/learning-loop pattern'i buraya oturur.
8. **Reporter / Dashboard Agent**
   - Completion rate, rollback rate, human override rate, token/run, MTTR, healthy_count etkisi gibi metrikleri çıkarır.

## Gerekli Bileşenler
- **Script/Bot:**
  - task classifier / topology selector
  - run ledger writer
  - checkpoint / rollback helper
  - worktree launcher
  - verify/eval runner
  - postmortem + learning writer
  - orchestration dashboard/exporter
- **MCP/Araç:**
  - GitHub / gh-axi veya GitHub API
  - browser/web research stack
  - MCPTube / ArXiv / Jina araştırma katmanı
  - mevcut Codex/Claude/CLI worker'ları
- **API:**
  - zorunlu değil; başlangıçta file + git + tmux ile yürür
  - ihtiyaç halinde LangSmith / OpenTelemetry / Langfuse benzeri tracing
  - gerekirse OpenAI Agents SDK / LangGraph / Microsoft Agent Framework belirli iş tiplerinde katman olarak eklenebilir
- **İnsan Müdahalesi:**
  - task priority seçimi
  - destructive action onayı
  - merge/release gate
  - yüksek riskli deploy ve ödeme akışları
  - quality bar ayarı

## Workflow Haritası
Tetikleyici
→ görev gelir
→ classifier işin tipini belirler
→ planner tek tip task contract üretir
→ state keeper run ID + artifact path + ownership açar
→ router doğru topology'yi seçer
→ worker'lar izole bağlamda çalışır
→ verifier çıktıyı test/rubric ile doğrular
→ başarısızsa rollback / retry / narrower reroute
→ başarılıysa sonuç ana sisteme aktarılır
→ reporter metrikleri yazar
→ memory agent dersi kalıcılaştırır

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** Mevcut UniverseCreator swarm'ı için **task contract + topology matrix + run ledger** standardı koymak. Yeni framework kurmadan bile kaliteyi zıplatır.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - tmux / file-based memory / git zaten var
  - mevcut research-planning akışı task contract'a dönüşebilir
  - worktree isolation pattern'i Git ve modern orchestrator repo'larından bire bir alınabilir
- **Proof-of-concept için minimum gereksinimler neler?**
  - 1 sayfalık topology matrix
  - 1 standart run dosyası şeması
  - 1 verification rubric
  - 1 pilot workflow: `research → plan → verify`
  - 1 basit scoreboard: completed / failed / retried / rolled back
- **Tahmini kurulum süresi ve ilk gelir beklentisi?**
  - Kurulum: **4-7 gün**
  - İlk hafta doğrudan gelir beklentisi: **düşük / dolaylı**
  - Gerçek kısa vade kazancı: daha az kırık run, daha hızlı teslim, daha az insan babysitting'i
  - Eğer dışarıya “orchestration audit / setup” diye paketlenirse ilk **$500-$1,500** setup geliri 2-6 hafta bandında mümkün olabilir; bu tahmindir.
- **Kısa vade tezi:** önce sistemi disipline et, sonra parallelism'i artır. Tersi aptallık.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay görünümü:**
  - görevler artık net topology ile koşuyor
  - her run için artifact ve verify izi var
  - retry/rollback mekanizması tanımlı
  - research, planning ve QA hatları izlenebilir halde
- **3. ay görünümü:**
  - coding işler için worktree-isolated worker'lar
  - gözlemlenebilirlik dashboard'u
  - failure taxonomy
  - learned playbook / stable protocol seti
  - seçili iş tiplerinde framework katmanı (örn. LangGraph veya Agents SDK) pilotta
- **Hangi metric'ler başarıyı gösterir?**
  - task completion rate
  - retry rate
  - rollback rate
  - human intervention rate
  - average token / run
  - mean time to recovery
  - verify pass rate
  - healthy_count / live_count etkisi
- **Hangi adımlar paralel çalışabilir?**
  - task taxonomy ve protocol tasarımı
  - worktree isolation
  - eval/rubric sistemi
  - logging/dashboard
  - memory/learning döngüsü
- **Ölçeklendirme için ne gerekiyor (insan, araç, bütçe)?**
  - sağlam tracing
  - daha disiplinli task intake
  - daha net ownership kuralları
  - belki hafif DB ve dashboard
  - gerekirse hosted runner / remote sandbox
- **Checkpoint'ler ve başarı kriterleri?**
  1. Hafta: topology matrix + task contract
  2. Hafta: pilot workflow + verify gate
  4. Hafta: rollback / retry / logs
  8-12. Hafta: coding worker isolation + eval dashboard + memory loop

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator, araştırma-planlama-inşa-QA-yayın öncesi doğrulama hattını yöneten gerçek bir orchestration kernel'e dönüşür. Ajanlar roleplay yapmaz; ölçülen üretim birimleri olur.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - orchestration audit / consulting
  - white-label coding swarm setup
  - agent run dashboard ürünü
  - rollback/eval/memory katmanı SaaS'ı
  - vertical workflows için “managed agent ops” hizmeti
- **Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?**
  - araştırma + plan + kod + QA + release gate'i tek protokol altında işletmek
  - multi-model dağıtım (Claude/Codex/başkaları) ama tek run sözleşmesiyle
  - her çalışmadan ders çıkartan file-first memory sistemi
  - iş tipine göre topology seçimi; herkese aynı swarm kalıbını dayatmamak
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. İlk faz: iç altyapı.
  - İkinci faz: danışmanlık / setup package.
  - Üçüncü faz: dashboard + orchestration kernel ürünü.
  - Dördüncü faz: template marketplace veya managed multi-agent ops.
- **Doğal evrim sırası:**
  1. iç kalite altyapısı
  2. repeatable run protocol
  3. dashboard + eval + rollback katmanı
  4. dış müşteriye paketlenebilir orchestration offering
  5. ürünleşmiş swarm OS

## Öncelik & Çaba Tahmini
- **Öncelik:** Çok yüksek
- **Kurulum Süresi:** ilk sağlam omurga için **1-2 hafta**, olgunlaşma için **1-3 ay**
- **Aylık İşletme Maliyeti:**
  - file/tmux/git ağırlıklı başlangıç: **$0-$50**
  - tracing / hosted eval / ekstra runner ile: **$50-$300+**
- **Potansiyel Gelir:**
  - iç leverage: daha fazla sağlıklı ürün, daha hızlı teslim
  - dış paketleme: **$1,000-$5,000/ay** managed orchestration veya **$500-$2,000** tek sefer setup; tahmindir
- **ROI Beklentisi:**
  - iç kullanımda **1-2 ay** içinde zaman/hata tasarrufu ile geri dönebilir
  - dış paketlemede **ilk 1-2 müşteri** break-even için yeterli olabilir

## Mevcut Sistemle Entegrasyon
- `universe_loop.sh`, tmux düzeni ve file-based memory zaten hazır. Yani sıfırdan platform kurmak yerine bu sisteme orchestration omurgası takılmalı.
- `STATE_SUMMARY.json` 2026-04-21 snapshot'ında **113 aktif / 86 live / 23 healthy**. Bu sayı şunu söylüyor: önce sağlık ve doğrulama zinciri, sonra daha fazla paralel iş.
- Mevcut ürün fabrikasına entegrasyon şöyle olur:
  - research işleri: multi-agent uygun
  - planning işleri: supervisor + verifier uygun
  - deploy / production mutation: daha dar yetkili, deterministic workflow uygun
  - content / SEO / docs: parallel committee veya worker swarm uygun
- Yani tek topology yok. İşe göre topology seçmeyen sistem sonunda kendi kendini sabote eder.

## Riskler & Dikkat Edilecekler
- **Framework thrash:** her hafta yeni framework denemek. Net zarar.
- **Aşırı paralellik:** sorunlu hattı daha hızlı sorunlu hale getirmek.
- **Gizli state:** nerede ne tutulduğu belli olmayan sistemler debugging'i öldürür.
- **Evaluation theater:** dashboard var diye kalite var sanmak.
- **Context poisoning:** çok fazla shared context ile tüm worker'ları aynı hataya sürüklemek.
- **Merge/worktree karmaşası:** ownership net değilse multi-agent kodlama diffleri birbirini yer.
- **Vendor lock-in:** orchestration mantığını tek framework API'sine gömmek.
- **Gizlilik/sır riski:** broad log/debug dump'ları secret sızdırabilir; orchestration katmanı redaction disiplinini de içermeli.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Topology matrix yaz:** hangi iş `single-agent`, hangisi `supervisor`, hangisi `hierarchical`, hangisi `deterministic workflow` olacak netleştir.
2. **Task contract + run ledger standardını çıkar:** her görev aynı şemayla başlasın, aynı verify mantığıyla bitsin.
3. **Tek pilot workflow seç:** research → plan → verify hattında worktree/isolation/logging disiplinini dene; sonuçlar iyi gelirse coding hattına genişlet.
