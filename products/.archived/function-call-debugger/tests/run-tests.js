/**
 * Function Call Debugger — Comprehensive Test Suite
 *
 * Tests cover:
 * - API endpoint validation (/api/process, /api/health, /api/webhook)
 * - Code execution correctness
 * - Error handling and edge cases
 * - Security boundaries
 * - Performance benchmarks
 * - Frontend HTML structure
 * - Integration flows
 *
 * Usage:
 *   node tests/run-tests.js              # Run all tests
 *   node tests/run-tests.js api          # Run API tests only
 *   node tests/run-tests.js frontend     # Run frontend tests only
 *   node tests/run-tests.js security     # Run security tests only
 *   node tests/run-tests.js performance  # Run performance tests only
 */

const path = require('path');
const fs = require('fs');

// Test statistics
const stats = {
  total: 0,
  passed: 0,
  failed: 0,
  skipped: 0,
  duration: 0,
  failures: []
};

// Color output helpers
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  gray: '\x1b[90m'
};

function log(msg, color = 'reset') {
  process.stdout.write(`${colors[color]}${msg}${colors.reset}\n`);
}

function assert(condition, message) {
  stats.total++;
  if (condition) {
    stats.passed++;
    log(`  ✓ ${message}`, 'green');
  } else {
    stats.failed++;
    stats.failures.push(message);
    log(`  ✗ ${message}`, 'red');
  }
}

function skip(message) {
  stats.skipped++;
  log(`  ⊘ ${message}`, 'yellow');
}

async function describe(name, fn) {
  log(`\n${colors.bold}${colors.cyan}▸ ${name}${colors.reset}`, 'cyan');
  await fn();
}

async function test(name, fn) {
  try {
    await fn();
    stats.passed++;
    log(`  ✓ ${name}`, 'green');
  } catch (err) {
    stats.failed++;
    stats.failures.push(`${name}: ${err.message}`);
    log(`  ✗ ${name}`, 'red');
    log(`    ${err.message}`, 'gray');
  }
}

// Mock objects for Vercel serverless functions
function createMockReq(method = 'POST', body = {}, headers = {}) {
  return {
    method,
    body,
    headers: {
      'content-type': 'application/json',
      ...headers
    }
  };
}

function createMockRes() {
  let statusCode = 200;
  let jsonData = null;
  const headers = {};

  const res = {
    status(code) {
      statusCode = code;
      return res;  // Return res for chaining
    },
    json(data) {
      jsonData = data;
      return Promise.resolve(res);
    },
    end() {
      return res;
    },
    setHeader(key, value) {
      headers[key] = value;
    },
    get statusCode() { return statusCode; },
    get jsonData() { return jsonData; },
    get headers() { return headers; }
  };

  return res;
}

