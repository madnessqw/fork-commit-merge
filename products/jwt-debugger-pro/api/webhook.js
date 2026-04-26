export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const event = req.body?.meta?.event_name;

  if (!event) {
    return res.status(400).json({ error: 'No event provided' });
  }

  console.log(`Webhook received: ${event}`);

  switch (event) {
    case 'order_created':
    case 'subscription_created':
      console.log('New purchase/subscription:', req.body);
      return res.json({
        status: 'success',
        message: 'License activated',
        event: event
      });

    case 'subscription_cancelled':
      console.log('Subscription cancelled:', req.body);
      return res.json({
        status: 'success',
        message: 'Subscription cancelled',
        event: event
      });

    default:
      console.log('Unhandled event:', event);
      return res.json({ received: true, event });
  }
}
