# GLM MICRO-CODER + ANALYST SKILL — UniverseCreator

**Bu dosyayı okuyan GLM:** Önce aktif kod işi yapıyorsun (Z.AI coding plan zorunluluğu), sonra healthcheck + analiz yapıyorsun. Hedef süre: <18 dakika.

> ⚠️ Z.AI Coding Plan Politikası: Coding olmayan kullanım → throttling. 3+ ihlal → kalıcı ban. Her cycle mutlaka commit yapılmalı.

---

## ⚡ Adım 0b — Hızlı Telegram Ping (İLK YAP — 2dk içinde)

Sisteme başladığını haber ver. Önce STATE_SUMMARY'yi oku, hemen gönder:

```bash
LIVE=$(python3 -c "import json; s=json.load(open('/home/gokhan/UniverseCreator/STATE_SUMMARY.json')); print(f'{s[\"healthy_count\"]}/{s[\"live_count\"]}')" 2>/dev/null || echo "?/?")
DGAP=$(python3 -c "import json; print(json.load(open('/home/gokhan/UniverseCreator/STATE_SUMMARY.json')).get('deploy_missing_or_bad_url',0))" 2>/dev/null || echo "?")
CYCLE=$(python3 -c "import json; print(json.load(open('/home/gokhan/UniverseCreator/STATE_SUMMARY.json')).get('cycle',0))" 2>/dev/null || echo "?")
ONERI_AGE=$(python3 -c "import os,time; f='/home/gokhan/UniverseCreator/analysis/oneri.md'; print(f'{(time.time()-os.stat(f).st_mtime)/60:.0f}dk önce' if os.path.exists(f) else 'yok')" 2>/dev/null)

printf '📊 <b>GLM CYCLE — %s</b>\n🕐 %s\n\n📦 Sağlık: %s | Deploy gap: %s\n🔄 Son oneri.md: %s\n\n⏳ Analiz devam ediyor...' \
    "$CYCLE" "$(date '+%d.%m %H:%M')" "$LIVE" "$DGAP" "$ONERI_AGE" \
    | /home/gokhan/UniverseCreator/scripts/telegram_send.sh
```

---

## 🔨 Adım 1 — AKTİF KOD GÖREVİ (ZORUNLU — Z.AI Coding Plan Policy)

> Bu adımı atlamak YASAKTİR. Her cycle'da mutlaka kod değişikliği + commit yapılmalı.

**Hedef süre: <8 dakika**

### 1a — glm_fix_brief.md Kontrolü

```bash
cat /home/gokhan/UniverseCreator/analysis/glm_fix_brief.md 2>/dev/null | head -80
```

`glm_fix_brief.md` varsa ve **küçük + güvenli** (< 60 satır diff, test edilebilir) bir görev içeriyorsa:

1. Görevi **doğrudan uygula** (kodu yaz, dosyaları düzenle)
2. Test çalıştır:
   ```bash
   cd /home/gokhan/UniverseCreator && python3 -m pytest tests/ -x -q 2>/dev/null || echo "test yok"
   ```
3. Commit yap:
   ```bash
   cd /home/gokhan/UniverseCreator
   git add -A
   git commit -m "fix(glm): [görev adı] — glm_fix_brief uygulandı"
   ```

**Büyük refactor / production deploy gerektiren işleri atla** → glm_fix_brief'te "Codex'e bırakıldı" not et.

---

### 1b — Quick Win (Brief boşsa veya Codex-scope ise)

Şu öncelik sırasına göre birini seç ve uygula:

1. `tests/` altında failing test → fix et, commit et
2. `scripts/` veya `engine/` altında küçük bug veya eksik hata yakalama → fix et, commit et
3. Herhangi bir `.py` / `.sh` dosyasında açıklayıcı yorum / docstring eksikse → ekle, commit et
4. `CODEBASE_MAP.md` içeriği güncel değilse → güncelle, commit et
5. Son 3 Codex commit'inde değiştirilen dosyalara test ekle, commit et

```bash
# Son Codex commit'lerini gör
cd /home/gokhan/UniverseCreator && git log --oneline -5 2>/dev/null
```

**Kural:** Her cycle minimum 1 commit. Commit yoksa Z.AI ban riski!

