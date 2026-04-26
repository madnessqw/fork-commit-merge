/**
 * JWT Decoder Pro — Health Check API
 */

export default function handler(req, res) {
  res.status(200).json({
    status: 'healthy',
    service: 'jwt-decoder-pro',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
}
