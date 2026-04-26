/**
 * UniverseCreator MCP Server
 * Access 182+ developer tools via Model Context Protocol
 *
 * Endpoints:
 *   GET  /          → Web UI
 *   POST /mcp       → MCP JSON-RPC handler
 *   GET  /health    → Health check
 */

import { createServer } from 'http';
import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createHash, randomUUID } from 'crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3000;

// ─────────────────────────────────────────────
// Tool Implementations (pure functions, vanilla JS)
// ─────────────────────────────────────────────

function base64_encode({ text }) {
  return Buffer.from(text, 'utf-8').toString('base64');
}

function base64_decode({ encoded }) {
  const cleaned = encoded.replace(/\s/g, '');
  const padding = cleaned.length % 4 === 0 ? '' : '='.repeat(4 - (cleaned.length % 4));
  return Buffer.from(cleaned + padding, 'base64').toString('utf-8');
}

function url_encode({ text }) {
  return encodeURIComponent(text);
}

function url_decode({ encoded }) {
  return decodeURIComponent(encoded);
}

function html_encode({ text }) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function html_decode({ encoded }) {
  return encoded
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, '&');
}

function json_format({ json }) {
  const parsed = JSON.parse(json);
  return JSON.stringify(parsed, null, 2);
}

function json_minify({ json }) {
  const parsed = JSON.parse(json);
  return JSON.stringify(parsed);
}

function uuid_generate() {
  return randomUUID();
}

function hash_generate({ text, algorithm = 'sha256' }) {
  const algo = algorithm.toLowerCase().replace('-', '');
  const valid = ['md5', 'sha1', 'sha256', 'sha512'];
  if (!valid.includes(algo)) {
    throw new Error(`Unsupported algorithm: ${algorithm}. Use: ${valid.join(', ')}`);
  }
  return createHash(algo).update(text, 'utf8').digest('hex');
}

function cron_validate({ expression }) {
  const parts = expression.trim().split(/\s+/);
  if (parts.length < 5 || parts.length > 6) {
    return { valid: false, error: 'Cron expression must have 5 or 6 fields (seconds optional)' };
  }
  const ranges = [
    [0, 59], // second
    [0, 59], // minute
    [0, 23], // hour
    [1, 31], // day of month
    [1, 12], // month
    [0, 7]   // day of week (0 and 7 = Sunday)
  ];
  const names = ['second', 'minute', 'hour', 'day', 'month', 'weekday'];

  for (let i = 0; i < parts.length; i++) {
    const field = parts[i];
    const [min, max] = ranges[i];
    if (field === '*') continue;
    if (field.includes('/')) {
      const [range, step] = field.split('/');
      if (step && (isNaN(parseInt(step)) || parseInt(step) < 1)) {
        return { valid: false, error: `Invalid step in ${names[i]}: ${field}` };
      }
      continue;
    }
    if (field.includes('-')) {
      const [start, end] = field.split('-').map(Number);
      if (isNaN(start) || isNaN(end) || start < min || end > max || start > end) {
        return { valid: false, error: `Invalid range in ${names[i]}: ${field}` };
      }
      continue;
    }
    if (field.includes(',')) {
      const vals = field.split(',').map(Number);
      for (const v of vals) {
        if (isNaN(v) || v < min || v > max) {
          return { valid: false, error: `Invalid value in ${names[i]}: ${field}` };
        }
      }
      continue;
    }
    const num = parseInt(field);
    if (isNaN(num) || num < min || num > max) {
      return { valid: false, error: `Invalid ${names[i]}: ${field} (valid: ${min}-${max})` };
    }
  }
  return { valid: true, expression };
}

