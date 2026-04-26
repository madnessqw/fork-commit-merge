// Health check endpoint
// GET /api/health

export default function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  return res.status(200).json({
    status: 'healthy',
    service: 'regex-visualizer-pro',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
}
