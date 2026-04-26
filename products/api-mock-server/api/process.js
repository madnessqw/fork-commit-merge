module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { action, endpoint, method, response } = req.body;

  try {
    switch (action) {
      case 'generate':
        const mockId = generateMockId();
        const mockUrl = `${req.headers.host}/api/mock/${mockId}`;
        return res.json({
          success: true,
          mockId,
          mockUrl,
          endpoint,
          method,
          message: 'Mock endpoint created'
        });

      case 'validate':
        const validation = validateEndpoint(endpoint, response);
        return res.json({ success: true, validation });

      default:
        return res.status(400).json({ error: 'Unknown action' });
    }
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

function generateMockId() {
  return 'mock_' + Math.random().toString(36).substring(2, 10);
}

function validateEndpoint(endpoint, response) {
  const issues = [];

  if (!endpoint || !endpoint.startsWith('/')) {
    issues.push('Endpoint must start with /');
  }

  if (response) {
    try {
      JSON.stringify(response);
    } catch {
      issues.push('Response must be valid JSON');
    }
  }

  return {
    valid: issues.length === 0,
    issues
  };
}
