module.exports = (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'json-diff-pro',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
};
