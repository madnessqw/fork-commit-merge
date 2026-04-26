export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Signature');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const event = req.body;
    const eventName = event?.meta?.event_name;

    switch (eventName) {
      case 'order_created':
      case 'checkout_completed':
        console.log('Purchase completed:', { orderId: event?.data?.id, timestamp: new Date().toISOString() });
        break;
      case 'subscription_created':
        console.log('Subscription created:', { subscriptionId: event?.data?.id });
        break;
      case 'test':
        console.log('Test webhook received');
        break;
      default:
        console.log(`Unhandled event type: ${eventName}`);
    }

    return res.status(200).json({ success: true, message: 'Webhook processed' });

  } catch (error) {
    console.error('Webhook error:', error);
    return res.status(500).json({ error: 'Webhook processing failed', details: error.message });
  }
}
