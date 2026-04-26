#!/usr/bin/env python3
"""
SEO Analyzer API v2.0
Extracts meta tags (title, description) from any URL via HTTP API.

Endpoints:
- GET /health - Health check
- POST /analyze - Single URL analysis
- POST /analyze-batch - Multiple URLs (up to 50)
- GET /export?format=json|csv - Export last analysis results

Usage:
    python seo_analyzer.py
    API runs on http://localhost:5055
"""

import json
import re
import csv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from io import StringIO

# In-memory cache for last results (for export endpoint)
_last_results = []

class SEOAnalyzer:
    """Core SEO analysis logic."""

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SEOAnalyzer/2.0)'
        }

    def fetch_url(self, url):
        """Fetch HTML content from URL."""
        try:
            req = Request(url, headers=self.headers)
            with urlopen(req, timeout=self.timeout) as response:
                return response.read().decode('utf-8', errors='ignore')
        except (URLError, HTTPError) as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")

    def extract_title(self, html):
        """Extract page title from HTML."""
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def extract_description(self, html):
        """Extract meta description from HTML."""
        match = re.search(
            r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']',
            html, re.IGNORECASE
        )
        if match:
            return match.group(1).strip()

        # Try alternate syntax
        match = re.search(
            r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']',
            html, re.IGNORECASE
        )
        return match.group(1).strip() if match else None

    def analyze(self, url):
        """Analyze single URL and return meta tags."""
        html = self.fetch_url(url)
        return {
            'url': url,
            'title': self.extract_title(html),
            'description': self.extract_description(html),
            'status': 'success'
        }

    def analyze_batch(self, urls):
        """Analyze multiple URLs."""
        results = []
        for url in urls:
            try:
                result = self.analyze(url)
                results.append(result)
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'status': 'failed'
                })
        return results


class APIHandler(BaseHTTPRequestHandler):
    """HTTP API request handler."""

    analyzer = SEOAnalyzer()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def send_json(self, data, status=200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_json({
                'status': 'healthy',
                'version': '2.0',
                'endpoints': ['/health', '/analyze', '/analyze-batch', '/export']
            })

        elif self.path.startswith('/export'):
            # Parse query params
            from urllib.parse import parse_qs, urlparse
            params = parse_qs(urlparse(self.path).query)
            fmt = params.get('format', ['json'])[0].lower()

            if fmt == 'csv':
                if not _last_results:
                    self.send_json({'error': 'No data to export'}, 404)
                    return

                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=['url', 'title', 'description', 'status'])
                writer.writeheader()
                writer.writerows(_last_results)

                self.send_response(200)
                self.send_header('Content-Type', 'text/csv')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(output.getvalue().encode())
            else:
                self.send_json({
                    'count': len(_last_results),
                    'data': _last_results
                })

        else:
            self.send_json({
                'error': 'Not found',
                'endpoints': {
                    'GET /health': 'Health check',
                    'GET /export?format=json|csv': 'Export last results'
                }
            }, 404)

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, 400)
            return

        if self.path == '/analyze':
            url = data.get('url')
            if not url:
                self.send_json({'error': 'Missing "url" field'}, 400)
                return

            try:
                result = self.analyzer.analyze(url)
                _last_results.clear()
                _last_results.append(result)
                self.send_json(result)
            except Exception as e:
                self.send_json({'url': url, 'error': str(e), 'status': 'failed'}, 400)

        elif self.path == '/analyze-batch':
            urls = data.get('urls', [])
            if not urls:
                self.send_json({'error': 'Missing "urls" array'}, 400)
                return

            if len(urls) > 50:
                self.send_json({'error': 'Maximum 50 URLs per batch'}, 400)
                return

            results = self.analyzer.analyze_batch(urls)
            _last_results.clear()
            _last_results.extend(results)

            self.send_json({
                'count': len(results),
                'results': results
            })

        else:
            self.send_json({
                'error': 'Not found',
                'endpoints': {
                    'POST /analyze': 'Analyze single URL',
                    'POST /analyze-batch': 'Analyze multiple URLs (max 50)'
                }
            }, 404)


def run_server(port=5055):
    """Start the API server."""
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    print(f"🚀 SEO Analyzer API v2.0")
    print(f"📡 Running on http://localhost:{port}")
    print(f"📝 Endpoints:")
    print(f"   GET  /health        - Health check")
    print(f"   POST /analyze       - Single URL analysis")
    print(f"   POST /analyze-batch - Batch analysis (up to 50 URLs)")
    print(f"   GET  /export        - Export results (JSON/CSV)")
    print(f"\n⏹️  Press Ctrl+C to stop")
    server.serve_forever()


if __name__ == '__main__':
    run_server()
