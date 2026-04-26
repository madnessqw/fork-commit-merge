---
name: exa-web-search-free
description: Free AI search via Exa MCP - web, code, company research. No API key needed.
---

# Exa Web Search (Free)

Neural search for web, code, and company research via Exa MCP. No API key required.

## Setup
Verify mcporter is configured:
```
mcporter list exa
```

If not listed:
```
mcporter config add exa https://mcp.exa.ai/mcp
```

## Core Tools

### Web Search
```
mcporter call 'exa.web_search_exa(query: "latest AI news 2026", numResults: 5)'
```
- `query` — Search query
- `numResults` (optional, default: 8)
- `type` (optional) — "auto", "fast", or "deep"

### Code Search
```
mcporter call 'exa.get_code_context_exa(query: "React hooks examples", tokensNum: 3000)'
```
- `query` — Code/API search query
- `tokensNum` (optional, default: 5000)

### Company Research
```
mcporter call 'exa.company_research_exa(companyName: "Anthropic", numResults: 3)'
```

## Tips
- Use `type: "fast"` for quick lookup, `"deep"` for thorough research
- Code: Lower `tokensNum` (1000-2000) for focused, higher (5000+) for comprehensive
