# Cozum Planlama — Cycle 1196 | 2026-04-26 04:51 UTC

## Oncelikli Eylemler (Toolsmith / GLM icin)

### 1. [ONEMLI — YAPILMASI GEREKEN] STATE Cycle Sync Fix
- **Sorun:** STATE.json cycle 1195'te, kimi_loop 1196/1197 calismis — STATE gecersiiz
- **Kok neden:** Kimi loop STATE'i guncellemiyor veya guncelleme basarisiz oluyor
- **Cozum:**
  1. `STATE.json`'i oku, `cycle` alanini bul
  2. `kimi_loop.log`'dan en son calisan cycle numarasini bul
  3. Fark varsa STATE'i guncelle
- **Kalici fix:** Her kimi loop sonunda STATE.json sync kontrolu ekle

### 2. [ONEMLI — YAPILMASI GEREKEN] Orphan Dizin Karar ve Temizlik
- **Sorun:** 117 orphan dizin tespit edildi — 15 has_code, 50 has_spec, 20 minimal, 13 dead, 11.5MB
- **Kok neden:** Dizin silme veya entegrasyon olmamis, birikmis
- **Cozum (GLM):**
  1. `orphan_cleanup_planner.py` ciktisini oku
  2. 15 code+spec'li dizinden spec-ready olanlari belirle
  3. `spec_ready_count` hesaplamasini duzelt — diskte spec varsa STATE'e ekle
- **Kalici fix:** Orphan bulundugunda otomatik bildirim + archive karari

### 3. [TEKRARLAYAN — P0] Vercel Alias Drift — 12 Urun
- **Sorun:** 5 active drift + 7 accepted drift urun var
- **Kok neden:** Vercel token invalid, alias atanamıyor
- **Cozum:** Gokhan Manuel — Vercel dashboard'dan device code: MJFC-THWB ile login ol, alias'ları duzelt
- **Kalici fix:** Vercel token yenileme + alias fix script

### 4. [TEKRARLAYAN — P1] Vercel Auth Blocked
- **Sorun:** `vercel_auth_issue=True` — deploy ve alias islemleri bloke
- **Kok neden:** Token expired/invalid
- **Cozum:** Gokhan Manuel — `vercel login` veya device code ile yeniden auth ol
- **Kalici fix:** Token yenileme mekanizmasi

### 5. [TEKRARLAYAN — P2] Codex Offline
- **Sorun:** Her iki Codex hesabi da limitte, Apr 28'e kadar offline
- **Kok neden:** Usage limit askint
- **Cozum:** GLM/Kimi build moduna gecmis durumda — devam ediyor
- **Kalici fix:** Ucuncu hesap ekleme veya usage monitoring

## Sistem Evrim Adimlari (Codex gorevi olabilir)

### SWARM-Level Fixes
1. **STATE sync guard** — kimi loop her calistiginda STATE.json cycle'unu log'daki ile karsilastir, fark varsa uyar
2. **Orphan dedupe pipeline** — her cycle'da disk STATE'i karsilastir, orphan = disk'te var STATE'te yok, bildir
3. **Dual canonical drift metric** — `active_drift` ve `accepted_drift` ayri say, dashboard'da ayri goster
4. **spec_ready_count fix** — diskte `SPEC.md` veya `product.json` olan urunleri say, STATE'e yansit
5. **Checkout URL validation loop** — Polar checkout URL'lerinin HTTP 200 dondugunu periyodik kontrol et

### Dust Cleanup
- 117 orphan dizinden 13 dead olanlari `scripts/orphan_archive.sh` ile _archived/ altina tası
- 50 has_spec'li orphan'den spec kalitesi ortalama uzeri olanlari `products/`'a tası

## Dusuk Oncelik
- **$0 revenue** — aktif checkout var ama satış yok, landing page veya pricing sorunu olabilir
- **spec_ready mismatch** — 4 urun spec-ready ama STATE'de 0, bu Cycle 1197 orphan temizligi ile cozulur

## Genel Sistem Notu
Sistem stabil calisiyor: 169/169 saglikli, 0 checkout gap. Ana sorunlar:
1. **Veri tutarliligi:** STATE 2 cycle gecersiiz — karar mekanizmasi yanlis veriye dayanabilir
2. **Orphan birikimi:** 117 dizin birikmis, zamanla buyuyen sorun
3. **Manuel Vercel islemleri:** Alias ve auth icin dashboard gerekiyor
4. **Codex offline:** Insaat ve iyilestirme duraksamis, Codex donunce devam edecek

Sistem saglikli ama veri tutarliligi ve Manuel Vercel islemleri oncelikli.