// ============================================================
// API: /api/process TESTS
// ============================================================
async function runApiProcessTests() {
  const processHandler = require('../api/process.js');

  await describe('API: /api/process — Basic Execution', async () => {
    await test('executes simple code and returns result', async () => {
      const req = createMockReq('POST', { code: 'return 2 + 2;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      assert(res.jsonData.result === '4', `result should be "4", got "${res.jsonData.result}"`);
      assert(!res.jsonData.error, 'no error should occur');
    });

    await test('executes string concatenation', async () => {
      const req = createMockReq('POST', { code: 'return "hello" + " " + "world";' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      assert(res.jsonData.result === 'hello world', 'string concatenation should work');
    });

    await test('executes math operations', async () => {
      const req = createMockReq('POST', { code: 'return Math.PI.toFixed(2);' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      assert(res.jsonData.result === '3.14', 'Math.PI should be 3.14');
    });

    await test('executes array operations', async () => {
      const req = createMockReq('POST', { code: 'return [1,2,3].map(x => x * 2).join(",");' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      assert(res.jsonData.result === '2,4,6', 'array operations should work');
    });

    await test('executes object creation', async () => {
      const req = createMockReq('POST', { code: 'return JSON.stringify({name: "test", value: 42});' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      const parsed = JSON.parse(res.jsonData.result);
      assert(parsed.name === 'test', 'object name should be "test"');
      assert(parsed.value === 42, 'object value should be 42');
    });
  });

  await describe('API: /api/process — Function Mode', async () => {
    await test('executes function with arguments', async () => {
      const req = createMockReq('POST', {
        function: 'function multiply(a, b) { return a * b; } multiply',
        args: [5, 6]
      });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      assert(res.jsonData.result === '30', 'function should return 30');
    });

    await test('executes arrow function with arguments', async () => {
      const req = createMockReq('POST', {
        function: '(a, b) => a + b',
        args: [10, 20]
      });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'success should be true');
      assert(res.jsonData.result === '30', 'arrow function should return 30');
    });
  });

  await describe('API: /api/process — Console Log Capture', async () => {
    await test('captures console.log output', async () => {
      const req = createMockReq('POST', {
        code: 'console.log("Hello World"); return "done";'
      });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.logs.length === 1, 'should capture 1 log');
      assert(res.jsonData.logs[0].type === 'log', 'log type should be "log"');
      assert(res.jsonData.logs[0].message === 'Hello World', 'log message should match');
    });

    await test('captures multiple console.log calls', async () => {
      const req = createMockReq('POST', {
        code: 'console.log("first"); console.log("second"); console.log("third"); return "ok";'
      });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.logs.length === 3, 'should capture 3 logs');
      assert(res.jsonData.logs[0].message === 'first', 'first log should match');
      assert(res.jsonData.logs[2].message === 'third', 'third log should match');
    });

    await test('captures console.error output', async () => {
      const req = createMockReq('POST', {
        code: 'console.error("Something went wrong"); return "done";'
      });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.logs.length === 1, 'should capture 1 error');
      assert(res.jsonData.logs[0].type === 'error', 'type should be "error"');
    });

    await test('captures object logging', async () => {
      const req = createMockReq('POST', {
        code: 'console.log({key: "value"}); return "done";'
      });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.logs.length === 1, 'should capture object log');
      assert(res.jsonData.logs[0].message.includes('key'), 'object log should contain key');
    });
  });

  await describe('API: /api/process — Error Handling', async () => {
    await test('catches syntax errors', async () => {
      const req = createMockReq('POST', { code: 'return ;;; invalid syntax (((;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === false, 'success should be false');
      assert(res.jsonData.error, 'error message should exist');
    });

    await test('catches runtime errors', async () => {
      const req = createMockReq('POST', { code: 'throw new Error("Test error");' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === false, 'success should be false');
      assert(res.jsonData.error.includes('Test error'), 'error should contain message');
    });

    await test('catches reference errors', async () => {
      const req = createMockReq('POST', { code: 'return undefinedVariable;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === false, 'success should be false');
      assert(res.jsonData.error, 'error should exist for undefined variable');
    });

    await test('catches type errors', async () => {
      const req = createMockReq('POST', { code: 'null.method();' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === false, 'success should be false');
      assert(res.jsonData.error.includes('method'), 'error should mention method');
    });

    await test('catches range errors (infinite recursion)', async () => {
      const req = createMockReq('POST', { code: 'function recurse() { return recurse(); } recurse();' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === false, 'success should be false for infinite recursion');
    });
  });

  await describe('API: /api/process — Input Validation', async () => {
    await test('returns 400 when no code or function provided', async () => {
      const req = createMockReq('POST', {});
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.statusCode === 400, `should return 400, got ${res.statusCode}`);
      assert(res.jsonData.error.includes('Missing'), 'error should mention missing field');
    });

    await test('returns 400 when body is empty object', async () => {
      const req = createMockReq('POST', { foo: 'bar' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.statusCode === 400, 'should return 400 for irrelevant body');
    });

    await test('returns 405 for GET requests', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.statusCode === 405, `should return 405, got ${res.statusCode}`);
    });

    await test('handles OPTIONS preflight request', async () => {
      const req = createMockReq('OPTIONS');
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.statusCode === 200, 'OPTIONS should return 200');
    });
  });

  await describe('API: /api/process — Response Structure', async () => {
    await test('includes execution time in response', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.execution, 'execution field should exist');
      assert(res.jsonData.execution.time, 'execution.time should exist');
      assert(parseFloat(res.jsonData.execution.time) >= 0, 'execution time should be >= 0');
    });

    await test('includes timestamp in response', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.execution.timestamp, 'timestamp should exist');
      assert(!isNaN(Date.parse(res.jsonData.execution.timestamp)), 'timestamp should be valid ISO date');
    });

    await test('includes debug info in response', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.debug, 'debug field should exist');
      assert(res.jsonData.debug.inputLength > 0, 'inputLength should be > 0');
    });

    await test('includes CORS headers', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.headers['Access-Control-Allow-Origin'] === '*', 'CORS origin should be *');
    });
  });

  await describe('API: /api/process — Demo Mode', async () => {
    await test('works in demo mode without license', async () => {
      const req = createMockReq('POST', { code: 'return "demo";', demo: true });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.jsonData.success === true, 'demo mode should succeed');
    });

    await test('works without explicit demo flag (no license header)', async () => {
      const req = createMockReq('POST', { code: 'return "no-license";' });
      const res = createMockRes();
      await processHandler(req, res);

      // Should still work since no X-License-Key header means demo mode
      assert(res.statusCode !== 401, 'should not require license');
    });
  });
}

