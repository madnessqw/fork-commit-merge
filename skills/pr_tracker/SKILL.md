---
name: pr_tracker
description: GitHub PR durumu takibi, merge/reject kontrolü ve WALLET.json güncelleme
---

# PR Tracker Skill

Açık PR'ların durumunu izler, merge/reject olaylarını yakalar ve WALLET.json'ı günceller.

## 1. PR Durum Kontrolü

```bash
# Tüm PR'ları listele
gh pr list --author universe7creator --state all --limit 30

# Belirli bir PR'ın detayını al
gh pr view PRNUMBER --repo OWNER/REPO --json state,title,mergedAt,closedAt

# Sadece merged olanlar
gh pr list --author universe7creator --state merged --limit 10

# Sadece closed (rejected) olanlar
gh pr list --author universe7creator --state closed --limit 10
```

## 2. İşlem Akışı

### Merged PR bulunca:
1. WALLET.json'da `balance` artır
2. `transactions` array'ine "income" entry ekle
3. CLAIMED_BOUNTIES.md'de durumu "merged" yap
4. Telegram'dan bildir: "PR #X merged! +$Y earned"

### Rejected/Closed PR bulunca:
1. CLAIMED_BOUNTIES.md'de durumu "rejected" yap
2. Sebebi öğren (PR comment'larını oku)
3. Aynı pattern'i tekrarlama

### 72+ saat bekleyen PR:
1. PR'a polite follow-up comment bırak
2. Telegram'dan owner'a mention at (gerekirse)

## 3. Periyodik Kontrol
- Her 3. cycle'da tüm open PR'ları kontrol et
- gh pr list çıktısını mind/RESEARCH_LOG.md'ye kaydet
- Stale PR'ları (7+ gün) close etmeyi düşün
