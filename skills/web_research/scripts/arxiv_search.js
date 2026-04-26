#!/usr/bin/env node
// arXiv Makale Arama - API key gereksiz
// Kullanım: node arxiv_search.js "machine learning agent" [--max 5]

const https = require('https');

const query = process.argv[2];
const maxResults = parseInt(process.argv.find((a, i) => process.argv[i-1] === '--max') || '5');

if (!query) {
  console.error('Kullanım: node arxiv_search.js "arama sorgusu" [--max N]');
  process.exit(1);
}

const searchQuery = encodeURIComponent(query);
const apiUrl = `/api/query?search_query=all:${searchQuery}&start=0&max_results=${maxResults}&sortBy=relevance&sortOrder=descending`;

const options = {
  hostname: 'export.arxiv.org',
  path: apiUrl,
  method: 'GET',
  headers: {
    'User-Agent': 'UniverseCreator/1.0'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      // Parse XML response
      const results = [];
      const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
      let match;
      
      while ((match = entryRegex.exec(data)) !== null) {
        const entry = match[1];
        const title = (entry.match(/<title>([\s\S]*?)<\/title>/) || [])[1]?.replace(/\s+/g, ' ').trim();
        const summary = (entry.match(/<summary>([\s\S]*?)<\/summary>/) || [])[1]?.replace(/\s+/g, ' ').trim();
        const published = (entry.match(/<published>(.*?)<\/published>/) || [])[1];
        const idMatch = entry.match(/<id>(.*?)<\/id>/);
        const id = idMatch ? idMatch[1] : '';
        
        // Get authors
        const authors = [];
        const authorRegex = /<author>\s*<name>(.*?)<\/name>/g;
        let authorMatch;
        while ((authorMatch = authorRegex.exec(entry)) !== null) {
          authors.push(authorMatch[1]);
        }
        
        results.push({
          title,
          authors: authors.slice(0, 3).join(', ') + (authors.length > 3 ? ` +${authors.length - 3} more` : ''),
          published: published?.split('T')[0],
          url: id,
          summary: summary?.substring(0, 300) + (summary?.length > 300 ? '...' : '')
        });
      }
      
      console.log(JSON.stringify({ query, results_count: results.length, results }, null, 2));
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
