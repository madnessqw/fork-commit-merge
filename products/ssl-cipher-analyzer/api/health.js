export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.json({ status: 'healthy', service: 'SSL Cipher Analyzer', timestamp: new Date().toISOString() });
}
