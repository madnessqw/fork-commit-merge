module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const event = req.body?.meta?.event_name;

  if (event === 'order_created' || event === 'subscription_created') {
    console.log('Payment received:', req.body);
    return res.status(200).json({
      success: true,
      message: 'Payment processed successfully'
    });
  }

  res.status(200).json({
    success: true,
    message: 'Webhook received'
  });
};
