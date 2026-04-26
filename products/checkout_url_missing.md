# 🔴 Manuel İşlem Gerekli — Checkout URL Eksik

Aşağıdaki ürünler LemonSqueezy'de oluşturulmalı ve checkout URL'leri STATE.json'a eklenmeli:

## Yüksek Öncelik (Son Deploy Edilenler):

### 1. Lorem Ipsum Generator Pro
```bash
# LemonSqueezy Dashboard → Products → Add Product
# Ürün adı: Lorem Ipsum Generator Pro
# Fiyat: $19
# Checkout oluştur → URL'yi kopyala

./scripts/set_checkout_url.sh lorem-ipsum-generator "<checkout_url>"
```
- Webhook: https://lorem-ipsum-generator-amber-eight.vercel.app/api/webhook
- Vercel: https://lorem-ipsum-generator-amber-eight.vercel.app
- GitHub: https://github.com/universe7creator/lorem-ipsum-generator

### 2. URL Builder Pro
```bash
./scripts/set_checkout_url.sh url-builder-pro "<checkout_url>"
```
- Webhook: https://url-builder-pro.vercel.app/api/webhook
- Vercel: https://url-builder-pro.vercel.app

### 3. YAML Converter Pro
```bash
./scripts/set_checkout_url.sh yaml-converter-pro "<checkout_url>"
```
- Webhook: https://yaml-converter-pro.vercel.app/api/webhook
- Vercel: https://yaml-converter-pro.vercel.app

## Orta Öncelik:

### 4. JWT Generator Pro
```bash
./scripts/set_checkout_url.sh jwt-generator-pro "<checkout_url>"
```
- Webhook: https://jwt-generator-pro.vercel.app/api/webhook

### 5. Timestamp Converter Pro
```bash
./scripts/set_checkout_url.sh timestamp-converter-pro "<checkout_url>"
```
- Webhook: https://timestamp-converter-pro-blond.vercel.app/api/webhook

### 6. Code Minifier Pro
```bash
./scripts/set_checkout_url.sh code-minifier-pro "<checkout_url>"
```
- Webhook: https://code-minifier-pro.vercel.app/api/webhook

### 7. Hash Generator Pro
```bash
./scripts/set_checkout_url.sh hash-generator-pro "<checkout_url>"
```
- Webhook: https://hash-generator-pro-nine.vercel.app/api/webhook

### 8. URL Encoder/Decoder Pro
```bash
./scripts/set_checkout_url.sh url-encoder-decoder "<checkout_url>"
```
- Webhook: https://url-encoder-decoder.vercel.app/api/webhook

### 9. Cron Expression Parser
```bash
./scripts/set_checkout_url.sh cron-expression-parser "<checkout_url>"
```
- Webhook: https://cron-expression-parser.vercel.app/api/webhook

## Düşük Öncelik (Vercel Protection Sorunu Var):

### 10. API Compare
```bash
# ÖNCE Vercel Dashboard'dan Password Protection'ı kapat
./scripts/set_checkout_url.sh api-compare "<checkout_url>"
```
- Vercel: https://api-compare-5pcffinor-madnessqws-projects.vercel.app

### 11. CSS to Tailwind
```bash
# ÖNCE Vercel Dashboard'dan Password Protection'ı kapat
./scripts/set_checkout_url.sh css-to-tailwind "<checkout_url>"
```
- Vercel: https://css-to-tailwind-htsc2qisb-madnessqws-projects.vercel.app

### 12. Password Generator Pro
```bash
# ÖNCE Vercel Dashboard'dan Password Protection'ı kapat
./scripts/set_checkout_url.sh password-generator-pro "<checkout_url>"
```
- Vercel: https://password-generator-fulhb6tzt-madnessqws-projects.vercel.app

---

## Toplam Eksik: 12 ürün

Bu ürünler LemonSqueezy'de oluşturulup checkout URL'leri eklendiğinde satışa hazır olacak.

*Oluşturulma tarihi: $(date -u +"%Y-%m-%d %H:%M:%S UTC")*
*Cycle: 860*
