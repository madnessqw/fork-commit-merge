// JSON Formatter Pro - API Endpoint
// POST /api/process - Format, validate, minify JSON

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Handle GET request - return health info
  if (req.method === 'GET') {
    return res.status(200).json({
      status: 'ok',
      service: 'JSON Formatter Pro API',
      version: '1.0.0',
      endpoints: {
        POST: '/api/process - Format, validate, minify JSON',
        GET: '/api/health - Health check'
      },
      features: [
        'format/beautify JSON',
        'validate JSON',
        'minify JSON',
        'syntax highlight info',
        'stats (chars, lines, depth)'
      ]
    });
  }

  // Handle POST request
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { input, action } = req.body;

    if (!input || typeof input !== 'string') {
      return res.status(400).json({
        error: 'Missing or invalid input',
        message: 'Please provide JSON string in "input" field'
      });
    }

    const actionType = action || 'format';

    let result;
    let success = true;
    let error = null;

    switch (actionType) {
      case 'format':
      case 'beautify':
        try {
          const parsed = JSON.parse(input);
          result = JSON.stringify(parsed, null, 2);
        } catch (e) {
          success = false;
          error = `Invalid JSON: ${e.message}`;
          result = null;
        }
        break;

      case 'minify':
        try {
          const parsed = JSON.parse(input);
          result = JSON.stringify(parsed);
        } catch (e) {
          success = false;
          error = `Invalid JSON: ${e.message}`;
          result = null;
        }
        break;

      case 'validate':
        try {
          JSON.parse(input);
          result = { valid: true, message: 'Valid JSON' };
        } catch (e) {
          result = { valid: false, error: e.message };
          success = false;
        }
        break;

      case 'stats':
        try {
          const parsed = JSON.parse(input);
          result = {
            valid: true,
            chars: input.length,
            lines: input.split('\n').length,
            sizeKB: (input.length / 1024).toFixed(2),
            depth: getMaxDepth(parsed),
            keys: countKeys(parsed),
            type: Array.isArray(parsed) ? 'array' : 'object'
          };
        } catch (e) {
          success = false;
          error = `Invalid JSON: ${e.message}`;
          result = null;
        }
        break;

      default:
        return res.status(400).json({
          error: 'Invalid action',
          message: 'Valid actions: format, beautify, minify, validate, stats'
        });
    }

    return res.status(200).json({
      success,
      action: actionType,
      result,
      error,
      timestamp: new Date().toISOString()
    });

  } catch (err) {
    return res.status(500).json({
      error: 'Internal server error',
      message: err.message
    });
  }
}

function getMaxDepth(obj, depth = 0) {
  if (obj === null || typeof obj !== 'object') return depth;
  let max = depth;
  for (const key in obj) {
    max = Math.max(max, getMaxDepth(obj[key], depth + 1));
  }
  return max;
}

function countKeys(obj, count = 0) {
  if (obj === null || typeof obj !== 'object') return count;
  if (Array.isArray(obj)) {
    for (const item of obj) {
      count = countKeys(item, count);
    }
  } else {
    for (const key in obj) {
      count++;
      count = countKeys(obj[key], count);
    }
  }
  return count;
}