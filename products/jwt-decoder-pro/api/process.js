/**
 * JWT Decoder Pro — Process API
 * Handles JWT decoding, signature verification, and claim validation
 */

const BASE64URLDecode = (str) => {
  // Replace URL-safe chars and add padding
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  const pad = str.length % 4;
  if (pad) {
    str += '='.repeat(4 - pad);
  }
  return atob(str);
};

const decodeBase64URL = (str) => {
  try {
    const decoded = BASE64URLDecode(str);
    return decodeURIComponent(
      decoded.split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')
    );
  } catch (e) {
    return null;
  }
};

const decodeJWT = (token) => {
  const parts = token.trim().split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid JWT format: expected 3 parts separated by dots');
  }

  const [headerB64, payloadB64, signatureB64] = parts;

  const headerStr = decodeBase64URL(headerB64);
  const payloadStr = decodeBase64URL(payloadB64);

  if (!headerStr || !payloadStr) {
    throw new Error('Failed to decode base64url segments');
  }

  let header;
  let payload;
  try {
    header = JSON.parse(headerStr);
    payload = JSON.parse(payloadStr);
  } catch (e) {
    throw new Error('Invalid JSON in JWT header or payload');
  }

  return {
    header: {
      raw: headerStr,
      parsed: header,
      alg: header.alg || 'unknown'
    },
    payload: {
      raw: payloadStr,
      parsed: payload
    },
    signature: signatureB64,
    signatureRaw: BASE64URLDecode(signatureB64)
  };
};

const formatJSON = (obj) => {
  return JSON.stringify(obj, null, 2);
};

const syntaxHighlight = (json) => {
  if (typeof json !== 'string') {
    json = JSON.stringify(json, null, 2);
  }
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, (match) => {
    let cls = 'json-number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) {
        cls = 'json-key';
        match = match.slice(0, -1);
        return '<span class="' + cls + '">' + match + '</span>:';
      } else {
        cls = 'json-string';
      }
    } else if (/true|false/.test(match)) {
      cls = 'json-boolean';
    } else if (/null/.test(match)) {
      cls = 'json-null';
    }
    return '<span class="' + cls + '">' + match + '</span>';
  });
};

const checkExpiration = (payload) => {
  if (!payload.exp) {
    return { expired: null, message: 'No expiration claim' };
  }

  const now = Math.floor(Date.now() / 1000);
  const exp = payload.exp;
  const expired = exp < now;

  if (expired) {
    const diff = now - exp;
    const days = Math.floor(diff / 86400);
    const hours = Math.floor((diff % 86400) / 3600);
    return {
      expired: true,
      message: `Expired ${days > 0 ? days + 'd ' : ''}${hours}h ago`
    };
  } else {
    const diff = exp - now;
    const days = Math.floor(diff / 86400);
    const hours = Math.floor((diff % 86400) / 3600);
    return {
      expired: false,
      message: `Valid for ${days > 0 ? days + 'd ' : ''}${hours}h`
    };
  }
};

const verifyHMAC = async (data, signature, secret, algorithm) => {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: { name: algorithm } },
    false,
    ['verify']
  );

  const [headerB64, payloadB64] = data.split('.');
  const message = `${headerB64}.${payloadB64}`;
  const messageBytes = enc.encode(message);

  // Decode signature from base64url
  const signatureBytes = Uint8Array.from(atob(signature.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));

  return await crypto.subtle.verify('HMAC', key, signatureBytes, messageBytes);
};

