---
name: web_research
description: Web araması ve URL içerik okuma — DuckDuckGo (ddgr), Jina Reader, arXiv
---

# Web Research Skill

UniverseCreator'a web araması ve içerik okuma yeteneği kazandırır. **Hiçbir API key gerekmez.**

## 1. Web Arama (ddgr — ANA ARAÇ)

```bash
ddgr --json -n 5 "arama sorgusu"
```

| Parametre | Açıklama |
|-----------|----------|
| `--json` | JSON formatında çıktı (zorunlu) |
| `-n 5` | Sonuç sayısı (varsayılan 10) |
| `-w example.com` | Belirli bir siteye kısıtla |
| `--noprompt` | İnteraktif mod kapalı (script için) |

### Örnek Kullanımlar
```bash
# Bounty arama
ddgr --json -n 10 "github bounty open issues reward"

# Platform keşfi
ddgr --json -n 5 "algora open source bounties"
ddgr --json -n 5 "gitcoin bounties developer"
ddgr --json -n 5 "onlydust contributions reward"

# Rakip analizi
ddgr --json -n 5 "AI developer tools trending 2026"

# Teknoloji araştırma
ddgr --json -n 5 "best practices code review automation"

# Site-spesifik arama
ddgr --json -n 5 -w github.com "good first issue bounty label:bounty"
```

### JSON Çıktı Formatı
```json
[
  {
    "abstract": "Sayfa özeti...",
    "title": "Başlık",
    "url": "https://example.com/page"
  }
]
```

## 2. URL İçerik Okuma (Jina Reader)

URL'yi markdown'a çevirir. API key gereksiz.

```bash
# Basit kullanım
curl -s "https://r.jina.ai/https://example.com" | head -200

# Spesifik bir bounty sayfasını oku
curl -s "https://r.jina.ai/https://github.com/OWNER/REPO/issues/123" | head -300
```

## 3. Akademik Arama (arXiv)

```bash
# arXiv API ile makale ara (API key gereksiz)
curl -s "http://export.arxiv.org/api/query?search_query=all:autonomous+agents&max_results=5" | head -200
```

## 4. Curl ile Direkt Sayfa Çekme

```bash
# GitHub API (rate limited ama auth gereksiz)
curl -s "https://api.github.com/search/issues?q=label:bounty+state:open&per_page=5"

# GitHub trending
curl -s "https://r.jina.ai/https://github.com/trending" | head -200
```

## 5. Araştırma Kayıt Protokolü

Her araştırma sonucunu kaydet:
```bash
echo "## $(date +%Y-%m-%d) Araştırma" >> mind/RESEARCH_LOG.md
echo "- Sorgu: [sorgu]" >> mind/RESEARCH_LOG.md
echo "- Sonuçlar: [özet]" >> mind/RESEARCH_LOG.md
echo "- Aksiyon: [ne yapılacak]" >> mind/RESEARCH_LOG.md
```
