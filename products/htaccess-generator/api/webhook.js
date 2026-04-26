export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const event = req.body?.meta?.event_name;

  // LemonSqueezy webhook handler
  if (event === 'order_created' || event === 'checkout_completed') {
    console.log('Payment received:', req.body);
    return res.status(200).json({ received: true });
  }

  return res.status(200).json({ received: true });
}
