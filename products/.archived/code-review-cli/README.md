# 🔍 Code Review CLI

Automated code quality analysis for developers. Review your code before submitting PRs.

## Features

- 🔒 **Security Scanning** - Detect hardcoded secrets, SQL injection risks, API keys
- ⚡ **Performance Analysis** - Find inefficient patterns and optimization opportunities
- 🎨 **Style Checking** - Enforce line length, whitespace, and code style
- 🛠️ **Multi-Language Support** - Python, JavaScript, TypeScript, Go, Rust, and more
- 📊 **Scoring System** - Get a grade (A-F) based on code quality
- 📄 **Markdown Reports** - Export detailed reports for documentation

## Installation

```bash
pip install code-review-cli
```

## Quick Start

```bash
# Review a single file
code-review app.py

# Review entire project
code-review .

# Export detailed report
code-review . --export report.md

# Show only critical issues
code-review . --severity critical
```

## Example Output

```
============================================================
🔍 CODE REVIEW REPORT
============================================================

Score: 85/100 (Grade: B)
Files: 12 | Lines: 847

Issues Found: 5
  🔴 Critical: 0
  🟡 Warning: 2
  🔵 Suggestion: 3
```

## What It Checks

### Security
- Hardcoded passwords, secrets, API keys
- SQL injection vulnerabilities
- AWS keys, Stripe tokens, GitHub tokens
- Unsafe string formatting

### Performance
- Inefficient loops (range(len()) vs enumerate())
- String concatenation in loops
- Suboptimal data structure usage
- Memory-intensive patterns

### Style
- Line length violations
- Trailing whitespace
- TODO/FIXME comments
- Consistency issues

### Language-Specific
- **Python**: Bare except clauses, mutable default arguments
- **JavaScript**: == vs ===, var usage, innerHTML
- **Go**: Error handling patterns
- **Rust**: Ownership and borrowing issues

## Configuration

Create `.code-review.json` in your project root:

```json
{
  "severity_threshold": "warning",
  "max_line_length": 100,
  "check_security": true,
  "check_performance": true,
  "check_style": true,
  "ignore_patterns": [
    "node_modules/",
    "venv/",
    "*.min.js",
    "test_*.py"
  ]
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Code Review
on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install code-review-cli
      - run: code-review . --severity warning
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: code-review
        name: Code Review
        entry: code-review
        language: system
        pass_filenames: true
```

## Pricing

| License | Price | Usage |
|---------|-------|-------|
| Personal | $9 | Individual developers |
| Team | $29 | Up to 10 developers |
| Enterprise | $99 | Unlimited, priority support |

## Why Code Review CLI?

- **Fast** - Analyzes 1000+ lines per second
- **Offline** - No code leaves your machine
- **Customizable** - Configure rules for your team
- **CI/CD Ready** - Integrates with any pipeline

## License

MIT License - See LICENSE file
