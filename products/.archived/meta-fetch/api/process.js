const cheerio = require('cheerio');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();

  const { url } = req.query;
  if (!url) {
    return res.status(400).json({ error: 'URL is required. Use ?url=...' });
  }

  // Basic URL validation
  let targetUrl;
  try {
    targetUrl = new URL(url.startsWith('http') ? url : `https://${url}`);
  } catch (e) {
    return res.status(400).json({ error: 'Invalid URL format' });
  }

  try {
    // Use jina.ai as proxy to fetch content (bypasses Vercel outbound restrictions)
    const jinaUrl = `https://r.jina.ai/${targetUrl.toString()}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    const response = await fetch(jinaUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; MetaFetch/1.0)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      },
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (!response.ok) {
      return res.status(response.status).json({ error: `Failed to fetch: ${response.status}` });
    }

    const html = await response.text();
    const $ = cheerio.load(html);

    // Extract title
    const title = $('title').text().trim() ||
      $('meta[property="og:title"]').attr('content') ||
      $('meta[name="twitter:title"]').attr('content') || '';

    // Extract description
    const description = $('meta[name="description"]').attr('content') ||
      $('meta[property="og:description"]').attr('content') ||
      $('meta[name="twitter:description"]').attr('content') || '';

    // Extract favicon
    let favicon = $('link[rel="icon"]').attr('href') ||
      $('link[rel="shortcut icon"]').attr('href') ||
      $('link[rel="apple-touch-icon"]').attr('href') ||
      '/favicon.ico';

    // Resolve relative favicon URLs
    if (favicon && !favicon.startsWith('http')) {
      favicon = new URL(favicon, targetUrl.origin).toString();
    }

    // Extract Open Graph data
    const ogTitle = $('meta[property="og:title"]').attr('content') || title;
    const ogDescription = $('meta[property="og:description"]').attr('content') || description;
    const ogImage = $('meta[property="og:image"]').attr('content');
    const ogUrl = $('meta[property="og:url"]').attr('content');
    const ogType = $('meta[property="og:type"]').attr('content');
    const siteName = $('meta[property="og:site_name"]').attr('content');

    // Resolve relative OG image URLs
    let resolvedOgImage = ogImage;
    if (ogImage && !ogImage.startsWith('http')) {
      resolvedOgImage = new URL(ogImage, targetUrl.origin).toString();
    }

    // Extract Twitter Card data
    const twitterCard = $('meta[name="twitter:card"]').attr('content') || 'summary';
    const twitterTitle = $('meta[name="twitter:title"]').attr('content') || title;
    const twitterDescription = $('meta[name="twitter:description"]').attr('content') || description;
    const twitterImage = $('meta[name="twitter:image"]').attr('content');
    const twitterSite = $('meta[name="twitter:site"]').attr('content');

    // Resolve relative Twitter image URLs
    let resolvedTwitterImage = twitterImage;
    if (twitterImage && !twitterImage.startsWith('http')) {
      resolvedTwitterImage = new URL(twitterImage, targetUrl.origin).toString();
    }

    // Extract other meta tags
    const author = $('meta[name="author"]').attr('content') ||
      $('meta[property="article:author"]').attr('content');
    const published = $('meta[property="article:published_time"]').attr('content');

    // Extract all images
    const images = [];
    $('img').each((i, el) => {
      if (i >= 20) return; // Limit to 20 images
      const src = $(el).attr('src') || $(el).attr('data-src');
      if (src) {
        let resolvedSrc = src;
        if (!src.startsWith('http')) {
          try {
            resolvedSrc = new URL(src, targetUrl.origin).toString();
          } catch (e) {
            return;
          }
        }
        if (!images.includes(resolvedSrc)) {
          images.push(resolvedSrc);
        }
      }
    });

    // Extract theme color
    const themeColor = $('meta[name="theme-color"]').attr('content');

    // Build response
    const result = {
      url: targetUrl.toString(),
      title,
      description,
      favicon,
      ogTitle,
      ogDescription,
      ogImage: resolvedOgImage,
      ogUrl: ogUrl || targetUrl.toString(),
      ogType,
      siteName,
      twitterCard,
      twitterTitle,
      twitterDescription,
      twitterImage: resolvedTwitterImage,
      twitterSite,
      author,
      published,
      images: images.slice(0, 10),
      themeColor,
      cached: false,
    };

    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json({
      error: 'Failed to extract metadata',
      message: error.message,
    });
  }
};