/**
 * Function Call Debugger API
 * Debug and trace function calls with detailed analytics
 */

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { code, function: fnString, args, mode } = req.body || {};

  // Demo mode - no license required
  const isDemo = req.body?.demo || !req.headers['x-license-key'];

  if (!code && !fnString) {
    return res.status(400).json({
      error: 'Missing required field: code or function',
      example: { code: 'console.log("Hello")', args: [] }
    });
  }

  try {
    const startTime = performance.now();

    let result = null;
    let logs = [];
    let error = null;

    // Capture console.log output
    const originalLog = console.log;
    const originalError = console.error;
    const capturedLogs = [];

    console.log = (...args) => {
      capturedLogs.push({ type: 'log', message: args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ') });
      originalLog.apply(console, args);
    };
    console.error = (...args) => {
      capturedLogs.push({ type: 'error', message: args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ') });
      originalError.apply(console, args);
    };

    try {
      // Execute the code
      if (code) {
        // Create a function from the code string
        const fn = new Function(code);
        result = fn();
      } else if (fnString && args) {
        // Parse and execute function with arguments
        const fn = new Function(`return ${fnString}`)();
        result = fn(...args);
      }
    } catch (e) {
      error = e.message;
    } finally {
      // Restore console
      console.log = originalLog;
      console.error = originalError;
    }

    const endTime = performance.now();
    const executionTime = (endTime - startTime).toFixed(2);

    return res.status(200).json({
      success: !error,
      result: result !== undefined ? (typeof result === 'object' ? result : String(result)) : null,
      error,
      logs: capturedLogs,
      execution: {
        time: executionTime,
        timestamp: new Date().toISOString()
      },
      debug: {
        inputLength: (code || fnString || '').length,
        argsProvided: args ? args.length : 0
      }
    });
  } catch (e) {
    return res.status(500).json({ error: 'Execution failed', details: e.message });
  }
};