export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.json({ status: 'healthy', service: 'Nginx Config Tester', timestamp: new Date().toISOString() });
}
