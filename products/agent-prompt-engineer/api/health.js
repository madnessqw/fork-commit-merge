module.exports = (req, res) => {
  res.status(200).json({
    status: 'healthy',
    product: 'agent-prompt-engineer',
    timestamp: new Date().toISOString()
  });
};
