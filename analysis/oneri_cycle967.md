# UniverseCreator Portföy Analizi — Cycle 967

**Tarih:** 2026-04-20
**Analist:** GLM Analyst (opencode)
**Önceki Rapor:** Cycle 956

---

## 0. Codex/Vercel Auth Durumu

| Kontrol | Durum |
|---------|-------|
| Vercel CLI | KURULU DEĞİL |
| Vercel Token | `vcp_258G...` mevcut ama INVALID |
| codex_auth_switch.md | BULUNAMADI (silinmiş) |
| STATE.json auth | `vercel_auth_issue: true` |
| Device Code | `MJFC-THWB` — kullanıcı onayı bekleniyor |
| Bloke ürün | `color-contrast-pro` |

**Sonuç:** Vercel deploy kanalı tamamen kapalı. Token yenileme veya device code onayı zorunlu.

---

## 1. Genel Durum

| Metrik | Cycle 956 | Cycle 967 | Değişim |
|--------|-----------|-----------|---------|
| Aktif ürün | 113 | 113 | = |
| Live | 47 | 47 | = |
| Building | 62 → | 55 | -7 (ghost cleanup) |
| Ready to Deploy | 3 → | 8 | +5 |
| Ready for Payment | — | 2 | NEW |
| Unknown | 1 | 1 | = |
| Sağlık Skoru | 41.6% | **41.6%** | = (hedef: >90%) |

**Değişim yok.** 11 cycle sonra hala aynı sağlık skorunda. Building ürünler azalmış ama canlı ürün artışı yok.

---

## 2. Kritik Sorunlar (Öncelik Sırası)

### P0 — 3 Hash URL Ürün HTTP 401 (MÜŞTERİ ERİŞİLEMEZ)

| Slug | Mevcut URL | İdeal URL | HTTP |
|------|-----------|-----------|------|
| pdf-forge | `...-7lpqmc4pl-madnessqws-...` | `https://pdf-forge.vercel.app` | 401 |
| diffmaster | `...-neoexql9p-madnessqws-...` | `https://diffmaster.vercel.app` | 401 |
| secretguard | `...-cbg7x1j1t-madnessqws-...` | `https://secretguard.vercel.app` | 401 |

**3 ürün satışa kapalı.** Vercel deploy hash'leri üzerinden publish edilmiş, canonical alias yok.

### P1 — 6 Şüpheli Checkout URL (SAHTE/PLACEHOLDER)

| Slug | Sorun |
|------|-------|
| html-beautifier | URL son eki `-001` |
| base64-pro | Fake UUID: `8a2f9c3e-4b5d-6e7f-8g9h-0i1j2k3l4m5n` |
| llm-token-lens | Fake UUID: `3f9a0d5b-2c4e-6f7g-9b0c-...` |
| color-contrast-pro | URL'de `placeholder-` ifadesi |
| ai-cost-dashboard | URL son eki `-001` |
| diffmaster | URL son eki `-001` |

**4 ürün kesinlikle satış yapamaz** (fake UUID veya placeholder). 2 ürün şüpheli (`-001`).

### P2 — 4 Live Ürün Vercel URL Eksik

| Slug | GitHub | Vercel |
|------|--------|--------|
| table-to-csv | OK | YOK |
| html-to-markdown-pro | OK | YOK |
| csv-to-json-pro | OK | YOK |
| graphql-query-builder | OK | YOK |

GitHub reposu var ama deploy edilmemiş. Checkout URL var ama müşteri ürünü göremiyor.

### P3 — 6 Duplicate Ürün Çifti

| Ürün Adı | Slug 1 (İyi) | Slug 2 (Kaldır) |
|-----------|--------------|-----------------|
| UUID Generator Pro | uuid-generator-pro (ready) | uuid-generator (building) |
| Timestamp Converter Pro | timestamp-converter-pro (live) | timestamp-converter (building) |
| TOML Parser Pro | toml-parser-pro (building) | toml-parser (building) |
| HTML to Markdown Pro | html-to-markdown-pro (live) | html-to-markdown (building) |
| HMAC Generator Pro | hmac-generator-pro (live) | hmac-generator (building) |
| Markdown Previewer Pro | markdown-previewer (empty) | markdown-previewer-pro (building) |

