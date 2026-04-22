# Vercel Canonical URL Drift - Manuel Düzeltme Talimatları

**Cycle:** 945
**Tarih:** 2026-04-20
**Sorun:** 5 üründe canonical URL (slug.vercel.app) çalışmıyor, preview URL çalışıyor

## Etkilenen Ürünler

| Ürün | Preview URL (Çalışan) | Canonical URL (Bozuk) | Hata |
|------|----------------------|----------------------|------|
| secretguard | secretguard-kappa.vercel.app | secretguard.vercel.app | 401 |
| ai-cost-dashboard | ai-cost-dashboard-jade.vercel.app | ai-cost-dashboard.vercel.app | 404 |
| webhook-tester | webhook-tester-beryl.vercel.app | webhook-tester.vercel.app | 404 |
| pdf-forge | pdf-forge-five.vercel.app | pdf-forge.vercel.app | 500 |
| diffmaster | diffmaster-rose.vercel.app | diffmaster.vercel.app | 401 |

## Düzeltme Adımları

### Yöntem 1: Vercel Dashboard (Önerilen)

1. https://vercel.com/dashboard adresine git
2. Her bir ürün için sırayla:
   a. Projeyi tıkla (örn: secretguard)
   b. "Settings" sekmesine git
   c. "Domains" bölümüne git
   d. "Add" butonuna tıkla
   e. Domain: `secretguard.vercel.app` yaz
   f. "Add" ile kaydet

3. Password Protection varsa kaldır:
   - Settings → Deployment Protection
   - "Password Protection" → OFF

### Yöntem 2: CLI (Token Düzeltilirse)

```bash
# Her ürün için:
vercel alias set secretguard-kappa.vercel.app secretguard.vercel.app
vercel alias set ai-cost-dashboard-jade.vercel.app ai-cost-dashboard.vercel.app
vercel alias set webhook-tester-beryl.vercel.app webhook-tester.vercel.app
vercel alias set pdf-forge-five.vercel.app pdf-forge.vercel.app
vercel alias set diffmaster-rose.vercel.app diffmaster.vercel.app
```

## Otomatik Denenenler

Cycle 945'te otomatik fix denendi:
- ✅ html-to-markdown-pro: Düzeltildi (deploy tamamlandı)
- ❌ 5 canonical drift: Manuel müdahale gerekiyor (token invalid)

## Sonraki Cycle

Bu drift düzeltildikten sonra:
- STATE_SUMMARY.json otomatik güncellenecek
- 58/58 ürün %100 healthy olacak
- INNOVATE moduna geçilebilir (yeni ürün)

---
**Not:** Vercel token invalid olduğu için CLI işlemleri başarısız. Dashboard üzerinden manuel düzeltme gerekiyor.