const verifyRSA = async (data, signatureB64, keyPem, algorithm) => {
  try {
    // Remove PEM headers and decode
    let pemContents = keyPem
      .replace(/-----BEGIN [A-Z0-9 ]+-----/, '')
      .replace(/-----END [A-Z0-9 ]+-----/, '')
      .replace(/\s/g, '');

    const keyData = Uint8Array.from(atob(pemContents), c => c.charCodeAt(0));

    let algorithmName;
    if (algorithm === 'RS256') {
      algorithmName = 'RSASSA-PKCS1-v1_5';
    } else {
      algorithmName = {
        RS256: 'RSASSA-PKCS1-v1_5',
        RS384: 'RSASSA-PKCS1-v1_5',
        RS512: 'RSASSA-PKCS1-v1_5'
      }[algorithm] || 'RSASSA-PKCS1-v1_5';
    }

    const hashName = {
      RS256: 'SHA-256',
      RS384: 'SHA-384',
      RS512: 'SHA-512'
    }[algorithm] || 'SHA-256';

    const key = await crypto.subtle.importKey(
      'spki',
      keyData.buffer,
      { name: algorithmName, hash: hashName },
      false,
      ['verify']
    );

    const [headerB64, payloadB64] = data.split('.');
    const message = `${headerB64}.${payloadB64}`;
    const messageBytes = new TextEncoder().encode(message);

    // Decode signature from base64url
    const signatureBytes = Uint8Array.from(atob(signatureB64.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));

    return await crypto.subtle.verify(algorithmName, key, signatureBytes, messageBytes);
  } catch (e) {
    console.error('RSA verify error:', e);
    return false;
  }
};

const verifySignature = async (decoded, algorithm, secret) => {
  if (algorithm === 'none' || !secret) {
    return { verified: null, message: 'No verification (unsigned or no secret)' };
  }

  try {
    const data = `${decoded.header.raw}.${decoded.payload.raw}`;

    if (algorithm.startsWith('HS')) {
      const verified = await verifyHMAC(data, decoded.signature, secret, algorithm);
      return { verified, message: verified ? 'Signature valid' : 'Signature invalid' };
    } else if (algorithm.startsWith('RS')) {
      const verified = await verifyRSA(data, decoded.signature, secret, algorithm);
      return { verified, message: verified ? 'Signature valid' : 'Signature invalid' };
    } else {
      return { verified: null, message: `Algorithm ${algorithm} not supported` };
    }
  } catch (e) {
    return { verified: false, message: 'Verification failed: ' + e.message };
  }
};

// DOM Elements
const jwtInput = document.getElementById('jwt-input');
const algorithmSelect = document.getElementById('algorithm');
const secretKeyInput = document.getElementById('secret-key');
const decodeBtn = document.getElementById('decode-btn');
const clearBtn = document.getElementById('clear-btn');
const outputDiv = document.getElementById('output');
const emptyState = document.getElementById('empty-state');
const errorAlert = document.getElementById('error-alert');
const warningAlert = document.getElementById('warning-alert');
const successAlert = document.getElementById('success-alert');

const headerOutput = document.getElementById('header-output');
const payloadOutput = document.getElementById('payload-output');
const signatureOutput = document.getElementById('signature-output');

const copyHeaderBtn = document.getElementById('copy-header-btn');
const copyPayloadBtn = document.getElementById('copy-payload-btn');
const copySigBtn = document.getElementById('copy-sig-btn');

const hideAlerts = () => {
  errorAlert.classList.add('hidden');
  warningAlert.classList.add('hidden');
  successAlert.classList.add('hidden');
};

const showError = (msg) => {
  hideAlerts();
  document.getElementById('error-message').textContent = msg;
  errorAlert.classList.remove('hidden');
};

const showWarning = (msg) => {
  hideAlerts();
  document.getElementById('warning-message').textContent = msg;
  warningAlert.classList.remove('hidden');
};

const showSuccess = (msg) => {
  hideAlerts();
  document.getElementById('success-message').textContent = msg;
  successAlert.classList.remove('hidden');
};

const copyToClipboard = async (text, btn) => {
  try {
    await navigator.clipboard.writeText(text);
    const original = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = original;
      btn.classList.remove('copied');
    }, 1500);
  } catch (e) {
    console.error('Copy failed:', e);
  }
};

