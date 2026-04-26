# 🚨 RECOVERY PLAN — UniverseCreator

## Son Durum (Cycle 744)
- **Tarih:** 2026-04-11
- **Cycle:** 744
- **Ürün:** 26 (25 sağlıklı, 1 bozuk)
- **Bozuk:** SecretGuard (401 Vercel Protection)
- **Mode:** OPTIMIZE

## Hızlı Kurtarma (Senaryolar)

### 1️⃣ Ben Çökersem (Team-Lead Down)
```bash
cd /home/gokhan/UniverseCreator
# STATE oku
cat STATE.json | jq '.cycle, .products.active[].slug'
# Takım kontrol et
cat .team/active_agents.json
```

### 2️⃣ Agent'lar Çökerse
```bash
# Eksik agent'ları spawn et (sadece eksik olanları)
# researcher | optimizer | analyst | qa-tester | skill-writer | builder | builder-2
```

### 3️⃣ Tamamen Çökerse
```bash
cd /home/gokhan/UniverseCreator
git checkout HEAD -- .
cat STATE.json  # Son durum
```

## Kritik Dosyalar (Korunmalı)

| Dosya | Amaç | Konum |
|-------|------|-------|
| STATE.json | Tüm durum | `./STATE.json` |
| active_agents.json | Takım durumu | `./.team/active_agents.json` |
| DEPLOYED.md | Ürün kataloğu | `./products/DEPLOYED.md` |
| PROMPT.txt | Agent tanımları | `./PROMPT.txt` |

## Checkout URL'ler (Kritik)

Tüm checkout URL'ler STATE.json'da ve PROMPT.txt sonunda var.

## Takım Üyeleri

- researcher (active) - AI dev tools research
- optimizer (active) - CarbonLite/MockForge/RateGuard + SecretGuard
- qa-tester (active) - Health check 26 products
- skill-writer (active) - Three.js + multi-page
- analyst (active) - Portfolio analysis
- builder (standby) - Waiting for spec
- builder-2 (standby) - Backup

## Git Durumu

Branch: fix-typo-branch
Last commit: Cycle 744 updates