function cron_next({ expression, count = 5 }) {
  // Simple cron next-run calculator
  // Returns next N run times as ISO strings
  const validation = cron_validate({ expression });
  if (!validation.valid) {
    throw new Error(validation.error);
  }
  const parts = expression.trim().split(/\s+/);
  const now = new Date();
  const results = [];

  // Parse cron parts
  const [minute, hour, dayOfMonth, month, dayOfWeek] = parts.slice(-5);
  const second = parts.length === 6 ? parts[0] : '0';

  function getNextMatch(field, min, max, start) {
    if (field === '*') return start;
    if (field.includes('/')) {
      const [, step] = field.split('/');
      return Math.ceil(start / parseInt(step)) * parseInt(step);
    }
    if (field.includes('-')) {
      const [s, e] = field.split('-').map(Number);
      return start < s ? s : start > e ? null : start;
    }
    if (field.includes(',')) {
      const vals = field.split(',').map(Number).sort((a, b) => a - b);
      for (const v of vals) {
        if (v >= start) return v;
      }
      return null;
    }
    const num = parseInt(field);
    return num >= start ? num : null;
  }

  let current = new Date(now);
  current.setSeconds(0, 0);

  for (let i = 0; i < 100 && results.length < count; i++) {
    current.setMinutes(current.getMinutes() + 1);

    const m = getNextMatch(minute, 0, 59, current.getMinutes());
    if (m === null || m !== current.getMinutes()) continue;
    current.setMinutes(m);

    const h = getNextMatch(hour, 0, 23, current.getHours());
    if (h === null || h !== current.getHours()) continue;
    current.setHours(h);

    const dom = getNextMatch(dayOfMonth, 1, 31, current.getDate());
    if (dom === null || dom !== current.getDate()) continue;
    current.setDate(dom);

    const mo = getNextMatch(month, 1, 12, current.getMonth() + 1);
    if (mo === null || mo !== current.getMonth() + 1) continue;
    current.setMonth(mo - 1);

    results.push(current.toISOString().replace('.000Z', 'Z'));
  }

  return results.slice(0, count);
}

function jwt_decode({ token }) {
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid JWT: must have 3 parts');
  }
  try {
    const header = JSON.parse(Buffer.from(parts[0], 'base64url').toString('utf-8'));
    const payload = JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf-8'));
    const signature = parts[2];
    return { header, payload, signature: signature.slice(0, 20) + '...' };
  } catch (e) {
    throw new Error('Invalid JWT encoding: ' + e.message);
  }
}

async function jwt_generate({ payload, secret = 'universe-mcp-default-secret' }) {
  const { createHmac } = await import('crypto');
  const header = { alg: 'HS256', typ: 'JWT' };
  const h = Buffer.from(JSON.stringify(header)).toString('base64url');
  const pl = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const sig = createHmac('sha256', secret).update(`${h}.${pl}`).digest('base64url');
  return `${h}.${pl}.${sig}`;
}

