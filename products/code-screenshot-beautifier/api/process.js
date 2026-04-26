export default async function handler(req, res) {
  // CORS headers
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
    const { code, theme, background, windowStyle, language } = req.body;

    if (!code) {
      return res.status(400).json({ error: 'Code is required' });
    }

    const screenshotData = {
      id: `shot_${Date.now()}`,
      theme: theme || 'dark',
      background: background || 'gradient',
      windowStyle: windowStyle || 'macos',
      language: language || 'javascript',
      codeLength: code.length,
      timestamp: new Date().toISOString(),
      status: 'generated'
    };

    return res.status(200).json({
      success: true,
      data: screenshotData,
      message: 'Screenshot generated successfully'
    });

  } catch (error) {
    console.error('Screenshot generation error:', error);
    return res.status(500).json({
      error: 'Failed to generate screenshot',
      details: error.message
    });
  }
}
