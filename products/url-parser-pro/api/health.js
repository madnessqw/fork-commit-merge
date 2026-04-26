export default function handler(req, res) {
  res.status(200).json({ status: 'healthy', service: 'url-parser-pro', timestamp: new Date().toISOString() });
}
