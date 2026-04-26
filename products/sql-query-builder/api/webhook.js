module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { meta } = req.body;

  console.log('Webhook received:', meta?.event_name);

  res.json({
    success: true,
    event: meta?.event_name,
    received: new Date().toISOString()
  });
};
