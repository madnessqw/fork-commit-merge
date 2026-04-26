export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { config } = req.body;
    if (!config) {
      return res.status(400).json({ error: 'Configuration is required' });
    }

    const issues = [];
    const recommendations = [];

    // Basic syntax checks
    if (!config.includes('server {')) {
      issues.push({ type: 'error', message: 'No server block found' });
    }

    if (config.includes('ssl on') && !config.includes('listen 443')) {
      recommendations.push({ type: 'warning', message: 'Consider using "listen 443 ssl" instead of "ssl on"' });
    }

    if (!config.includes('server_tokens')) {
      recommendations.push({ type: 'security', message: 'Add "server_tokens off;" to hide Nginx version' });
    }

    if (!config.includes('X-Frame-Options')) {
      recommendations.push({ type: 'security', message: 'Add X-Frame-Options header to prevent clickjacking' });
    }

    if (config.includes('root') && !config.includes('try_files')) {
      recommendations.push({ type: 'performance', message: 'Consider adding try_files for better error handling' });
    }

    // SSL checks
    if (config.includes('listen 443 ssl')) {
      if (!config.includes('ssl_protocols')) {
        recommendations.push({ type: 'security', message: 'Specify ssl_protocols to disable older TLS versions' });
      }
      if (!config.includes('ssl_ciphers')) {
        recommendations.push({ type: 'security', message: 'Configure strong SSL ciphers' });
      }
    }

    const valid = issues.length === 0;

    res.json({
      valid,
      issues,
      recommendations,
      stats: {
        lines: config.split('\n').length,
        serverBlocks: (config.match(/server\s*\{/g) || []).length,
        locationBlocks: (config.match(/location\s+/g) || []).length
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    res.status(500).json({ error: 'Failed to validate config', message: error.message });
  }
}
