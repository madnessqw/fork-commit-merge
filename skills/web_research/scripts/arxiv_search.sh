#!/bin/bash
# arXiv Makale Arama - API key gereksiz
# Kullanım: bash arxiv_search.sh "machine learning agent" [max_results]

QUERY="$1"
MAX="${2:-5}"

if [ -z "$QUERY" ]; then
  echo "Kullanım: bash arxiv_search.sh \"arama sorgusu\" [max_results]"
  exit 1
fi

ENCODED_QUERY=$(echo "$QUERY" | sed 's/ /+/g')
URL="https://export.arxiv.org/api/query?search_query=all:${ENCODED_QUERY}&start=0&max_results=${MAX}&sortBy=relevance&sortOrder=descending"

RESULT=$(curl -sL "$URL" 2>/dev/null)

if [ -z "$RESULT" ]; then
  echo '{"error": "No response from arXiv API"}'
  exit 1
fi

# Parse XML to simplified output
echo "$RESULT" | python3 -c "
import sys, re, json

data = sys.stdin.read()
entries = re.findall(r'<entry>(.*?)</entry>', data, re.DOTALL)
results = []
for e in entries:
    title = re.search(r'<title>(.*?)</title>', e, re.DOTALL)
    summary = re.search(r'<summary>(.*?)</summary>', e, re.DOTALL)
    published = re.search(r'<published>(.*?)</published>', e)
    aid = re.search(r'<id>(.*?)</id>', e)
    authors = re.findall(r'<name>(.*?)</name>', e)
    
    results.append({
        'title': ' '.join(title.group(1).split()) if title else '',
        'authors': ', '.join(authors[:3]) + (f' +{len(authors)-3} more' if len(authors) > 3 else ''),
        'published': published.group(1).split('T')[0] if published else '',
        'url': aid.group(1) if aid else '',
        'summary': (' '.join(summary.group(1).split()))[:300] + '...' if summary else ''
    })

print(json.dumps({'query': '$QUERY', 'results_count': len(results), 'results': results}, indent=2))
"
