module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const event = req.body;
  const eventName = event?.meta?.event_name || event?.meta?.custom_data?.event_name || 'unknown';

  console.log(`[webhook] Received event: ${eventName}`);

  res.status(200).json({ received: true, event: eventName });
};
