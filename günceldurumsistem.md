# Güncel Durum Sistemi — 2026-04-22

**Tarih:** 22 Nisan 2026, ~05:15 UTC+3 (~02:15 UTC)  
**Kapsam:** Bu oturumda yapılan tüm değişiklikler, sistem durumu, açık sorunlar ve sonraki adımlar.

---

## 1. YAPILAN DEĞİŞİKLİKLER

### 1.1 SYSTEM_ARCHITECTURE.md — Büyük Genişleme (428 → 697 satır)

Codex EVOLVE modunun güvenli çalışabilmesi için master referans belge yeniden yazıldı.

**Eklenen bölümler:**
- **§0: Vizyon** — FİZİKSEL YAPAY ZEKA OLMAK + $500K hedef tier tablosu (mevcut: ~$118/ay)
- **§1.1: tmux haritası** — 3 session, tüm pencere isimleri
- **§1.2: Prompt dosyası haritası** — hangi dosya → hangi CLI → hangi mekanizma
- **§1.3: ⛔ EVOLVE KORUMA ZONU** — dokunulamaz dosyalar listesi (loop scriptleri, crontab, prompt dosyaları)
- **§2-4: Tam loop mekanikleri** — CYCLE_INTERVAL, lock, watchdog, temp script pattern
- **§9: Deploy pipeline** — Vercel → LemonSqueezy → checkout_url flow
- **§10: EVOLVE güvenlik sınırları** — DOKUNMA LİSTESİ
- **§13: Real-time monitoring komutları**

### 1.2 Skill Mimarisi v2 — Tüm Dosyalar Oluşturuldu/Güncellendi

| Dosya | Durum | Anahtar Ekleme |
|---|---|---|
| `skills/SKILL_MAP.md` | **YENİ** ✅ | Master routing — hangi agent hangi skill, ne zaman |
| `WORKFLOW.md` | **YENİ** ✅ | Pipeline kural kitabı, sinyal sahiplikleri, tetik koşulları |
| `CODEBASE_MAP.md` | **YENİ** ✅ | Klasör + anahtar dosya haritası (repo scan yerine bu okunur) |
| `skills/agents/qa_tester.md` | **YENİ** ✅ | QA agent — codex_result.md → qa_result.md → deploy sinyal |
| `skills/task_contract_template.md` | **YENİ** ✅ | Standart task contract şablonu |
| `skills/agents/strategist.md` | **YENİ** ✅ | Benefit-first analiz, sistem-planlama arşiv entegrasyonu |
| `skills/agents/planner.md` | **GÜNCELLENDİ** ✅ | Mimari çıkarma, adım-adım işlem haritası formatı |
| `skills/agents/researcher.md` | **GÜNCELLENDİ** ✅ | 30dk cadence, derin-arastirma entegrasyonu, projeler.txt ilham |
| `skills/agents/builder.md` | **GÜNCELLENDİ** ✅ | execution_plan.md okuma, build_checklist.md entegrasyonu |
| `skills/codex_skill.md` | **GÜNCELLENDİ** ✅ | EVOLVE modu, run_ledger, qa_pending, auto-deploy |
| `skills/glm_analyst.md` | **GÜNCELLENDİ** ✅ | qa_result staleness kontrolü, researcher_needed sinyal |
| `~/.codex/skills/universe-creator/SKILL.md` | **YENİ** ✅ | Codex'in doğru skill konumu, 5 mod |

### 1.3 Run Ledger Aktif

`logs/run_ledger.jsonl` — Codex artık her cycle'da kayıt yazıyor.

**Mevcut kayıtlar:**
```
ledger-init-20260422         INIT      cycle 1073
codex-20260422-0140  EXECUTION health/canonical drift fix   18 min  $0.08  cycle 1073
codex-20260422-0506  EXECUTION slug canonical drift hard.   24 min  $0.09  cycle 1075
```

### 1.4 Codex Cycle 1075 — Canonical Drift Hardening

- `scripts/update_summary.py` + `scripts/health_check.py` güçlendirildi
- Live ürünlerde canonical URL, preview alias'ın arkasına saklanmıyor
- canonical drift sayısı düzeltildi: 0 → **8** (gerçek drift bulundu)
- 21 test passed
- Commit: `9553fab`

---

## 2. MEVCUT SİSTEM DURUMU

### 2.1 Agent Durumu

| Agent | Durum | Son Aktivite |
|---|---|---|
| **Claude** | ✅ AKTİF | Cycle 616 — pdf-forge 500 fix çalışıyor (~6 dakika) |
| **Codex** | ✅ TAMAMLANDI | Cycle 1075 bitti, canonical drift hardening |
| **GLM** | ⚠️ SORUNLU | Her cycle "Killed" alıyor (bkz. §4.2) |