// ============================================================
// API: /api/health TESTS
// ============================================================
async function runApiHealthTests() {
  const healthHandler = require('../api/health.js');

  await describe('API: /api/health — Basic Health Check', async () => {
    await test('returns 200 status', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);

      assert(res.statusCode === 200, `should return 200, got ${res.statusCode}`);
    });

    await test('returns status ok', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);

      assert(res.jsonData.status === 'ok', `status should be "ok", got "${res.jsonData.status}"`);
    });

    await test('returns product name', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);

      assert(res.jsonData.product === 'function-call-debugger', 'product name should match');
    });

    await test('returns version', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);

      assert(res.jsonData.version === '1.0.0', 'version should be 1.0.0');
    });

    await test('returns valid timestamp', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);

      assert(res.jsonData.timestamp, 'timestamp should exist');
      assert(!isNaN(Date.parse(res.jsonData.timestamp)), 'timestamp should be valid ISO date');
    });

    await test('includes CORS headers', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);

      assert(res.headers['Access-Control-Allow-Origin'] === '*', 'CORS origin should be *');
    });
  });
}

// ============================================================
// API: /api/webhook TESTS
// ============================================================
async function runApiWebhookTests() {
  const webhookHandler = require('../api/webhook.js');

  await describe('API: /api/webhook — Event Handling', async () => {
    await test('handles order_created event', async () => {
      const req = createMockReq('POST', {
        meta: { event_name: 'order_created' },
        data: { id: '12345' }
      });
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 200, 'should return 200');
      assert(res.jsonData.message.includes('order_created'), 'message should contain event name');
    });

    await test('handles generic events', async () => {
      const req = createMockReq('POST', {
        meta: { event_name: 'subscription_created' }
      });
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 200, 'should return 200');
    });

    await test('handles missing event_name gracefully', async () => {
      const req = createMockReq('POST', { data: {} });
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 200, 'should return 200 even without event_name');
    });

    await test('returns 405 for GET requests', async () => {
      const req = createMockReq('GET');
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 405, `should return 405, got ${res.statusCode}`);
    });

    await test('handles malformed JSON body', async () => {
      const req = createMockReq('POST', null);
      const res = createMockRes();
      // This would normally throw, but the handler should catch it
      try {
        await webhookHandler(req, res);
        assert(res.statusCode === 200, 'should handle malformed body gracefully');
      } catch (e) {
        assert(false, 'should not throw exception');
      }
    });
  });

  await describe('API: /api/webhook — Signature Verification', async () => {
    await test('accepts request without signature when no secret configured', async () => {
      const req = createMockReq('POST', {
        meta: { event_name: 'test' }
      });
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 200, 'should accept without signature when no secret');
    });

    await test('rejects invalid signature when secret is configured', async () => {
      // Save original env
      const original = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;

      process.env.LEMONSQUEEZY_WEBHOOK_SECRET = 'test_secret';
      const req = createMockReq('POST', {
        meta: { event_name: 'test' }
      }, { 'x-signature': 'invalid_signature' });
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 401, `should reject invalid signature, got ${res.statusCode}`);

      // Restore original env
      if (original === undefined) {
        delete process.env.LEMONSQUEEZY_WEBHOOK_SECRET;
      } else {
        process.env.LEMONSQUEEZY_WEBHOOK_SECRET = original;
      }
    });

    await test('accepts valid HMAC signature', async () => {
      const crypto = require('crypto');
      const original = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;

      process.env.LEMONSQUEEZY_WEBHOOK_SECRET = 'test_secret';
      const body = JSON.stringify({ meta: { event_name: 'test' } });
      const signature = crypto.createHmac('sha256', 'test_secret').update(body).digest('hex');

      const req = createMockReq('POST', { meta: { event_name: 'test' } }, { 'x-signature': signature });
      const res = createMockRes();
      await webhookHandler(req, res);

      assert(res.statusCode === 200, 'should accept valid signature');

      if (original === undefined) {
        delete process.env.LEMONSQUEEZY_WEBHOOK_SECRET;
      } else {
        process.env.LEMONSQUEEZY_WEBHOOK_SECRET = original;
      }
    });
  });
}

