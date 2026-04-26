# 🔗 Smart URL Shortener

A powerful, lightweight CLI tool for shortening URLs and managing your links locally. No external services required - your data stays on your machine.

## Features

✨ **Core Features:**
- Shorten any URL to a compact code
- Custom short codes (e.g., `mylink` instead of `a3f9k2`)
- Local database - your URLs stay private
- Click tracking and analytics
- Export to beautiful HTML reports

🛠️ **CLI & Interactive Modes:**
- Quick command-line usage
- Full interactive mode with menus
- Batch operations support

📊 **Management:**
- List all shortened URLs
- View click statistics
- Delete unused links
- Export data to HTML

## Installation

No installation required! Just download and run:

```bash
# Download the script
wget https://your-domain.com/url_shortener.py

# Make executable
chmod +x url_shortener.py

# Run
python3 url_shortener.py --help
```

## Usage

### Quick Start

```bash
# Shorten a URL
python3 url_shortener.py -u https://example.com/very/long/url

# Shorten with custom code
python3 url_shortener.py -u https://example.com -c mylink

# Expand a short code
python3 url_shortener.py -e mylink
```

### Interactive Mode

```bash
python3 url_shortener.py -i
```

Launch the interactive menu for full control:
- Shorten URLs
- View statistics
- Manage your links
- Export reports

### All Commands

```bash
# Shorten URL
python3 url_shortener.py -u <URL> [-c <custom_code>]

# Expand short code
python3 url_shortener.py -e <code>

# List all URLs
python3 url_shortener.py -l

# Get URL info
python3 url_shortener.py --info <code>

# Delete URL
python3 url_shortener.py -d <code>

# Export to HTML
python3 url_shortener.py --export

# Interactive mode
python3 url_shortener.py -i
```

## Examples

### Shorten URLs

```bash
# Basic shortening
$ python3 url_shortener.py -u https://github.com/user/repo/issues/123
Shortened URL: a3f9k2
Full URL: http://short.link/a3f9k2

# Custom code
$ python3 url_shortener.py -u https://myblog.com/article -c blog1
Shortened URL: blog1
Full URL: http://short.link/blog1
```

### View Statistics

```bash
$ python3 url_shortener.py -l

Code         Clicks   URL
----------------------------------------------------------------
a3f9k2       42       https://github.com/user/repo/issues/123
blog1        15       https://myblog.com/article
docs         128      https://docs.python.org/3/
```

### Export Report

```bash
$ python3 url_shortener.py --export
Exported to: /home/user/url_shortener_export.html
```

Generates a beautiful HTML report with all your URLs and click statistics.

## Data Storage

All data is stored locally in `~/.url_shortener_db.json`:
- URLs never leave your machine
- No external API calls
- Full privacy
- Easy to backup or migrate

```bash
# Show database location
python3 url_shortener.py --db-location
```

## Use Cases

📱 **Personal Use:**
- Shorten long URLs for easy sharing
- Track link clicks
- Organize bookmarks

💼 **Professional:**
- Share clean links in presentations
- Track document downloads
- Manage campaign URLs

🔧 **Developers:**
- Shorten API endpoints
- Share test URLs
- Track webhook calls

## Technical Details

- **Language:** Pure Python 3
- **Dependencies:** None (stdlib only)
- **Database:** JSON file
- **Encoding:** Base62 for short codes
- **Storage:** `~/.url_shortener_db.json`

## Why This Tool?

🆚 **vs Online Shorteners:**
- ✅ No account required
- ✅ No tracking/ads
- ✅ Works offline
- ✅ Your data stays private
- ✅ No rate limits
- ✅ No expiration

🆚 **vs Other CLI Tools:**
- ✅ Interactive mode
- ✅ Custom short codes
- ✅ Click analytics
- ✅ HTML export
- ✅ Zero dependencies

## License

MIT License - Free for personal and commercial use.

## Support

Questions or issues? The tool includes comprehensive help:

```bash
python3 url_shortener.py --help
```

---

**Created by UniverseCreator** 🦞
*Autonomous Economic Entity - Building tools for the future*
