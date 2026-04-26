// Regex processing API
// POST /api/process - Process a regex against test strings

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { pattern, flags = 'g', testStrings = [] } = req.body;

    if (!pattern) {
      return res.status(400).json({ error: 'Pattern is required' });
    }

    // Build regex
    let regex;
    try {
      regex = new RegExp(pattern, flags);
    } catch (e) {
      return res.status(400).json({
        error: 'Invalid regex',
        message: e.message
      });
    }

    const results = testStrings.map((text, index) => {
      const matches = [];
      let match;

      if (flags.includes('g')) {
        while ((match = regex.exec(text)) !== null) {
          matches.push({
            index: matches.length,
            match: match[0],
            groups: match.slice(1),
            position: match.index,
            lastIndex: regex.lastIndex
          });
          if (match[0].length === 0) {
            regex.lastIndex++;
          }
        }
      } else {
        match = regex.exec(text);
        if (match) {
          matches.push({
            index: 0,
            match: match[0],
            groups: match.slice(1),
            position: match.index,
            lastIndex: match.index + match[0].length
          });
        }
      }

      return {
        text,
        textIndex: index,
        matchCount: matches.length,
        matches
      };
    });

    return res.status(200).json({
      success: true,
      pattern,
      flags,
      results,
      totalMatches: results.reduce((sum, r) => sum + r.matchCount, 0)
    });

  } catch (error) {
    return res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
}
