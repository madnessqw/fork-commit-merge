export default function handler(req, res) {
  res.status(200).json({ status: 'ok', service: 'mcp-hub', timestamp: new Date().toISOString() });
}
