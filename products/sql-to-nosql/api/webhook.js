module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');
  
  if (req.method === 'POST') {
    const event = req.body;
    console.log('[Webhook] Received:', event.meta?.event_name);
    return res.status(200).json({ received: true });
  }
  
  return res.status(200).json({ status: 'webhook endpoint ready' });
};
