export default function handler(req, res) {
  const event = req.body?.meta?.event_name;
  console.log('[Webhook] Event:', event);
  
  res.status(200).json({ received: true });
}