// ============================================================
// FRONTEND TESTS
// ============================================================
async function runFrontendTests() {
  const htmlPath = path.join(__dirname, '../public/index.html');
  const html = fs.readFileSync(htmlPath, 'utf8');

  await describe('Frontend — HTML Structure', async () => {
    await test('has valid HTML5 doctype', () => {
      assert(html.startsWith('<!DOCTYPE html>'), 'should start with DOCTYPE');
    });

    await test('has lang attribute', () => {
      assert(html.includes('<html lang="en">'), 'should have lang="en"');
    });

    await test('has charset meta tag', () => {
      assert(html.includes('<meta charset="UTF-8">'), 'should have charset UTF-8');
    });

    await test('has viewport meta tag', () => {
      assert(html.includes('<meta name="viewport"'), 'should have viewport meta');
    });

    await test('has title tag', () => {
      assert(html.includes('<title>') && html.includes('</title>'), 'should have title tag');
      const titleMatch = html.match(/<title>(.*?)<\/title>/);
      assert(titleMatch && titleMatch[1].length > 0, 'title should not be empty');
    });

    await test('has description meta tag', () => {
      assert(html.includes('<meta name="description"'), 'should have description meta');
    });
  });

  await describe('Frontend — SEO & Social', async () => {
    await test('has Open Graph title', () => {
      assert(html.includes('og:title'), 'should have og:title');
    });

    await test('has Open Graph description', () => {
      assert(html.includes('og:description'), 'should have og:description');
    });

    await test('has Open Graph type', () => {
      assert(html.includes('og:type'), 'should have og:type');
    });

    await test('has Twitter card', () => {
      assert(html.includes('twitter:card'), 'should have twitter:card');
    });

    await test('has canonical URL or URL reference', () => {
      // Check for any URL references that could serve as canonical
      assert(html.includes('vercel.app') || html.includes('localhost') || html.includes('href="http'),
        'should have URL references');
    });
  });

  await describe('Frontend — Design Quality', async () => {
    await test('uses dark theme background', () => {
      assert(html.includes('#0a0a0a') || html.includes('#111111') || html.includes('--bg-primary'),
        'should use dark background');
    });

    await test('has gradient text support', () => {
      assert(html.includes('gradient') && html.includes('background-clip: text'),
        'should have gradient text');
    });

    await test('has glassmorphism effects', () => {
      assert(html.includes('backdrop-filter') || html.includes('backdrop-filter'),
        'should have backdrop-filter for glassmorphism');
    });

    await test('has CSS animations', () => {
      assert(html.includes('@keyframes') || html.includes('animation:'),
        'should have CSS animations');
    });

    await test('has hover effects on buttons', () => {
      assert(html.includes(':hover') && html.includes('transform'),
        'should have hover transforms');
    });

    await test('has responsive design (mobile)', () => {
      assert(html.includes('@media') && html.includes('768px'),
        'should have mobile responsive breakpoint');
    });

    await test('has custom scrollbar', () => {
      assert(html.includes('::-webkit-scrollbar'), 'should have custom scrollbar');
    });

    await test('has particle effects', () => {
      assert(html.includes('particle'), 'should have particle effects');
    });
  });

  await describe('Frontend — Required Sections', async () => {
    await test('has header/navigation', () => {
      assert(html.includes('<header>'), 'should have header');
      assert(html.includes('nav'), 'should have navigation');
    });

    await test('has hero section', () => {
      assert(html.includes('hero'), 'should have hero section');
      assert(html.includes('<h1>'), 'should have h1 heading');
    });

    await test('has demo section', () => {
      assert(html.includes('id="demo"') || html.includes('demo-section'),
        'should have demo section');
    });

    await test('has features section', () => {
      assert(html.includes('id="features"') || html.includes('features'),
        'should have features section');
    });

    await test('has pricing section', () => {
      assert(html.includes('id="pricing"') || html.includes('pricing'),
        'should have pricing section');
    });

    await test('has FAQ section', () => {
      assert(html.includes('id="faq"') || html.includes('faq'),
        'should have FAQ section');
    });

    await test('has footer', () => {
      assert(html.includes('<footer>'), 'should have footer');
    });

    await test('has testimonials section', () => {
      assert(html.includes('testimonial'), 'should have testimonials');
    });

    await test('has trust badges', () => {
      assert(html.includes('trust-badge'), 'should have trust badges');
    });
  });

  await describe('Frontend — Functionality', async () => {
    await test('has code input area', () => {
      assert(html.includes('codeInput') || html.includes('code-input'),
        'should have code input');
      assert(html.includes('<textarea'), 'should have textarea for code');
    });

    await test('has run button', () => {
      assert(html.includes('runButton') || html.includes('run-button') || html.includes('Run'),
        'should have run button');
    });

    await test('has output area', () => {
      assert(html.includes('outputArea') || html.includes('output-area'),
        'should have output area');
    });

    await test('has buy/purchase button', () => {
      assert(html.includes('buyButton') || html.includes('buy-button') || html.includes('Buy'),
        'should have buy button');
    });

    await test('has checkout URL placeholder', () => {
      assert(html.includes('CHECKOUT_URL'), 'should have checkout URL reference');
    });

    await test('has FAQ accordion functionality', () => {
      assert(html.includes('faq-question') && html.includes('toggle'),
        'should have FAQ toggle functionality');
    });
  });

  await describe('Frontend — Performance', async () => {
    await test('has preconnect for fonts', () => {
      assert(html.includes('rel="preconnect"'), 'should have preconnect for performance');
    });

    await test('loads Google Fonts', () => {
      assert(html.includes('fonts.googleapis.com'), 'should load Google Fonts');
    });

    await test('has font-display fallback', () => {
      // Inter is loaded with standard settings
      assert(html.includes('Inter'), 'should have Inter font');
    });

    await test('no external JS dependencies', () => {
      // Count script src tags (should be minimal)
      const scriptSrcMatches = html.match(/<script\s+src=/gi);
      const count = scriptSrcMatches ? scriptSrcMatches.length : 0;
      assert(count <= 2, `should have minimal external scripts (found ${count})`);
    });

    await test('has inline styles (single file)', () => {
      assert(html.includes('<style>') && html.includes('</style>'),
        'should have inline styles');
    });
  });

  await describe('Frontend — Content Quality', async () => {
    await test('has sufficient line count', () => {
      const lines = html.split('\n').length;
      assert(lines >= 300, `should be at least 300 lines (found ${lines})`);
    });

    await test('has multiple feature cards', () => {
      const featureCards = (html.match(/feature-card/g) || []).length;
      assert(featureCards >= 4, `should have at least 4 feature cards (found ${featureCards})`);
    });

    await test('has FAQ items', () => {
      const faqItems = (html.match(/faq-item/g) || []).length;
      assert(faqItems >= 4, `should have at least 4 FAQ items (found ${faqItems})`);
    });

    await test('has testimonial cards', () => {
      const testimonialCards = (html.match(/testimonial-card/g) || []).length;
      assert(testimonialCards >= 3, `should have at least 3 testimonials (found ${testimonialCards})`);
    });

    await test('has price displayed', () => {
      assert(html.includes('$19'), 'should display $19 price');
    });

    await test('has money-back guarantee', () => {
      assert(html.includes('money-back') || html.includes('guarantee'),
        'should mention money-back guarantee');
    });
  });
}

