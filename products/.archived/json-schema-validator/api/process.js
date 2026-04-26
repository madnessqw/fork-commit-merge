const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true, verbose: true });
addFormats(ajv);

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { json, schema } = req.body;

    if (!json || !schema) {
      return res.status(400).json({
        valid: false,
        errors: [{ message: 'Both JSON and Schema are required' }]
      });
    }

    let parsedJson, parsedSchema;

    try {
      parsedJson = typeof json === 'string' ? JSON.parse(json) : json;
    } catch (e) {
      return res.status(400).json({
        valid: false,
        errors: [{ message: 'Invalid JSON: ' + e.message }]
      });
    }

    try {
      parsedSchema = typeof schema === 'string' ? JSON.parse(schema) : schema;
    } catch (e) {
      return res.status(400).json({
        valid: false,
        errors: [{ message: 'Invalid JSON Schema: ' + e.message }]
      });
    }

    const validate = ajv.compile(parsedSchema);
    const valid = validate(parsedJson);

    if (valid) {
      return res.status(200).json({
        valid: true,
        errors: [],
        message: 'JSON is valid against the schema'
      });
    } else {
      const errors = validate.errors.map(err => ({
        path: err.instancePath || '/',
        message: `${err.instancePath || 'root'} ${err.message}`,
        keyword: err.keyword,
        params: err.params
      }));

      return res.status(200).json({
        valid: false,
        errors,
        message: 'JSON is NOT valid against the schema'
      });
    }
  } catch (error) {
    console.error('[DEBUG] Validation error:', error);
    return res.status(500).json({
      valid: false,
      errors: [{ message: 'Server error: ' + error.message }]
    });
  }
};