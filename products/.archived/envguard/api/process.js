/**
 * EnvGuard API — Environment Variable Validator & Security Auditor
 * Validates .env files against schemas, detects security issues
 */

/** @type {import('@vercel/node').VercelApiHandler} */
module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { envContent, framework, strict } = req.body || {};

  if (!envContent || typeof envContent !== 'string') {
    return res.status(400).json({ error: 'envContent string is required' });
  }

  const parsed = parseEnv(envContent);
  const errors = [];
  const warnings = [];
  const securityIssues = [];
  const suggestions = [];

  // Check for empty values
  for (const [key, value] of Object.entries(parsed)) {
    if (value === '') {
      warnings.push({ key, message: `Empty value for ${key}` });
    }
  }

  // Detect exposed secrets
  const secretPatterns = {
    AWS_KEY: /^AKIA[0-9A-Z]{16}$/,
    PRIVATE_KEY: /-----BEGIN (RSA |EC )?PRIVATE KEY-----/,
    SLACK_TOKEN: /^xox[baprs]-/,
    GITHUB_TOKEN: /^gh[pousr]_[A-Za-z0-9_]{36,}$/,
    STRIPE_KEY: /^(sk|rk)_(live|test)_[A-Za-z0-9]{24,}$/,
    GOOGLE_KEY: /^AIza[0-9A-Za-z_-]{35}$/,
    SENDGRID_KEY: /^SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}$/,
  };

  for (const [key, value] of Object.entries(parsed)) {
    for (const [type, regex] of Object.entries(secretPatterns)) {
      if (regex.test(value)) {
        securityIssues.push({
          key,
          type,
          severity: type === 'PRIVATE_KEY' ? 'critical' : 'high',
          message: `Possible ${type.replace(/_/g, ' ')} detected in ${key}`,
        });
      }
    }
  }

  // Framework-specific required vars
  const frameworkRequired = {
    nextjs: ['DATABASE_URL', 'NEXTAUTH_SECRET', 'NEXTAUTH_URL'],
    express: ['PORT', 'NODE_ENV'],
    django: ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS'],
    rails: ['SECRET_KEY_BASE', 'RAILS_ENV', 'DATABASE_URL'],
    laravel: ['APP_KEY', 'APP_ENV', 'DB_CONNECTION'],
  };

  if (framework && frameworkRequired[framework]) {
    for (const required of frameworkRequired[framework]) {
      if (!(required in parsed)) {
        errors.push({ key: required, message: `Required ${framework} variable missing: ${required}` });
      }
    }
  }

  // Strict mode checks
  if (strict) {
    for (const [key, value] of Object.entries(parsed)) {
      if (value.includes(' ') && !value.startsWith('"') && !value.startsWith("'")) {
        errors.push({ key, message: `Value for ${key} contains spaces, should be quoted` });
      }
    }
  }

  // Suggestions
  const keyNames = Object.keys(parsed);
  if (!keyNames.some(k => k.includes('NODE_ENV') || k.includes('ENV'))) {
    suggestions.push('Consider adding NODE_ENV for environment distinction');
  }
  if (!keyNames.some(k => k.includes('LOG'))) {
    suggestions.push('Consider adding a LOG_LEVEL variable');
  }
  if (keyNames.length < 3) {
    suggestions.push('Very few environment variables — ensure all config is externalized');
  }

  const score = calculateScore(errors, warnings, securityIssues);

  return res.status(200).json({
    valid: errors.length === 0 && securityIssues.filter(i => i.severity === 'critical').length === 0,
    score,
    total: keyNames.length,
    errors,
    warnings,
    securityIssues,
    suggestions,
    summary: {
      errors: errors.length,
      warnings: warnings.length,
      securityIssues: securityIssues.length,
      critical: securityIssues.filter(i => i.severity === 'critical').length,
      high: securityIssues.filter(i => i.severity === 'high').length,
    },
  });
};

function parseEnv(content) {
  const result = {};
  const lines = content.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIndex = trimmed.indexOf('=');
    if (eqIndex === -1) continue;
    const key = trimmed.substring(0, eqIndex).trim();
    let value = trimmed.substring(eqIndex + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }
  return result;
}

function calculateScore(errors, warnings, securityIssues) {
  let score = 100;
  score -= errors.length * 15;
  score -= warnings.length * 5;
  score -= securityIssues.filter(i => i.severity === 'critical').length * 25;
  score -= securityIssues.filter(i => i.severity === 'high').length * 10;
  return Math.max(0, Math.min(100, score));
}
