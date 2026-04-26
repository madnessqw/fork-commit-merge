#!/usr/bin/env node
// Jina Reader - URL'yi temiz markdown'a çevirir
// API key gereksiz, tamamen ücretsiz
// Kullanım: node read_url.js "https://example.com"

const https = require('https');

const url = process.argv[2];
if (!url) {
  console.error('Kullanım: node read_url.js "https://example.com"');
  process.exit(1);
}

const jinaUrl = `https://r.jina.ai/${url}`;

const options = {
  hostname: 'r.jina.ai',
  path: `/${url}`,
  method: 'GET',
  headers: {
    'Accept': 'text/plain',
    'User-Agent': 'UniverseCreator/1.0'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200) {
      // Truncate if too long (save tokens)
      const maxChars = 8000;
      if (data.length > maxChars) {
        console.log(data.substring(0, maxChars));
        console.log(`\n--- [TRUNCATED: ${data.length} chars total, showing first ${maxChars}] ---`);
      } else {
        console.log(data);
      }
    } else {
      console.error(`Error: HTTP ${res.statusCode}`);
      console.error(data.substring(0, 500));
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('Request error:', e.message);
  process.exit(1);
});

req.setTimeout(15000, () => {
  console.error('Request timeout (15s)');
  req.destroy();
  process.exit(1);
});

req.end();
