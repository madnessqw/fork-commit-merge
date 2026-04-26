export default function handler(req, res) {
  res.status(200).json({
    status: 'healthy',
    service: 'htaccess-generator',
    timestamp: new Date().toISOString(),
    uptime: '100%'
  });
}