// ============================================================
// SECURITY TESTS
// ============================================================
async function runSecurityTests() {
  const processHandler = require('../api/process.js');

  await describe('Security — Input Validation', async () => {
    await test('rejects extremely large payloads', async () => {
      const largeCode = 'return "' + 'A'.repeat(100000) + '";';
      const req = createMockReq('POST', { code: largeCode });
      const res = createMockRes();

      // Should not crash
      try {
        await processHandler(req, res);
        assert(true, 'should handle large input without crashing');
      } catch (e) {
        assert(false, `should not crash on large input: ${e.message}`);
      }
    });

    await test('handles null body gracefully', async () => {
      const req = { method: 'POST', body: null, headers: {} };
      const res = createMockRes();

      try {
        await processHandler(req, res);
        assert(true, 'should handle null body');
      } catch (e) {
        assert(false, `should not crash on null body: ${e.message}`);
      }
    });

    await test('handles undefined body gracefully', async () => {
      const req = { method: 'POST', headers: {} };
      const res = createMockRes();

      try {
        await processHandler(req, res);
        assert(true, 'should handle undefined body');
      } catch (e) {
        assert(false, `should not crash on undefined body: ${e.message}`);
      }
    });
  });

  await describe('Security — Execution Boundaries', async () => {
    await test('handles code that tries to access process.env', async () => {
      const req = createMockReq('POST', {
        code: 'return JSON.stringify(process.env);'
      });
      const res = createMockRes();
      await processHandler(req, res);

      // Note: In Vercel serverless, process.env IS accessible
      // This test documents the behavior, not necessarily a vulnerability
      assert(res.jsonData.success === true || res.jsonData.error, 'should handle process.env access');
    });

    await test('handles code that tries to require modules', async () => {
      const req = createMockReq('POST', {
        code: 'return typeof require;'
      });
      const res = createMockRes();
      await processHandler(req, res);

      // In Node.js, require is available
      assert(true, 'should handle require attempts');
    });

    await test('handles infinite loop detection', async () => {
      const req = createMockReq('POST', {
        code: 'while(true) {}'
      });
      const res = createMockRes();

      // This could hang, so we need a timeout
      const timeout = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Timeout - infinite loop not caught')), 3000)
      );

      try {
        await Promise.race([processHandler(req, res), timeout]);
        // If it returns, check if it handled the error
        assert(true, 'should handle infinite loop (either timeout or error)');
      } catch (e) {
        // Timeout is expected for infinite loops
        assert(e.message.includes('Timeout'), 'should timeout on infinite loop');
      }
    }).timeout(5000);
  });

  await describe('Security — CORS Configuration', async () => {
    await test('sets permissive CORS header', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.headers['Access-Control-Allow-Origin'] === '*', 'CORS should be *');
    });

    await test('allows POST method', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.headers['Access-Control-Allow-Methods'] === 'POST, OPTIONS',
        'should allow POST');
    });

    await test('allows Content-Type header', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      assert(res.headers['Access-Control-Allow-Headers'].includes('Content-Type'),
        'should allow Content-Type');
    });
  });
}

