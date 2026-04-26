#!/bin/bash
# URL İçerik Okuma - curl ile web sayfası markdown'a çevirir
# Kullanım: bash read_url.sh "https://example.com" [max_chars]

URL="$1"
MAX_CHARS="${2:-8000}"

if [ -z "$URL" ]; then
  echo "Kullanım: bash read_url.sh \"https://example.com\" [max_chars]"
  exit 1
fi

# Method 1: Try Jina Reader
CONTENT=$(curl -sL "https://r.jina.ai/${URL}" -H "Accept: text/plain" -H "User-Agent: UniverseCreator/1.0" --max-time 15 2>/dev/null)

# Method 2: Fallback to direct curl + html2text
if [ -z "$CONTENT" ] || [ ${#CONTENT} -lt 100 ]; then
  CONTENT=$(curl -sL "$URL" -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" --max-time 15 2>/dev/null | \
    python3 -c "
import sys, re, html
data = sys.stdin.read()
# Remove scripts, styles
data = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL)
data = re.sub(r'<style[^>]*>.*?</style>', '', data, flags=re.DOTALL)
# Remove tags
data = re.sub(r'<[^>]+>', ' ', data)
# Clean whitespace
data = re.sub(r'\s+', ' ', data).strip()
data = html.unescape(data)
print(data)
" 2>/dev/null)
fi

if [ -z "$CONTENT" ]; then
  echo "Error: Could not fetch content from $URL"
  exit 1
fi

# Truncate if too long
if [ ${#CONTENT} -gt $MAX_CHARS ]; then
  echo "${CONTENT:0:$MAX_CHARS}"
  echo ""
  echo "--- [TRUNCATED: ${#CONTENT} chars total, showing first ${MAX_CHARS}] ---"
else
  echo "$CONTENT"
fi
