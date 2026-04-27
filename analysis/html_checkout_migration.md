# HTML Checkout Migration Report — Cycle 180

**Date:** 2026-04-27
**Status:** NO INTERNET — local analysis only
**Scope:** All 183 live products

---

## Mevcut Durum

| Metric | Count |
|--------|-------|
| Toplam ürün | 183 |
| product.json Polar checkout_url | 183 |
| HTML'de Polar buy button | 9 |
| HTML'de lemonsqueezy URL (migration gerekli) | ~50+ |
| HTML'de buy button yok | ~135 |

---

## Migration Gerektiren Ürünler (Polar'a Geçiş)

### A) Lemonsqueezy → Polar Migration (HTML = lemonsqueezy, product.json = Polar)

| Slug | product.json checkout_url | HTML checkout_url | Durum |
|------|-------------------------|-------------------|-------|
| uuid-generator-pro | polar_cl_wWCB79jXpmnLwd8vZjs5... | profitbridge.lemonsqueezy.com | ❌ MISMATCH |
| url-forge | polar_cl_b1pyWYFkCm1R625auU1U... | profitbridge.lemonsqueezy.com | ❌ MISMATCH |
| ... | | | |

### B) Buy Button Eksik (product.json'da var, HTML'de yok)

Bu ürünlerin HTML'inde hiç buy button yok. Eklenmesi gerekiyor:
- tüm ürünlerin %70'i bu kategoride

---

## checkout_url Uyumsuzluğu Analizi

### Lemonsqueezy → Polar Taşınması Gereken Ürünler

```
uuid-generator-pro: product.json=https://buy.polar.sh/polar_cl_wWCB79jXpmnLwd8vZjs5... HTML=https://profitbridge.lemonsqueezy.com/...
url-forge: product.json=https://buy.polar.sh/polar_cl_b1pyWYFkCm1R625auU1U... HTML=https://profitbridge.lemonsqueezy.com/...
```

### Fix Stratejisi (İnternet Geri Gelince)

1. **polar_checkout_sync.py sync-links** — checkout link'i Polar'da güncelle
2. **HTML grep + replace** — lemonsqueezy URL'leri Polar URL ile değiştir
3. **Buy button yoksa ekle** — uygun yere `<a href="polar_checkout_url" class="btn-primary">Buy $X</a>`

### HTML Buy Button Ekleme Pattern

```html
<!-- Standart buy button (header içinde) -->
<a href="https://buy.polar.sh/polar_cl_XXXX" target="_blank" 
   class="btn btn-primary" style="text-decoration:none;background:#10b981;color:#fff;border-color:#10b981;">
   Buy $X
</a>
```

---

## Alınan Aksiyonlar (Cycle 180)

- [x] xterm-web: buy button + Polar checkout URL eklendi
  - URL: https://buy.polar.sh/polar_cl_PngBLZ9OKHYun4EAWwphEaRfSX2V9vmjTNlaM0AkL0R
  - Fiyat: $9
  - Location: header-actions içinde
  - Commit: xterm-web/public/index.html (untracked)

---

## Sonraki Adımlar (İnternet Geri Gelince)

1. `polar_checkout_sync.py sync-links --status live --status ready_for_payment --replace-non-polar` çalıştır
2. Lemonsqueezy kullanan ürünleri Polar'a migrate et
3. Tüm 183 ürüne HTML buy button ekle
4. Checkout URL'i doğrula

---

## Bilinen Migration Pattern

| Kaynak | Hedef | Örnek |
|--------|-------|-------|
| lemonsqueezy checkout URL | Polar checkout URL | `profitbridge.lemonsqueezy.com` → `buy.polar.sh/polar_cl_XXXX` |
| Buy button yok | Buy button ekle | `<a href="polar_url" class="btn-primary">Buy $X</a>` |
