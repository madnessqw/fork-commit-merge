const { transformText, generateStats } = require('./utils.js');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { text, mode, action } = req.body || {};

    if (!text && text !== '') {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Transform action
    if (action === 'transform' && mode) {
      const result = transformText(text, mode);
      return res.status(200).json({
        success: true,
        result,
        mode,
        originalLength: text.length,
        resultLength: result.length
      });
    }

    // Analyze action
    if (action === 'analyze') {
      const stats = generateStats(text);
      return res.status(200).json({
        success: true,
        stats
      });
    }

    // Batch transform (all modes)
    if (action === 'batch') {
      const modes = ['upper', 'lower', 'title', 'sentence', 'camel', 'pascal', 'snake', 'kebab', 'slug'];
      const results = {};
      modes.forEach(m => {
        results[m] = transformText(text, m);
      });
      const stats = generateStats(text);
      return res.status(200).json({
        success: true,
        results,
        stats
      });
    }

    return res.status(400).json({ error: 'Invalid action. Use: transform, analyze, or batch' });

  } catch (error) {
    console.error('Text transform error:', error);
    return res.status(500).json({
      error: 'Transformation failed',
      message: error.message
    });
  }
};
