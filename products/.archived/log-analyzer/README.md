# Log Analyzer CLI

Parse, analyze, and visualize log files from the command line. Quickly identify errors, patterns, and anomalies.

## Features

- **Multi-format support** - Python, web server, syslog, and generic logs
- **Error detection** - Automatically find and categorize errors
- **Pattern search** - Find specific strings or regex patterns
- **Time filtering** - Analyze specific time ranges
- **Real-time following** - Watch logs as they grow (like `tail -f`)
- **Visual reports** - ASCII bar charts for quick insights
- **JSON export** - Export results for further processing
- **CI/CD ready** - Exit codes for automation

## Installation

```bash
# Download directly
curl -O https://your-domain.com/log-analyzer.py
chmod +x log-analyzer.py
mv log-analyzer.py ~/.local/bin/log-analyzer

# Or use the unified installer
curl -fsSL https://your-domain.com/install.sh | bash
```

## Usage

### Basic Analysis
```bash
log-analyzer app.log
```

### Show Only Errors
```bash
log-analyzer app.log --errors-only
```

### Search for Pattern
```bash
log-analyzer app.log --pattern "Database connection"
```

### Filter by Level
```bash
log-analyzer app.log --level ERROR
```

### Time Range
```bash
log-analyzer app.log --since "2024-01-01 00:00:00" --until "2024-01-02 00:00:00"
```

### Real-time Following
```bash
log-analyzer app.log --real-time
```

### Export to JSON
```bash
log-analyzer app.log --json --export analysis.json
```

## Sample Output

```
============================================================
LOG ANALYSIS REPORT
============================================================
Total lines analyzed: 15234

LOG LEVELS:
----------------------------------------
  INFO              9876 ( 64.8%) ████████████████████████████████
  DEBUG             4123 ( 27.1%) ██████████████
  WARNING            987 (  6.5%) ███
  ERROR              248 (  1.6%) █

ERRORS FOUND: 248
----------------------------------------
  Line 452: ERROR - Database connection timeout...
  Line 891: ERROR - Failed to process request...

TOP 10 FREQUENT MESSAGES:
----------------------------------------
  2345x  User login successful
   987x  Cache miss for key
   456x  API request completed
```

## Supported Log Formats

- Python logging (standard format)
- Apache/Nginx access logs
- Syslog
- Custom timestamp formats

## Use Cases

- **Debugging** - Find errors quickly in large log files
- **Monitoring** - Watch logs in real-time during deployments
- **Analysis** - Understand traffic patterns and error rates
- **Reporting** - Generate JSON reports for stakeholders
- **CI/CD** - Automated log checking in pipelines

## Pricing

- **Individual:** $9
- **Complete Bundle (15 tools):** $49
- **Team License:** $129

## License

MIT License - See LICENSE file for details.
