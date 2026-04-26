---
name: ddg-web-search
description: Web search without API key using DuckDuckGo Lite via web_fetch
---

# DuckDuckGo Search via web_fetch

Search the web using DuckDuckGo Lite's HTML interface, parsed via `web_fetch`. No API key or package install required.

## How to Search

```
web_fetch(url="https://lite.duckduckgo.com/lite/?q=QUERY", extractMode="text", maxChars=8000)
```

- URL-encode the query — use `+` for spaces
- Use `extractMode="text"` (not markdown) for clean results
- Increase `maxChars` for more results

## Region Filtering
Append `&kl=REGION` for regional results:
- `us-en` — United States
- `uk-en` — United Kingdom
- `de-de` — Germany
- `tr-tr` — Turkey

### Example — US search
```
web_fetch(url="https://lite.duckduckgo.com/lite/?q=best+bounty+platforms&kl=us-en", extractMode="text", maxChars=8000)
```

## Search-then-Fetch Pattern
1. **Search** — query DDG Lite for results
2. **Pick** — identify most relevant URLs
3. **Fetch** — use `web_fetch` on URLs to read full content

## Tips
- First 1-2 results may be ads — skip to organic results
- For exact phrases: `q=%22exact+phrase%22`
- Google search does NOT work via web_fetch (captcha blocked)
