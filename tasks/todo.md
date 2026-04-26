# TODO.md — Active Task Queue
> Agent picks from here when choosing WORK. Sorted by priority.
> ℹ️ UPDATED 2026-03-25 by Gokhan. Platforms below are active. Check config/accounts.json for details.

## 🔴 P0 URGENT — Do THIS Cycle

### 🏆 BountyHub Bounty Çöz (PayPal ile HEMEN para alınır!)
- [ ] BountyHub'da bounty ara ve çöz (0% fee, PayPal ödeme)
  - Site: https://www.bountyhub.dev
  - Login: GitHub OAuth (universe7creator) — ZATEN KAYITLI ✅
  - Payout: PayPal (chaotikss@gmail.com) — Türkiye'ye direkt ödeme
  - Hedefler: Evershop #630 ($30), Freelens #1280 ($50)
  - İş akışı: Issue oku → Çöz → PR gönder → bountyhub.dev'de claim et

### Dev.to Makale Yayınla (Pasif gelir)
- [ ] 8 hazır makaleyi Dev.to'ya yayınla
  - API Key: config/accounts.json → dev_to.api_key — AKTİF ✅
  - Kullanıcı: universe7creator / Can Koylan
  - Nasıl: skills/content_publisher/SKILL.md oku
  - Komut: curl -X POST https://dev.to/api/articles ...

### PR Durumunu Kontrol Et
- [ ] Mevcut PR'ların durumunu kontrol et
  - `gh pr list --author universe7creator --state all --limit 20`
  - Merged olanları WALLET.json'a "earned" olarak ekle
  - Closed/rejected olanları CLAIMED_BOUNTIES.md'ye "rejected" yaz

## 🟡 P1 HIGH PRIORITY

### Algora Bounty Çöz (Daha büyük ödüller, Stripe ile)
- [ ] Algora bounty çöz (algora.io — ZATEN KAYITLI ✅)
  - Isaac #45 ($850 RAG Pipeline) — düşük rekabet, Python uyumlu
  - Archestra #3378 ($500) — Agent schedule triggers, JavaScript
  - Archestra #1301 ($900) — MCP Apps support
  - İş akışı: GitHub issue çöz → PR gönder → Algora ödemeyi otomatik tetikler

### Yeni Bounty Ara (ddgr ile)
- [ ] `ddgr --json -n 10 "github bounty open issues reward"`
  - mind/CLAIMED_BOUNTIES.md kontrol et (tekrar etme!)
  - ⛔ CONTRIBUTING.md GÖNDERME — bu pattern YASAK!

## 🟢 P2 NORMAL PRIORITY

- [ ] LemonSqueezy'de ilk ürünü oluştur (DevTools CLI Bundle $4.99)
  - Mağaza: CodeForge Labs — https://codeforgelabs.lemonsqueezy.com
- [ ] Her 3. cycle araştırma yap (ddgr)
- [ ] PR merge takibi — 72 saatten fazla bekleyen PR'lara follow-up

## ⛔ YASAKLAR
- CONTRIBUTING.md PR'ları YASAK (35 PR, 0 merge = %0 başarı)
- Aynı bounty'i tekrar claim ETME — mind/CLAIMED_BOUNTIES.md kontrol et
- Yeni bir platform/kaynak ihtiyacın varsa Gokhan'a Telegram'dan bildir

## ℹ️ AKTİF PLATFORMLAR (signup gerekmez)
| Platform | Durum | Ödeme |
|----------|-------|-------|
| BountyHub | ✅ AKTİF | PayPal → chaotikss@gmail.com |
| Algora | ✅ AKTİF | Stripe Connect → Akbank |
| Dev.to | ✅ AKTİF | API key mevcut |
| LemonSqueezy | ✅ AKTİF | CodeForge Labs mağazası |
| GitHub | ✅ AKTİF | gh CLI mevcut |
| PayPal | ✅ AKTİF | chaotikss@gmail.com |
