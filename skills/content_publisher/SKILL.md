---
name: content_publisher
description: Blog/makale yazma, SEO optimizasyonu ve platform yayınlama
---

# Content Publisher Skill

Blog yazıları, teknik makaleler ve ürün tanıtımları oluşturur ve yayınlar.

## 1. İçerik Türleri

### Teknik Blog (Dev.to/Medium)
- AI tool development tutorials
- Open source contribution guides
- Code optimization tips
- Framework comparisons

### Ürün Tanıtımı (LemonSqueezy)
- DevTools CLI bundle
- JSON Formatter, Regex Tester, CSV Converter, Base64 Encoder

### Social Posts (Twitter/X)
- Bounty kazanma hikayeleri
- Tool tanıtımları
- Open source katkı raporları

## 2. Blog Post Template

```markdown
---
title: [Catchy, SEO-friendly title]
published: true
description: [150 char description]
tags: [tag1, tag2, tag3, tag4]
---

## Introduction
[Hook — neden bu yazıyı okumalı]

## Problem
[Çözülen sorun]

## Solution
[Adım adım çözüm]

## Code
[Kod örnekleri]

## Conclusion
[Özet + CTA]
```

## 2.5 Yazar Kuralları (KRİTİK)

- **Yazar adı:** "Can Koylan" (universe7creator)
- ⛔ "UniverseCreator", "Autonomous AI Agent", "bot" gibi ifadeler KULLANMA
- ⛔ Makalenin altına bot imzası KOYMA
- İmza kullanacaksan: "Written by Can Koylan — Software Developer"
- AI tool kullandığından bahsetme — güven kırar, SEO'ya zarar verir

## 3. SEO Kuralları
- Title: 60 karakter max, anahtar kelime başta
- Description: 150 karakter, action-oriented
- Tags: max 4, trending olanları kullan
- Başlıklar: H2, H3 hiyerarşisi
- Kod blokları: syntax highlighting ile
- İç/dış linkler: en az 2-3

## 4. Yayınlama

### Dev.to API ✅ AKTIF
```bash
# API Key: config/accounts.json → dev_to.api_key
API_KEY=$(cat config/accounts.json | python3 -c "import sys,json;print(json.load(sys.stdin)['dev_to']['api_key'])")

# Makale yayınla
curl -X POST "https://dev.to/api/articles" \
  -H "Content-Type: application/json" \
  -H "api-key: $API_KEY" \
  -d '{
    "article": {
      "title": "...",
      "body_markdown": "...",
      "published": true,
      "tags": ["ai", "python", "automation", "opensource"]
    }
  }'

# Makaleleri listele
curl -s "https://dev.to/api/articles/me" -H "api-key: $API_KEY"
```

### Algora Bounty'leri ✅ AKTIF
- Algora.io'da bounty bul → GitHub issue'yu oku → Çözüm yaz → PR gönder
- Ödeme: Direkt USD (Stripe/PayPal)
- RTC'den çok daha değerli — öncelikli hedef

### Hazır İçerikler (output/ klasörü)
- `output/articles/` — yayınlanmayı bekleyen makaleler
- `output/blog-ai-automation-2026.md` — AI automation yazısı
- `work/blog-posts/` — 4+ RustChain/BoTTube makalesi
- `work/social-media-posts/` — tweet/Reddit/Dev.to postları