---

### 1c — Sonucu Yaz: analysis/glm_code_result.md

```bash
cat > /home/gokhan/UniverseCreator/analysis/glm_code_result.md << 'CODERESULT'
# GLM Code Result
**Tarih:** YYYY-MM-DD HH:MM | **Cycle:** N

## Ne Yapıldı
[Kısa açıklama — hangi dosyalar değişti, neden]

## Değişen Dosyalar
- `path/to/file.py` — [ne değişti]

## Test Sonucu
[pytest çıktısı veya "test yok / atlandı"]

## Commit
[git commit hash + mesaj]
CODERESULT
```

---

## Adım 1d — Repo / Release Durum Verisi

```bash
# Özet durum
cat /home/gokhan/UniverseCreator/STATE_SUMMARY.json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('Toplam:', d.get('total_products',0))
print('Live:', d.get('live_count',0))
print('Healthy:', d.get('healthy_count',0))
print('Checkout coverage:', d.get('checkout_coverage','?'))
" 2>/dev/null || cat /home/gokhan/UniverseCreator/STATE_SUMMARY.json 2>/dev/null | head -30

# Son sorunlar
tail -20 /home/gokhan/UniverseCreator/issues/issues.jsonl 2>/dev/null || echo "issues.jsonl yok"

# En son Codex araştırma özeti (varsa)
ls /home/gokhan/UniverseCreator/sistem-planlama/planlama*.md 2>/dev/null | tail -1 | xargs -I{} tail -30 {} 2>/dev/null || echo "Henüz planlama dosyası yok"
```

---

## Adım 2 — Kritik Kod / Release Sorun Tespiti

Şunları kontrol et:
1. **Checkout eksik live ürünler**: `co=false` veya checkout_url boş + status=live
2. **Vercel blocked**: live ama erişilemiyor (ssoProtection)
3. **Deploy URL eksik**: live ama URL yok
4. **Sağlık skoru**: healthy/live oranı (hedef >%90)

```bash
python3 -c "
import json
try:
    state = json.load(open('/home/gokhan/UniverseCreator/STATE.json'))
    prods = state.get('products', {}).get('active', [])
    no_checkout = [p['slug'] for p in prods if p.get('status')=='live' and not p.get('checkout_url','').startswith('http')]
    no_url = [p['slug'] for p in prods if p.get('status')=='live' and not p.get('url','').startswith('http')]
    print(f'Checkout eksik live: {len(no_checkout)}')
    print(f'URL eksik live: {len(no_url)}')
    if no_checkout[:5]: print('İlk 5:', no_checkout[:5])
except Exception as e:
    print(f'STATE.json okuma hatası: {e}')
" 2>/dev/null
```

---

## Adım 2b — Kod / Optimize Fırsatı Handoff'u

Analiz sırasında net, küçük ve güvenli bir kod/release iyileştirmesi görürsen handoff üret:

- **Kod/otomasyon işi ise:** `analysis/glm_fix_brief.md` yaz.
- **Task doğrudan Codex'e uygunsa:** `analysis/codex_task.md` için kısa ve net görev bırak.
- **Landing page / SEO / UX polish ise:** `.signals/optimizer_needed` yaz ve kısa bir not ekle.

Kurallar:
- Büyük rewrite yok.
- İnsan müdahalesi gerektiren payout / KYC / vendor policy kararlarını kodla "çözülmüş" gibi yazma.
- Sadece dosya bazlı, kısa, uygulanabilir brief üret.

Örnek `analysis/glm_fix_brief.md` formatı:

```markdown
## GLM Fix Brief
**Tarih:** YYYY-MM-DD HH:MM

| Alan | Not |
|---|---|
| Problem | ... |
| Önerilen dosyalar | ... |
| Kabul kriteri | ... |
| Risk | ... |
```

---

## Adım 3 — Kodla İlgili Yeni Dosyaları Dahil Et

Eğer kod/release/ci ile ilgili yeni dosyalar varsa, oneri.md'ye kısa özet ekle:

```bash
# Yeni kod/release dosyaları
ls -t /home/gokhan/UniverseCreator/sistem-planlama/*.md 2>/dev/null | head -4 | while read f; do
    echo "=== $f ==="
    head -15 "$f"
    echo ""
done
```

