export default function handler(req, res) {
  res.json({
    status: 'healthy',
    service: 'jwt-debugger-pro',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
}
