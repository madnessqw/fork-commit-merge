// LemonSqueezy webhook handler
const crypto = require('crypto');

module.exports = async (req, res) => {
  // CORS headers
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
    const { meta, data } = req.body;

    if (!meta || !meta.event_name) {
      return res.status(400).json({ error: 'Invalid webhook payload' });
    }

    const event = meta.event_name;

    // Log event for debugging
    console.log(`Webhook received: ${event}`, JSON.stringify({ meta, data: data ? { id: data.id, type: data.type } : null }));

    switch (event) {
      case 'order_created':
      case 'subscription_created':
        await handleOrderCreated(data);
        break;
      case 'subscription_payment_success':
        await handlePaymentSuccess(data);
        break;
      case 'subscription_expired':
      case 'subscription_cancelled':
        await handleSubscriptionExpired(data);
        break;
      default:
        console.log(`Unhandled event: ${event}`);
    }

    return res.status(200).json({ received: true, event });

  } catch (error) {
    console.error('Webhook error:', error);
    return res.status(500).json({ error: 'Webhook processing failed' });
  }
};

async function handleOrderCreated(data) {
  console.log('Order created:', data.id);
  // In production: Store license key in database
  // For now, we just log it
}

async function handlePaymentSuccess(data) {
  console.log('Payment success:', data.id);
  // In production: Activate license, send email
}

async function handleSubscriptionExpired(data) {
  console.log('Subscription expired:', data.id);
  // In production: Deactivate license
}