---

## Adım 3b — QA Result Kontrolü

```bash
cat /home/gokhan/UniverseCreator/analysis/qa_result.md 2>/dev/null || echo "qa_result.md yok"
```

- `FAIL` görürsen: `analysis/oneri.md`'ye `"QA FAIL: {slug} — {sorun}"` satırı ekle
- 2 cycle boyunca FAIL kalıyorsa Telegram'a `"⚠️ QA FAIL tekrar ediyor"` bildirimi gönder:

```bash
# qa_result.md FAIL durumunda Telegram bildirimi (2 cycle tekrar ediyorsa)
QA_CONTENT=$(cat /home/gokhan/UniverseCreator/analysis/qa_result.md 2>/dev/null || echo "")
if echo "$QA_CONTENT" | grep -q "FAIL"; then
    QA_TS=$(stat -c %Y /home/gokhan/UniverseCreator/analysis/qa_result.md 2>/dev/null || echo 0)
    NOW=$(date +%s)
    QA_AGE=$(( NOW - QA_TS ))
    # >2400s = 2 cycle (20dk*2) ise tekrar ediyor
    if [ "$QA_AGE" -gt 2400 ]; then
        /home/gokhan/UniverseCreator/scripts/telegram_send.sh --msg "⚠️ QA FAIL tekrar ediyor — qa_result.md ${QA_AGE}s süredir FAIL"
    fi
fi
```

---

## Adım 3c — run_ledger.jsonl Özeti

```bash
tail -20 /home/gokhan/UniverseCreator/logs/run_ledger.jsonl 2>/dev/null | python3 -c "
import json, sys
lines = [json.loads(l) for l in sys.stdin if l.strip()]
if not lines:
    print('run_ledger.jsonl boş veya yok')
else:
    fail = sum(1 for l in lines if l.get('status') == 'fail')
    modes = set(l.get('mode') for l in lines if l.get('mode'))
    print(f'Son 20 cycle: {fail} fail, modlar: {modes}')
" 2>/dev/null || echo "run_ledger.jsonl okunamadı"
```

---

## Adım 3d — codex_task.md Staleness Kontrolü

```bash
TASK_AGE=$(( $(date +%s) - $(stat -c %Y /home/gokhan/UniverseCreator/analysis/codex_task.md 2>/dev/null || echo 0) ))
echo "codex_task.md yaşı: ${TASK_AGE}s"
# >6300s = 105dk = 3 codex cycle → stale
if [ "$TASK_AGE" -gt 6300 ]; then
    echo "⚠️ codex_task.md stale (${TASK_AGE}s)" >> /home/gokhan/UniverseCreator/analysis/oneri.md
    echo "UYARI: codex_task.md stale — analysis/oneri.md'ye eklendi"
fi
```

---

## Adım 3e — .signals/researcher_needed Yazma

```bash
# STATE_SUMMARY'den deploy_missing ve spec_ready oku
python3 -c "
import json, time, os

try:
    summary = json.load(open('/home/gokhan/UniverseCreator/STATE_SUMMARY.json'))
except:
    summary = {}

deploy_gap = summary.get('deploy_missing', 0) or summary.get('no_url_count', 0)
spec_ready = summary.get('spec_ready', 0)

# Son researcher_done timestamp kontrolü
researcher_done_ts = 0
try:
    rd = json.load(open('/home/gokhan/UniverseCreator/analysis/researcher_done.json'))
    researcher_done_ts = rd.get('ts', 0)
except:
    pass

now = time.time()
research_age = now - researcher_done_ts if researcher_done_ts else 99999

trigger = False
reason = ''
if deploy_gap > 20:
    trigger = True; reason = 'deploy_gap'
elif spec_ready > 5:
    trigger = True; reason = 'spec_ready'
elif research_age > 10800:  # 3 saat
    trigger = True; reason = 'research_stale'

if trigger:
    os.makedirs('/home/gokhan/UniverseCreator/.signals', exist_ok=True)
    with open('/home/gokhan/UniverseCreator/.signals/researcher_needed', 'w') as f:
        json.dump({'reason': reason, 'ts': int(now), 'deploy_gap': deploy_gap, 'spec_ready': spec_ready}, f)
    print(f'✅ .signals/researcher_needed yazıldı (reason={reason})')
else:
    print(f'ℹ️ Researcher tetikleme gerekmedi (deploy_gap={deploy_gap}, spec_ready={spec_ready}, research_age={int(research_age)}s)')
" 2>/dev/null
```

