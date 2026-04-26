module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { code, language, options = {} } = req.body;

  if (!code || !language) {
    return res.status(400).json({ error: 'Code and language are required' });
  }

  try {
    // Basic formatting for demonstration
    const formatted = formatCode(code, language, options);

    res.json({
      success: true,
      formatted,
      language,
      originalLength: code.length,
      formattedLength: formatted.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

function formatCode(code, language, options) {
  // Basic formatting rules (in production, use proper formatters like prettier)
  let formatted = code;

  // Remove multiple empty lines
  formatted = formatted.replace(/\\n{3,}/g, '\\n\\n');

  // Basic indentation based on language
  switch (language.toLowerCase()) {
    case 'javascript':
    case 'typescript':
    case 'js':
    case 'ts':
      formatted = formatJavaScript(formatted, options);
      break;
    case 'python':
    case 'py':
      formatted = formatPython(formatted, options);
      break;
    case 'css':
    case 'scss':
    case 'sass':
      formatted = formatCSS(formatted, options);
      break;
    case 'html':
      formatted = formatHTML(formatted, options);
      break;
    case 'json':
      try {
        const parsed = JSON.parse(formatted);
        formatted = JSON.stringify(parsed, null, options.indentSize || 2);
      } catch {
        // Keep original if invalid JSON
      }
      break;
    case 'sql':
      formatted = formatSQL(formatted, options);
      break;
    default:
      // Generic formatting
      formatted = formatGeneric(formatted, options);
  }

  return formatted;
}

function formatJavaScript(code, options) {
  const indent = ' '.repeat(options.indentSize || 2);

  // Add semicolons if missing (optional)
  if (options.semi !== false) {
    code = code.replace(/([^;{}\\s])\\n/g, '$1;\\n');
  }

  // Basic brace formatting
  code = code.replace(/\\{\\s*/g, ' {\\n');
  code = code.replace(/\\s*\\}/g, '\\n}');

  return code;
}

function formatPython(code, options) {
  // Ensure proper indentation for Python
  const lines = code.split('\\n');
  let indentLevel = 0;
  const indent = ' '.repeat(options.indentSize || 4);

  return lines.map(line => {
    const stripped = line.trim();
    if (stripped.endsWith(':')) {
      const result = indent.repeat(indentLevel) + stripped;
      indentLevel++;
      return result;
    } else if (stripped === '' || stripped.startsWith('#')) {
      return line;
    } else if (indentLevel > 0 && stripped !== '') {
      return indent.repeat(indentLevel) + stripped;
    }
    return stripped;
  }).join('\\n');
}

function formatCSS(code, options) {
  // Format CSS properties
  code = code.replace(/\\s*{/g, ' {\\n  ');
  code = code.replace(/;\\s*/g, ';\\n  ');
  code = code.replace(/\\s*}/g, '\\n}\\n');
  return code;
}

function formatHTML(code, options) {
  // Basic HTML formatting
  const indent = ' '.repeat(options.indentSize || 2);
  let formatted = '';
  let indentLevel = 0;

  // Simple tag-based formatting
  const tokens = code.split(/(<[^>]+>)/g);
  tokens.forEach(token => {
    if (token.startsWith('</')) indentLevel--;
    formatted += indent.repeat(Math.max(0, indentLevel)) + token.trim() + '\\n';
    if (token.startsWith('<') && !token.startsWith('</') && !token.endsWith('/>')) indentLevel++;
  });

  return formatted;
}

function formatSQL(code, options) {
  const keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'GROUP BY', 'ORDER BY', 'HAVING', 'INSERT', 'UPDATE', 'DELETE'];

  let formatted = code;
  keywords.forEach(keyword => {
    const regex = new RegExp(`\\\\b${keyword}\\\\b`, 'gi');
    formatted = formatted.replace(regex, `\\n${keyword}`);
  });

  return formatted;
}

function formatGeneric(code, options) {
  // Remove trailing whitespace
  return code.split('\\n').map(line => line.trimEnd()).join('\\n');
}
