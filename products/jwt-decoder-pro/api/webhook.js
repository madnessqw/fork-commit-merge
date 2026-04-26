/**
 * JWT Decoder Pro — Webhook Handler
 * Handles payment webhooks from Polar
 */

export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Verify webhook signature (Polar provides signature in headers)
  const signature = req.headers['polar-signature'];
  const webhookSecret = process.env.POLAR_WEBHOOK_SECRET;

  if (webhookSecret && signature) {
    // In production, verify the webhook signature here
    // const isValid = verifyPolarWebhook(req.body, signature, webhookSecret);
  }

  const event = req.body?.event;

  if (!event) {
    return res.status(400).json({ error: 'Missing event type' });
  }

  switch (event) {
    case 'payment.created':
      // Handle new payment
      console.log('Payment created:', req.body);
      break;

    case 'payment.succeeded':
      // Handle successful payment - deliver access
      console.log('Payment succeeded:', req.body);
      break;

    case 'payment.failed':
      // Handle failed payment
      console.log('Payment failed:', req.body);
      break;

    case 'subscription.created':
      // Handle new subscription
      console.log('Subscription created:', req.body);
      break;

    case 'subscription.cancelled':
      // Handle subscription cancellation
      console.log('Subscription cancelled:', req.body);
      break;

    default:
      console.log('Unhandled webhook event:', event);
  }

  res.status(200).json({ received: true });
}
