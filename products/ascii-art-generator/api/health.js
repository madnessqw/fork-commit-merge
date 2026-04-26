export default function handler(req, res) {
  res.json({ status: 'ok', service: 'ascii-art-generator', timestamp: new Date().toISOString() });
}