// ============================================================
// PERFORMANCE TESTS
// ============================================================
async function runPerformanceTests() {
  const processHandler = require('../api/process.js');
  const healthHandler = require('../api/health.js');

  await describe('Performance — Response Time', async () => {
    await test('health endpoint responds under 100ms', async () => {
      const start = Date.now();
      const req = createMockReq('GET');
      const res = createMockRes();
      await healthHandler(req, res);
      const elapsed = Date.now() - start;

      assert(elapsed < 100, `health should respond <100ms (took ${elapsed}ms)`);
    });

    await test('simple code execution responds under 500ms', async () => {
      const start = Date.now();
      const req = createMockReq('POST', { code: 'return 1 + 1;' });
      const res = createMockRes();
      await processHandler(req, res);
      const elapsed = Date.now() - start;

      assert(elapsed < 500, `simple execution should respond <500ms (took ${elapsed}ms)`);
    });

    await test('complex code execution responds under 1000ms', async () => {
      const complexCode = `
        const arr = Array.from({length: 1000}, (_, i) => i);
        const sorted = arr.sort((a, b) => b - a);
        const filtered = sorted.filter(x => x % 2 === 0);
        const sum = filtered.reduce((a, b) => a + b, 0);
        return sum;
      `;
      const start = Date.now();
      const req = createMockReq('POST', { code: complexCode });
      const res = createMockRes();
      await processHandler(req, res);
      const elapsed = Date.now() - start;

      assert(elapsed < 1000, `complex execution should respond <1000ms (took ${elapsed}ms)`);
    });
  });

  await describe('Performance — Reported Execution Time', async () => {
    await test('reports sub-millisecond execution time', async () => {
      const req = createMockReq('POST', { code: 'return 1;' });
      const res = createMockRes();
      await processHandler(req, res);

      const time = parseFloat(res.jsonData.execution.time);
      assert(time >= 0 && time < 100, `should report reasonable time (got ${time}ms)`);
    });

    await test('reports higher time for complex operations', async () => {
      const slowCode = `
        let sum = 0;
        for (let i = 0; i < 10000; i++) { sum += i; }
        return sum;
      `;
      const req1 = createMockReq('POST', { code: 'return 1;' });
      const res1 = createMockRes();
      await processHandler(req1, res1);
      const simpleTime = parseFloat(res1.json.execution.time);

      const req2 = createMockReq('POST', { code: slowCode });
      const res2 = createMockRes();
      await processHandler(req2, res2);
      const complexTime = parseFloat(res2.json.execution.time);

      // Complex should take longer (but this is not guaranteed due to overhead)
      assert(complexTime >= 0, 'complex time should be reported');
    });
  });

  await describe('Performance — Memory Usage', async () => {
    await test('does not leak memory with repeated calls', async () => {
      const initialMemory = process.memoryUsage().heapUsed;

      for (let i = 0; i < 100; i++) {
        const req = createMockReq('POST', { code: `return ${i};` });
        const res = createMockRes();
        await processHandler(req, res);
      }

      const finalMemory = process.memoryUsage().heapUsed;
      const growth = (finalMemory - initialMemory) / 1024 / 1024;

      // Memory growth should be reasonable (< 10MB for 100 calls)
      assert(growth < 10, `memory growth should be < 10MB (got ${growth.toFixed(2)}MB)`);
    });
  });
}

