export default function handler(req, res) {
  res.status(200).json({
    status: 'healthy',
    service: 'mcp-server-scaffolder',
    timestamp: new Date().toISOString()
  });
}
