export default function handler(req, res) {
  res.status(200).json({
    status: 'healthy',
    service: 'htpasswd-generator',
    timestamp: new Date().toISOString()
  });
}