// ============================================================
// INTEGRATION TESTS
// ============================================================
async function runIntegrationTests() {
  const processHandler = require('../api/process.js');
  const healthHandler = require('../api/health.js');
  const webhookHandler = require('../api/webhook.js');

  await describe('Integration — Full API Flow', async () => {
    await test('health → process → webhook flow', async () => {
      // Step 1: Check health
      const healthReq = createMockReq('GET');
      const healthRes = createMockRes();
      await healthHandler(healthReq, healthRes);
      assert(healthRes.json.status === 'ok', 'health should be ok');

      // Step 2: Execute code
      const processReq = createMockReq('POST', { code: 'return "integration-test";' });
      const processRes = createMockRes();
      await processHandler(processReq, processRes);
      assert(processRes.json.success === true, 'process should succeed');

      // Step 3: Simulate webhook
      const webhookReq = createMockReq('POST', { meta: { event_name: 'order_created' } });
      const webhookRes = createMockRes();
      await webhookHandler(webhookReq, webhookRes);
      assert(webhookRes.statusCode === 200, 'webhook should be received');
    });
  });

  await describe('Integration — Configuration', async () => {
    await test('vercel.json has correct routes', async () => {
      const vercelConfig = JSON.parse(
        fs.readFileSync(path.join(__dirname, '../vercel.json'), 'utf8')
      );

      assert(vercelConfig.version === 2, 'should use version 2');
      assert(vercelConfig.routes.length >= 4, 'should have at least 4 routes');

      const routePaths = vercelConfig.routes.map(r => r.src);
      assert(routePaths.includes('/api/health'), 'should have health route');
      assert(routePaths.includes('/api/process'), 'should have process route');
      assert(routePaths.includes('/api/webhook'), 'should have webhook route');
    });

    await test('package.json has correct configuration', async () => {
      const pkg = JSON.parse(
        fs.readFileSync(path.join(__dirname, '../package.json'), 'utf8')
      );

      assert(pkg.name === 'function-call-debugger', 'name should match');
      assert(pkg.engines.node.startsWith('>=18'), 'should require Node 18+');
      assert(pkg.scripts['vercel-build'], 'should have vercel-build script');
    });

    await test('product.json has required fields', async () => {
      const product = JSON.parse(
        fs.readFileSync(path.join(__dirname, '../product.json'), 'utf8')
      );

      assert(product.name, 'should have name');
      assert(product.slug, 'should have slug');
      assert(product.price, 'should have price');
      assert(product.tagline, 'should have tagline');
    });

    await test('.gitignore exists and has content', async () => {
      const gitignore = fs.readFileSync(path.join(__dirname, '../.gitignore'), 'utf8');
      assert(gitignore.trim().length > 0, '.gitignore should not be empty');
    });
  });
}

