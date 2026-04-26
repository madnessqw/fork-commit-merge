const Ajv = require('ajv');
const yaml = require('js-yaml');
const fjp = require('fast-json-patch');

const ajv = new Ajv({ allErrors: true, strict: false });

function jsonResponse(res, status, body) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.status(status).json(body);
}

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return jsonResponse(res, 200, { ok: true });
  if (req.method !== 'POST') return jsonResponse(res, 405, { error: 'Method not allowed' });

  try {
    const { action, input, schema, inputA, inputB, fromFormat, toFormat } = req.body;

    if (!action) return jsonResponse(res, 400, { error: 'Missing action parameter' });

    switch (action) {
      case 'format': {
        const parsed = parseInput(input, fromFormat);
        const formatted = JSON.stringify(parsed, null, 2);
        return jsonResponse(res, 200, { result: formatOutput(formatted, toFormat || 'json') });
      }

      case 'minify': {
        const parsed = parseInput(input, fromFormat);
        return jsonResponse(res, 200, { result: JSON.stringify(parsed) });
      }

      case 'validate': {
        try {
          const parsed = parseInput(input, fromFormat);
          let schemaErrors = [];
          if (schema) {
            const schemaObj = typeof schema === 'string' ? JSON.parse(schema) : schema;
            const validate = ajv.compile(schemaObj);
            const valid = validate(parsed);
            if (!valid && validate.errors) {
              schemaErrors = validate.errors.map(e => ({
                path: e.instancePath || '/',
                message: e.message
              }));
            }
          }
          return jsonResponse(res, 200, { valid: true, type: getType(parsed), schemaErrors });
        } catch (e) {
          return jsonResponse(res, 200, { valid: false, error: e.message });
        }
      }

      case 'escape': {
        return jsonResponse(res, 200, { result: JSON.stringify(input) });
      }

      case 'unescape': {
        const unescaped = JSON.parse(input);
        return jsonResponse(res, 200, { result: typeof unescaped === 'string' ? unescaped : JSON.stringify(unescaped, null, 2) });
      }

      case 'keys': {
        const parsed = parseInput(input, fromFormat);
        return jsonResponse(res, 200, { keys: extractKeys(parsed) });
      }

      case 'values': {
        const parsed = parseInput(input, fromFormat);
        return jsonResponse(res, 200, { values: extractValues(parsed) });
      }

      case 'flatten': {
        const parsed = parseInput(input, fromFormat);
        return jsonResponse(res, 200, { result: JSON.stringify(flattenJSON(parsed), null, 2) });
      }

      case 'diff': {
        const a = parseInput(inputA, fromFormat);
        const b = parseInput(inputB, fromFormat);
        const patches = fjp.compare(a, b);
        return jsonResponse(res, 200, {
          diff: patches,
          summary: {
            added: patches.filter(p => p.op === 'add').length,
            removed: patches.filter(p => p.op === 'remove').length,
            replaced: patches.filter(p => p.op === 'replace').length,
            identical: patches.length === 0
          }
        });
      }

      case 'convert': {
        const parsed = parseInput(input, fromFormat || 'json');
        let converted;
        switch (toFormat) {
          case 'yaml': converted = yaml.dump(parsed); break;
          case 'xml': converted = jsonToXml(parsed); break;
          case 'toml': converted = jsonToToml(parsed); break;
          case 'json': converted = JSON.stringify(parsed, null, 2); break;
          default: converted = JSON.stringify(parsed, null, 2);
        }
        return jsonResponse(res, 200, { result: converted });
      }

      case 'parse-path': {
        const parsed = parseInput(input, fromFormat);
        const { path } = req.body;
        try {
          const value = path.split('.').reduce((obj, key) => {
            const numKey = /^\d+$/.test(key) ? parseInt(key) : key;
            return obj?.[numKey];
          }, parsed);
          return jsonResponse(res, 200, { value, found: value !== undefined });
        } catch {
          return jsonResponse(res, 200, { value: null, found: false, error: 'Invalid path' });
        }
      }

      default:
        return jsonResponse(res, 400, { error: `Unknown action: ${action}` });
    }
  } catch (err) {
    return jsonResponse(res, 500, { error: err.message || 'Internal server error' });
  }
};

function parseInput(input, format) {
  if (!input) throw new Error('Input is required');
  switch (format) {
    case 'yaml': return yaml.load(input);
    case 'json':
    default: return JSON.parse(input);
  }
}

function formatOutput(jsonStr, format) {
  switch (format) {
    case 'yaml': return yaml.dump(JSON.parse(jsonStr));
    case 'json':
    default: return jsonStr;
  }
}

function getType(val) {
  if (val === null) return 'null';
  if (Array.isArray(val)) return 'array';
  return typeof val;
}

function extractKeys(obj, prefix = '', keys = []) {
  if (typeof obj !== 'object' || obj === null) return keys;
  for (const [key, value] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${key}` : key;
    keys.push(path);
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      extractKeys(value, path, keys);
    }
  }
  return keys;
}

function extractValues(obj, values = []) {
  if (obj === null || typeof obj !== 'object') return values;
  for (const value of Object.values(obj)) {
    if (typeof value === 'object' && value !== null) {
      extractValues(value, values);
    } else {
      values.push(value);
    }
  }
  return values;
}

function flattenJSON(obj, prefix = '', result = {}) {
  for (const [key, value] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      flattenJSON(value, path, result);
    } else {
      result[path] = value;
    }
  }
  return result;
}

function jsonToXml(obj, rootName = 'root') {
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<${rootName}>`;
  function serialize(obj, indent = '  ') {
    if (typeof obj !== 'object' || obj === null) return String(obj);
    let result = '\n';
    for (const [key, value] of Object.entries(obj)) {
      const tag = key.replace(/[^a-zA-Z0-9_-]/g, '_');
      if (Array.isArray(value)) {
        for (const item of value) {
          result += `${indent}<${tag}>${typeof item === 'object' ? serialize(item, indent + '  ') : item}</${tag}>\n`;
        }
      } else if (typeof value === 'object' && value !== null) {
        result += `${indent}<${tag}>${serialize(value, indent + '  ')}${indent}</${tag}>\n`;
      } else {
        result += `${indent}<${tag}>${value}</${tag}>\n`;
      }
    }
    return result;
  }
  xml += serialize(obj);
  xml += `</${rootName}>`;
  return xml;
}

function jsonToToml(obj, prefix = '') {
  const lines = [];
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (Array.isArray(value)) {
      lines.push(`${fullKey} = [${value.map(v => typeof v === 'string' ? `"${v}"` : v).join(', ')}]`);
    } else if (typeof value === 'object' && value !== null) {
      lines.push(`\n[${fullKey}]`);
      lines.push(jsonToToml(value, fullKey));
    } else if (typeof value === 'boolean') {
      lines.push(`${fullKey} = ${value}`);
    } else if (typeof value === 'string') {
      lines.push(`${fullKey} = "${value}"`);
    } else {
      lines.push(`${fullKey} = ${value}`);
    }
  }
  return lines.join('\n');
}
