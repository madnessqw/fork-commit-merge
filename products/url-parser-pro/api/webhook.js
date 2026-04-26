export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  const { meta, data } = req.body || {};
  
  if (meta?.event_name === 'order_created' || meta?.event_name === 'subscription_created') {
    console.log('License activated:', data?.license_key);
    return res.status(200).json({ success: true, event: meta.event_name });
  }
  
  res.status(200).json({ received: true });
}
