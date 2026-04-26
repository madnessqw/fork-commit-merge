# Vercel Protection Sorunu - Manuel Çözüm Rehberi

**Tarih:** 2026-04-17
**Cycle:** 805
**Sorun:** 4 üründe Vercel Password Protection aktif, bu nedenle 401 hatası dönüyor

## Etkilenen Ürünler

| # | Ürün | Slug | Vercel URL | Durum |
|---|------|------|------------|-------|
| 1 | HTTP Pulse | http-pulse | https://http-pulse-3t76r1qiu-madnessqws-projects.vercel.app | 🔴 401 |
| 2 | DataFlip | dataflip | https://dataflip-c75m3wvzn-madnessqws-projects.vercel.app | 🔴 401 |
| 3 | Regex Tester Pro | regex-tester-pro | https://regex-tester-4bp9bfjq3-madnessqws-projects.vercel.app | 🔴 401 |
| 4 | Webhook Tester | webhook-tester | https://webhook-tester-2dl7d2vs3-madnessqws-projects.vercel.app | 🔴 401 |

## Manuel Çözüm Adımları

### Adım 1: Vercel Dashboard'a Giriş

```bash
# CLI ile login (eğer token varsa)
vercel login

# Veya browser'dan:
# https://vercel.com/dashboard
```

### Adım 2: Projeyi Seç

1. Vercel Dashboard'a git
2. `madnessqws-projects` workspace'ini seç
3. Etkilenen projeden birini seç (örn: `http-pulse`)

### Adım 3: Settings > Protection

1. Sol menüden **Settings** → **Protection** sekmesine git
2. **Password Protection** bölümünü bul
3. **Password Protection** = **Disabled** olarak ayarla
4. **Save** butonuna tıkla

### Adım 4: Deploy Yeniden Tetikle (Opsiyonel)

Eğer değişiklik otomatik deploy edilmezse:

```bash
# Projeyi rebuild et
cd products/<slug>
vercel --prod
```

### Adım 5: Doğrula

```bash
# Test komutu
curl -sI https://<url>/ | head -5

# HTTP 200 bekleniyor (401 yerine)
```

## CLI Alternatif (Eğer Token Var)

```bash
# Protection'ı CLI ile kapatma (beta feature, her zaman çalışmayabilir)
vercel project update <project-id> --password-protection=false
```

## Otomasyon Notu

CLI üzerinden Password Protection yönetimi Vercel'de sınırlıdır. Manuel dashboard girişi en güvenilir yöntemdir.

## Tekrar Kontrol

Her ürün için şu URL'ler test edilmeli:

```bash
curl -s https://http-pulse-3t76r1qiu-madnessqws-projects.vercel.app/api/health
curl -s https://dataflip-c75m3wvzn-madnessqws-projects.vercel.app/api/health
curl -s https://regex-tester-4bp9bfjq3-madnessqws-projects.vercel.app/api/health
curl -s https://webhook-tester-2dl7d2vs3-madnessqws-projects.vercel.app/api/health
```

**Başarı kriteri:** Tümü HTTP 200 döndürmeli.

## STATE.json Güncellemesi

Çözüldükten sonra STATE.json'da şu ürünlerin health_status'unu `healthy` olarak güncelle:
- http-pulse
- dataflip
- regex-tester-pro
- webhook-tester
