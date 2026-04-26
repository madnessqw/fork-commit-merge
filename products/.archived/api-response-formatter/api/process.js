import { XMLParser, XMLBuilder } from 'fast-xml-parser';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { input, format, schema, indent } = req.body;
    
    if (!input) {
      return res.status(400).json({ error: 'Input is required' });
    }

    let result;
    let originalFormat = detectFormat(input);
    
    // Format detection and conversion
    if (format === 'json' || (format === 'auto' && originalFormat === 'json')) {
      // Parse and re-stringify for formatting
      const parsed = JSON.parse(input);
      result = JSON.stringify(parsed, null, indent || 2);
    } else if (format === 'xml' || (format === 'auto' && originalFormat === 'xml')) {
      // XML processing
      const parser = new XMLParser({ 
        ignoreAttributes: false,
        attributeNamePrefix: "@_"
      });
      const parsed = parser.parse(input);
      const builder = new XMLBuilder({ 
        ignoreAttributes: false,
        attributeNamePrefix: "@_",
        format: true,
        indentBy: indent || 2
      });
      result = builder.build(parsed);
    } else {
      // Default to JSON
      const parsed = JSON.parse(input);
      result = JSON.stringify(parsed, null, indent || 2);
    }

    // Schema validation if provided
    let validation = null;
    if (schema && format !== 'xml') {
      try {
        const Ajv = require('ajv');
        const ajv = new Ajv();
        const validate = ajv.compile(JSON.parse(schema));
        const data = JSON.parse(input);
        validation = { valid: validate(data) };
        if (!validation.valid) {
          validation.errors = validate.errors;
        }
      } catch (e) {
        validation = { error: e.message };
      }
    }

    res.status(200).json({
      success: true,
      formatted: result,
      originalFormat,
      targetFormat: format === 'auto' ? originalFormat : format,
      validation,
      stats: {
        lines: result.split('\n').length,
        chars: result.length,
        size: new Blob([result]).size
      }
    });

  } catch (error) {
    res.status(400).json({ 
      error: 'Invalid input',
      message: error.message,
      hint: 'Make sure your JSON/XML is valid'
    });
  }
}

function detectFormat(input) {
  const trimmed = input.trim();
  if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
    return 'json';
  } else if (trimmed.startsWith('<') || trimmed.startsWith('<?xml')) {
    return 'xml';
  }
  return 'unknown';
}
