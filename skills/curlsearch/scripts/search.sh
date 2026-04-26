#!/bin/bash
# Multi-engine web search using curl
# Usage: bash search.sh "query" [engine] [max_results]

QUERY="$1"
ENGINE="${2:-duckduckgo}"
MAX="${3:-5}"

if [ -z "$QUERY" ]; then
  echo "Usage: bash search.sh \"query\" [duckduckgo|google|bing] [max_results]"
  exit 1
fi

# Sanitize input
QUERY=$(echo "$QUERY" | sed 's/[^a-zA-Z0-9 _\-\.~]//g')
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY', safe=''))")

case "$ENGINE" in
  duckduckgo|ddg)
    URL="https://html.duckduckgo.com/html/?q=${ENCODED}"
    ;;
  bing)
    URL="https://www.bing.com/search?q=${ENCODED}&count=${MAX}"
    ;;
  google)
    URL="https://www.google.com/search?q=${ENCODED}&num=${MAX}"
    ;;
  *)
    echo "Unknown engine: $ENGINE. Use: duckduckgo, google, bing"
    exit 1
    ;;
esac

RESULT=$(curl -sL "$URL" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  --max-time 10 2>/dev/null)

if [ -z "$RESULT" ]; then
  echo "{\"error\": \"No response from $ENGINE\"}"
  exit 1
fi

# Extract results using python
echo "$RESULT" | python3 -c "
import sys, re, json, html

data = sys.stdin.read()

# Remove scripts and styles
data = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL)
data = re.sub(r'<style[^>]*>.*?</style>', '', data, flags=re.DOTALL)

# Find links with titles
results = []
# Generic pattern for search results
links = re.findall(r'<a[^>]*href=\"(https?://[^\"]+)\"[^>]*>(.*?)</a>', data, re.DOTALL)
seen = set()
for url, title in links:
    title = re.sub(r'<[^>]+>', '', title).strip()
    title = html.unescape(title)
    if not title or len(title) < 5: continue
    if 'duckduckgo.com' in url or 'bing.com' in url or 'google.com' in url: continue
    if url in seen: continue
    seen.add(url)
    # DDG redirect
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if 'uddg' in params:
        url = urllib.parse.unquote(params['uddg'][0])
    results.append({'title': title[:120], 'url': url})
    if len(results) >= int('$MAX'): break

print(json.dumps({'engine': '$ENGINE', 'query': '$QUERY', 'count': len(results), 'results': results}, indent=2))
"
