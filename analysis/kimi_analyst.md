# Kimi Analyst Brief — Adım Adım Görev

## ÖNCELİK SIRASI (KRİTİK)

**⚠️ DÖNGÜYE HER ZAMAN BURADAN BAŞLA — AŞAĞIĞI İZLEME:**

```
1. CHECKOUT ÖNCELİK: polar_checkout_sync.py sync-links çalıştır, gap varsa kapat
2. SATIŞ STRATEJİSİ: @sales-strategist subagent çağır, ürün analizi yap
3. SİSTEM ANALİZİ: Sağlık, error pattern, evolution assessment
```

## Bu Döngünün Odak Alanları

### 0. CHECKOUT KONTROLÜ (ÖNCE!)
```bash
cd /home/gokhan/UniverseCreator
# Checkout gap kontrol et
python3 scripts/polar_checkout_sync.py sync-links --status live --status ready_for_payment --replace-non-polar 2>&1 | tail -20
```

### 0b. SATIŞ STRATEJİSİ (İKİNCİ ÖNCELİK)
```bash
# OpenCode sales-strategist subagent çağır
@sales-strategist analyze current product portfolio for sales optimization opportunities
# veya
@paid-social-strategist suggest traffic and conversion improvements for checkout pages
```

### 1. Sistem Sağlık Kontrolü
```bash
# Oku:
cat /home/gokhan/UniverseCreator/STATE.json
# Vercel deployment durumu:
cat /home/gokhan/UniverseCreator/logs/health_trend.jsonl | tail -20
# Son commit'ler:
git log --oneline -20 --no-walk
```

### 2. Lesson Learned Analizi
```bash
# Son lesson'lar:
ls -lt /home/gokhan/UniverseCreator/lessons/*.md 2>/dev/null | head -5
cat /home/gokhan/UniverseCreator/lessons/checkout-url-lessons.md 2>/dev/null
```

### 3. Error Pattern Analizi
```bash
# Son hatalar:
tail -50 /home/gokhan/UniverseCreator/logs/errors.log
tail -50 /home/gokhan/UniverseCreator/logs/codex_loop.log | grep -i "error\|fail"
```

### 4. Evolution Assessment
```bash
# Son 10 cycle commit:
git log --oneline -10
# Analyse: Hangi alanlarda ilerleme var? Hangisi stagnate?
```

## Çıktı Formatı (kimi_rapor_{timestamp}.md)

```markdown
# Kimi Cycle {NUM} Rapor — {TARIH}

## Checkout Durumu
- Checkout Gap: N ürün
- Sync-links sonucu: [BAŞARILI/BAŞARISIZ]
- Düzeltilen: N

## Satış Stratejisi Analizi
- @sales-strategist çıktısı: [Özet]
- Dönüşüm önerileri: [Liste]
- Fiyat optimizasyonu: [Öneriler]

## Sistem Durumu
- Health Score: X%
- Live Products: N
- Unhealthy: N
- Canonical Drift: N

## Tespit Edilen Sorunlar
1. [Sorun] — [Kısa açıklama]
2. [Sorun] — [Kısa açıklama]

## Evolution Assessment
- İlerleme: [Alanlar]
- Stagnate: [Alanlar]
- Öneriler: [Yapılabilir (ekleme yok, sadece analiz)]

## Lessons İndeksi
- Okunan: lesson_xyz.md
- Çıkarım: [Ne öğrenildi]

## Sonraki Adımlar (Otonom)
- [GLM'e öneri]
- [Codex'e öneri]
```

## Telegram Mesaj Formatı

```
🔬 Kimi Cycle {NUM}
💰 Checkout: {GAP} | 📊 Satış Stratejisi: [ÖNERİ]
📊 Sağlık: {X}% | 🔴 Sorun: {N} | 📈 Öneri: {Z}
🕐 {SAAT}
```
