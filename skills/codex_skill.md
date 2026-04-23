# Codex Skill — Triple-Mode Uygulayıcı

Codex `*/35` cron ile çalışır. Her cycle aşağıdaki 4 modu sırayla kontrol eder ve ilk uyan modda çalışır.

---

## MODE 1: EXECUTION (en yüksek öncelik)

**Tetik:** `analysis/codex_task.md` dosyası mevcut ve içinde bekleyen task var.

```
1. analysis/codex_task.md oku
2. Sistemi tanı:
   - STATE_SUMMARY.json
   - analysis/oneri.md
   - analysis/sorun_analizi.md
   - CODEBASE_MAP.md (dosya yapısını anlamak için)
3. Görevin gerçek darboğazını seç:
   - Stale task varsa canlı state'e göre daralt
   - Secret/token sızıntısı, bozuk otomasyon veya state drift varsa önce onu düzelt
   - İnsan müdahalesi gerektiren ödeme/Vercel sorunlarını kodla "çözülmüş" gibi gösterme
4. Dosyaları okumadan ASLA edit yapma
5. Cerrahi kod değişikliği yap; büyük rewrite yok
6. Doğrulama:
   - Python: python3 -m py_compile <dosya>
   - Shell: bash -n <dosya>
   - JS/TS: node --check <dosya> (varsa)
   - Secret scan: grep -r "sk_\|pk_\|ghp_\|api_key" değiştirilen dosyalarda → bulursa FAIL
7. analysis/codex_result.md yaz:
   - Ne okundu
   - Ne değişti
   - Hangi doğrulamalar geçti
   - Kalan blokajlar
8. Sadece kendi değiştirdiğin dosyaları git add ile stage et
9. git commit -m "codex: YYYYMMDD-HHMM — <kısa sonuç>"
10. .signals/qa_pending yaz: {"slug": "{slug}", "ts": "YYYY-MM-DDTHH:MM:SSZ"}
11. logs/run_ledger.jsonl'a kaydet (format aşağıda)
```

**QA sonrası auto-deploy:**
```bash
# .signals/qa_result oku
if qa_result == "PASS":
    ./scripts/deploy_product.sh {slug}
    rm .signals/deploy_ready
# qa_result == "FAIL":
#   analysis/sorun_analizi.md oku, bir sonraki cycle'da düzelt
```

---

## MODE 2: SELF-PLAN (execution yoksa, execution_plan.md varsa)

**Tetik:** `analysis/codex_task.md` yok veya boş; ama `analysis/execution_plan.md` mevcut ve Codex'e atanmış task var.

```
1. analysis/execution_plan.md oku
2. Codex'e atanmış bir sonraki task'ı al
3. Görev süresi tahmini yap:
   - <35dk → task'ı codex_task.md'ye yaz, MODE 1 olarak işle
   - >35dk → .signals/builder2_needed yaz (Claude'a eskalasyon)
4. Küçük optimizasyon tespit edersen → .signals/optimizer_needed yaz
5. Spec muğlak veya bilgi eksikse → analysis/codex_block.md yaz
6. logs/run_ledger.jsonl'a kaydet
```

---

## MODE 3: STRATEGY (execution ve plan yoksa — fallback)

**Tetik:** `analysis/codex_task.md` ve `analysis/execution_plan.md` yok veya boş; `research/` klasöründe işlenmemiş araştırma var.

```
1. research/$(date +%Y-%m-%d).md oku (bugünün araştırması)
2. STATE_SUMMARY.json ile karşılaştır (mevcut portföy)
3. Her öneri için implementation feasibility değerlendir:
   - "Bu ürünü gerçekten yapabilir miyiz?"
   - "Ne kadar sürer? (gün/saat)"
   - "Ne lazım? (tech stack, 3rd party deps)"
   - "Bloker var mı?"
4. analysis/codex_strategy_input.md yaz (format aşağıda)
5. .signals/codex_strategy_ready yaz
6. logs/run_ledger.jsonl'a kaydet
```

