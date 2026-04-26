module.exports = async (req, res) => {
  // Simple health check endpoint
  const health = {
    status: "healthy",
    timestamp: new Date().toISOString(),
    service: "api-security-scanner",
    version: "1.0.0"
  };

  res.status(200).json(health);
};