**Oneri:** Live/ready olan versiyonları koru, building olan duplicate'leri STATE.json'dan kaldır.

### P4 — 55 Building Ürünün 54'ünde GitHub Repo YOK (Ghost Products)

55 building ürünün sadece 1'inde (`cron-master`) GitHub URL var. Geri kalan 54 ürünün **hiçbir kodu yok** — sadece STATE.json'da kayıtlı isimler.

**Bu ürünler gerçekte mevcut değil.** Building statüsünde değiller, hiç oluşturulmamışlar.

### P5 — 8 Ready to Deploy Ürün Checkout Eksik

uuid-generator-pro, html-entity, webterminal-pro, cron-expression-builder, toml-toolkit, html-entities, nanoid-generator, ip-network-tools — hepsi deploy hazır ama checkout URL yok.

---

## 3. Fiyat Dağılımı

| Fiyat | Sayı | Oran | Değerlendirme |
|-------|------|------|---------------|
| $9 | 63 | 55.8% | AŞIRI DOLU |
| $19 | 45 | 39.8% | İyi |
| $12 | 2 | 1.8% | Boş |
| $14 | 2 | 1.8% | Boş |
| $29 | 1 | 0.9% | Neredeyse boş |

**Sorun:** %56'lık $9 segment'te rekabet kendi içinden. Premium segment ($29-$49) neredeyse yok.

---

## 4. Kategori Analizi

| Kategori | Ürün | Durum |
|----------|------|-------|
| Format Dönüştürücü | 20 | Aşırı dolu |
| URL/HTTP/API | 14 | İyi |
| JSON/XML/YAML/TOML | 13 | Doymak üzere |
| Renk/CSS/Frontend | 12 | İyi |
| Kriptografi/Güvenlik | 11 | İyi |
| Cron/Zaman | 7 | AŞIRI TEKRAR (5 cron ürünü) |
| Veri/Grafik | 3 | Boş |
| TOML Araçları | 4 | Aşırı niş |

**Boş kategoriler (fırsat):**
- AI/LLM Araçları (2 ürün)
- Database/SQL araçları (1 ürün)
- DevOps Monitoring (0 ürün)
- Testing Araçları (1 ürün)

---

## 5. Aksiyon Planı

### ACIL (Bugün)
1. **Vercel CLI kur + token yenile** → `npm i -g vercel && vercel login`
2. **3 hash URL düzelt** → `vercel --prod` ile canonical deploy
3. **4 fake checkout düzelt** → base64-pro, llm-token-lens, color-contrast-pro, html-beautifier gerçek LemonSqueezy URL

### YÜKSEK ÖNCELİK (1-2 gün)
4. **6 duplicate temizle** → STATE.json'dan building olanları kaldır
5. **54 ghost product temizle** → GitHub repo'su olmayan building ürünleri kaldır veya _archived/ altına taşı
6. **4 Live + Vercel eksik deploy** → table-to-csv, html-to-markdown-pro, csv-to-json-pro, graphql-query-builder
7. **8 ready_to_deploy ürünü deploy et** → Vercel + LemonSqueezy checkout

### ORTA ÖNCELİK (1 hafta)
8. **Cron kategorisi daralt** → 5 ürün yerine 1-2 güçlü ürün
9. **Premium segment aç** → $29-$49 fiyatla kaliteli ürünler
10. **Boş kategorilere ürün** → AI araçları, DevOps, Database

---

## 6. Gelir Potansiyeli

| Senaryo | Live | Ortalama Fiyat | Aylık Gelir |
|---------|------|---------------|-------------|
| Mevcut (47 live, 4 fake checkout) | 43 etkili | $14 | $0-50 (kanıt yok) |
| Düzeltme sonrası (55 live, hepsi checkout) | 55 | $15 | $100-500 |
| Ghost cleanup + deploy (70 live) | 70 | $16 | $500-2000 |
| Hedef (100+ live, SEO aktif) | 100+ | $18 | $5000+ |

**$500K hedef:** 70 satış/gün x $20 x 365 gün. Ciddi SEO + marketing + premium ürün stratejisi gerekli.

---

*Analiz tamamlandı. GLM Analyst — Cycle 967*
