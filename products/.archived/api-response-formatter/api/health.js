export default function handler(req, res) {
  res.status(200).json({ 
    status: 'ok', 
    product: 'api-response-formatter',
    timestamp: new Date().toISOString()
  });
}