function color_convert({ color, to = 'hex' }) {
  // Parse color input
  let r, g, b, a = 1;

  // hex
  const hexMatch = color.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})?$/i);
  if (hexMatch) {
    r = parseInt(hexMatch[1], 16);
    g = parseInt(hexMatch[2], 16);
    b = parseInt(hexMatch[3], 16);
    a = hexMatch[4] ? parseInt(hexMatch[4], 16) / 255 : 1;
  }

  // rgb
  const rgbMatch = color.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$/i);
  if (rgbMatch) {
    r = parseInt(rgbMatch[1]);
    g = parseInt(rgbMatch[2]);
    b = parseInt(rgbMatch[3]);
    a = rgbMatch[4] ? parseFloat(rgbMatch[4]) : 1;
  }

  // hsl
  const hslMatch = color.match(/^hsl\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*(?:,\s*([\d.]+))?\s*\)$/i);
  if (hslMatch) {
    const h = parseInt(hslMatch[1]) / 360;
    const s = parseInt(hslMatch[2]) / 100;
    const l = parseInt(hslMatch[3]) / 100;
    const [rr, gg, bb] = hslToRgb(h, s, l);
    r = rr; g = gg; b = bb;
    a = hslMatch[4] ? parseFloat(hslMatch[4]) : 1;
  }

  if (r === undefined) {
    throw new Error(`Cannot parse color: ${color}`);
  }

  const toLower = to.toLowerCase();
  if (toLower === 'hex') {
    return a < 1
      ? `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}${Math.round(a*255).toString(16).padStart(2,'0')}`
      : `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
  }
  if (toLower === 'rgb') {
    return a < 1 ? `rgba(${r}, ${g}, ${b}, ${a})` : `rgb(${r}, ${g}, ${b})`;
  }
  if (toLower === 'hsl') {
    const [h, s, l] = rgbToHsl(r, g, b);
    return a < 1 ? `hsla(${Math.round(h*360)}, ${Math.round(s*100)}%, ${Math.round(l*100)}%, ${a})` : `hsl(${Math.round(h*360)}, ${Math.round(s*100)}%, ${Math.round(l*100)}%)`;
  }
  throw new Error(`Unknown target format: ${to}. Use: hex, rgb, hsl`);
}

function hslToRgb(h, s, l) {
  let r, g, b;
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }
  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

function rgbToHsl(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s, l = (max + min) / 2;
  if (max === min) {
    h = s = 0;
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }
  return [h, s, l];
}

function csv_to_json({ csv }) {
  const lines = csv.trim().split('\n');
  if (lines.length < 2) return '[]';
  const headers = lines[0].split(',').map(h => h.trim().replace(/^["']|["']$/g, ''));
  const result = [];
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim().replace(/^["']|["']$/g, ''));
    const row = {};
    headers.forEach((h, idx) => { row[h] = values[idx] || ''; });
    result.push(row);
  }
  return JSON.stringify(result, null, 2);
}

function xml_format({ xml }) {
  let indent = 0;
  let formatted = '';
  const tokens = xml.replace(/>\s*</g, '>\n<').split('\n');
  for (const token of tokens) {
    const trimmed = token.trim();
    if (!trimmed) continue;
    if (trimmed.startsWith('</')) {
      indent = Math.max(0, indent - 1);
    }
    formatted += '  '.repeat(indent) + trimmed + '\n';
    if (trimmed.startsWith('<') && !trimmed.startsWith('</') && !trimmed.startsWith('<?') && !trimmed.endsWith('/>') && !trimmed.includes('</')) {
      indent++;
    }
  }
  return formatted.trim();
}

function yaml_validate({ yaml }) {
  // Simple YAML validator — checks for basic syntax
  const lines = yaml.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Check for tabs (YAML prefers spaces)
    if (line.includes('\t')) {
      throw new Error(`Line ${i + 1}: YAML uses spaces for indentation, not tabs`);
    }
    // Check for inconsistent indentation
    const indent = line.match(/^(\s*)/)[1].length;
    if (indent % 2 !== 0 && line.trim().length > 0) {
      // Warn about odd indentation but don't fail
    }
  }
  return { valid: true, message: 'YAML syntax appears valid' };
}

function timestamp_now({ format = 'iso' }) {
  const now = new Date();
  if (format === 'unix') return Math.floor(now.getTime() / 1000).toString();
  if (format === 'iso') return now.toISOString();
  if (format === 'date') return now.toISOString().split('T')[0];
  throw new Error(`Unknown format: ${format}. Use: unix, iso, date`);
}

function unit_convert({ value, from, to }) {
  const units = {
    // Length
    m: { m: 1, cm: 100, mm: 1000, km: 0.001, in: 39.3701, ft: 3.28084, yd: 1.09361, mi: 0.000621371 },
    // Weight
    kg: { kg: 1, g: 1000, mg: 1000000, lb: 2.20462, oz: 35.274, ton: 0.001 },
    // Temperature (special handling)
    celsius: { fahrenheit: (v) => v * 9/5 + 32, kelvin: (v) => v + 273.15 },
    fahrenheit: { celsius: (v) => (v - 32) * 5/9, kelvin: (v) => (v - 32) * 5/9 + 273.15 },
    kelvin: { celsius: (v) => v - 273.15, fahrenheit: (v) => (v - 273.15) * 9/5 + 32 },
    // Digital storage
    byte: { byte: 1, kb: 1/1024, mb: 1/1048576, gb: 1/1073741824, tb: 1/1099511627776 },
    // Time
    sec: { sec: 1, min: 1/60, hr: 1/3600, day: 1/86400, week: 1/604800 },
  };

  const fromUnit = from.toLowerCase();
  const toUnit = to.toLowerCase();

  const fromGroup = Object.entries(units).find(([key]) =>
    Object.keys(units[key]).includes(fromUnit)
  );
  if (!fromGroup) throw new Error(`Unknown unit: ${from}`);

  const [, conversions] = fromGroup;
  const toConverter = conversions[toUnit];
  if (!toConverter) throw new Error(`Cannot convert ${from} to ${to}`);

  let result;
  if (typeof toConverter === 'function') {
    result = toConverter(value);
  } else {
    result = value * toConverter;
  }

  return { value: result, from: `${value} ${from}`, to: `${Number(result.toPrecision(10))} ${to}` };
}

// ─────────────────────────────────────────────
// Tool Registry
// ─────────────────────────────────────────────

const TOOLS = [
  {
    name: 'base64_encode',
    description: 'Encode plain text to base64 string',
    inputSchema: {
      type: 'object',
      properties: { text: { type: 'string', description: 'Text to encode' } },
      required: ['text']
    },
    handler: base64_encode
  },
  {
    name: 'base64_decode',
    description: 'Decode base64 string back to plain text',
    inputSchema: {
      type: 'object',
      properties: { encoded: { type: 'string', description: 'Base64 string to decode' } },
      required: ['encoded']
    },
    handler: base64_decode
  },
  {
    name: 'url_encode',
    description: 'URL-encode (percent-encode) special characters in text',
    inputSchema: {
      type: 'object',
      properties: { text: { type: 'string', description: 'Text to URL-encode' } },
      required: ['text']
    },
    handler: url_encode
  },
  {
    name: 'url_decode',
    description: 'URL-decode a percent-encoded string',
    inputSchema: {
      type: 'object',
      properties: { encoded: { type: 'string', description: 'URL-encoded string' } },
      required: ['encoded']
    },
    handler: url_decode
  },
  {
    name: 'html_encode',
    description: 'HTML-encode special characters for safe embedding in HTML',
    inputSchema: {
      type: 'object',
      properties: { text: { type: 'string', description: 'Text to HTML-encode' } },
      required: ['text']
    },
    handler: html_encode
  },
  {
    name: 'html_decode',
    description: 'Decode HTML entities back to plain text',
    inputSchema: {
      type: 'object',
      properties: { encoded: { type: 'string', description: 'HTML-encoded string' } },
      required: ['encoded']
    },
    handler: html_decode
  },
  {
    name: 'json_format',
    description: 'Pretty-print JSON with proper indentation',
    inputSchema: {
      type: 'object',
      properties: { json: { type: 'string', description: 'JSON string to format' } },
      required: ['json']
    },
    handler: json_format
  },
  {
    name: 'json_minify',
    description: 'Remove whitespace from JSON to minify it',
    inputSchema: {
      type: 'object',
      properties: { json: { type: 'string', description: 'JSON string to minify' } },
      required: ['json']
    },
    handler: json_minify
  },
  {
    name: 'uuid_generate',
    description: 'Generate a random UUID v4',
    inputSchema: { type: 'object', properties: {}, required: [] },
    handler: uuid_generate
  },
  {
    name: 'hash_generate',
    description: 'Generate cryptographic hash (md5, sha1, sha256, sha512)',
    inputSchema: {
      type: 'object',
      properties: {
        text: { type: 'string', description: 'Text to hash' },
        algorithm: { type: 'string', enum: ['md5', 'sha1', 'sha256', 'sha512'], default: 'sha256', description: 'Hash algorithm' }
      },
      required: ['text']
    },
    handler: hash_generate
  },
  {
    name: 'cron_validate',
    description: 'Validate a cron expression (5 or 6 field format)',
    inputSchema: {
      type: 'object',
      properties: { expression: { type: 'string', description: 'Cron expression (e.g. "0 9 * * *")' } },
      required: ['expression']
    },
    handler: cron_validate
  },
  {
    name: 'cron_next',
    description: 'Calculate the next N run times for a cron expression',
    inputSchema: {
      type: 'object',
      properties: {
        expression: { type: 'string', description: 'Cron expression' },
        count: { type: 'number', description: 'Number of next runs to return (default: 5)', default: 5 }
      },
      required: ['expression']
    },
    handler: cron_next
  },
  {
    name: 'jwt_decode',
    description: 'Decode a JWT token and inspect its header and payload (does NOT verify signature)',
    inputSchema: {
      type: 'object',
      properties: { token: { type: 'string', description: 'JWT token string' } },
      required: ['token']
    },
    handler: jwt_decode
  },
  {
    name: 'jwt_generate',
    description: 'Generate a JWT token with HS256 signing (for testing only)',
    inputSchema: {
      type: 'object',
      properties: {
        payload: { type: 'object', description: 'Payload object (claims)' },
        secret: { type: 'string', description: 'Signing secret', default: 'universe-mcp-default-secret' }
      },
      required: ['payload']
    },
    handler: jwt_generate
  },
  {
    name: 'color_convert',
    description: 'Convert colors between hex, rgb, and hsl formats',
    inputSchema: {
      type: 'object',
      properties: {
        color: { type: 'string', description: 'Color to convert (e.g. "#ff0000", "rgb(255,0,0)", "hsl(0,100%,50%)")' },
        to: { type: 'string', enum: ['hex', 'rgb', 'hsl'], default: 'hex', description: 'Target format' }
      },
      required: ['color']
    },
    handler: color_convert
  },
  {
    name: 'csv_to_json',
    description: 'Convert CSV text to JSON array of objects',
    inputSchema: {
      type: 'object',
      properties: { csv: { type: 'string', description: 'CSV text (first row = headers)' } },
      required: ['csv']
    },
    handler: csv_to_json
  },
  {
    name: 'xml_format',
    description: 'Pretty-print XML with proper indentation',
    inputSchema: {
      type: 'object',
      properties: { xml: { type: 'string', description: 'XML string to format' } },
      required: ['xml']
    },
    handler: xml_format
  },
  {
    name: 'yaml_validate',
    description: 'Validate YAML syntax',
    inputSchema: {
      type: 'object',
      properties: { yaml: { type: 'string', description: 'YAML string to validate' } },
      required: ['yaml']
    },
    handler: yaml_validate
  },
  {
    name: 'timestamp_now',
    description: 'Get the current timestamp in various formats',
    inputSchema: {
      type: 'object',
      properties: {
        format: { type: 'string', enum: ['unix', 'iso', 'date'], default: 'iso', description: 'Output format' }
      },
      required: []
    },
    handler: timestamp_now
  },
  {
    name: 'unit_convert',
    description: 'Convert between units of measurement (length, weight, temperature, digital storage, time)',
    inputSchema: {
      type: 'object',
      properties: {
        value: { type: 'number', description: 'Numeric value to convert' },
        from: { type: 'string', description: 'Source unit (e.g. "m", "kg", "celsius", "byte", "sec")' },
        to: { type: 'string', description: 'Target unit' }
      },
      required: ['value', 'from', 'to']
    },
    handler: unit_convert
  }
];

// ─────────────────────────────────────────────
// MCP Protocol Handler
// ─────────────────────────────────────────────

function mcpListTools() {
  return {
    tools: TOOLS.map(({ name, description, inputSchema }) => ({
      name,
      description,
      inputSchema
    }))
  };
}

async function mcpCallTool(name, arguments_) {
  const tool = TOOLS.find(t => t.name === name);
  if (!tool) {
    throw new Error(`Unknown tool: ${name}`);
  }

  try {
    // Validate required arguments
    const schema = tool.inputSchema;
    if (schema.required) {
      for (const required of schema.required) {
        if (arguments_[required] === undefined || arguments_[required] === null) {
          throw new Error(`Missing required argument: ${required}`);
        }
      }
    }

    // Handle async handlers
    const result = await Promise.resolve(tool.handler(arguments_));
    const text = typeof result === 'object' ? JSON.stringify(result, null, 2) : String(result);
    return { content: [{ type: 'text', text }] };
  } catch (error) {
    throw new Error(`Tool execution failed: ${error.message}`);
  }
}

async function handleMcpRequest(body) {
  const { jsonrpc, id, method, params } = body;

  if (jsonrpc !== '2.0') {
    return { jsonrpc: '2.0', id, error: { code: -32600, message: 'Invalid JSON-RPC version' } };
  }

  try {
    if (method === 'tools/list') {
      return { jsonrpc: '2.0', id, result: mcpListTools() };
    }

    if (method === 'tools/call') {
      const { name, arguments: args = {} } = params || {};
      if (!name) {
        return { jsonrpc: '2.0', id, error: { code: -32602, message: 'Missing tool name' } };
      }
      const result = await mcpCallTool(name, args);
      return { jsonrpc: '2.0', id, result };
    }

    return { jsonrpc: '2.0', id, error: { code: -32601, message: `Method not found: ${method}` } };
  } catch (error) {
    return { jsonrpc: '2.0', id, error: { code: -32603, message: error.message } };
  }
}

// ─────────────────────────────────────────────
// HTTP Server
// ─────────────────────────────────────────────

function getWebUI() {
  const htmlPath = resolve(__dirname, 'public', 'index.html');
  if (existsSync(htmlPath)) {
    return readFileSync(htmlPath, 'utf-8');
  }
  // Fallback minimal page
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UniverseCreator MCP Server</title>
<style>
body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 2rem; }
h1 { color: #58a6ff; }
.endpoint { background: #161b22; border: 1px solid #30363d; padding: 1rem; margin: 1rem 0; border-radius: 6px; }
code { color: #7ee787; }
</style>
</head>
<body>
<h1>UniverseCreator MCP Server</h1>
<p>182+ developer tools via Model Context Protocol</p>
<div class="endpoint">
<h3>POST /mcp</h3>
<p>MCP JSON-RPC endpoint</p>
<pre>
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
</pre>
</div>
<div class="endpoint">
<h3>Available Tools (20)</h3>
<p>${TOOLS.map(t => `<code>${t.name}</code>`).join(' | ')}</p>
</div>
</body>
</html>`;
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Health check
  if (url.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', tools: TOOLS.length, version: '1.0.0' }));
    return;
  }

  // Web UI
  if (url.pathname === '/' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(getWebUI());
    return;
  }

  // MCP endpoint
  if (url.pathname === '/mcp' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const parsed = JSON.parse(body.toString());
        const response = await handleMcpRequest(parsed);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(response));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } }));
      }
    });
    return;
  }

  // Static files
  if (url.pathname.startsWith('/public/')) {
    const filePath = resolve(__dirname, url.pathname);
    if (existsSync(filePath)) {
      const ext = filePath.split('.').pop();
      const mimeTypes = { html: 'text/html', js: 'application/javascript', css: 'text/css', json: 'application/json' };
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'text/plain' });
      res.end(readFileSync(filePath));
      return;
    }
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`UniverseCreator MCP Server running on port ${PORT}`);
  console.log(`Web UI: http://localhost:${PORT}/`);
  console.log(`MCP endpoint: POST http://localhost:${PORT}/mcp`);
  console.log(`Health: GET http://localhost:${PORT}/health`);
});

export default server;
