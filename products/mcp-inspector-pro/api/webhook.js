export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  const event = req.body?.meta?.event_name;
  
  if (event === 'order_created' || event === 'license_activated') {
    console.log('License event:', event);
    return res.status(200).json({ 
      received: true, 
      event: event,
      processed: true 
    });
  }
  
  res.status(200).json({ received: true });
}
