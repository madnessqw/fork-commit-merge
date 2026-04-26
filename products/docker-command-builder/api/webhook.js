// LemonSqueezy Webhook Handler
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const event = req.body;

    // Log the webhook event
    console.log('Webhook received:', JSON.stringify(event, null, 2));

    // Check for LemonSqueezy signature if available
    const signature = req.headers['x-signature'] || req.headers['x-lemonsqueezy-signature'];

    // Handle different event types
    const eventName = event?.meta?.event_name || event?.event_name || 'unknown';

    switch (eventName) {
      case 'order_created':
      case 'order_successful':
        // Handle new purchase
        console.log('New purchase:', event.data?.id);
        break;

      case 'subscription_created':
        // Handle subscription
        console.log('New subscription:', event.data?.id);
        break;

      case 'subscription_cancelled':
        // Handle cancellation
        console.log('Subscription cancelled:', event.data?.id);
        break;

      default:
        console.log('Unhandled event:', eventName);
    }

    return res.status(200).json({
      received: true,
      event: eventName,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Webhook error:', error);
    return res.status(500).json({ error: error.message });
  }
}
