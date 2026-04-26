// LemonSqueezy webhook handler
module.exports = async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const event = req.body;
    const eventName = event?.meta?.event_name || 'unknown';

    console.log(`Webhook received: ${eventName}`);
    console.log('Event data:', JSON.stringify(event, null, 2));

    switch (eventName) {
      case 'order_created':
        console.log('New order created');
        // Handle new purchase
        break;
      case 'order_refunded':
        console.log('Order refunded');
        // Handle refund
        break;
      case 'subscription_created':
        console.log('New subscription');
        break;
      case 'subscription_cancelled':
        console.log('Subscription cancelled');
        break;
      default:
        console.log(`Unhandled event: ${eventName}`);
    }

    res.status(200).json({
      received: true,
      event: eventName,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: 'Webhook processing failed' });
  }
};
