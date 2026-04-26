module.exports = function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.status(200).json({ status: 'healthy', service: 'universe-hub', timestamp: new Date().toISOString() });
};
