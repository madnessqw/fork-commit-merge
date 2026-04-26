---
name: curlsearch
description: Web search using curl + multiple search engines (DuckDuckGo, Google, Bing)
---

# Curl Search Skill

Web search using curl + multiple search engines. Lightweight alternative when dedicated search APIs are unavailable.

## Usage

```bash
bash /home/gokhan/UniverseCreator-otonom/skills/curlsearch/scripts/search.sh "search query" [engine] [max_results]
```

- `engine`: duckduckgo (default), google, bing, baidu
- `max_results`: 1-20 (default: 5)

## Examples

```bash
# DuckDuckGo search (default)
bash /home/gokhan/UniverseCreator-otonom/skills/curlsearch/scripts/search.sh "github bounty platform"

# Google search
bash /home/gokhan/UniverseCreator-otonom/skills/curlsearch/scripts/search.sh "AI developer tools" google 10

# Bing search
bash /home/gokhan/UniverseCreator-otonom/skills/curlsearch/scripts/search.sh "open source bounty" bing 5
```

## Requirements
- `curl` (pre-installed)
- `python3` (pre-installed)
