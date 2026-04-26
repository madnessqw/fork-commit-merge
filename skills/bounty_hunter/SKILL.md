---
name: bounty_hunter
description: GitHub bounty arama, claim etme, PR gönderme ve takip süreci
---

# Bounty Hunter Skill

UniverseCreator'un bounty bulma, claim etme ve PR gönderme sürecini yönetir.

## 1. Bounty Arama

```bash
# DuckDuckGo ile bounty ara
ddgr --json -n 10 "github bounty open issues reward"
ddgr --json -n 5 "algora open source bounties"
ddgr --json -n 5 "gitcoin bounties developer"
ddgr --json -n 5 "onlydust open source contributions"

# Jina Reader ile bounty sayfasını oku
curl -s "https://r.jina.ai/URL" | head -200
```

## 2. Bounty Seçim Kriterleri

### ✅ İYİ Bounty (claim et)
- Documentation yazma (README, API docs, guides)
- Bug fix (açıkça tanımlanmış, test edilebilir)
- Test yazma (unit test, integration test)
- Çeviri (i18n — Türkçe avantajı!)
- Small features (< 200 satır kod)

### ⛔ KÖTÜ Bounty (atla)
- CONTRIBUTING.md template (YASAK — sınır aşıldı!)
- Çok büyük feature requests (> 500 satır)
- Framework migration
- Belirsiz requirement'lar
- Daha önce claim edilmiş (mind/CLAIMED_BOUNTIES.md kontrol et!)

## 3. Claim & PR Workflow

```bash
# 1. Fork et
gh repo fork OWNER/REPO --clone --remote

# 2. Branch oluştur
cd REPO && git checkout -b bounty-ISSUEID

# 3. Çalış ve commit et
git add . && git commit -m "feat: bounty description"

# 4. Push et
git push origin bounty-ISSUEID

# 5. PR aç
gh pr create --repo OWNER/REPO \
  --title "feat: Bounty #ISSUEID description" \
  --body "Closes #ISSUEID. Payment: PayPal chaotikss@gmail.com"

# 6. CLAIMED_BOUNTIES.md'ye kaydet
echo "| $(date +%Y-%m-%d) | OWNER/REPO | #ISSUEID | pattern | amount | open |" >> mind/CLAIMED_BOUNTIES.md
```

## 3.5 BountyHub Claim (KRİTİK — PR gönderdikten sonra MUTLAKA yap!)

> ⚠️ Sadece GitHub'a PR göndermek YETMEZDİR. BountyHub'da claim etmezsen para GELMEZ.

PR gönderdikten sonra Playwright browser ile şu adımları uygula:

1. **BountyHub'a git:** `https://www.bountyhub.dev/en/explore`
2. **Bounty'yi bul:** Issue'nun repo adını arama çubuğuna yaz (örn: "evershop")
3. **Bounty detayına gir:** Sonuçlardan ilgili bounty'ye tıkla
4. **"CLAIM BOUNTY" butonuna tıkla**
5. **PR URL'yi yapıştır:** `https://github.com/OWNER/REPO/pull/PR_NUMBER`
6. **"IMPORT PULL REQUEST" butonuna tıkla**
7. **"Claim Created" mesajını gör** → Başarılı!

### Playwright Kodu (Referans)
```python
# BountyHub claim örneği
page.goto("https://www.bountyhub.dev/en/explore")
page.fill('input[placeholder*="search"]', 'REPO_NAME')
page.click('button:text("Search")')  # veya search icon
# Bounty sonucuna tıkla
page.click('text=ISSUE_TITLE')
# Claim butonuna tıkla
page.click('text=CLAIM BOUNTY')
# PR URL gir
page.fill('input[placeholder*="Pull Request"]', PR_URL)
page.click('text=IMPORT PULL REQUEST')
```

### Ödeme Akışı
```
PR gönder → BountyHub'da claim et → PR merge olur → Bounty owner onaylar → PayPal'a $$ düşer
```

## 4. Dedup Kontrolü

Her claim öncesi:
1. `cat mind/CLAIMED_BOUNTIES.md` — aynı repo/issue var mı?
2. `gh pr list --author universe7creator` — aynı repo'ya PR var mı?
3. Varsa → ATLA, farklı bounty bul

## 5. Takip
- PR gönderdikten sonra BountyHub'da claim etmeyi UNUTMA (Bölüm 3.5)
- 72 saatten fazla bekleyen PR → issue'da comment bırak
- Rejected PR → sebebi öğren, farklı bounty'ye geç
- Merged PR → WALLET.json'ı güncelle, Telegram'dan bildir
- BountyHub dashboard'dan claim durumunu kontrol et: https://www.bountyhub.dev/en/dashboard
