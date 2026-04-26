export default function handler(req, res) {
  res.status(200).json({
    status: 'healthy',
    service: 'mcp-inspector-pro',
    timestamp: new Date().toISOString()
  });
}
