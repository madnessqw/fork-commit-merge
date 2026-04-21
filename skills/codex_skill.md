# Codex Skill — Uzun Vadeli Kod Uygulayıcı

Bu dosyayı okuyan Codex Agent, UniverseCreator içinde **uygulayıcı** modundadır: önce state'i anlar, sonra küçük ama kalıcı kod değişikliği yapar, sonucu kanıtla yazar ve commit eder.

## Sıra

1. `analysis/codex_task.md` oku.
2. Sistemi tanı:
   - `STATE_SUMMARY.json`
   - `analysis/oneri.md`
   - `analysis/sorun_analizi.md`
   - Gerekirse `analysis/cozum_planlama.md` ve `analysis/kullanici_gereksinim.md`
3. Görevin gerçek darboğazını seç:
   - Stale task varsa canlı state'e göre daralt.
   - Secret/token sızıntısı, bozuk otomasyon veya state drift varsa önce onu düzelt.
   - İnsan müdahalesi gerektiren ödeme/Vercel sorunlarını kodla “çözülmüş” gibi gösterme.
4. Dosyaları okumadan edit yapma.
5. Cerrahi kod değişikliği yap; büyük rewrite yok.
6. Doğrula:
   - Python dosyaları için `python3 -m py_compile ...`
   - Shell dosyaları için `bash -n ...`
   - State/summary değiştiyse ilgili script'i çalıştır.
7. `analysis/codex_result.md` yaz:
   - Ne okundu
   - Ne değişti
   - Hangi doğrulamalar geçti
   - Kalan blokajlar
8. Sadece kendi değiştirdiğin dosyaları `git add` ile stage et.
9. `git commit -m "codex: YYYYMMDD-HHMM — <kısa sonuç>"` ile commit at.

## Çatışma Kuralı

`analysis/codex_task.md` araştırma modu gibi no-code bir spec söylüyor ama doğrudan insan bu skill'i kod/commit için çalıştırdıysa:

- Research çıktısını bozma.
- Production ürüne dokunmadan güvenli altyapı/otomasyon iyileştirmesi seç.
- Bu çatışmayı `analysis/codex_result.md` içinde açıkça yaz.

## Güvenlik

- Token, webhook, API key, credential dosyaya yazılmaz.
- Geniş config/report dump yok; okuma gerekiyorsa redaction kullan.
- Telegram/e-posta/post gibi dış bildirimler default kapalıdır; explicit opt-in/env yoksa gönderme.
- Git remote URL'lerini raw basma; tokenlı remote görürsen düz URL'ye çevir.
