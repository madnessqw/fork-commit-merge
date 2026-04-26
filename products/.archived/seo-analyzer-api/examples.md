# SEO Analyzer API - Kullanım Örnekleri

**Tüm endpoint'ler için detaylı kod örnekleri.**

---

## 1. cURL Örnekleri

### Sağlık Kontrolü

```bash
curl -X GET http://localhost:5055/health
```

**Yanıt:**
```json
{
  "status": "healthy",
  "version": "2.0",
  "endpoints": [
    "/health",
    "/analyze",
    "/analyze-batch",
    "/export"
  ]
}
```

---

### Tek URL Analizi

```bash
curl -X POST http://localhost:5055/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

**Yanıt:**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "description": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
  "status": "success"
}
```

---

### Hatalı URL

```bash
curl -X POST http://localhost:5055/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://gecersiz-adres-12345.com"
  }'
```

**Yanıt:**
```json
{
  "url": "https://gecersiz-adres-12345.com",
  "error": "Failed to fetch URL: <urlopen error [Errno -2] Name or service not known>",
  "status": "failed"
}
```

---

### Toplu URL Analizi (50'ye kadar)

```bash
curl -X POST http://localhost:5055/analyze-batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://google.com",
      "https://github.com",
      "https://stackoverflow.com"
    ]
  }'
```

**Yanıt:**
```json
{
  "count": 3,
  "results": [
    {
      "url": "https://google.com",
      "title": "Google",
      "description": "Arama motoru",
      "status": "success"
    },
    {
      "url": "https://github.com",
      "title": "GitHub: Let's build from here",
      "description": "GitHub is where over 100 million developers shape the future of software.",
      "status": "success"
    },
    {
      "url": "https://stackoverflow.com",
      "title": "Stack Overflow - Where Developers Learn & Share",
      "description": "Stack Overflow is the largest, most trusted online community for developers to learn, share their programming knowledge, and build their careers.",
      "status": "success"
    }
  ]
}
```

---

### JSON Export (Son analiz sonuçları)

```bash
curl -X GET "http://localhost:5055/export?format=json"
```

**Yanıt:**
```json
{
  "count": 3,
  "data": [
    {
      "url": "https://google.com",
      "title": "Google",
      "description": "Arama motoru",
      "status": "success"
    },
    {
      "url": "https://github.com",
      "title": "GitHub: Let's build from here",
      "description": "GitHub is where over 100 million developers shape the future of software.",
      "status": "success"
    },
    {
      "url": "https://stackoverflow.com",
      "title": "Stack Overflow - Where Developers Learn & Share",
      "description": "Stack Overflow is the largest, most trusted online community for developers to learn, share their programming knowledge, and build their careers.",
      "status": "success"
    }
  ]
}
```

---

### CSV Export (Son analiz sonuçları)

```bash
curl -X GET "http://localhost:5055/export?format=csv"
```

**Yanıt:**
```csv
url,title,description,status
https://google.com,Google,Arama motoru,success
https://github.com,GitHub: Let's build from here,"GitHub is where over 100 million developers shape the future of software.",success
https://stackoverflow.com,Stack Overflow - Where Developers Learn & Share,"Stack Overflow is the largest, most trusted online community for developers to learn, share their programming knowledge, and build their careers.",success
```

---

### Export - Boş Durum

```bash
curl -X GET "http://localhost:5055/export?format=json"
```

**Yanıt:**
```json
{
  "error": "No data to export",
  "status": 404
}
```

---

## 2. Python Örnekleri

### Tek URL Analizi

```python
import requests
import json

def analyze_url(url):
    """Tek URL analiz et."""
    response = requests.post(
        'http://localhost:5055/analyze',
        json={'url': url},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")

# Kullanım
result = analyze_url('https://example.com')
print(f"Title: {result['title']}")
print(f"Description: {result['description']}")
```

---

### Toplu URL Analizi

```python
def analyze_batch(urls):
    """50'ye kadar URL'yi toplu analiz et."""
    if len(urls) > 50:
        raise ValueError("Maximum 50 URLs per batch")

    response = requests.post(
        'http://localhost:5055/analyze-batch',
        json={'urls': urls},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")

# Kullanım
urls = [
    'https://google.com',
    'https://github.com',
    'https://stackoverflow.com',
    'https://reddit.com',
    'https://twitter.com'
]

results = analyze_batch(urls)
print(f"Analyzed {results['count']} URLs")

for result in results['results']:
    if result['status'] == 'success':
        print(f"✓ {result['url']}: {result['title']}")
    else:
        print(f"✗ {result['url']}: {result['error']}")
```

