# API Tester CLI 🌐

Professional API testing and validation tool for developers. Test REST APIs, validate responses, and automate API testing workflows.

## Features

- 🚀 **Quick Testing** - Test any endpoint with a single command
- 📊 **Test Collections** - Run multiple tests from JSON files
- 📈 **Detailed Reports** - Success rates, response times, status codes
- 🎯 **Flexible Validation** - Custom headers, expected status codes, timeouts
- 💾 **Export Results** - JSON or text output for CI/CD integration
- 🎨 **Interactive Mode** - Guided testing for complex scenarios

## Installation

```bash
# Clone and install
git clone <repo>
cd products/api-tester
pip install requests

# Make executable
chmod +x api_tester.py

# Optional: Add to PATH
mv api_tester.py ~/.local/bin/api-tester
```

## Usage

### Quick Test

```bash
# Simple GET request
api-tester https://api.example.com/users

# POST with JSON data
api-tester https://api.example.com/users \
  --method POST \
  --data '{"name":"John","email":"john@example.com"}'

# With custom headers
api-tester https://api.example.com/protected \
  --header "Authorization: Bearer token123" \
  --header "Content-Type: application/json"
```

### Interactive Mode

```bash
api-tester --interactive
```

### Test Collections

Create a JSON file with multiple tests:

```json
[
  {
    "url": "https://api.example.com/users",
    "method": "GET",
    "expected_status": 200
  },
  {
    "url": "https://api.example.com/users",
    "method": "POST",
    "data": {"name": "Test User"},
    "headers": {"Authorization": "Bearer token"},
    "expected_status": 201
  }
]
```

Run the collection:

```bash
api-tester --collection tests.json --output results.txt
```

## Options

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Run in interactive mode |
| `-m, --method` | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS) |
| `-d, --data` | Request body as JSON string |
| `-H, --header` | Custom headers (repeatable) |
| `-e, --expected` | Expected status code (default: 200) |
| `-t, --timeout` | Request timeout in seconds (default: 30) |
| `-c, --collection` | Run tests from JSON file |
| `-o, --output` | Save results to file |
| `--format` | Output format: text or json |

## Examples

### Test API Health

```bash
api-tester https://api.example.com/health --expected 200
```

### Test Authentication

```bash
api-tester https://api.example.com/profile \
  --header "Authorization: Bearer YOUR_TOKEN" \
  --expected 200
```

### CI/CD Integration

```bash
# Exit code 0 if all tests pass, 1 if any fail
api-tester --collection integration-tests.json || exit 1
```

### Export Results

```bash
api-tester https://api.example.com/users --format json --output results.json
```

## Sample Output

```
============================================================
API TEST REPORT
============================================================
Total Tests: 2
Passed: 2 ✅
Failed: 0 ❌
Success Rate: 100.0%
============================================================

Test 1: ✅ PASS
  URL: GET https://api.example.com/users
  Status: 200
  Response Time: 145.32ms

Test 2: ✅ PASS
  URL: POST https://api.example.com/users
  Status: 201
  Response Time: 234.56ms
```

## Use Cases

- **API Development** - Test endpoints during development
- **CI/CD Pipelines** - Automated API testing in builds
- **Monitoring** - Health checks for production APIs
- **Documentation** - Validate API examples
- **Debugging** - Inspect responses and headers

## Pricing

- **Individual**: $9
- **Complete Bundle** (13 tools): $49 (45% savings)
- **Team License** (10 users): $129

## License

MIT License - See LICENSE file for details
