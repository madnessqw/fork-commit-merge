export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { action, token, secret, algorithm } = req.body;

  try {
    switch (action) {
      case 'decode': {
        const decoded = decodeJWT(token);
        return res.json({ success: true, decoded });
      }

      case 'verify': {
        const verified = verifyJWT(token, secret);
        return res.json({ success: true, verified });
      }

      case 'analyze': {
        const analysis = analyzeJWT(token);
        return res.json({ success: true, analysis });
      }

      case 'generate': {
        const { payload, header } = req.body;
        const newToken = generateJWT(payload, secret, algorithm || 'HS256', header);
        return res.json({ success: true, token: newToken });
      }

      default:
        return res.status(400).json({ error: 'Unknown action. Use: decode, verify, analyze, generate' });
    }
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
}

function decodeJWT(token) {
  if (!token) throw new Error('Token is required');

  const parts = token.split('.');
  if (parts.length !== 3) throw new Error('Invalid JWT format - expected 3 parts');

  const header = JSON.parse(base64UrlDecode(parts[0]));
  const payload = JSON.parse(base64UrlDecode(parts[1]));
  const signature = parts[2];

  return { header, payload, signature };
}

function verifyJWT(token, secret) {
  const decoded = decodeJWT(token);

  // Comprehensive validation checks
  const issues = [];
  const warnings = [];
  const now = Math.floor(Date.now() / 1000);

  // Expiration check
  if (decoded.payload.exp) {
    const expDate = new Date(decoded.payload.exp * 1000);
    if (decoded.payload.exp < now) {
      issues.push(`Token expired on ${expDate.toISOString()}`);
    } else {
      const timeLeft = decoded.payload.exp - now;
      if (timeLeft < 3600) warnings.push(`Token expires in ${Math.floor(timeLeft / 60)} minutes`);
    }
  } else {
    warnings.push('Token has no expiration (exp claim)');
  }

  // Not before check
  if (decoded.payload.nbf && decoded.payload.nbf > now) {
    issues.push(`Token not valid until ${new Date(decoded.payload.nbf * 1000).toISOString()}`);
  }

  // Issued at check
  if (decoded.payload.iat && decoded.payload.iat > now) {
    issues.push('Token issued in the future');
  }

  // Algorithm security checks
  const alg = decoded.header.alg;
  if (alg === 'none') {
    issues.push('CRITICAL: Insecure algorithm "none" detected');
  }
  if (alg === 'HS256' && secret && secret.length < 32) {
    warnings.push('HS256 secret should be at least 32 characters for security');
  }

  // Check for sensitive claims
  const sensitiveClaims = ['password', 'ssn', 'credit_card', 'cvv', 'secret'];
  const payloadKeys = Object.keys(decoded.payload).map(k => k.toLowerCase());
  for (const claim of sensitiveClaims) {
    if (payloadKeys.some(k => k.includes(claim))) {
      warnings.push(`Potentially sensitive claim detected: ${claim}`);
    }
  }

  return {
    valid: issues.length === 0,
    issues,
    warnings,
    decoded,
    algorithm: alg,
    expiresAt: decoded.payload.exp ? new Date(decoded.payload.exp * 1000).toISOString() : null,
    issuedAt: decoded.payload.iat ? new Date(decoded.payload.iat * 1000).toISOString() : null
  };
}

function analyzeJWT(token) {
  const decoded = decodeJWT(token);
  const verified = verifyJWT(token);

  // Algorithm analysis
  const algStrength = {
    'none': 'critical',
    'HS256': 'medium',
    'HS384': 'medium',
    'HS512': 'strong',
    'RS256': 'strong',
    'RS384': 'strong',
    'RS512': 'strong',
    'ES256': 'strong',
    'ES384': 'strong',
    'ES512': 'strong'
  };

  return {
    decoded,
    security: {
      algorithm: decoded.header.alg,
      algorithmStrength: algStrength[decoded.header.alg] || 'unknown',
      hasExpiration: !!decoded.payload.exp,
      hasIssuedAt: !!decoded.payload.iat,
      hasNotBefore: !!decoded.payload.nbf,
      hasSubject: !!decoded.payload.sub,
      hasIssuer: !!decoded.payload.iss,
      hasAudience: !!decoded.payload.aud,
      hasJwtId: !!decoded.payload.jti
    },
    validation: {
      valid: verified.valid,
      issues: verified.issues,
      warnings: verified.warnings
    },
    recommendations: generateRecommendations(decoded, verified)
  };
}

function generateRecommendations(decoded, verified) {
  const recs = [];

  if (!decoded.payload.exp) {
    recs.push('Add exp (expiration) claim to limit token lifetime');
  }
  if (!decoded.payload.iat) {
    recs.push('Add iat (issued at) claim for better tracking');
  }
  if (!decoded.payload.sub) {
    recs.push('Add sub (subject) claim to identify the token owner');
  }
  if (decoded.header.alg === 'HS256') {
    recs.push('Consider upgrading to RS256 or ES256 for asymmetric verification');
  }
  if (verified.warnings.length === 0 && verified.issues.length === 0) {
    recs.push('Token follows best practices');
  }

  return recs;
}

function generateJWT(payload, secret, algorithm, customHeader = {}) {
  if (!payload) throw new Error('Payload is required');
  if (!secret) throw new Error('Secret is required for HS algorithms');

  const header = { alg: algorithm, typ: 'JWT', ...customHeader };

  const headerB64 = base64UrlEncode(JSON.stringify(header));
  const payloadB64 = base64UrlEncode(JSON.stringify(payload));
  const signature = generateSignature(headerB64, payloadB64, secret, algorithm);

  return `${headerB64}.${payloadB64}.${signature}`;
}

function generateSignature(headerB64, payloadB64, secret, algorithm) {
  const crypto = require('crypto');
  const data = `${headerB64}.${payloadB64}`;

  switch (algorithm) {
    case 'HS256':
      return base64UrlEncode(crypto.createHmac('sha256', secret).update(data).digest());
    case 'HS384':
      return base64UrlEncode(crypto.createHmac('sha384', secret).update(data).digest());
    case 'HS512':
      return base64UrlEncode(crypto.createHmac('sha512', secret).update(data).digest());
    default:
      throw new Error(`Algorithm ${algorithm} not supported for generation`);
  }
}

function base64UrlDecode(str) {
  // Add padding if needed
  const padding = 4 - (str.length % 4);
  if (padding !== 4) {
    str += '='.repeat(padding);
  }

  // Replace URL-safe characters
  str = str.replace(/-/g, '+').replace(/_/g, '/');

  return Buffer.from(str, 'base64').toString('utf8');
}

function base64UrlEncode(str) {
  return Buffer.from(str)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}
