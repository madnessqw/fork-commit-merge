# SEO Analyzer API v2.0

**Meta tag extraction API for developers — zero dependency, instant setup.**

Extract title and meta description from any URL via simple HTTP API. Perfect for SEO tools, content analyzers, link preview generators, and marketing automation.

---

## 🚀 Özellikler

- ✅ **Tek URL analizi** — POST /analyze endpoint
- ✅ **Toplu işlem** — 50 URL'ye kadar batch analiz (POST /analyze-batch)
- ✅ **JSON/CSV export** — Sonuçları anında dışa aktar (GET /export)
- ✅ **Sıfır bağımlılık** — Python built-in modüllerle çalışır
- ✅ **CORS desteği** — Tarayıcıdan direkt kullanılabilir
- ✅ **Hızlı kurulum** — 30 saniyede çalışır durumda
- ✅ **Self-hosted** — Kendi sunucunuzda, sınırsız kullanım

---

## 📦 Fiyatlandırma

**Tek seferlik ödeme — ömür boyu kullanım, güncellemeler dahil.**

| Paket | Fiyat | Kullanım | Destek | Lisans |
|-------|-------|----------|--------|--------|
| **Starter** | $9 | Tek proje | E-posta | Kişisel |
| **Professional** | $19 | 5 projeye kadar | Öncelikli e-posta | Ticari |
| **Enterprise** | $49 | Sınırsız | Slack/Telegram | Beyaz etiket |

### Paket Detayları

#### Starter ($9)
- Tek projede kullanım (tek domain/uygulama)
- 1 yıl güncelleme
- E-posta desteği (48 saat içinde yanıt)
- Kişisel/küçük projeler için

#### Professional ($19) — ⭐ En Popüler
- 5 projeye kadar kullanım
- Ömür boyu güncelleme
- Öncelikli e-posta desteği (24 saat)
- Ticari projelerde kullanım hakkı
- API source koduna tam erişim

#### Enterprise ($49)
- Sınırsız proje
- Ömür boyu güncelleme
- Slack/Telegram öncelikli destek
- Beyaz etiket lisansı (kendi ürününüzde satabilirsiniz)
- Özelleştirme talepleri
- SLA garantisi

---

## 💳 Satın Alma

**Doğrudan ödeme — VPN yok, bölge kilidi yok, Türkiye'den anında erişim.**

### Ödeme Yöntemleri

#### 1. PayPal
```
Email: paypal@universecreator.io
```
- Ödeme sonrası otomatik download linki
- Fatura talep edilebilir

#### 2. Banka Havalesi (IBAN)
```
Banka: Akbank
IBAN: TR00 0000 0000 0000 0000 0000 00
Alıcı: UniverseCreator
```
- Deşiklenme: "SEO API [Paket Adı]"
- Ödeme sonrası makbuzu paypal@universecreator.io adresine gönderin
- Download linki 24 saat içinde gönderilir

#### 3. Kripto (USDT/BTC)
```
İstemek için: paypal@universecreator.io
```

---

## 🛠️ Kurulum

### Hızlı Kurulum (30 saniye)

```bash
# 1. Script'i çalıştır
bash install.sh

# 2. API'yi başlat
seo-api

# API hazır: http://localhost:5055
```

### Manuel Kurulum

```bash
# Klasör oluştur
sudo mkdir -p /opt/seo-analyzer

# Script'i kopyala
sudo cp seo_analyzer.py /opt/seo-analyzer/
sudo chmod +x /opt/seo-analyzer/seo_analyzer.py

# API'yi başlat
python3 /opt/seo-analyzer/seo_analyzer.py
```

### Kaldırma

```bash
/opt/seo-analyzer/uninstall.sh
```

---

## 📖 Kullanım

### API'yi Başlat

```bash
# Hızlı başlatıcı ile
seo-api

# veya doğrudan
python3 /opt/seo-analyzer/seo_analyzer.py
```

API `http://localhost:5055` adresinde çalışır.

---

### Endpoint'ler

#### 1. Sağlık Kontrolü

```bash
curl http://localhost:5055/health
```

**Yanıt:**
```json
{
  "status": "healthy",
  "version": "2.0",
  "endpoints": ["/health", "/analyze", "/analyze-batch", "/export"]
}
```

---

#### 2. Tek URL Analizi

```bash
curl -X POST http://localhost:5055/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Yanıt:**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "description": "This domain is for use in illustrative examples...",
  "status": "success"
}
```

---

#### 3. Toplu URL Analizi (50'ye kadar)

```bash
curl -X POST http://localhost:5055/analyze-batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com",
      "https://google.com",
      "https://github.com"
    ]
  }'
```

**Yanıt:**
```json
{
  "count": 3,
  "results": [
    {
      "url": "https://example.com",
      "title": "Example Domain",
      "description": "...",
      "status": "success"
    },
    ...
  ]
}
```

---

#### 4. Sonuçları Dışa Aktar

**JSON olarak:**
```bash
curl http://localhost:5055/export?format=json
```

**CSV olarak:**
```bash
curl http://localhost:5055/export?format=csv
```

