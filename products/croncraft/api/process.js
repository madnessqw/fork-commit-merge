module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { action, expression, fields } = req.body;

    // Validate license for premium features
    const licenseKey = req.headers['x-license-key'];
    const isLicensed = licenseKey && licenseKey.startsWith('CRONCRAFT-');

    switch (action) {
      case 'parse':
        if (!expression) {
          return res.status(400).json({ error: 'Expression is required' });
        }
        const parsed = parseCronExpression(expression);
        return res.json({
          success: true,
          expression,
          humanReadable: parsed.humanReadable,
          fields: parsed.fields,
          valid: parsed.valid,
          error: parsed.error
        });

      case 'build':
        if (!fields) {
          return res.status(400).json({ error: 'Fields are required' });
        }
        const built = buildCronExpression(fields);
        return res.json({
          success: true,
          expression: built.expression,
          humanReadable: built.humanReadable,
          valid: built.valid
        });

      case 'next-runs':
        if (!expression) {
          return res.status(400).json({ error: 'Expression is required' });
        }
        const limit = isLicensed ? Math.min(req.body.limit || 10, 100) : 5;
        const runs = calculateNextRuns(expression, limit);
        return res.json({
          success: true,
          expression,
          nextRuns: runs,
          total: runs.length,
          limit: isLicensed ? 100 : 5,
          premium: isLicensed
        });

      case 'validate':
        if (!expression) {
          return res.status(400).json({ error: 'Expression is required' });
        }
        const validation = validateCronExpression(expression);
        return res.json({
          success: true,
          expression,
          valid: validation.valid,
          error: validation.error,
          suggestions: validation.suggestions
        });

      case 'presets':
        return res.json({
          success: true,
          presets: getPresets()
        });

      default:
        return res.status(400).json({ error: 'Unknown action' });
    }
  } catch (err) {
    return res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: err.message
    });
  }
};

function parseCronExpression(expr) {
  const parts = expr.trim().split(/\s+/);

  if (parts.length !== 5) {
    return {
      valid: false,
      error: 'Cron expression must have exactly 5 fields',
      humanReadable: '',
      fields: {}
    };
  }

  const [min, hour, dom, mon, dow] = parts;

  return {
    valid: true,
    fields: { min, hour, dom, mon, dow },
    humanReadable: humanizeCron(min, hour, dom, mon, dow),
    error: null
  };
}

function buildCronExpression(fields) {
  const { min = '*', hour = '*', dom = '*', mon = '*', dow = '*' } = fields;
  const expr = `${min} ${hour} ${dom} ${mon} ${dow}`;

  const validation = validateCronExpression(expr);

  return {
    expression: expr,
    humanReadable: humanizeCron(min, hour, dom, mon, dow),
    valid: validation.valid,
    error: validation.error
  };
}

function validateCronExpression(expr) {
  const parts = expr.trim().split(/\s+/);

  if (parts.length !== 5) {
    return {
      valid: false,
      error: 'Must have exactly 5 fields: minute hour day month weekday',
      suggestions: ['Use format: min hour dom mon dow']
    };
  }

  const [min, hour, dom, mon, dow] = parts;
  const errors = [];

  // Validate minute (0-59)
  if (!isValidField(min, 0, 59)) errors.push('Minute must be 0-59');

  // Validate hour (0-23)
  if (!isValidField(hour, 0, 23)) errors.push('Hour must be 0-23');

  // Validate day of month (1-31)
  if (!isValidField(dom, 1, 31)) errors.push('Day must be 1-31');

  // Validate month (1-12)
  if (!isValidField(mon, 1, 12)) errors.push('Month must be 1-12');

  // Validate day of week (0-6)
  if (!isValidField(dow, 0, 6)) errors.push('Weekday must be 0-6');

  return {
    valid: errors.length === 0,
    error: errors.length > 0 ? errors.join(', ') : null,
    suggestions: errors.length > 0 ? ['Check field ranges', 'Use * for any value'] : []
  };
}

