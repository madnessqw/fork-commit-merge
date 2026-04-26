// Security vulnerability patterns
const PATTERNS = {
  // Prompt Injection Detection
  prompt_injection: [
    { regex: /ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts?|rules?)/gi, severity: 'high', description: 'Potential prompt injection attempt - ignoring instructions' },
    { regex: /forget\s+(everything|all|what)\s+(you|I)\s+(told|said|know)/gi, severity: 'high', description: 'Prompt injection - memory manipulation attempt' },
    { regex: /system\s*:\s*["\'].*?(jailbreak|dAN|do anything)/gi, severity: 'high', description: 'Jailbreak attempt detected in system prompt' },
    { regex: /you\s+are\s+now\s+(DAN|Doctor|different)/gi, severity: 'high', description: 'Role manipulation attempt detected' },
    { regex: /#{1,6}\s*(system|user|assistant)\s*prompt/gi, severity: 'medium', description: 'Potential prompt injection via markdown headers' },
    { regex: /```system\s*\n/gi, severity: 'medium', description: 'System prompt injection via code block' },
    { regex: /\b(bypass|override|disable)\s+(safety|filter|restriction)/gi, severity: 'high', description: 'Safety mechanism bypass attempt' }
  ],

  // Credential Exposure Detection
  credential_exposure: [
    { regex: /api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9_-]{20,}["\']/gi, severity: 'high', description: 'Hardcoded API key detected' },
    { regex: /secret[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9_-]{20,}["\']/gi, severity: 'high', description: 'Hardcoded secret key detected' },
    { regex: /password\s*[=:]\s*["\'][^"\']{8,}["\']/gi, severity: 'high', description: 'Hardcoded password detected' },
    { regex: /token\s*[=:]\s*["\'][a-zA-Z0-9_-]{20,}["\']/gi, severity: 'high', description: 'Hardcoded token detected' },
    { regex: /sk-[a-zA-Z0-9]{20,}/g, severity: 'critical', description: 'OpenAI API key detected' },
    { regex: /xox[baprs]-[a-zA-Z0-9]{10,}/g, severity: 'critical', description: 'Slack token detected' },
    { regex: /gh[pousr]_[a-zA-Z0-9]{36,}/g, severity: 'critical', description: 'GitHub token detected' },
    { regex: /aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*["\'][A-Z0-9]{20}["\']/gi, severity: 'critical', description: 'AWS Access Key ID detected' },
    { regex: /private[_-]?key\s*[=:]\s*["\'](-----BEGIN|EC PRIVATE)/gi, severity: 'critical', description: 'Private key detected' },
    { regex: /bearer\s+[a-zA-Z0-9_-]{20,}/gi, severity: 'high', description: 'Bearer token in authorization header' },
    { regex: /Authorization:\s*[Bb]earer/g, severity: 'medium', description: 'Authorization header found - ensure secure handling' }
  ],

  // MCP Misconfiguration Detection
  mcp_misconfig: [
    { regex: /mcp[_-]?server.*?admin.*?true/gi, severity: 'high', description: 'MCP server with admin privileges - over-privileged' },
    { regex: /mcp[_-]?server.*?allow[_-]?exec.*?:\s*\[.*?\*.*?\]/gi, severity: 'high', description: 'MCP server allows execution of any command' },
    { regex: /mcp[_-]?server.*?read[_-]?only\s*:\s*false/gi, severity: 'medium', description: 'MCP server write-enabled when read-only expected' },
    { regex: /mcp[_-]?server.*?timeout\s*:\s*0/gi, severity: 'medium', description: 'MCP server with no timeout - potential DoS risk' },
    { regex: /mcp[_-]?server.*?capabilities\s*:\s*\[.*?(file|exec|shell).*?\]/gi, severity: 'high', description: 'MCP server has dangerous capabilities (file/exec/shell)' },
    { regex: /tools:\s*\[.*?("execute"|"run"|"shell"|"eval").*?\]/gi, severity: 'high', description: 'Dangerous tool exposed via MCP' }
  ],

  // Tool Vulnerability Detection
  tool_vulnerability: [
    { regex: /\beval\s*\(/gi, severity: 'high', description: 'Dangerous eval() usage - code injection risk' },
    { regex: /\bexec\s*\(/gi, severity: 'high', description: 'Dangerous exec() usage - command injection risk' },
    { regex: /\bsystem\s*\(/gi, severity: 'high', description: 'Dangerous system() usage - shell command injection' },
    { regex: /\bos\.system\s*\(/gi, severity: 'high', description: 'os.system() call - command injection risk' },
    { regex: /\bsubprocess\.call\s*\([^,]+,\s*shell\s*=\s*True/gi, severity: 'high', description: 'subprocess with shell=True - command injection risk' },
    { regex: /\bchild_process\.exec\s*\(/gi, severity: 'high', description: 'child_process.exec() - shell command injection risk' },
    { regex: /\bchild_process\.spawn\s*\([^,]+,\s*shell\s*:\s*true/gi, severity: 'high', description: 'child_process spawn with shell - command injection' },
    { regex: /dangerouslySetInnerHTML/gi, severity: 'high', description: 'React dangerouslySetInnerHTML - XSS risk' },
    { regex: /innerHTML\s*=\s*[^;]/gi, severity: 'medium', description: 'Direct innerHTML assignment - potential XSS' },
    { regex: /__import__\s*\(\s*["\']os["\']\)\.(system|popen)/gi, severity: 'high', description: 'Dynamic os import with system/popen - command injection' },
    { regex: /import\s*\(\s*["\']subprocess["\']\)/gi, severity: 'medium', description: 'Dynamic subprocess import - verify usage' },
    { regex: /\bfetch\s*\([^)]*\bdangerous\b[^)]*\)/gi, severity: 'high', description: 'Fetch to potentially dangerous URL' }
  ]
};

function scanCode(code, language) {
  const vulnerabilities = [];
  const lines = code.split('\n');

  // Scan for each vulnerability type
  for (const [type, patterns] of Object.entries(PATTERNS)) {
    for (const pattern of patterns) {
      let match;
      // Reset regex lastIndex
      pattern.regex.lastIndex = 0;

      while ((match = pattern.regex.exec(code)) !== null) {
        // Find line number
        const lineNumber = code.substring(0, match.index).split('\n').length;
        const lineContent = lines[lineNumber - 1]?.trim() || '';

        // Check if this vulnerability is already reported (avoid duplicates)
        const exists = vulnerabilities.some(v =>
          v.type === type &&
          v.line === lineNumber &&
          v.description === pattern.description
        );

        if (!exists) {
          vulnerabilities.push({
            type: type.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
            severity: pattern.severity,
            line: lineNumber,
            description: pattern.description,
            match: lineContent.substring(0, 60) + (lineContent.length > 60 ? '...' : '')
          });
        }
      }
    }
  }

  // Sort by severity
  const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  vulnerabilities.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);

  // Calculate security score
  let score = 100;
  vulnerabilities.forEach(v => {
    switch (v.severity) {
      case 'critical': score -= 25; break;
      case 'high': score -= 15; break;
      case 'medium': score -= 8; break;
      case 'low': score -= 3; break;
    }
  });
  score = Math.max(0, score);

  return {
    vulnerabilities,
    score,
    summary: {
      total: vulnerabilities.length,
      critical: vulnerabilities.filter(v => v.severity === 'critical').length,
      high: vulnerabilities.filter(v => v.severity === 'high').length,
      medium: vulnerabilities.filter(v => v.severity === 'medium').length,
      low: vulnerabilities.filter(v => v.severity === 'low').length
    },
    scanType: language || 'auto-detected'
  };
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-License-Key');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { code, language } = req.body;

    if (!code || typeof code !== 'string') {
      return res.status(400).json({ error: 'Code is required' });
    }

    if (code.length > 100000) {
      return res.status(400).json({ error: 'Code too long. Maximum 100KB allowed.' });
    }

    const result = scanCode(code, language);
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json({ error: 'Scan failed: ' + error.message });
  }
};