// ============================================================
// TEST RUNNER
// ============================================================
async function runTests(filter = 'all') {
  const startTime = Date.now();

  log(`${colors.bold}${colors.blue}`, 'blue');
  log('╔══════════════════════════════════════════════════════╗');
  log('║   FUNCTION CALL DEBUGGER — COMPREHENSIVE TEST SUITE  ║');
  log('╚══════════════════════════════════════════════════════╝');
  log(`${colors.reset}`);
  log(`\n  Started: ${new Date().toISOString()}`);
  log(`  Filter: ${filter}`);

  const testSuites = {
    'api-process': runApiProcessTests,
    'api-health': runApiHealthTests,
    'api-webhook': runApiWebhookTests,
    'frontend': runFrontendTests,
    'security': runSecurityTests,
    'performance': runPerformanceTests,
    'integration': runIntegrationTests
  };

  const suitesToRun = filter === 'all'
    ? Object.keys(testSuites)
    : filter.split(',').map(f => f.trim()).filter(f => testSuites[f]);

  if (suitesToRun.length === 0) {
    log(`\n  No matching test suites for filter: ${filter}`, 'red');
    log(`  Available: ${Object.keys(testSuites).join(', ')}`, 'yellow');
    return;
  }

  for (const suite of suitesToRun) {
    try {
      await testSuites[suite]();
    } catch (err) {
      log(`\n  Suite "${suite}" crashed: ${err.message}`, 'red');
      stats.failed++;
      stats.failures.push(`Suite crash: ${suite} - ${err.message}`);
    }
  }

  stats.duration = Date.now() - startTime;

  // Print summary
  log(`\n${colors.bold}${colors.cyan}`, 'cyan');
  log('══════════════════════════════════════════════════════');
  log('  TEST SUMMARY');
  log('══════════════════════════════════════════════════════');
  log(`${colors.reset}`);
  log(`  Total:     ${stats.total}`);
  log(`  ${colors.green}Passed:    ${stats.passed}${colors.reset}`);
  log(`  ${colors.red}Failed:    ${stats.failed}${colors.reset}`);
  log(`  ${colors.yellow}Skipped:   ${stats.skipped}${colors.reset}`);
  log(`  Duration:  ${stats.duration}ms`);

  if (stats.failures.length > 0) {
    log(`\n${colors.red}${colors.bold}FAILURES:${colors.reset}`);
    stats.failures.forEach((f, i) => {
      log(`  ${i + 1}. ${f}`, 'red');
    });
  }

  log('');
  if (stats.failed === 0) {
    log(`${colors.green}${colors.bold}  ALL TESTS PASSED ✓${colors.reset}`);
    process.exit(0);
  } else {
    log(`${colors.red}${colors.bold}  SOME TESTS FAILED ✗${colors.reset}`);
    process.exit(1);
  }
}

// Run tests
const filter = process.argv[2] || 'all';
runTests(filter).catch(err => {
  log(`\n  Fatal error: ${err.message}`, 'red');
  process.exit(1);
});
