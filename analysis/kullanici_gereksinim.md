# Kullanici Gereksinim Analizi — 2026-04-26 04:51 UTC

## Manuel Yapilmasi Gerekenler (Otomate Edilemeyen)

### Vercel Alias Fix — KRITIK
- 12 urunun Vercel alias'ini dashboard'dan duzeltmek
- Device code: MJFC-THWB
- Active drift (5): croncraft, chmod-calculator, terminal-os, terraink, nginx-config
- Accepted drift (7): jwt-generator, pdf-forge, webhook-tester, email-validator-pro, diffmaster, html-entity-encoder, timestamp-converter

### Vercel Token Yenileme
- `vercel_auth_issue=True` durumu duzeltmek icin yeniden auth olunmasi gerekiyor
- Deploy ve alias islemleri bloke

### Orphan Dizin Karari
- 117 dizin icinden hangilerinin entegre edileceğine karar verilmeli
- 15 has_code + 50 has_spec = 65 potansiyel entegre edilebilir
- 13 dead = silme/adandirma adayi

## Acil (Gelir Engelliyor)
1. **Vercel alias fix** — 12 urunun dogru URL'ye yonlenmesi gerekiyor
2. **$0 revenue** — aktif checkout var ama satış yok. Landing page, pricing, trafik mi?

## Dusuk Oncelik (Gelir Etkilemiyor)
- Orphan dizin archive — 11.5MB waste ama sistemi etkilemiyor
- spec_ready_count mismatch — 4 urunun STATE'e yansimasi

## Otomasyon Plani (Sonraki Adim)
| Gorev | Sorumlu | Durum |
|-------|---------|-------|
| STATE cycle sync | kimi loop | STATE 2 cycle gecersiz, guncelleme mekanizmasi lazim |
| orphan dedupe | GLM | 117 dizin temizlik plani mevcut |
| spec_ready_state sync | GLM | disk=4, STATE=0, duzeltilmeli |
| Vercel alias fix | Gokhan Manuel | device code MJFC-THWB ile dashboard'dan |
| Vercel token | Gokhan Manuel | yeniden auth gerekli |