## Adım 3f — Codex Multi Auth Sağlık Kontrolü

```bash
cat /home/gokhan/UniverseCreator/.signals/codex_auth_state.json 2>/dev/null || echo "codex_auth_state yok"
tail -40 /home/gokhan/UniverseCreator/logs/codex_loop.log 2>/dev/null | grep -E "Auth preference|account .*auth/limit issue|fallback account|codex_auth_state|cma activate|usage limit|high demand|429|rate limit" || true
```

- `preferred_account` değişmişse: Codex bir sonraki cycle'da o hesabı ilk deneyecek
- `last_result = auth_switch_*` ise: hesap değişmiş, sebep auth/limit
- `last_result = failure` ise: auth dışı hata, hesabı boşuna zıplatma

---

## Adım 4 — analysis/oneri.md Güncelle

`/home/gokhan/UniverseCreator/analysis/oneri.md` dosyasını güncelle (eski path `oneri.md` değil):

```markdown
# UniverseCreator Analiz Raporu
**Tarih:** YYYY-MM-DD HH:MM | **Cycle:** [N]

## Codex Durumu
- Son mode: {EXECUTION/STRATEGY/IDLE}
- codex_task.md: {fresh/stale}
- Son run: {başarılı/başarısız}

## QA Durumu
- Son QA: {PASS/FAIL/YOK}
- Tekrar eden FAIL: {varsa slug}

## Portföy Özeti
- Toplam: X | Live: X | Healthy: X (%..)
- Deploy gap: X (>20 → researcher tetikle)
- Checkout eksik: X

## Kritik Öncelikler
1. [En acil sorun + sinyal durumu]
2. [İkinci sorun]

## Araştırma Durumu
- Son researcher: {son researcher_done timestamp}
- Researcher sinyal gönderildi mi: {evet/hayır}

## Öneriler
[Somut, uygulanabilir adımlar]
```

---

## Adım 5 — Telegram Bildirimi (ZORUNLU)

```bash
# oneri.md'den özet al
OZET=$(head -20 /home/gokhan/UniverseCreator/analysis/oneri.md 2>/dev/null | grep -E "^-|^#|^•" | head -6 | tr '\n' '\n' || echo "Analiz tamamlandı")

# STATE_SUMMARY'den metrikler
LIVE=$(python3 -c "import json; s=json.load(open('/home/gokhan/UniverseCreator/STATE_SUMMARY.json')); print(f'{s[\"healthy_count\"]}/{s[\"live_count\"]}')" 2>/dev/null || echo "?/?")
DGAP=$(python3 -c "import json; print(json.load(open('/home/gokhan/UniverseCreator/STATE_SUMMARY.json')).get('deploy_missing_or_bad_url',0))" 2>/dev/null || echo "?")

printf '📊 <b>GLM ANALİZ — %s</b>\n\n📦 Sağlık: %s | Deploy gap: %s\n\n💡 <b>Öneriler:</b>\n%s\n\n%s' \
    "$(date '+%d.%m %H:%M')" "$LIVE" "$DGAP" "$OZET" \
    "${BLOKER:+⚠️ Bloker: $BLOKER}" \
    | /home/gokhan/UniverseCreator/scripts/telegram_send.sh

# Kritik bloker varsa yardım iste
# /home/gokhan/UniverseCreator/scripts/telegram_send.sh --help-request "GLM" "Açıklama"
```

---

## ⚠️ GLM'nin Rolleri
- **Micro-Coder (BİRİNCİL)**: Her cycle aktif kod yazar, test çalıştırır, commit atar — Z.AI policy zorunluluğu
- **Gözlemci + Analist**: Portföy sağlık durumunu izler, oneri.md üretir
- **Handoff üretici**: Büyük işler için glm_fix_brief.md yazar, Codex'e devreder
- **Kurtarıcı değil**: Production deploy yapma, sadece scripts/tests/docs kodla ve raporla