### 2.2 Ürün Metrikleri

```
Toplam aktif:   142
Live:            78
Sağlıklı:        76 (%97.4)
Sağlıksız:        2 (pdf-forge, diffmaster)
Checkout gap:     0 ✅
Deploy gap:      20 (URL eksik/bozuk)
Canonical drift:  8 (yeni tespit, cycle 1075)
Spec-ready:      27 (inşa bekliyor)
```

### 2.3 Aktif Sinyal Dosyaları

| Sinyal | İçerik | Yaş |
|---|---|---|
| `.signals/qa_pending` | `{"slug": "health-canonical-drift", "ts": "...02:07Z"}` | ~8 dk |
| `.signals/health.json` | loop health bilgisi | güncel |
| `.signals/status` | loop status | güncel |

### 2.4 Son 5 Commit

```
9553fab  codex: 20260422-0506 — slug canonical drift hardening
9ef1342  session: Cycle 1074 checkpoint - 18 specs added, diffmaster fix
4acde8e  spec: Add 18 new product specs (Cycle 1074)
dc80432  codex: 20260422-0439 — prefer ideal health probe
bbd34cf  docs: update FACTORY.md with latest workflow rules
```

---

## 3. CLAUDE AKTIF GÖREVI (Cycle 616)

Claude şu anda sırayla üç görev çalıştırıyor:

1. **✔ css-gradient-studio deploy** — Vercel deploy başarılı
2. **▶ pdf-forge 500 fix** — `./scripts/fix_vercel_protection.sh pdf-forge` çalışıyor (~6dk)
3. **☐ diffmaster 401 fix** — sırada bekliyor

> **Not:** Bu iki ürün Vercel-tarafı koruma/hata gerektiriyor. Kod değişikliğiyle tam çözüm garanti değil; Vercel dashboard'da manuel adım gerekebilir.

---

## 4. AÇIK SORUNLAR

### 4.1 QA-TESTER Otomatik Tetik Mekanizması Yok

**Durum:** `qa_pending` sinyali yazılıyor (Codex her build sonrası), ama QA-TESTER otomatik tetiklenmiyor.

**Etki:** deploy_ready sinyali üretilmiyor → otomatik deploy gate devre dışı.

**Geçici durum:** Claude FACTORY.md'de QA adımlarını kendisi yapıyor.

**Çözüm yolu:** `scripts/researcher_loop.sh` benzeri bir `qa_trigger.sh` + cron — ya da Claude'un PROMPT.txt'sinde qa_pending varsa QA-TESTER spawn etme talimatı.

### 4.2 GLM Loop — Her Cycle Killed

**Durum:** `opencode run` başlatılıyor, "INFO refreshing" yazdırıyor, 20 dakika sonra bir sonraki cycle SIGKILL ile öldürüyor.

**Etki:** GLM hiçbir zaman görevini tamamlamıyor. Ancak Codex `analysis/oneri.md` ve `analysis/sorun_analizi.md` dosyalarını kendi cycle'ında yazıyor → sistem fonksiyonel.

**Kök neden:** `opencode run` 20 dakikadan fazla sürüyor. Her yeni cron tetiklemesi önceki çalışmayı kill ediyor.

**Çözüm yolu (önerim):** `glm_loop.sh`'da timeout'u 35 dakikaya çıkar VEYA `opencode run` prompt'unu daha kısa bir görevle sınırla. (Loop scriptine dokunmadan: `prompts/glm_prompt.txt`'i kısalt.)

### 4.3 State Cycle Drift

**Durum:**
- `STATE.json` cycle: 759
- Loop log cycle: 616  
- `logs/run_ledger.jsonl` cycle: 1073/1075

Üç farklı cycle sayacı var. Bu da raporlamayı karmaşıklaştırıyor.

**Etki:** Analiz yaparken hangi cycle'a bakıldığı belirsizleşiyor.

**Çözüm yolu:** `STATE.json` cycle'ını `universe_loop.sh`'daki CYCLE sayacıyla senkronize et veya her system'in kendi cycle'ını kullansın ama raporlarda ikisi de yazılsın.

### 4.4 canonical_drift: 8 (Yeni Tespit)

Cycle 1075 öncesi `canonical_url_drift = 0` raporlanıyordu. Codex'in hardening değişikliği gerçek drift'i ortaya çıkardı: **8 ürün canonical URL sorunu yaşıyor**.

Bu ürünler bir sonraki Codex cycle'ında düzeltme için sıraya girecek.

### 4.5 deploy_gap: 20

20 ürünün Vercel URL'si eksik veya bozuk. Spec-ready backlog (27 ürün) varken bunlar önceliklendirilmeli.

