// LemonSqueezy Webhook Handler for API Mock Generator
// Processes license key validation and activation

const LICENSE_DB = new Map();

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Signature');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    const { meta, data } = body;

    if (!meta || !meta.event_name) {
      return res.status(400).json({ error: 'Invalid webhook payload' });
    }

    const event = meta.event_name;
    const response = {
      received: true,
      event,
      timestamp: new Date().toISOString()
    };

    switch (event) {
      case 'order_created':
      case 'subscription_created':
        if (data && data.attributes) {
          const licenseKey = data.attributes.license_key;
          const customerEmail = data.attributes.user_email || data.attributes.customer?.email;

          if (licenseKey) {
            LICENSE_DB.set(licenseKey, {
              email: customerEmail,
              activated: false,
              created_at: new Date().toISOString(),
              product: 'api-mock-generator'
            });
            response.license_key = licenseKey;
            response.status = 'license_created';
          }
        }
        break;

      case 'license_key_activated':
        if (data && data.attributes && data.attributes.key) {
          const key = data.attributes.key;
          if (LICENSE_DB.has(key)) {
            const record = LICENSE_DB.get(key);
            record.activated = true;
            record.activated_at = new Date().toISOString();
            LICENSE_DB.set(key, record);
            response.status = 'license_activated';
          }
        }
        break;

      case 'order_refunded':
        response.status = 'refund_processed';
        break;

      default:
        response.status = 'event_received';
    }

    return res.status(200).json(response);

  } catch (error) {
    return res.status(500).json({
      error: 'Webhook processing failed',
      message: error.message
    });
  }
}

// License validation endpoint
export async function validateLicense(licenseKey) {
  if (!LICENSE_DB.has(licenseKey)) {
    return { valid: false, error: 'License not found' };
  }

  const record = LICENSE_DB.get(licenseKey);

  if (!record.activated) {
    return { valid: false, error: 'License not activated' };
  }

  return {
    valid: true,
    product: record.product,
    email: record.email,
    activated_at: record.activated_at
  };
}
