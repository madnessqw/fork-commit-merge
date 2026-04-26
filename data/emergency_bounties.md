# Emergency Bounties - BountyHub

**Tarih:** 2026-04-03
**Hesap:** universe7creator (GitHub)
**Durum:** $0 bakiye - ACIL

---

## Önerilen Bounty'ler (1 Saatten Az Çözülebilir)

### 1. **[Class - Warrior] Sword Specialization doesn't proc with some melee abilities** ⭐ EN İYİ SEÇİM

| Alan | Değer |
|------|-------|
| **Repo** | azerothcore/azerothcore-wotlk |
| **Issue** | #20250 |
| **Link** | https://github.com/azerothcore/azerothcore-wotlk/issues/20250 |
| **Bounty** | $50.00 |
| **Language** | C++ |
| **Durum** | ✅ AÇIK - Claim YOK |
| **Tahmini Süre** | 30-45 dk |

**Problem:** Sword Specialization talent, Hamstring, Sunder Armor ve Rend yetenekleriyle proc olmuyor.

**Çözüm Önerisi:** `spell_mage.cpp` benzeri spell dosyasında Proc sistemini güncellemek. Mevcut örnekler (Sudden Death, Mongoose) zaten doğru çalışıyor - onları referans alarak ekleme yapılabilir.

---

### 2. **[Warrior] Recklessness + Juggernaut causes non-critical mortal strike/slam hits to occur**

| Alan | Değer |
|------|-------|
| **Repo** | azerothcore/azerothcore-wotlk |
| **Issue** | #20741 |
| **Link** | https://github.com/azerothcore/azerothcore-wotlk/issues/20741 |
| **Bounty** | $50.00 |
| **Language** | C++ |
| **Durum** | ✅ AÇIK - Claim YOK |
| **Tahmini Süre** | 30-60 dk |

**Problem:** Recklessness + Juggernaut kombinasyonu non-critical hit'lere neden oluyor.

---

### 3. **[Mage] Arcane Concentration should give every tick of Blizzard a chance to proc Clearcasting**

| Alan | Değer |
|------|-------|
| **Repo** | azerothcore/azerothcore-wotlk |
| **Issue** | #11462 |
| **Link** | https://github.com/azerothcore/azerothcore-wotlk/issues/11462 |
| **Bounty** | $50.00 |
| **Language** | C++ |
| **Durum** | ⚠️ Claim var ama reddedilmiş |

**Not:** Daha önce reddedilmiş bir PR var ama farklı bir yaklaşımla kabul edilebilir.

---

## Araştırılan Ancak Uygun Olmayanlar

| Proje | Issue | Neden Uygun Değil |
|-------|-------|------------------|
| Freelens | #1280 Custom Theme | Claim var, reddedilmiş |
| Evershop | #630 Category bug | 5+ PR denenmiş, hepsi reddedilmiş |
| AzerothCore | #22571 Map Partitioning | Çok büyük feature request |
| Electron | #48191 macOS dialog | macOSbuild gerektirir, claim var |

---

## Harcama Planı

**Hedef:** En az $50 kazanmak için Warrior Sword Specialization issue'yu çöz.

**Adımlar:**
1. ⏳ Issue #20250'yi claim et
2. ⏳ AzerothCore repo'sunu forkla ve clonela
3. ⏳ İlgili spell dosyasını bul (spell_proc system)
4. ⏳ Hamstring, Sunder Armor, Rend'i Sword Spec proc listesine ekle
5. ⏳ Test et ve PR aç
6. ⏳ BountyHub'da claim et

---

## Notlar

- BountyHub %10 creator fee alıyor, geriye $45 kalır
- Ödeme Stripe üzerinden 121 ülkeye yapılabiliyor
- GitHub ile giriş yapıldı (universe7creator)