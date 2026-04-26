// Health check endpoint for API Mock Generator
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  return res.status(200).json({
    status: 'healthy',
    service: 'api-mock-generator',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    endpoints: {
      mock: '/api/process',
      webhook: '/api/webhook',
      health: '/api/health'
    }
  });
}
