module.exports = (req, res) => {
  res.status(200).json({
    status: 'ok',
    product: 'api-spec-validator',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
};
