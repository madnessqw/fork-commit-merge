/**
 * RegexCraft AI — AI-powered regex builder, tester, and explainer
 * POST /api/process
 * Body: { description, testString, pattern, flags, preset }
 */
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // Common regex presets
  const PRESETS = {
    email: { pattern: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', flags: 'gi', name: 'Email Address' },
    url: { pattern: 'https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)', flags: 'gi', name: 'URL' },
    phone: { pattern: '\\+?[1-9]\\d{1,14}', flags: 'g', name: 'Phone Number (E.164)' },
    ip: { pattern: '\\b(?:(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\b', flags: 'g', name: 'IPv4 Address' },
    date: { pattern: '\\b\\d{4}[-/]\\d{2}[-/]\\d{2}\\b', flags: 'g', name: 'Date (YYYY-MM-DD)' },
    hex: { pattern: '#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\\b', flags: 'g', name: 'Hex Color' },
    slug: { pattern: '[a-z0-9]+(?:-[a-z0-9]+)*', flags: 'g', name: 'URL Slug' },
    uuid: { pattern: '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', flags: 'g', name: 'UUID' },
    html: { pattern: '<([a-z][a-z0-9]*)\\b[^>]*>(.*?)<\\/\\1>', flags: 'gis', name: 'HTML Tags' },
    markdown_link: { pattern: '\\[([^\\]]+)\\]\\(([^)]+)\\)', flags: 'g', name: 'Markdown Link' },
    username: { pattern: '^[a-zA-Z0-9_]{3,20}$', flags: '', name: 'Username' },
    strong_password: { pattern: '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$', flags: '', name: 'Strong Password' },
    credit_card: { pattern: '\\b(?:\\d[ -]*?){13,19}\\b', flags: 'g', name: 'Credit Card Number' },
    zipcode: { pattern: '\\b\\d{5}(?:-\\d{4})?\\b', flags: 'g', name: 'ZIP Code' },
    hashtag: { pattern: '#[a-zA-Z0-9_]+', flags: 'g', name: 'Hashtag' },
    mention: { pattern: '@[a-zA-Z0-9_]+', flags: 'g', name: '@ Mention' },
    bitcoin: { pattern: '\\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\\b', flags: 'g', name: 'Bitcoin Address' },
    ssn: { pattern: '\\b\\d{3}-\\d{2}-\\d{4}\\b', flags: 'g', name: 'SSN' },
    mac: { pattern: '([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', flags: 'g', name: 'MAC Address' },
  };

  // Description-to-pattern mappings (keyword-based AI simulation)
  const DESCRIPTION_MAP = [
    { keywords: ['email', 'mail', 'e-mail'], preset: 'email' },
    { keywords: ['url', 'link', 'http', 'website', 'web address'], preset: 'url' },
    { keywords: ['phone', 'telephone', 'mobile'], preset: 'phone' },
    { keywords: ['ip', 'internet protocol', 'ipv4'], preset: 'ip' },
    { keywords: ['date', 'time', 'timestamp'], preset: 'date' },
    { keywords: ['hex', 'color', 'colour'], preset: 'hex' },
    { keywords: ['slug', 'url-friendly'], preset: 'slug' },
    { keywords: ['uuid', 'guid'], preset: 'uuid' },
    { keywords: ['html', 'tag', 'element'], preset: 'html' },
    { keywords: ['markdown', 'md link'], preset: 'markdown_link' },
    { keywords: ['username', 'user name'], preset: 'username' },
    { keywords: ['password', 'strong pass'], preset: 'strong_password' },
    { keywords: ['credit card', 'card number'], preset: 'credit_card' },
    { keywords: ['zip', 'postal code'], preset: 'zipcode' },
    { keywords: ['hashtag'], preset: 'hashtag' },
    { keywords: ['mention', '@'], preset: 'mention' },
    { keywords: ['bitcoin', 'btc', 'wallet'], preset: 'bitcoin' },
    { keywords: ['ssn', 'social security'], preset: 'ssn' },
    { keywords: ['mac', 'mac address'], preset: 'mac' },
  ];

  function findPattern(desc) {
    const lower = desc.toLowerCase();
    for (const entry of DESCRIPTION_MAP) {
      if (entry.keywords.some(k => lower.includes(k))) {
        const preset = PRESETS[entry.preset];
        return { pattern: preset.pattern, flags: preset.flags, name: preset.name, confidence: 0.9 };
      }
    }
    return null;
  }

  function explainPattern(pattern, flags) {
    const parts = [];
    if (pattern.includes('@')) parts.push('Matches email-like patterns with @ symbol');
    if (pattern.includes('http')) parts.push('Matches HTTP/HTTPS URLs');
    if (pattern.includes('a-fA-F')) parts.push('Matches hexadecimal characters');
    if (pattern.includes('\\d')) parts.push('Uses digit shorthand (\\d = 0-9)');
    if (pattern.includes('\\w')) parts.push('Uses word character shorthand (\\w = letters, digits, underscore)');
    if (pattern.includes('+')) parts.push('Uses + quantifier (one or more)');
    if (pattern.includes('*')) parts.push('Uses * quantifier (zero or more)');
    if (pattern.includes('?') && !pattern.includes('\\?')) parts.push('Uses ? quantifier (optional or non-greedy)');
    if (pattern.startsWith('^')) parts.push('Anchored to start of string (^)');
    if (pattern.endsWith('$')) parts.push('Anchored to end of string ($)');
    if (pattern.includes('\\.')) parts.push('Matches literal dot character');
    if (pattern.includes('[')) parts.push('Uses character class [...]');
    if (pattern.includes('(?:')) parts.push('Uses non-capturing group');
    if (pattern.includes('(') && !pattern.includes('(?:')) parts.push('Uses capturing groups');
    if (pattern.includes('|')) parts.push('Uses alternation (OR logic)');
    if (pattern.includes('\\b')) parts.push('Uses word boundary (\\b)');
    if (pattern.includes('{')) parts.push('Uses quantifier {n,m}');
    if (pattern.includes('(?=')) parts.push('Uses positive lookahead assertion');
    if (pattern.includes('(?!')) parts.push('Uses negative lookahead assertion');
    if (flags.includes('i')) parts.push('Case-insensitive matching (flag: i)');
    if (flags.includes('g')) parts.push('Global matching — finds all occurrences (flag: g)');
    if (flags.includes('m')) parts.push('Multi-line mode (flag: m)');
    return parts.length > 0 ? parts : ['Custom regex pattern'];
  }

  function calculateComplexity(pattern) {
    let score = 0;
    if (pattern.length > 50) score += 2;
    if (pattern.length > 100) score += 2;
    const capturingGroups = (pattern.match(/\(/g) || []).length - (pattern.match(/\(\?:/g) || []).length;
    if (capturingGroups > 3) score += 3;
    if (pattern.includes('*') || pattern.includes('+')) score += 1;
    if (pattern.includes('{') && pattern.includes(',')) score += 2;
    if (pattern.includes('|')) score += 1;
    if (pattern.includes('(?=')) score += 3;
    if (pattern.includes('(?!')) score += 3;
    if (pattern.includes('.*') || pattern.includes('.+')) score += 2;
    if (score <= 2) return { level: 'Simple', score, description: 'Easy to read and maintain' };
    if (score <= 5) return { level: 'Moderate', score, description: 'Some complexity, review recommended' };
    if (score <= 8) return { level: 'Complex', score, description: 'Consider simplifying or adding comments' };
    return { level: 'Very Complex', score, description: 'High risk of ReDoS — refactor recommended' };
  }

  try {
    const body = req.body;
    const { description, testString, pattern: inputPattern, flags: inputFlags, preset: inputPreset } = body || {};

    let pattern = inputPattern;
    let flags = inputFlags || 'g';
    let name = 'Custom Pattern';
    let confidence = 1.0;

    // Resolve from preset
    if (inputPreset && PRESETS[inputPreset]) {
      pattern = PRESETS[inputPreset].pattern;
      flags = PRESETS[inputPreset].flags;
      name = PRESETS[inputPreset].name;
    }

    // Resolve from description
    if (!pattern && description) {
      const found = findPattern(description);
      if (found) {
        pattern = found.pattern;
        flags = found.flags;
        name = found.name;
        confidence = found.confidence;
      } else {
        return res.status(400).json({
          error: 'No matching pattern found for description',
          suggestion: 'Try: email, url, phone, date, hex color, uuid, username, password, credit card, hashtag',
          available_presets: Object.keys(PRESETS)
        });
      }
    }

    if (!pattern) {
      return res.status(400).json({ error: 'Either "description", "pattern", or "preset" is required' });
    }

    // Validate pattern compiles
    let compiledRegex;
    try {
      compiledRegex = new RegExp(pattern, flags);
    } catch (e) {
      return res.status(400).json({ error: `Invalid regex: ${e.message}` });
    }

    // Test against string
    let testResults = null;
    if (testString) {
      const matches = [...testString.matchAll(compiledRegex)];
      testResults = {
        input: testString,
        hasMatch: matches.length > 0,
        matchCount: matches.length,
        matches: matches.slice(0, 50).map(m => ({
          text: m[0],
          index: m.index,
          groups: m.slice(1).filter(Boolean).length > 0 ? m.slice(1).filter(Boolean) : undefined,
        })),
      };
    }

    return res.status(200).json({
      success: true,
      pattern,
      flags,
      name,
      confidence,
      explanation: explainPattern(pattern, flags),
      complexity: calculateComplexity(pattern),
      test: testResults,
      presets_available: Object.keys(PRESETS),
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return res.status(500).json({ error: error.message, success: false });
  }
};