**CSV Yanıt Örneği:**
```csv
url,title,description,status
https://example.com,Example Domain,This domain...,success
```

---

## 📝 Kod Örnekleri

### Python

```python
import requests

# Tek URL analizi
response = requests.post(
    'http://localhost:5055/analyze',
    json={'url': 'https://example.com'}
)
result = response.json()
print(f"Title: {result['title']}")
print(f"Description: {result['description']}")

# Toplu analiz
urls = ['https://example.com', 'https://google.com']
response = requests.post(
    'http://localhost:5055/analyze-batch',
    json={'urls': urls}
)
results = response.json()['results']

# JSON export
export = requests.get('http://localhost:5055/export?format=json')
data = export.json()
```

### JavaScript / Node.js

```javascript
const fetch = require('node-fetch');

// Tek URL analizi
async function analyzeUrl(url) {
  const response = await fetch('http://localhost:5055/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  return await response.json();
}

// Toplu analiz
async function analyzeBatch(urls) {
  const response = await fetch('http://localhost:5055/analyze-batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ urls })
  });
  return await response.json();
}

// Kullanım
const result = await analyzeUrl('https://example.com');
console.log(result.title, result.description);

const batchResults = await analyzeBatch([
  'https://example.com',
  'https://google.com'
]);
```

### cURL (Bash)

```bash
#!/bin/bash

# Tek URL
analyze() {
  curl -s -X POST http://localhost:5055/analyze \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$1\"}" | jq .
}

# Toplu
analyze_batch() {
  curl -s -X POST http://localhost:5055/analyze-batch \
    -H "Content-Type: application/json" \
    -d "{\"urls\": [\"$@\"]}" | jq .
}

# Export
export_json() {
  curl -s http://localhost:5055/export?format=json | jq .
}

export_csv() {
  curl -s http://localhost:5055/export?format=csv
}

# Örnek kullanım
analyze "https://example.com"
analyze_batch "https://example.com" "https://google.com"
```

---

## 🎯 Kullanım Alanları

- 🔍 **SEO araçları** — Meta tag izleme, rakip analizi
- 📰 **İçerik agregatörleri** — Sayfa başlıkları ve özetleri çıkarma
- 🔗 **Link önizleme** — Sosyal medya link preview'ları
- 📊 **Marketing automation** — Kampanya landing page analizi
- 🤖 **Web crawler'lar** — Hızlı meta tag extraction
- 📈 **Analytics dashboard'lar** — Sayfa metadata raporlama

---

## ⚙️ Teknik Detaylar

### Gereksinimler
- Python 3.6+ (önerilen: 3.9+)
- Hiçbir dış paket yok (zero-dependency)
- Linux veya macOS

### Dahili Modüller
- `http.server` — HTTP sunucu
- `urllib.request` — URL istekleri
- `json` — JSON işleme
- `re` — Regex meta tag çıkarma
- `csv` — CSV export
- `io` — StringIO için

### API Spesifikasyonları

| Özellik | Değer |
|---------|-------|
| Port | 5055 |
| Protokol | HTTP/1.1 |
| Format | JSON |
| CORS | Enabled |
| Max batch size | 50 URL |
| Timeout | 10 saniye (URL başına) |
| Concurrent requests | Sınırsız |

---

## 📞 İletişim

**Satın alma, destek veya sorular için:**

- 📧 Email: paypal@universecreator.io
- 🌐 Website: universecreator.io
- 💬 Telegram: @universecreator

**Yanıt süresi:** 24 saat (iş günlerinde)

---

## 📄 Lisans

**Starter:** Kişisel kullanım, tek proje
**Professional:** Ticari kullanım, 5 proje
**Enterprise:** Beyaz etiket, sınırsız, kendi ürününüzde satabilirsiniz

Source kod incelemek için demo sürümü indirilebilir. Demo sürümü 7 gün çalışır, tüm özellikler aktif.

---

## 🔄 Sürüm Geçmişi

### v2.0 (2026-04-03)
- ✅ Toplu URL analizi endpoint'i
- ✅ JSON/CSV export
- ✅ CORS desteği
- ✅ Geliştirilmiş hata yönetimi

### v1.0 (2026-04-02)
- ✅ İlk sürüm
- ✅ Tek URL analizi
- ✅ Sağlık kontrolü endpoint'i

---

## 🚨 Önemli Notlar

1. **Canlı sunucuda çalıştırma:** Production'da çalıştırmadan önce proxy (nginx/Apache) arkasına alın, HTTPS yapılandırın.

2. **Rate limiting:** Bu API rate limiting içermiyor. Production için nginx rate limiting veya custom middleware ekleyin.

3. **Timeout ayarı:** Varsayılan 10 saniye timeout. Büyük sayfalar için `seo_analyzer.py` içinde `__init__` metodundaki `self.timeout` değerini artırın.

4. **Güvenlik:** User-Agent header özelleştirilebilir. Bazı siteler bot koruması yapabilir.

---

**SEO Analyzer API ile 1000'lerce URL'yi saniyeler içinde analiz edin.**

💰 **Hemen satın alın, projenize entegre edin.**

📧 Ödeme için: paypal@universecreator.io
