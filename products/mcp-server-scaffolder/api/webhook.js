export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  const event = req.body?.meta?.event_name;
  
  if (event === 'order_created') {
    console.log('Order received:', req.body.data);
    return res.status(200).json({ status: 'received', event });
  }
  
  res.status(200).json({ status: 'ignored', event });
}
