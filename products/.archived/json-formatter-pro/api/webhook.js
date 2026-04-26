// LemonSqueezy Webhook Handler
// Handles license key validation and order events

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

    // Log the webhook event (in production, store in database)
    console.log('Webhook event:', event);

    const eventName = event?.meta?.event_name || event?.event;
    const payload = event?.data?.attributes || event;

    switch (eventName) {
      case 'order_created':
      case 'subscription_created':
        // New purchase - activate license
        console.log('New order:', payload);
        return res.status(200).json({
          success: true,
          message: 'Order processed',
          orderId: payload?.id
        });

      case 'subscription_updated':
        // Subscription renewed or updated
        console.log('Subscription updated:', payload);
        return res.status(200).json({
          success: true,
          message: 'Subscription updated'
        });

      case 'subscription_cancelled':
        // Subscription cancelled
        console.log('Subscription cancelled:', payload);
        return res.status(200).json({
          success: true,
          message: 'Subscription cancelled'
        });

      case 'license_key_created':
        // New license key created
        console.log('License key created:', payload);
        return res.status(200).json({
          success: true,
          message: 'License key created'
        });

      case 'license_key_validated':
        // License key validated
        console.log('License validated:', payload);
        return res.status(200).json({
          success: true,
          message: 'License validated'
        });

      default:
        console.log('Unhandled event:', eventName);
        return res.status(200).json({
          success: true,
          message: 'Event received'
        });
    }

  } catch (err) {
    console.error('Webhook error:', err);
    return res.status(500).json({
      error: 'Webhook processing failed',
      message: err.message
    });
  }
}