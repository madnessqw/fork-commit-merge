module.exports = (req, res) => {
  res.json({
    status: 'healthy',
    service: 'code-formatter-universal',
    timestamp: new Date().toISOString()
  });
};
