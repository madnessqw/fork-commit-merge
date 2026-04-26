module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { action, options } = req.body;
    const licenseKey = req.headers['x-license-key'];

    // Validate license for premium features
    let hasLicense = false;
    if (licenseKey) {
      // Simple license validation - in production, verify against LemonSqueezy API
      hasLicense = licenseKey.startsWith('BMS-') || licenseKey.length > 20;
    }

    switch (action) {
      case 'generate-mockup':
        // Return mockup configuration data
        return res.status(200).json({
          success: true,
          data: {
            browsers: ['chrome', 'safari', 'firefox'],
            themes: ['dark', 'light'],
            backgrounds: [
              { id: 'gradient-purple', name: 'Gradient Purple', colors: ['#667eea', '#764ba2'] },
              { id: 'gradient-blue', name: 'Gradient Blue', colors: ['#1e3c72', '#2a5298'] },
              { id: 'gradient-orange', name: 'Gradient Orange', colors: ['#f093fb', '#f5576c'] },
              { id: 'solid-dark', name: 'Solid Dark', colors: ['#0a0a0a'] },
              { id: 'solid-light', name: 'Solid Light', colors: ['#f5f5f5'] }
            ],
            exportFormats: hasLicense ? ['png', 'jpg', 'webp', 'svg'] : ['png', 'jpg'],
            premium: hasLicense,
            message: hasLicense ? 'Full access granted' : 'Basic access. Purchase for premium features.'
          }
        });

      case 'validate-license':
        return res.status(200).json({
          valid: hasLicense,
          tier: hasLicense ? 'premium' : 'free',
          features: hasLicense ? ['all'] : ['basic']
        });

      default:
        return res.status(400).json({ error: 'Unknown action' });
    }
  } catch (error) {
    console.error('Process error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
};
