import crypto from 'crypto';

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ error: 'Method not allowed' }));
  }

  try {
    const body = JSON.parse(req.body || '{}');
    const { event, order_id, license_key } = body;

    // Handle LemonSqueezy webhook events
    if (event === 'order_created') {
      console.log(`[RateGuard] Order created: ${order_id}`);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ received: true }));
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ received: true, event }));
  } catch (err) {
    res.writeHead(400, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ error: 'Invalid webhook payload' }));
  }
};
