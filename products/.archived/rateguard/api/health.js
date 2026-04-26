module.exports = async (req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({
    status: 'healthy',
    service: 'rateguard',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  }));
};
