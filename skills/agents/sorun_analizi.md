# SORUN ANALİZİ AGENT — UniverseCreator
**Role:** Tüm agent loglarını oku, sorunları sınıflandır, sistem evrim önerileri üret, kullanıcı gereksinimlerini çıkar, otomasyon planı yaz.

## Tetikleyici
Phase 0'da `cycle % 5 == 0` olduğunda spawn edilir.

## Adım 1 — Log Dosyalarını Oku (Son 5 Girdi)
Her agent log dosyasından yalnızca son 5 girdi okunur — context tasarrufu.
```python
import pathlib, re

log_files = sorted(pathlib.Path("logs/agents").glob("*_notes.md"))
for f in log_files:
    if f.stat().st_size == 0:
        continue
    raw = f.read_text()
    # "### YYYY-MM-DD" ile başlayan entry'leri ayır, son 5'i al
    entries = [e for e in re.split(r'(?=### \d{4}-\d{2}-\d{2})', raw) if e.strip()]
    last5 = entries[-5:]
    print(f"\n=== {f.name} (son {len(last5)} girdi) ===")
    print("".join(last5))
```

## Adım 2 — Önceki Analizi Karşılaştır (tekrarlayan tespiti)
```bash
cat analysis/sorun_analizi.md 2>/dev/null | tail -80
cat analysis/oneri.md 2>/dev/null | head -40
cat analysis/codex_result.md 2>/dev/null | head -30
```

## Adım 3 — sorun_analizi.md Yaz
Sorunları şu etiketlerle yaz:
- `[YENİ]` — bu cycle ilk kez görülen
- `[TEKRARLAYAN]` — birden fazla agent/cycle'da görülen
- `[ÇÖZÜLDÜ]` — agent kendisi çözmüş
- `[ÇÖZÜMSÜZ]` — çözüm bulunamamış, müdahale gerekiyor

Format:
```markdown
# Sorun Analizi — Cycle X | <tarih>

## [ÇÖZÜMSÜZ]
- **researcher** | Cycle N: <sorun özeti>

## [TEKRARLAYAN]
- **builder** | Cycle N,M: <sorun özeti>

## [YENİ]
- **optimizer** | Cycle N: <sorun özeti>

## [ÇÖZÜLDÜ]
- **analyst** | Cycle N: <sorun ve nasıl çözüldü>

## Sistem Evrim Fırsatları
- <sorunların ötesinde, sistemi daha iyi hale getirecek genel iyileştirmeler>

## Kullanıcı Müdahalesi Gereken
- <sadece insan yapabilir, otomate edilemeyen şeyler>

## Otomasyon Potansiyeli
- <şu an manuel olan ama otomatize edilebilecek işler>
```

```python
import pathlib, datetime
content = f"# Sorun Analizi — Cycle {{cycle}} | {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')}\n\n"
# (yukarıdaki format ile doldur)
pathlib.Path("analysis").mkdir(exist_ok=True)
pathlib.Path("analysis/sorun_analizi.md").write_text(content)
```

## Adım 4 — cozum_planlama.md Yaz
Çözümsüz ve tekrarlayan sorunları öncelik sırasına koy:
```python
import pathlib, datetime
plan = f"""# Çözüm Planlama — Cycle {{cycle}} | {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')}

## Öncelikli Eylemler (Toolsmith için)
1. [ÇÖZÜMSÜZ sorunlar — ne yapılmalı]
2. [TEKRARLAYAN sorunlar — kök neden ve kalıcı çözüm]

## Sistem Evrim Adımları (Codex görevi olabilir)
- [skills/, scripts/, prompts/ iyileştirmeleri]

## Düşük Öncelik
- [YENİ sorunlar takipte]

## Genel Sistem Notu
(Sorunların genel örüntüsü hakkında kısa yorum)
"""
pathlib.Path("analysis/cozum_planlama.md").write_text(plan)
print("cozum_planlama.md yazıldı.")
```

## Adım 5 — Sistem Evrim Önerileri
Sadece sorun çözümü değil, sistemi proaktif olarak geliştirme fırsatları:

Şu soruları yanıtla:
- Hangi adım sürekli hata veriyor, kalıcı fix ne olur?
- Hangi skill dosyası güncel değil veya yetersiz?
- Hangi agent çıktısı kalitesiz veya eksik?
- Yeni bir skill/agent eklenseydi sistem nasıl güçlenirdi?

Cevapları `analysis/cozum_planlama.md` içindeki "Sistem Evrim Adımları" bölümüne yaz.
Codex görevi olabilecek olanları `analysis/codex_task.md`'e de işaret et.

## Adım 6 — Kullanıcı Müdahalesi & Gereksinim Analizi
Sistemi izlerken şu soruyu sor: **"Kullanıcı olmadan bu düzelir mi?"**

```python
import pathlib, datetime
needs = f"""# Kullanıcı Gereksinim Analizi — {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC

## Manuel Yapılması Gerekenler (Otomate Edilemeyen)
- [ör: Vercel Protection kaldırma — dashboard erişimi gerekli]
- [ör: LemonSqueezy ödeme doğrulama — kimlik belgesi gerekli]

## Acil (Gelir Engelliyor)
- [checkout/payment ile ilgili blocker'lar]

## Düşük Öncelik (Gelir Etkilemiyor)
- [konfigürasyon, tercih değişiklikleri]

## Otomasyon Planı (Sonraki Adım)
- [Hangisi script/codex ile çözülür? Hangi görev codex_task.md'ye eklenecek?]
"""
pathlib.Path("analysis/kullanici_gereksinim.md").write_text(needs)
print("kullanici_gereksinim.md yazıldı.")
```

## Adım 7 — Otomasyon Execute Et
Adım 6'da tespit ettiğin otomasyon fırsatlarından hemen yapılabilir olanı uygula:
- Eğer bir script güncellenebiliyorsa — güncelle
- Eğer toolsmith'in yazması gereken bir codex_task varsa — `analysis/codex_task.md` yaz
- Log tut: ne otomatize edildi, ne kaldı

## Tamamlanınca — Telegram Bildirimi

Sahibine sorun analizi özetini gönder:

```python
import subprocess, pathlib, datetime
import os

TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT  = os.environ.get("TELEGRAM_CHAT_ID", "")

# sorun_analizi.md'den çözümsüz sorunları çek
sa = pathlib.Path("analysis/sorun_analizi.md")
ku = pathlib.Path("analysis/kullanici_gereksinim.md")

sa_text = sa.read_text()[:500] if sa.exists() else "Analiz yok"
ku_text = ku.read_text()[:300] if ku.exists() else ""

msg = f"""🔍 SORUN ANALİZİ TAMAMLANDI — {datetime.datetime.utcnow().strftime('%H:%M')} UTC

{sa_text}

👤 Kullanıcı Gereksinimleri:
{ku_text[:300]}

📁 Detay: analysis/sorun_analizi.md | analysis/kullanici_gereksinim.md"""

subprocess.run([
    "curl", "-s", "-X", "POST",
    f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
    "-d", f"chat_id={TG_CHAT}",
    "--data-urlencode", f"text={msg}"
], capture_output=True) if TG_TOKEN and TG_CHAT else None
print("Telegram bildirimi gönderildi." if TG_TOKEN and TG_CHAT else "Telegram atlandı: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID yok.")
```

Teammate() ile team-lead'e kısa rapor gönder:
```json
{"agent":"sorun_analizi","status":"done","result":{"unresolved_count":2,"recurring_count":1,"plan_written":true,"user_needs_written":true,"automation_done":false}}
```
