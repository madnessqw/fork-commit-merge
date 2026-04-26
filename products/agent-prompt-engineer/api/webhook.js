module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const event = req.body;

  if (event.meta?.event_name === 'order_created' || event.meta?.event_name === 'checkout_completed') {
    console.log('Payment received:', event.data?.id);
    return res.status(200).json({ success: true });
  }

  res.status(200).json({ received: true });
};
