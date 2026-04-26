module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { meta, data } = req.body || {};

  if (meta?.event_name === 'order_created' || meta?.event_name === 'subscription_created') {
    return res.json({
      status: 'success',
      message: 'License activated',
      license_key: `BIN-${Date.now()}-${Math.random().toString(36).substring(2, 8).toUpperCase()}`
    });
  }

  res.json({ status: 'received' });
};
