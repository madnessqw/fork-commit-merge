const crypto = require('crypto');

// In-memory rate limit store (edge-compatible, per-deployment)
const rateStore = new Map();

const CLEANUP_INTERVAL = 60_000; // Clean up every minute
setInterval(() => {
  const now = Date.now();
  for (const [key, data] of rateStore.entries()) {
    if (now - data.windowStart > 60_000) rateStore.delete(key);
  }
}, CLEANUP_INTERVAL);

function getRateKey(req) {
  // Priority: API key > IP > fallback
  const apiKey = req.headers['x-rateguard-key'] || req.headers['x-api-key'];
  if (apiKey) return `key:${apiKey}`;

  const forwarded = req.headers['x-forwarded-for'];
  if (forwarded) return `ip:${forwarded.split(',')[0].trim()}`;

  return `ip:unknown`;
}

function checkRateLimit(key, limit, windowMs) {
  const now = Date.now();
  let entry = rateStore.get(key);

  if (!entry || now - entry.windowStart > windowMs) {
    entry = { count: 0, windowStart: now };
    rateStore.set(key, entry);
  }

  entry.count++;
  const remaining = Math.max(0, limit - entry.count);
  const resetTime = entry.windowStart + windowMs;

  return {
    limited: entry.count > limit,
    count: entry.count,
    limit,
    remaining,
    resetAt: new Date(resetTime).toISOString(),
    retryAfter: entry.count > limit ? Math.ceil((resetTime - now) / 1000) : 0
  };
}

module.exports = async (req, res) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Default config
  const config = {
    limit: parseInt(req.headers['x-ratelimit-limit'] || '60'),
    windowMs: parseInt(req.headers['x-ratelimit-window'] || '60000'), // 1 minute
    key: getRateKey(req)
  };

  const result = checkRateLimit(config.key, config.limit, config.windowMs);

  // Set rate limit headers
  res.setHeader('X-RateGuard-Limit', config.limit);
  res.setHeader('X-RateGuard-Remaining', result.remaining);
  res.setHeader('X-RateGuard-Reset', result.resetAt);
  res.setHeader('X-RateGuard-Count', result.count);

  if (result.limited) {
    res.setHeader('Retry-After', result.retryAfter);
    res.writeHead(429, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      error: 'rate_limit_exceeded',
      message: `Too many requests. Limit: ${config.limit} per ${config.windowMs/1000}s`,
      retryAfter: result.retryAfter,
      limit: config.limit,
      remaining: 0
    }));
    return;
  }

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({
    allowed: true,
    limit: config.limit,
    remaining: result.remaining,
    resetAt: result.resetAt,
    key: config.key.substring(0, 20) + '...'
  }));
};
