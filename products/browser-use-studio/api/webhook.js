export default function handler(req, res) {
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
    const { meta, data } = req.body;
    const eventName = meta?.event_name || 'unknown';

    console.log('Webhook received:', eventName, JSON.stringify(req.body).slice(0, 500));

    // Handle LemonSqueezy webhooks
    if (eventName.includes('order_created') || eventName.includes('payment_success')) {
      const licenseKey = generateLicenseKey();
      console.log('License generated:', licenseKey);
    }

    res.status(200).json({
      received: true,
      event: eventName,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(200).json({
      received: true,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
}

function generateLicenseKey() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let key = '';
  for (let i = 0; i < 16; i++) {
    if (i > 0 && i % 4 === 0) key += '-';
    key += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return key;
}
