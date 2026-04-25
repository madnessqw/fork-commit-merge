# Sağlıksız Ürün Raporu - Cycle 1098
**Tarih:** 2026-04-22
**Toplam Sağlıksız:** 12 ürün

## 🔴 Kritik Sorun (Timeout/FAIL)

| Ürün | URL | Durum | Çözüm |
|------|-----|-------|-------|
| jwt-generator | https://jwt-generator.vercel.app | Timeout (0) | Redeploy + API fix |
| pdf-forge | https://pdf-forge.vercel.app | Timeout (0) | Redeploy + API fix |
| html-entity-encoder | https://html-entity-encoder.vercel.app | Timeout (0) | Redeploy + API fix |

## 🟡 Health Check Eksik (Null)

| Ürün | URL | Durum | Çözüm |
|------|-----|-------|-------|
| webterminal-pro | https://webterminal-pro.vercel.app | Null | Health check çalıştır |
| html-entities | https://html-entities.vercel.app | Null | Health check çalıştır |
| html-minifier-pro | https://html-minifier-pro.vercel.app | Null | Health check çalıştır |
| css-grid-gen | https://css-grid-gen.vercel.app | Null | Health check çalıştır |
| dockerfile-generator | https://dockerfile-generator.vercel.app | Null | Health check çalıştır |
| markdown-previewer-pro | https://markdown-previewer-pro.vercel.app | Null | Health check çalıştır |
| image-compressor-pro | https://image-compressor-pro.vercel.app | Null | Health check çalıştır |
| email-validator-pro | https://email-validator-pro.vercel.app | Null | Health check çalıştır |
| terminal-theme-studio | https://terminal-theme-studio.vercel.app | Null | Health check çalıştır |

## Eylem Planı

1. **Vercel limit reset sonrası (12-18 saat):**
   - jwt-generator redeploy + API fix
   - pdf-forge redeploy + API fix
   - html-entity-encoder redeploy

2. **Health check batch:**
   - Tüm null status ürünler için health check çalıştır
   - 401/403 hataları varsa Vercel protection kaldır

3. **Öncelik:** jwt-generator ve pdf-forge (en kritik)
