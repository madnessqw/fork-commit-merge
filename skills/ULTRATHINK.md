# ULTRATHINK.md — Düşünme Protokolü

> Her işlem öncesi bu protokolü uygula. Hızlı hareket etmek ile DOĞRU hareket etmek aynı şey değil. Bir daha baştan başlamak yerine, ilk seferde doğruyu yap.

---

## Neden ULTRATHINK?

Bir agentın en büyük hatası: "hata → düzelt → hata → düzelt" döngüsü.  
Bu döngü:
- Zaman harcar (her döngü burn rate)
- Commit geçmişini kirletir (10 "fix: ..." commit)
- Sistemi geri iter

**Çözüm:** Her işlemden önce derin düşün. Az hareket, yüksek değer.

---

## 3-Adım ULTRATHINK Protokolü

Her işlem öncesi şu 3 soruyu yanıtla:

### Adım 1 — ROI Sorusu
> "Bu hamle şirketin hedefine ne kadar değer katıyor?"

- Spesifik ölçülebilir etki nedir? ("daha iyi olur" değil — "$X gelir yolu açılır" veya "N ürün satılabilir hale gelir")
- Şu an en yüksek değerli görev bu mu? Daha yüksek ROI'li başka şey var mı?
- Bu görevi atlasam ne kaybederim?

**Hedef**: Önce en yüksek değerli işe odaklan.

### Adım 2 — 3 Alternatif
> "Bu sorunu çözmenin en az 3 farklı yolu nedir?"

| # | Yol | Hız | Güvenilirlik | Risk |
|---|---|---|---|---|
| A | [Yol 1] | ... | ... | ... |
| B | [Yol 2] | ... | ... | ... |
| C | [Yol 3] | ... | ... | ... |

- Hangisi en etkili kombinasyonu sunuyor?
- Risk nerede en yüksek? Fallback planı var mı?
- Seçilen yolun neden en iyi olduğunu 1 cümleyle açıkla.

**Hedef**: Körce ilk akla gelen çözümü değil, düşünülmüş en iyi çözümü uygula.

### Adım 3 — Kalite Önce
> "Bu adımı yaparsam, bir daha geri dönmek zorunda kalır mıyım?"

- Dosyayı okumadan düzenleme yapma
- Varsayım değil, doğrulama: dosyayı önce oku, sonra değiştir
- Commit öncesi: syntax check + secret scan
- Çalışıp çalışmadığından emin olmadan tamamlandı deme

**Hedef**: "Describe" değil "DO" — her adım ölçülebilir bir çıktı üretir.

---

## "Describe vs DO" Problemi (logic-md'den)

**Kötü:**
> "Ürünlerin checkout URL'lerini güncelleyecektim ve Polar API'yi çağırarak checkout linkler oluştururduk..."

**İyi:**
> `polar_checkout_sync.py` çalıştırıldı → 12 ürünün `product.json` dosyasına `checkout_url` yazıldı → commit `abc123` yapıldı.

**Fark:** İlki niyet tanımlıyor. İkincisi somut çıktı üretir.

Her adımın beklenen ÇIKTISI belirlenmeli:
- Bu adımı tamamladığımda **hangi dosya değişti** veya **hangi komut çalıştı**?
- Çıktı yoksa → adım tamamlanmadı.

---

## Output Contract Prensibi

Her önemli adım için kendin şunu sor:

```
Bu adımın output'u ne?
  → Değiştirilen dosya: [dosya adı]
  → Çalıştırılan komut: [komut]
  → Oluşturulan artifact: [dosya/commit/mesaj]
  
Bu output mevcut değilse → adım BAŞARISIZ → fallback uygula
```

---

## Fallback Kuralı

Bir adım başarısız olursa:
1. `lessons/checkout-url-lessons.md`'e not yaz: ne denendi, neden başarısız, sonraki cycle ne yapılmalı
2. Telegram'a gönder: ne yapıldı, nerede takıldı
3. Dur — düzeltilmiş haliyle bir sonraki cycle'a bırak

**Asla:** "Belki çalışmıştır" diyerek commit yapma. Doğrula, sonra commit et.

---

## ULTRATHINK Hızı

Toplam düşünme süresi: **2-3 dakika** (35dk veya 20dk cycle'ın küçük bir kısmı).  
Bu 2-3 dakika, 15 dakikalık "hata → düzelt" döngüsünü engeller.

**Her cycle'da ULTRATHINK = daha az geri adım = daha fazla ilerleme.**
