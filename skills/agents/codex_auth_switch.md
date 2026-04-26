# Codex Auth Healthcheck & Account Switch

**Bu skill:** UniverseCodex tmux session'ını izler, auth/limit sorunlarını tespit eder ve
`scripts/codex_loop.sh` içindeki stateful hesap yönlendirmesini açıklar.

## Adım 1 — Log'a Bak, Sorun Var mı?

```bash
# Son 20 satır log
tail -20 /home/gokhan/UniverseCreator/logs/codex_loop.log

# Son başarılı araştırma dosyası var mı?
ls -lt /home/gokhan/UniverseCreator/sistem-planlama/arastirma*.md 2>/dev/null | head -3 || echo "HENüZ ARAŞTIRMA DOSYASI YOK"

# Counter ne durumda?
cat /home/gokhan/UniverseCreator/sistem-planlama/counter.txt 2>/dev/null || echo "Counter yok"

# Running flag var mı? (araştırma devam ediyor mu)
ls -la /tmp/codex_research_running.flag 2>/dev/null && echo "ARAŞTIRMA DEVAM EDİYOR" || echo "Şu an çalışmıyor (cron bekliyor)"
```

## Adım 2 — Sorun Tespiti

```bash
# "usage limit" / "high demand" / 429 / rate limit son 50 satırda var mı?
tail -50 /home/gokhan/UniverseCreator/logs/codex_loop.log | grep -c "usage limit\|high demand\|Reconnecting\|429\|rate limit" || true
```

Yorumlama:
- **0 hata + arastirma*.md dosyaları var**: ✅ Normal çalışıyor
- **Hata var + son cycle'da MD dosyası yazılmamış**: ⚠️ Hesap sorunlu
- **"usage limit" veya "high demand" var**: 🔴 Hesap geçişi gerekli

## Adım 3 — Hesap Geçişi (Sadece Sorun Varsa)

```bash
# Şu an aktif hesap hangisi?
CMA_DISABLE_KEYRING=1 ~/bin/cma list 2>/dev/null || echo "cma list komutu yok"

# Dynamic loop artık `.signals/codex_auth_state.json` içindeki `preferred_account`
# değerine göre ilk hesabı seçer. Son auth/limit hatasında diğer hesaba geçer.
# Manuel override gerekiyorsa sadece şu iki komut kullanılır:
CMA_DISABLE_KEYRING=1 ~/bin/cma activate 1
CMA_DISABLE_KEYRING=1 ~/bin/cma activate 2

# Yeni cycle'ı zorla tetikle
bash /home/gokhan/UniverseCreator/scripts/codex_loop.sh
```

## Adım 4 — Codex Araştırma Modu Kontrolü

```bash
# Araştırma modu aktif mi? (production değil mi?)
grep -c "ARAŞTIRMA & PLANLAMA MODU" /home/gokhan/UniverseCreator/prompts/codex_prompt.txt && echo "✅ Araştırma modu aktif" || echo "⚠️ Production modda!"

# Kaç araştırma dosyası üretildi?
ls /home/gokhan/UniverseCreator/sistem-planlama/arastirma*.md 2>/dev/null | wc -l || echo "0 dosya"
ls /home/gokhan/UniverseCreator/sistem-planlama/planlama*.md 2>/dev/null | wc -l || echo "0 dosya"
```

## Adım 5 — Özet Rapor

Tüm kontroller sonunda şunu raporla (GLM'nin oneri.md bölümüne ekle):

```
## Codex Healthcheck
- Araştırma modu: [AKTİF/PASİF]
- Son başarılı araştırma: [N dakika önce / YOK]
- Üretilen dosya sayısı: [araştırma N, planlama N]
- Auth durumu: [OK / hesap1 limit / hesap2 limit / ikisi de limit]
- Aktif hesap: [1/2]
- Son hata: [usage limit / high demand / başka hata / yok]
- Yapılan işlem: [Hesap geçişi / Zorla tetikleme / Sorun yok]
```