const renderOutput = (decoded, verifyResult) => {
  // Show output, hide empty state
  outputDiv.classList.remove('hidden');
  emptyState.classList.add('hidden');

  // Header
  headerOutput.innerHTML = syntaxHighlight(formatJSON(decoded.header.parsed));
  document.getElementById('header-alg-badge').textContent = decoded.header.alg;

  // Payload
  payloadOutput.innerHTML = syntaxHighlight(formatJSON(decoded.payload.parsed));

  // Signature
  signatureOutput.textContent = decoded.signature;

  // Expiration
  const expResult = checkExpiration(decoded.payload.parsed);
  document.getElementById('status-algorithm').textContent = `Alg: ${decoded.header.alg}`;
  document.getElementById('status-exp').textContent = expResult.message;

  const expBadge = document.getElementById('exp-badge');
  const validBadge = document.getElementById('valid-badge');
  const expDot = document.getElementById('status-dot-exp');

  if (expResult.expired === true) {
    expBadge.classList.remove('hidden');
    validBadge.classList.add('hidden');
    expDot.classList.remove('green');
    expDot.classList.add('red');
  } else if (expResult.expired === false) {
    expBadge.classList.add('hidden');
    validBadge.classList.remove('hidden');
    expDot.classList.remove('green', 'red');
    expDot.classList.add('green');
  } else {
    expBadge.classList.add('hidden');
    validBadge.classList.add('hidden');
    expDot.classList.remove('green', 'red');
    expDot.classList.add('yellow');
  }

  // Signature verification
  document.getElementById('status-sig').textContent = verifyResult.message;

  const sigValidBadge = document.getElementById('sig-valid-badge');
  const sigNoneBadge = document.getElementById('sig-none-badge');
  const sigDot = document.getElementById('status-dot-sig');

  if (verifyResult.verified === true) {
    sigValidBadge.classList.remove('hidden');
    sigNoneBadge.classList.add('hidden');
    sigDot.classList.remove('green', 'red', 'yellow');
    sigDot.classList.add('green');
  } else if (verifyResult.verified === false) {
    sigValidBadge.classList.add('hidden');
    sigNoneBadge.classList.add('hidden');
    sigDot.classList.remove('green', 'red', 'yellow');
    sigDot.classList.add('red');
  } else {
    sigValidBadge.classList.add('hidden');
    sigDot.classList.remove('green', 'red', 'yellow');
    sigDot.classList.add('yellow');
  }

  // Warnings
  if (decoded.header.alg === 'none' || !decoded.header.alg) {
    showWarning('This token is UNSIGNED. Do not trust this token in production.');
  }
};

const handleDecode = async () => {
  hideAlerts();

  const token = jwtInput.value.trim();
  if (!token) {
    showError('Please enter a JWT token');
    return;
  }

  try {
    const decoded = decodeJWT(token);
    const algorithm = algorithmSelect.value;
    const secret = secretKeyInput.value;

    const verifyResult = await verifySignature(decoded, algorithm, secret);

    renderOutput(decoded, verifyResult);

    if (verifyResult.verified === false) {
      showWarning('Signature verification FAILED. The token may have been tampered with.');
    } else if (decoded.header.alg === 'none') {
      showWarning('This token is unsigned (alg: none). This is a security risk.');
    }
  } catch (e) {
    showError(e.message);
    outputDiv.classList.add('hidden');
    emptyState.classList.remove('hidden');
  }
};

const handleClear = () => {
  hideAlerts();
  jwtInput.value = '';
  secretKeyInput.value = '';
  algorithmSelect.value = 'HS256';
  outputDiv.classList.add('hidden');
  emptyState.classList.remove('hidden');
};

// Event listeners
decodeBtn.addEventListener('click', handleDecode);
clearBtn.addEventListener('click', handleClear);

jwtInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.ctrlKey) {
    handleDecode();
  }
});

copyHeaderBtn.addEventListener('click', () => {
  copyToClipboard(headerOutput.textContent, copyHeaderBtn);
});

copyPayloadBtn.addEventListener('click', () => {
  copyToClipboard(payloadOutput.textContent, copyPayloadBtn);
});

copySigBtn.addEventListener('click', () => {
  copyToClipboard(signatureOutput.textContent, copySigBtn);
});

// Expose decode function globally for API use
window.jwtDecoder = {
  decode: decodeJWT,
  verify: verifySignature,
  checkExpiration,
  formatJSON,
  syntaxHighlight
};