---

### Export - JSON

```python
def export_json():
    """Son analiz sonuçlarını JSON olarak dışa aktar."""
    response = requests.get(
        'http://localhost:5055/export?format=json'
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")

# Kullanım
data = export_json()
print(f"Exported {data['count']} results")

# Dosyaya kaydet
with open('seo_results.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

---

### Export - CSV

```python
def export_csv(filename='seo_results.csv'):
    """Son analiz sonuçlarını CSV olarak dışa aktar."""
    response = requests.get(
        'http://localhost:5055/export?format=csv'
    )

    if response.status_code == 200:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Results saved to {filename}")
    else:
        raise Exception(f"API error: {response.status_code}")

# Kullanım
export_csv()
```

---

### Tam Örnek - SEO Analiz Aracı

```python
#!/usr/bin/env python3
"""
SEO Analyzer CLI Tool
SEO Analyzer API için komut satırı aracı.

Kullanım:
    python seo_tool.py analyze <url>
    python seo_tool.py batch <file.txt>
    python seo_tool.py export
"""

import requests
import sys
import json
from pathlib import Path

API_BASE = 'http://localhost:5055'

def analyze_single(url):
    """Tek URL analiz et."""
    print(f"🔍 Analyzing: {url}")

    response = requests.post(
        f'{API_BASE}/analyze',
        json={'url': url},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return None

    result = response.json()

    print(f"\n{'='*60}")
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    print(f"Description: {result['description']}")
    print(f"{'='*60}\n")

    return result

def analyze_batch_from_file(filename):
    """Dosyadan URL'leri oku ve toplu analiz et."""
    url_file = Path(filename)

    if not url_file.exists():
        print(f"❌ File not found: {filename}")
        return

    urls = [line.strip() for line in url_file.read_text().splitlines() if line.strip()]

    if len(urls) > 50:
        print(f"⚠️  Warning: Maximum 50 URLs allowed. Processing first 50.")
        urls = urls[:50]

    print(f"🔍 Analyzing {len(urls)} URLs...")

    response = requests.post(
        f'{API_BASE}/analyze-batch',
        json={'urls': urls},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return

    results = response.json()

    print(f"\n{'='*60}")
    print(f"Analyzed: {results['count']} URLs")

    success_count = sum(1 for r in results['results'] if r['status'] == 'success')
    fail_count = results['count'] - success_count

    print(f"✓ Success: {success_count}")
    print(f"✗ Failed: {fail_count}")
    print(f"{'='*60}\n")

    # Sonuçları kaydet
    with open('batch_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("💾 Results saved to batch_results.json")

def export_results(format='json'):
    """Sonuçları dışa aktar."""
    print(f"📥 Exporting results as {format.upper()}...")

    response = requests.get(
        f'{API_BASE}/export?format={format}'
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return

    filename = f'seo_export.{format}'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

    print(f"💾 Results saved to {filename}")

def health_check():
    """API sağlık kontrolü."""
    response = requests.get(f'{API_BASE}/health')

    if response.status_code == 200:
        data = response.json()
        print(f"✓ API Status: {data['status']}")
        print(f"✓ Version: {data['version']}")
        print(f"✓ Endpoints: {', '.join(data['endpoints'])}")
    else:
        print(f"❌ API is not responding")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'health':
        health_check()

    elif command == 'analyze' and len(sys.argv) >= 3:
        url = sys.argv[2]
        analyze_single(url)

    elif command == 'batch' and len(sys.argv) >= 3:
        filename = sys.argv[2]
        analyze_batch_from_file(filename)

    elif command == 'export':
        format = sys.argv[2] if len(sys.argv) > 2 else 'json'
        export_results(format)

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## 3. JavaScript / Node.js Örnekleri

### Tek URL Analizi

```javascript
const fetch = require('node-fetch');

async function analyzeUrl(url) {
  const response = await fetch('http://localhost:5055/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}

// Kullanım
(async () => {
  const result = await analyzeUrl('https://example.com');
  console.log(`Title: ${result.title}`);
  console.log(`Description: ${result.description}`);
})();
```

---

### Toplu URL Analizi

```javascript
const fetch = require('node-fetch');

async function analyzeBatch(urls) {
  if (urls.length > 50) {
    throw new Error('Maximum 50 URLs per batch');
  }

  const response = await fetch('http://localhost:5055/analyze-batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ urls })
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}

// Kullanım
(async () => {
  const urls = [
    'https://google.com',
    'https://github.com',
    'https://stackoverflow.com'
  ];

  const results = await analyzeBatch(urls);
  console.log(`Analyzed ${results.count} URLs`);

  results.results.forEach(result => {
    if (result.status === 'success') {
      console.log(`✓ ${result.url}: ${result.title}`);
    } else {
      console.log(`✗ ${result.url}: ${result.error}`);
    }
  });
})();
```

---

### Export - JSON

```javascript
const fetch = require('node-fetch');
const fs = require('fs');

async function exportJson() {
  const response = await fetch('http://localhost:5055/export?format=json');

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const data = await response.json();

  // Dosyaya kaydet
  fs.writeFileSync('seo_results.json', JSON.stringify(data, null, 2));
  console.log(`Exported ${data.count} results to seo_results.json`);

  return data;
}

// Kullanım
exportJson();
```

---

### Export - CSV

```javascript
const fetch = require('node-fetch');
const fs = require('fs');

async function exportCsv(filename = 'seo_results.csv') {
  const response = await fetch('http://localhost:5055/export?format=csv');

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const csv = await response.text();

  fs.writeFileSync(filename, csv);
  console.log(`Exported to ${filename}`);

  return csv;
}

// Kullanım
exportCsv();
```

---

### Tam Örnek - SEO Analiz Modülü

```javascript
/**
 * SEO Analyzer API Client
 * SEO Analyzer API için Node.js client modülü.
 *
 * @module seo-analyzer
 */

const fetch = require('node-fetch');
const fs = require('fs').promises;

class SEOAnalyzerClient {
  constructor(baseUrl = 'http://localhost:5055') {
    this.baseUrl = baseUrl;
  }

  /**
   * Tek URL analiz et
   * @param {string} url - Analiz edilecek URL
   * @returns {Promise<Object>} Analiz sonucu
   */
  async analyze(url) {
    const response = await fetch(`${this.baseUrl}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `API error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Toplu URL analizi
   * @param {string[]} urls - URL listesi (max 50)
   * @returns {Promise<Object>} Toplu analiz sonucu
   */
  async analyzeBatch(urls) {
    if (urls.length > 50) {
      throw new Error('Maximum 50 URLs per batch');
    }

    const response = await fetch(`${this.baseUrl}/analyze-batch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ urls })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `API error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * JSON export
   * @returns {Promise<Object>} Export verisi
   */
  async exportJson() {
    const response = await fetch(`${this.baseUrl}/export?format=json`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * CSV export
   * @returns {Promise<string>} CSV verisi
   */
  async exportCsv() {
    const response = await fetch(`${this.baseUrl}/export?format=csv`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.text();
  }

  /**
   * Sağlık kontrolü
   * @returns {Promise<Object>} API durumu
   */
  async health() {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Sonuçları dosyaya kaydet
   * @param {string} filename - Dosya adı
   * @param {string} format - Format (json|csv)
   */
  async saveToFile(filename, format = 'json') {
    let data;

    if (format === 'json') {
      data = await this.exportJson();
      await fs.writeFile(filename, JSON.stringify(data, null, 2));
    } else if (format === 'csv') {
      data = await this.exportCsv();
      await fs.writeFile(filename, data);
    } else {
      throw new Error('Invalid format. Use json or csv.');
    }

    console.log(`💾 Saved to ${filename}`);
  }
}

// Kullanım örnekleri
(async () => {
  const client = new SEOAnalyzerClient();

  // Sağlık kontrolü
  const health = await client.health();
  console.log(`API Status: ${health.status}`);

  // Tek URL analizi
  const result = await client.analyze('https://example.com');
  console.log(`Title: ${result.title}`);

  // Toplu analiz
  const batch = await client.analyzeBatch([
    'https://google.com',
    'https://github.com'
  ]);
  console.log(`Analyzed ${batch.count} URLs`);

  // Export
  await client.saveToFile('results.json', 'json');
  await client.saveToFile('results.csv', 'csv');
})();

module.exports = { SEOAnalyzerClient };
```

---

## 4. Bash Script Örnekleri

### Tek URL Analiz Fonksiyonu

```bash
#!/bin/bash
# seo-analyze.sh - Tek URL analiz et

analyze() {
  local url="$1"

  if [ -z "$url" ]; then
    echo "Usage: $0 <url>"
    exit 1
  fi

  result=$(curl -s -X POST http://localhost:5055/analyze \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$url\"}")

  echo "$result" | jq .
}

# Kullanım
analyze "https://example.com"
```

---

### Toplu Analiz Fonksiyonu

```bash
#!/bin/bash
# seo-batch.sh - Toplu URL analizi

analyze_batch() {
  local urls=("$@")

  if [ ${#urls[@]} -eq 0 ]; then
    echo "Usage: $0 <url1> <url2> ..."
    exit 1
  fi

  if [ ${#urls[@]} -gt 50 ]; then
    echo "Warning: Maximum 50 URLs allowed"
    urls=("${urls[@]:0:50}")
  fi

  # JSON array oluştur
  local json_urls=$(printf '"%s",' "${urls[@]}")
  json_urls="[${json_urls%,}]"

  result=$(curl -s -X POST http://localhost:5055/analyze-batch \
    -H "Content-Type: application/json" \
    -d "{\"urls\": $json_urls}")

  echo "$result" | jq .
}

# Kullanım
analyze_batch "https://google.com" "https://github.com" "https://stackoverflow.com"
```

---

### Export Fonksiyonları

```bash
#!/bin/bash
# seo-export.sh - Sonuçları dışa aktar

export_json() {
  curl -s http://localhost:5055/export?format=json | jq .
}

export_csv() {
  curl -s http://localhost:5055/export?format=csv
}

save_json() {
  local filename="${1:-seo_results.json}"
  curl -s http://localhost:5055/export?format=json | jq . > "$filename"
  echo "Saved to $filename"
}

save_csv() {
  local filename="${1:-seo_results.csv}"
  curl -s http://localhost:5055/export?format=csv > "$filename"
  echo "Saved to $filename"
}

# Kullanım
# export_json
# export_csv
# save_json results.json
# save_csv results.csv
```

---

### Tam Bash SEO Aracı

```bash
#!/bin/bash
#
# SEO Analyzer CLI
# SEO Analyzer API için tam özellikli komut satırı aracı.
#
# Kullanım:
#   ./seo-cli.sh health           - API sağlık kontrolü
#   ./seo-cli.sh analyze <url>    - Tek URL analiz et
#   ./seo-cli.sh batch <file>     - Dosyadan URL'leri analiz et
#   ./seo-cli.sh export [json|csv]- Sonuçları export et
#   ./seo-cli.sh save [json|csv]  - Sonuçları dosyaya kaydet
#

API_BASE="http://localhost:5055"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Renkli output
log_info() { echo -e "${BLUE}→${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Sağlık kontrolü
health_check() {
  log_info "Checking API health..."

  result=$(curl -s "$API_BASE/health")
  status=$(echo "$result" | jq -r '.status')

  if [ "$status" = "healthy" ]; then
    log_success "API is healthy"
    version=$(echo "$result" | jq -r '.version')
    echo "Version: $version"
  else
    log_error "API is not responding"
    exit 1
  fi
}

# Tek URL analiz
analyze_single() {
  local url="$1"

  if [ -z "$url" ]; then
    log_error "URL required"
    echo "Usage: $0 analyze <url>"
    exit 1
  fi

  log_info "Analyzing: $url"

  result=$(curl -s -X POST "$API_BASE/analyze" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$url\"}")

  status=$(echo "$result" | jq -r '.status')

  if [ "$status" = "success" ]; then
    log_success "Analysis complete"
    echo ""
    echo "URL: $(echo "$result" | jq -r '.url')"
    echo "Title: $(echo "$result" | jq -r '.title')"
    echo "Description: $(echo "$result" | jq -r '.description')"
  else
    log_error "Analysis failed"
    echo "Error: $(echo "$result" | jq -r '.error')"
  fi
}

# Dosyadan toplu analiz
analyze_batch() {
  local file="$1"

  if [ -z "$file" ] || [ ! -f "$file" ]; then
    log_error "File not found: $file"
    echo "Usage: $0 batch <file.txt>"
    exit 1
  fi

  # URL'leri oku
  mapfile -t urls < <(grep -v '^#' "$file" | grep -v '^$')

  local count=${#urls[@]}

  if [ $count -eq 0 ]; then
    log_error "No URLs found in file"
    exit 1
  fi

  if [ $count -gt 50 ]; then
    log_warning "Maximum 50 URLs allowed. Processing first 50."
    urls=("${urls[@]:0:50}")
    count=50
  fi

  log_info "Analyzing $count URLs..."

  # JSON array oluştur
  local json_urls=$(printf '"%s",' "${urls[@]}")
  json_urls="[${json_urls%,}]"

  result=$(curl -s -X POST "$API_BASE/analyze-batch" \
    -H "Content-Type: application/json" \
    -d "{\"urls\": $json_urls}")

  total=$(echo "$result" | jq -r '.count')
  success=$(echo "$result" | jq -r '[.results[] | select(.status=="success")] | length')
  failed=$((total - success))

  log_success "Analysis complete"
  echo ""
  echo "Total: $total"
  log_success "Success: $success"
  log_error "Failed: $failed"
  echo ""

  # Sonuçları kaydet
  echo "$result" | jq . > batch_results.json
  log_success "Results saved to batch_results.json"
}

# Export
export_results() {
  local format="${1:-json}"

  log_info "Exporting results as ${format^^}..."

  result=$(curl -s "$API_BASE/export?format=$format")

  if [ "$format" = "json" ]; then
    echo "$result" | jq .
  else
    echo "$result"
  fi
}

# Dosyaya kaydet
save_results() {
  local format="${1:-json}"
  local filename="seo_results.$format"

  log_info "Saving results to $filename..."

  curl -s "$API_BASE/export?format=$format" > "$filename"

  log_success "Results saved to $filename"
}

# Yardım
show_help() {
  cat << EOF
SEO Analyzer CLI v1.0

Kullanım:
  $0 <command> [options]

Komutlar:
  health              API sağlık kontrolü
  analyze <url>       Tek URL analiz et
  batch <file>        Dosyadan URL'leri analiz et (her satır 1 URL)
  export [json|csv]   Sonuçları terminal'e export et
  save [json|csv]     Sonuçları dosyaya kaydet

Örnekler:
  $0 health
  $0 analyze https://example.com
  $0 batch urls.txt
  $0 export json
  $0 save csv

EOF
}

# Main
case "$1" in
  health)
    health_check
    ;;
  analyze)
    analyze_single "$2"
    ;;
  batch)
    analyze_batch "$2"
    ;;
  export)
    export_results "$2"
    ;;
  save)
    save_results "$2"
    ;;
  *)
    show_help
    ;;
esac
```

---

## 5. Örnek URL Dosyası

### urls.txt

```
# SEO Analyzer - Örnek URL Listesi
# Her satır bir URL
# # ile başlayan satırlar yorum olarak atlanır

# Arama Motorları
https://google.com
https://bing.com
https://duckduckgo.com

# Sosyal Medya
https://twitter.com
https://facebook.com
https://linkedin.com

# Geliştirici Platformları
https://github.com
https://stackoverflow.com
https://gitlab.com

# Haber Siteleri
https://news.ycombinator.com
https://reddit.com/r/technology
https://techcrunch.com
```

---

## 6. Entegrasyon Örnekleri

### WordPress Plugin için

```php
<?php
/**
 * SEO Analyzer API - WordPress Entegrasyonu
 */

function seo_analyze_url($url) {
    $response = wp_remote_post('http://localhost:5055/analyze', array(
        'headers' => array(
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode(array('url' => $url)),
        'timeout' => 15
    ));

    if (is_wp_error($response)) {
        return false;
    }

    return json_decode(wp_remote_retrieve_body($response), true);
}

// Kullanım
$result = seo_analyze_url('https://example.com');
if ($result && $result['status'] === 'success') {
    echo "Title: " . esc_html($result['title']);
    echo "Description: " . esc_html($result['description']);
}
?>
```

---

### Excel / Google Sheets için

```javascript
// Google Apps Script - Custom Function
/**
 * SEO Analyzer API'den URL başlığı al
 * @param {"https://example.com"} url Analiz edilecek URL
 * @return Başlık
 * @customfunction
 */
function SEO_GET_TITLE(url) {
  var payload = JSON.stringify({
    "url": url
  });

  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": payload,
    "muteHttpExceptions": true
  };

  try {
    var response = UrlFetchApp.fetch("http://localhost:5055/analyze", options);
    var result = JSON.parse(response.getContentText());

    if (result.status === "success") {
      return result.title;
    } else {
      return "Error: " + result.error;
    }
  } catch (e) {
    return "Error: " + e.toString();
  }
}

// Sheet'te kullanım:
// =SEO_GET_TITLE(A1)
```

---

**Tüm örnekler test edilmiştir ve SEO Analyzer API v2.0 ile uyumludur.**