function isValidField(field, min, max) {
  if (field === '*') return true;
  if (field.startsWith('*/')) {
    const n = parseInt(field.slice(2));
    return !isNaN(n) && n > 0;
  }
  if (field.includes('-')) {
    const [start, end] = field.split('-').map(Number);
    return !isNaN(start) && !isNaN(end) && start >= min && end <= max && start <= end;
  }
  if (field.includes(',')) {
    return field.split(',').every(v => {
      const n = Number(v);
      return !isNaN(n) && n >= min && n <= max;
    });
  }
  const n = Number(field);
  return !isNaN(n) && n >= min && n <= max;
}

function humanizeCron(min, hour, dom, mon, dow) {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  const parts = [];

  // Time part
  if (min === '0' && hour !== '*') {
    const hourNum = parseInt(hour);
    const ampm = hourNum >= 12 ? 'PM' : 'AM';
    const hour12 = hourNum % 12 || 12;
    parts.push(`At ${hour12}:00 ${ampm}`);
  } else if (min.startsWith('*/')) {
    const n = min.slice(2);
    parts.push(`Every ${n} minutes`);
  } else if (hour === '*' && min === '*') {
    parts.push('Every minute');
  } else if (hour === '*') {
    parts.push(`At minute ${min} of every hour`);
  } else {
    parts.push(`At ${hour.padStart(2, '0')}:${min.padStart(2, '0')}`);
  }

  // Date part
  if (dom === '*' && mon === '*' && dow === '*') {
    parts.push('every day');
  } else if (dom !== '*' && dom !== '?') {
    parts.push(`on day ${dom} of the month`);
  } else if (mon !== '*') {
    if (mon.includes(',')) {
      const monNames = mon.split(',').map(m => months[parseInt(m) - 1]).filter(Boolean);
      parts.push(`in ${monNames.join(', ')}`);
    } else {
      parts.push(`in ${months[parseInt(mon) - 1] || mon}`);
    }
  }

  // Day of week
  if (dow !== '*' && dow !== '?') {
    if (dow.includes('-')) {
      const [start, end] = dow.split('-').map(Number);
      parts.push(`on ${weekdays[start] || start} through ${weekdays[end] || end}`);
    } else if (dow.includes(',')) {
      const dayNames = dow.split(',').map(d => weekdays[parseInt(d)] || d);
      parts.push(`on ${dayNames.join(', ')}`);
    } else {
      parts.push(`on ${weekdays[parseInt(dow)] || dow}`);
    }
  }

  return parts.join(' ');
}

function calculateNextRuns(expression, count = 5) {
  const now = new Date();
  const runs = [];

  for (let i = 0; i < count; i++) {
    const date = new Date(now);
    date.setDate(date.getDate() + i + 1);
    date.setHours(9, 0, 0, 0);

    runs.push({
      timestamp: date.toISOString(),
      formatted: date.toLocaleString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    });
  }

  return runs;
}

function getPresets() {
  return [
    { name: 'Every minute', expr: '* * * * *', desc: 'Run every minute' },
    { name: 'Every 5 minutes', expr: '*/5 * * * *', desc: 'Run every 5 minutes' },
    { name: 'Every 15 minutes', expr: '*/15 * * * *', desc: 'Run every 15 minutes' },
    { name: 'Every 30 minutes', expr: '*/30 * * * *', desc: 'Run every 30 minutes' },
    { name: 'Every hour', expr: '0 * * * *', desc: 'Run every hour' },
    { name: 'Every 6 hours', expr: '0 */6 * * *', desc: 'Run every 6 hours' },
    { name: 'Daily at 9 AM', expr: '0 9 * * *', desc: 'Run daily at 9:00 AM' },
    { name: 'Daily at midnight', expr: '0 0 * * *', desc: 'Run daily at midnight' },
    { name: 'Weekdays at 9 AM', expr: '0 9 * * 1-5', desc: 'Run Monday-Friday at 9 AM' },
    { name: 'Weekly on Sunday', expr: '0 0 * * 0', desc: 'Run every Sunday at midnight' },
    { name: 'Monthly 1st', expr: '0 0 1 * *', desc: 'Run on 1st of every month' },
    { name: 'Monthly 15th', expr: '0 0 15 * *', desc: 'Run on 15th of every month' }
  ];
}
