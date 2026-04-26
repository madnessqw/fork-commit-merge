function toCamelCase(str) {
  return str.replace(/[-_\s]+(.)?/g, (_, c) => c ? c.toUpperCase() : '');
}

function toSnakeCase(str) {
  return str.replace(/([a-z0-9])([A-Z])/g, '$1_$2')
             .replace(/[-\s]+/g, '_')
             .toLowerCase();
}

function toKebabCase(str) {
  return str.replace(/([a-z0-9])([A-Z])/g, '$1-$2')
             .replace(/[_\s]+/g, '-')
             .toLowerCase();
}

function toPascalCase(str) {
  return str.replace(/[-_\s]+(.)?/g, (_, c) => c ? c.toUpperCase() : '')
            .replace(/^(.)/, (_, c) => c.toUpperCase());
}

function toConstantCase(str) {
  return toSnakeCase(str).toUpperCase();
}

function toDotCase(str) {
  return toSnakeCase(str).replace(/_/g, '.');
}

function toPathCase(str) {
  return toKebabCase(str).replace(/-/g, '/');
}

function toTitleCase(str) {
  return str.replace(/\w\S*/g, (txt) =>
    txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  );
}

function toSentenceCase(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

const CONVERTERS = {
  camelCase: toCamelCase,
  snake_case: toSnakeCase,
  kebab_case: toKebabCase,
  PascalCase: toPascalCase,
  CONSTANT_CASE: toConstantCase,
  dot.case: toDotCase,
  path_case: toPathCase,
  Title_Case: toTitleCase,
  Sentence_case: toSentenceCase,
};

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { text, targetCase } = req.body || {};

    if (!text) return res.status(400).json({ error: 'text is required' });
    if (!targetCase) return res.status(400).json({ error: 'targetCase is required' });

    const converter = CONVERTERS[targetCase];
    if (!converter) {
      return res.status(400).json({
        error: 'Invalid targetCase',
        validCases: Object.keys(CONVERTERS)
      });
    }

    const result = converter(String(text));
    return res.status(200).json({ result, targetCase, original: text });
  } catch (err) {
    return res.status(500).json({ error: 'Conversion failed', details: err.message });
  }
};
