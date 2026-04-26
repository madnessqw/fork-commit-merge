module.exports = (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-mock-server',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
};
