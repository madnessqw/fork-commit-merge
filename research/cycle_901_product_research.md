# Ürün Araştırma Raporu — Cycle 901
## Tarih: 2026-04-19

---

## 1. Git Command Builder

### Pazar Analizi
- **Mevcut oyuncular:** GitHub Copilot CLI, Warp Terminal, Amazon Q, Aider
- **Boşluk:** Tüm mevcut çözümler terminal/IDE kurulumu gerektiriyor, **browser-based basit alternatif** yok
- **Hedef kitle:** Git öğrenmek isteyen junior developer'lar, nadir git kullanan tasarımcılar/PM'ler

### Ürün Özellikleri
- **Core:** Doğal dil → Git komutu dönüşümü
- **Örnek dönüşümler:**
  - "undo last commit" → `git reset HEAD~1 --soft`
  - "create new branch from main" → `git checkout -b feature-branch main`
  - "see what changed in last commit" → `git show --stat HEAD`
- **Fiyat:** $19 (one-time)
- **Teknoloji:** Vercel serverless + basit NLP mapping

### Farklılaştırıcılar
- History/bookmarks özelliği
- Komut açıklaması (ne yapıyor, ne zaman kullanılır)
- Kopyala-yapıştır kolaylığı
- Offline çalışabilir (client-side only)

---

## 2. HTTP API Client (Browser-Based)

### Pazar Analizi
- **Mevcut oyuncular:** Hoppscotch (açık kaynak, ücretsiz), HTTPie, Bruno
- **Boşluk:** **Basit, hafif, hesap gerektirmeyen** alternatif
- **Hedef kitle:** Hızlı API testi yapmak isteyen developer'lar, Postman'in ağırlığından bıkanlar

### Ürün Özellikleri
- **Core:** Browser'da çalışan HTTP client
- **Metodlar:** GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Headers:** Key-value editor, preset seçenekleri (Content-Type, Auth, vs.)
- **Body:** JSON, form-data, raw text editörleri
- **Response:** Syntax highlighted JSON/XML/HTML, status code, response time
- **Fiyat:** $19 (one-time) veya $9 (daha düşük fiyatla pazara giriş)

### Farklılaştırıcılar
- History (localStorage)
- Collection/bookmark özelliği
- curl komutu export
- Response formatter/beautifier
- Hesap gerektirmez

---

## Öneri

**Öncelik sırası:**
1. **HTTP API Client** — Daha geniş kullanıcı kitlesi, daha net farklılaştırma
2. **Git Command Builder** — Niche ama öğrenme odaklı pazar

**Sonraki adım:** HTTP API Client için product spec oluştur, build phase'e geç.