---

## 5. YENİ MİMARİ KAZANIMLARI

Bu oturumda eklenen kalıcı yapılar:

### Sinyal Haberleşme Protokolü (`.signals/`)

Sistem artık dosya-tabanlı sinyal mekanizmasıyla çalışıyor:

```
Codex build tamamlar → qa_pending yazar
QA-TESTER (henüz manuel) → qa_result yazar (PASS/FAIL)
QA PASS → deploy_ready → Codex deploy_product.sh
GLM analiz → researcher_needed sinyali
Researcher tamamlar → researcher_done sinyali
```

### Run Ledger

`logs/run_ledger.jsonl` — pattern analizi için temel. Her Codex cycle kaydediliyor.

### EVOLVE Modu (Codex)

Codex artık `~/.codex/skills/universe-creator/SKILL.md`'deki EVOLVE modunda:
1. `projeler.txt` ve `sistem-planlama/` arşivini okur
2. Kendi tespit ettiği sorunu planlar
3. Execute eder + review eder
4. `analysis/codex_selfevolve_report.md`'ye kaydeder

Tetik: Codex cycle başında `codex_task.md` yoksa → STRATEGY → EVOLVE değerlendirmesi yapar.

---

## 6. SONRAKİ ADIMLAR (Önerilen)

### Acil (Bu Hafta)

1. **qa_pending otomatik tetik** — PROMPT.txt'e ekle: "qa_pending varsa QA-TESTER spawn et"
2. **GLM prompt kısalt** — `prompts/glm_prompt.txt` daha kısa görev ver ki 20dk'dan önce bitsin
3. **canonical_drift 8** — Codex bir sonraki cycle'da çözecek, izle
4. **deploy_gap 20** — spec-ready 27'den seçim yaparak deploy et

### Orta Vadeli

5. **researcher_loop.sh** cron + aktif tetik
6. **QA-TESTER gerçek deploy gate** — deploy_ready sinyali üretene kadar deploy yok
7. **State cycle senkronizasyonu** — tek cycle sayacı veya çapraz referans

### Uzun Vadeli

8. **Strategist otomatik spawn** — `researcher_done` sinyalinde Claude otomatik tetiklesin
9. **Run ledger analizi** — pattern analizi için weekly review
10. **GLM alternatifi** değerlendirme — model değiştirme veya opencode yerine direct API

---

## 7. BİLİNEN HATALAR / SESLİ NOTLAR

- **pdf-forge** ve **diffmaster** — Vercel-tarafı sorundur. Kod değişikliği tam çözüm getirmeyebilir.
- **PROMPT.txt dokunulmasın** — Claude loop için kritik, her değişiklik dikkatli yapılmalı
- **Loop scriptlerine dokunulmasın** — `universe_loop.sh`, `codex_loop.sh`, `glm_loop.sh` — çalışıyor
- **run_ledger format sabit kalmalı** — Codex her cycle append ediyor, şema değişmemeli
- `~/.claude/skills/codex/` klasörü yanlış yerdi → zaten silinmedi ama Codex bu yola erişemiyor, gerçek yer `~/.codex/skills/universe-creator/`

---

## 8. REFERANS DOSYALAR

Bu oturumda değiştirilen / oluşturulan tüm dosyalar:

```
/home/gokhan/UniverseCreator/
├── SYSTEM_ARCHITECTURE.md          ← master referans (697 satır)
├── WORKFLOW.md                     ← pipeline kural kitabı
├── CODEBASE_MAP.md                 ← repo haritası
├── logs/run_ledger.jsonl           ← aktif run ledger
├── skills/
│   ├── SKILL_MAP.md               ← skill routing master
│   ├── codex_skill.md             ← EVOLVE + run_ledger eklendi
│   ├── glm_analyst.md             ← staleness + researcher sinyal
│   ├── task_contract_template.md  ← standart task şablonu
│   └── agents/
│       ├── strategist.md          ← YENİ — benefit-first, arşiv enteg.
│       ├── planner.md             ← sistem mimarisi + işlem haritası
│       ├── researcher.md          ← 30dk, derin-arastirma, projeler.txt
│       ├── builder.md             ← execution_plan entegrasyonu
│       └── qa_tester.md          ← YENİ — build gate agent
└── ~/.codex/skills/universe-creator/SKILL.md   ← Codex EVOLVE skill
```

---

*Bu belge 2026-04-22 oturumunda oluşturulmuştur. Sistem izleme yaklaşık 2 saat sürdü (05:06–07:15 UTC+3 aralığı, compaction nedeniyle kısmi). Bir sonraki oturumda bu belgeyi okumak yeterli olacak.*