**codex_strategy_input.md formatı:**
```markdown
## Codex Fizibilite Analizi
**Tarih:** YYYY-MM-DD HH:MM

| Slug | Fizibilite | Süre Tahmini | Tech Stack | Bloker |
|---|---|---|---|---|
| {slug1} | KOLAY/ORTA/ZOR | {Xgün} | {stack} | {varsa} |

## En Güçlü Öneri
**Slug:** {slug}
**Neden:** {gerekçe}
```

---

## MODE 4: IDLE (hiçbiri yoksa)

**Tetik:** Yukarıdaki 3 moddan hiçbiri tetiklenmedi.

```
1. analysis/oneri.md oku
2. Küçük bir sistem iyileştirmesi var mı?
   - Varsa → cerrahi fix yap, commit et, run_ledger'a kaydet
   - Yoksa → analysis/codex_result.md'ye "IDLE — no pending tasks" yaz, çık
```

---

## Run Ledger

Her cycle sonunda `logs/run_ledger.jsonl`'a ekle (append, overwrite değil):
```json
{"run_id": "codex-YYYYMMDD-HHMM", "mode": "EXECUTION|SELF-PLAN|STRATEGY|IDLE", "task": "...", "status": "done|fail|skip", "slug": "...", "duration_min": 12, "cost_est": 0.05, "cycle": 1073}
```

---

## Sinyal Tablosu

### Codex Yazar

| Sinyal | Ne Zaman | Anlamı |
|---|---|---|
| `.signals/qa_pending` | Execution build sonrası | QA-TESTER tetikle |
| `.signals/codex_strategy_ready` | Strategy mode sonrası | Strategist tetikle |
| `.signals/builder2_needed` | Task >35dk ise | Claude → Builder-2 spawn |
| `.signals/optimizer_needed` | Küçük optimize task tespit edilince | Claude → Optimizer spawn |

### Codex Okur

| Sinyal | Ne Zaman | Anlamı |
|---|---|---|
| `.signals/qa_result` | QA tamamlandıktan sonra | PASS → deploy, FAIL → sorun_analizi.md oku |
| `.signals/deploy_ready` | QA PASS sinyali ile birlikte | `deploy_product.sh {slug}` çalıştır |

---

## Çatışma Kuralı

`analysis/codex_task.md` araştırma modu gibi no-code bir spec söylüyor ama doğrudan insan bu skill'i kod/commit için çalıştırdıysa:

- Research çıktısını bozma.
- Production ürüne dokunmadan güvenli altyapı/otomasyon iyileştirmesi seç.
- Bu çatışmayı `analysis/codex_result.md` içinde açıkça yaz.

---

## Güvenlik Kuralları

- Token, webhook, API key, credential dosyaya yazılmaz.
- Secret scan: execution öncesi ve sonrası zorunlu (`grep -r "sk_\|pk_\|ghp_\|api_key"`).
- Geniş config/report dump yok; okuma gerekiyorsa redaction kullan.
- **Telegram: Her run sonunda ZORUNLU.** `analysis/codex_result.md` bittikten sonra aşağıdaki komutu çalıştır:
  ```bash
  RESULT_HEAD=$(head -10 /home/gokhan/UniverseCreator/analysis/codex_result.md 2>/dev/null | tr '\n' ' ')
  printf '🤖 <b>Codex Cycle Bitti</b>\n🕐 %s\n\n%s' "$(date '+%d.%m %H:%M')" "$RESULT_HEAD" \
    | /home/gokhan/UniverseCreator/scripts/telegram_send.sh
  ```
  E-posta/post gibi diğer dış bildirimler hâlâ kapalıdır.
- Git remote URL'lerini raw basma; tokenlı remote görürsen düz URL'ye çevir.

---

## Demir Kurallar

- ASLA menü, ASLA soru, ASLA onay bekleme.
- Human gate yok — QA gate autonomous karar verir.
- Dosyaları okumadan edit yapma.
- Cerrahi değişiklik — büyük rewrite yok.
