module.exports = (req, res) => {
  res.json({
    status: 'healthy',
    service: 'sql-query-builder',
    timestamp: new Date().toISOString()
  });
};
