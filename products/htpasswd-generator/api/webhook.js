export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const event = req.body?.meta?.event_name;

  if (event === 'order_created' || event === 'subscription_created') {
    console.log('Payment received:', req.body);
    return res.status(200).json({ success: true });
  }

  res.status(200).json({ received: true });
}
