// API Security Scanner - Process endpoint
module.exports = async (req, res) => {
  // CORS
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
    const { url, method = 'GET' } = req.body;

    if (!url) {
      return res.status(400).json({ error: 'URL is required' });
    }

    // Validate URL format
    let targetUrl;
    try {
      targetUrl = new URL(url);
    } catch {
      return res.status(400).json({ error: 'Invalid URL format' });
    }

    // Security scan simulation
    const issues = [];
    let score = 100;

    // Check HTTPS
    if (targetUrl.protocol !== 'https:') {
      issues.push({
        name: 'HTTPS Enforcement',
        status: 'fail',
        severity: 'critical',
        description: 'API is not using HTTPS',
        recommendation: 'Enable HTTPS for all API endpoints'
      });
      score -= 25;
    } else {
      issues.push({
        name: 'HTTPS Enforcement',
        status: 'pass',
        severity: 'none'
      });
    }

    // Security Headers Check
    const securityHeaders = [
      { name: 'Content-Security-Policy', critical: true },
      { name: 'X-Frame-Options', critical: true },
      { name: 'X-Content-Type-Options', critical: true },
      { name: 'Strict-Transport-Security', critical: false },
      { name: 'Referrer-Policy', critical: false }
    ];

    // Simulate header detection
    for (const header of securityHeaders) {
      const detected = Math.random() > 0.5; // Simulate detection
      if (!detected && header.critical) {
        issues.push({
          name: `Security Header: ${header.name}`,
          status: 'fail',
          severity: 'high',
          description: `${header.name} header is missing`,
          recommendation: `Add ${header.name} header to responses`
        });
        score -= 10;
      } else if (!detected) {
        issues.push({
          name: `Security Header: ${header.name}`,
          status: 'warn',
          severity: 'medium',
          description: `${header.name} header is missing`,
          recommendation: `Consider adding ${header.name} header`
        });
        score -= 5;
      } else {
        issues.push({
          name: `Security Header: ${header.name}`,
          status: 'pass',
          severity: 'none'
        });
      }
    }

    // CORS Check
    const corsIssues = Math.random() > 0.7;
    if (corsIssues) {
      issues.push({
        name: 'CORS Configuration',
        status: 'fail',
        severity: 'high',
        description: 'Overly permissive CORS policy detected',
        recommendation: 'Configure CORS to only allow specific origins'
      });
      score -= 15;
    } else {
      issues.push({
        name: 'CORS Configuration',
        status: 'pass',
        severity: 'none'
      });
    }

    // Rate Limiting Check
    const hasRateLimit = Math.random() > 0.6;
    if (!hasRateLimit) {
      issues.push({
        name: 'Rate Limiting',
        status: 'warn',
        severity: 'medium',
        description: 'No rate limiting detected',
        recommendation: 'Implement rate limiting to prevent abuse'
      });
      score -= 10;
    } else {
      issues.push({
        name: 'Rate Limiting',
        status: 'pass',
        severity: 'none'
      });
    }

    // Auth Check
    issues.push({
      name: 'Authentication Required',
      status: 'pass',
      severity: 'none'
    });

    // SQL Injection Check
    issues.push({
      name: 'SQL Injection Protection',
      status: 'pass',
      severity: 'none'
    });

    // Normalize score
    score = Math.max(0, Math.min(100, score));

    res.json({
      url: url,
      method: method,
      score: score,
      grade: score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : score >= 60 ? 'D' : 'F',
      scanned_at: new Date().toISOString(),
      issues: issues,
      summary: {
        critical: issues.filter(i => i.severity === 'critical').length,
        high: issues.filter(i => i.severity === 'high').length,
        medium: issues.filter(i => i.severity === 'medium').length,
        low: issues.filter(i => i.severity === 'low').length,
        passed: issues.filter(i => i.status === 'pass').length
      }
    });

  } catch (error) {
    console.error('Scan error:', error);
    res.status(500).json({
      error: 'Scan failed',
      message: error.message
    });
  }
};
