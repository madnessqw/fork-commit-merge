# Strateji Dosyası — UniverseCreator Gelir Stratejileri
> Bu dosyayı her 3. cycle'da oku ve uygula.

## Temel Prensipler

### 1. Derinlik > Genişlik
- Az ama kaliteli iş üret. 50 yarım ürün yerine 3 tam ürün.
- Her ürünü/bounty'yi TAMAMLA, sonra sonrakine geç.

### 2. 3'te 1 Araştırma Döngüsü
- Cycle N: Execute (bounty/ürün üret)
- Cycle N+1: Execute (devam, PR kontrol)
- Cycle N+2: ARAŞTIRMA (ddgr ile web search, yeni fırsat, plan)

### 3. Pending ≠ Earned
- PR merge olmadan gelir claim ETME
- WALLET.json'da sadece merged PR'lar "earned" olabilir

### 4. ROI Hesabı
- Cycle maliyeti: ~$0.02. Minimum hedef: $0.10/cycle
- 5 cycle $0 gerçek gelir = STRATEJİ DEĞİŞTİR

### 5. Anti-Spam
- CONTRIBUTING.md aynı pattern max 3 repo — SINIR AŞILDI, ARTIK KULLANMA
- Aynı bounty'i tekrar claim ETME — mind/CLAIMED_BOUNTIES.md kontrol et
- Aynı pattern'i 5+ kez tekrarlama — farklı içerik üret

## Gelir Kanalları (ÖNCELİK SIRASI)
1. **🏆 BountyHub** (✅ AKTİF — EN ÖNCELİKLİ) — bountyhub.dev, PayPal ile ödeme
   - 0% hunter fee! PayPal → chaotikss@gmail.com → HEMEN çekilebilir
   - Hedefler: Evershop #630 ($30), Freelens #1280 ($50), AzerothCore ($50)
2. **Algora Bounties** (✅ AKTİF) — algora.io, Stripe Connect ile ödeme (yarın doğrulanacak)
   - Hedefler: Isaac #45 ($850), Archestra #3378 ($500), #1301 ($900)
3. **GitHub Bounties** (✅ AKTİF) — ddgr ile bounty ara. CONTRIBUTING.md YASAK!
4. **Dev.to Blog** (✅ AKTİF) — API key: config/accounts.json → dev_to.api_key
   - 8 makale hazır! curl ile yayınla
5. **Ürün Satışı** (✅ AKTİF) — LemonSqueezy "CodeForge Labs"
6. **Freelance** (⏳ BEKLEYEN) — Fiverr/Upwork henüz açılmadı

## Survival Tiers
| Tier | Balance | İsim | Davranış |
|------|---------|------|----------|
| 0 | $0 | AWAKENING | Acil gelir üret, minimal risk |
| 1 | $0-5 | SURVIVAL | Bounty odaklı, tek kanal |
| 2 | $5-50 | GROWING | Çeşitlendir, 2 kanal |
| 3 | $50-500 | THRIVING | Ürün + freelance, 3+ kanal |
| 4 | $500-5000 | ALPHA | Altyapı yatırımı, VPS |
| 5 | $5000+ | EMPEROR | Multi-agent, full SaaS |

## Web Arama Komutları
```bash
# Bounty arama
ddgr --json -n 5 "github bounty open issues reward"

# Platform keşfet
ddgr --json -n 5 "algora bounties open source"

# Rakip analizi
ddgr --json -n 5 "AI developer tools trending 2026"

# URL oku (Jina Reader — API key gereksiz)
curl -s "https://r.jina.ai/URL" | head -200
```

## Karar Ağacı
1. mind/CLAIMED_BOUNTIES.md oku (tekrar etme)
2. Her 3. cycle mi? → ARAŞTIRMA yap (ddgr)
3. Bounty var mı? → Claim et, çalış, PR aç
4. Bounty yok? → Ürün/içerik üret
5. Cycle sonu → STATE.json güncelle, Telegram rapor
