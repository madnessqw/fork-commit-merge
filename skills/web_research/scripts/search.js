#!/usr/bin/env node
// DuckDuckGo Web Search - API key gereksiz
// Kullanım: node search.js "arama sorgusu" --max 10

const https = require('https');
const querystring = require('querystring');

const query = process.argv[2];
const maxResults = parseInt(process.argv.find((a, i) => process.argv[i-1] === '--max') || '5');

if (!query) {
  console.error('Kullanım: node search.js "arama sorgusu" [--max N]');
  process.exit(1);
}

// DuckDuckGo HTML lite endpoint - ücretsiz ve API key gereksiz
const searchUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;

const options = {
  hostname: 'html.duckduckgo.com',
  path: `/html/?q=${encodeURIComponent(query)}`,
  method: 'GET',
  headers: {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      // Parse HTML results
      const results = [];
      const titleRegex = /<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gs;
      const snippetRegex = /<a[^>]*class="result__snippet"[^>]*>(.*?)<\/a>/gs;
      
      let titleMatch;
      const titles = [];
      const urls = [];
      while ((titleMatch = titleRegex.exec(data)) !== null && titles.length < maxResults) {
        let url = titleMatch[1];
        // DuckDuckGo redirects through uddg parameter
        const uddgMatch = url.match(/uddg=([^&]*)/);
        if (uddgMatch) {
          url = decodeURIComponent(uddgMatch[1]);
        }
        titles.push(titleMatch[2].replace(/<[^>]*>/g, '').trim());
        urls.push(url);
      }
      
      let snippetMatch;
      const snippets = [];
      while ((snippetMatch = snippetRegex.exec(data)) !== null && snippets.length < maxResults) {
        snippets.push(snippetMatch[1].replace(/<[^>]*>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').trim());
      }
      
      for (let i = 0; i < titles.length; i++) {
        results.push({
          position: i + 1,
          title: titles[i],
          url: urls[i],
          snippet: snippets[i] || ''
        });
      }
      
      if (results.length === 0) {
        console.log(JSON.stringify({ query, error: 'No results found', raw_length: data.length }));
      } else {
        console.log(JSON.stringify({ query, results_count: results.length, results }, null, 2));
      }
    } catch (e) {
      console.error('Parse error:', e.message);
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('Request error:', e.message);
  process.exit(1);
});

req.end();
