# Market Research Guide — Researcher Agent İçin
**Version:** 1.0 | **Başlangıç Cycle:** 1 | **Güven skoru:** Temel

---

## Başarılı Ürün Kriterleri

| Kriter | Eşik |
|--------|------|
| Fiyat aralığı | $5-49 one-time |
| Yapılabilirlik | Vercel + Node.js ile |
| Hedef kitle | Developer, freelancer, küçük işletme |
| Problem netliği | 10 saniyede anlatılabilir |
| Rakip sayısı | 1-5 (çok kalabalık kategorilerden kaçın) |
| Build süresi | 2-3 cycle içinde MVP |

---

## Araştırma Kaynakları (Öncelik Sırasıyla)

### 1. GitHub Trending (En Güvenilir)
```bash
gh api '/search/repositories?q=stars:>100+created:>2026-01-01&sort=stars' | jq '.items[:10] | .[] | {name, description, stargazers_count}'
```

### 2. ProductHunt
```bash
curl -s 'https://r.jina.ai/https://www.producthunt.com/topics/developer-tools' | head -100
```

### 3. IndieHackers
```bash
curl -s 'https://r.jina.ai/https://www.indiehackers.com/products?sorting=newest' | head -100
```

### 4. Hacker News
```bash
curl -s 'https://r.jina.ai/https://news.ycombinator.com/show' | head -100
```

---

## En Çok Satan Kategori Geçmişi

| Kategori | Açıklama | Risk |
|---------|---------|------|
| API tools | Geliştiriciler için API wrapper | Düşük |
| Data formatting | JSON/CSV/XML dönüştürücüler | Düşük |
| URL tools | URL analizi, shortener, checker | Düşük |
| Image tools | OG image, resize, optimize | Orta |
| Code tools | Formatter, linter, validator | Düşük |
| Monitoring | Uptime, health check, ping | Orta |

---

## Kaçınılacak Kategoriler

- Tam anlamıyla doymuş piyasa (ChatGPT wrapper, yapay zeka sohbet botu)
- LLM API gerektiren ama pahalı olan araçlar
- Çok niş, az potansiyel müşteri kitlesi
- 3+ cycle gerektiren büyük projeler

---

## Araştırma Çıktı Formatı

```json
{
  "name": "Ürün Adı",
  "tagline": "Tek cümle açıklama",
  "problem": "Developer'lar X yapmak için Y vakit harcıyor",
  "solution": "Z ile bunu 1 satırda yap",
  "price": "$19",
  "evidence": "ProductHunt'ta 500+ upvote, GitHub 1200 star",
  "competitors": [
    {"name": "Rakip", "price": "$49/ay", "url": "https://..."}
  ],
  "api_spec": {
    "endpoint": "/api/process",
    "input": {"key": "value"},
    "output": {"result": "value"}
  }
}
```

---

## Başarılı Ürün Örnekleri (Referans)
*(skill-writer tarafından doldurulur)*

## Hızlı Red Bayrakları
- "Bir dakikada yüzlerce şey yapabilir" → Odaksız, başarısız
- Rakipler çok güçlü ve ücretsiz → Geç
- Demo'su zor açıklanıyor → Geç

---

## Cycle 637 Guncellemeleri

### Mevcut Portfolio Durumu
- **24 aktif urun** - Tumu $19 fiyattan
- **22/24 urun checkout'lu** (%91.6 coverage)
- **Checkout bekleyenler:** universe-hub (portfolio hub), llm-token-lens (LLM araci)
- **OPTIMIZE mode aktif** - Yeni build yok, mevcut urunler iyilestiriliyor

### Yeni Eklenen Urunler (Son Cycle'lar)
| Urun | Kategori | Durum |
|------|----------|-------|
| MockForge | API Testing | Live, checkout'lu |
| RateGuard | API Rate Limiting | Live, checkout'lu |
| PDF Forge | PDF Generation | Live, checkout'lu |
| LLM TokenLens | LLM Debugging | Live, checkout bekliyor |
| Universe Hub | Portfolio | Live, hub urun |

### Bos Kategoriler (Firsat)
- API Security (ScanGuard onerilmisti)
- Image Processing (PixelForge)
- LLM Cost Optimization (PromptOps)
- OpenAPI/Schema (SchemaForge)
- Web Performance (PulseCheck)

### Arastirma Notlari - Cycle 637
- **En iyi firsat:** API Security Scanner (ScanGuard) - Guvenlik kategorisi bos
- **Alternatif:** Image Processing, LLM Cost Optimizer
- **Fiyat onerisi:** $29 (premium kategoriler icin)
- **Kanalan kategoriler:** ChatGPT wrapper, AI sohbet botu (doymus piyasa)
