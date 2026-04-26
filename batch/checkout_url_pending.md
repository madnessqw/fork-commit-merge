# LemonSqueezy Checkout URL Pending - Cycle 997

Bu dosya, LemonSqueezy'de checkout URL'si oluşturulması gereken ürünleri listeler.

## Eksik Checkout URL'ler (13 ürün)

| # | Ürün Adı | Slug | Fiyat | Vercel URL | Webhook URL |
|---|----------|------|-------|------------|-------------|
| 1 | Text Transformer Pro | text-transformer-pro | $9 | https://text-transformer-pro-theta.vercel.app | https://text-transformer-pro-theta.vercel.app/api/webhook |
| 2 | CronCraft | croncraft | $9 | https://croncraft-zeta.vercel.app | https://croncraft-zeta.vercel.app/api/webhook |
| 3 | EnvGuard Pro | envguard-pro | $9 | https://envguard-pro.vercel.app | https://envguard-pro.vercel.app/api/webhook |
| 4 | API Spec Validator | api-spec-validator | $19 | - | - |
| 5 | Color Contrast Pro | color-contrast-pro | $19 | https://color-contrast-d8xl589m2-madnessqws-projects.vercel.app | https://color-contrast-d8xl589m2-madnessqws-projects.vercel.app/api/webhook |
| 6 | Markdown Table Generator | markdown-table-generator | $9 | https://markdown-table-generator-hmp70qdla-madnessqws-projects.vercel.app | https://markdown-table-generator-hmp70qdla-madnessqws-projects.vercel.app/api/webhook |
| 7 | DiffForge | diffforge | $9 | https://diffforge.vercel.app | https://diffforge.vercel.app/api/webhook |
| 8 | Chart Studio | chart-studio | $9 | https://chart-studio-5tag4enn2-madnessqws-projects.vercel.app | https://chart-studio-5tag4enn2-madnessqws-projects.vercel.app/api/webhook |
| 9 | Code Snippet Manager | code-snippet-manager | $9 | https://code-snippet-manager.vercel.app | https://code-snippet-manager.vercel.app/api/webhook |
| 10 | Email Signature Generator | email-signature | $9 | https://email-signature.vercel.app | https://email-signature.vercel.app/api/webhook |
| 11 | HMAC Generator Pro | hmac-generator | $9 | https://hmac-generator.vercel.app | https://hmac-generator.vercel.app/api/webhook |
| 12 | Timestamp Converter Pro | timestamp-converter | $19 | https://timestamp-converter-k2cqva0od-madnessqws-projects.vercel.app | https://timestamp-converter-k2cqva0od-madnessqws-projects.vercel.app/api/webhook |
| 13 | HTML Entity Encoder/Decoder | html-entity | $9 | https://html-entity.vercel.app | https://html-entity.vercel.app/api/webhook |

## Manuel Oluşturma Adımları

1. https://app.lemonsqueezy.com'a giriş yap
2. Her ürün için "New Product" oluştur
3. Ürün adı, fiyat ve açıklamayı gir
4. Webhook URL'sini ayarla (yukarıdaki tablodan)
5. Checkout URL'i kopyala
6. `./scripts/set_checkout_url.sh <slug> <checkout_url>` ile STATE.json'a ekle

## Hızlı Script

```bash
# Örnek kullanım:
./scripts/set_checkout_url.sh text-transformer-pro "https://profitbridge.lemonsqueezy.com/checkout/buy/XXXX"
```

## Notlar

- api-spec-validator: Vercel URL'si eksik - önce deploy edilmeli
- Oluşturulma tarihi: 2026-04-21
- Cycle: 997
