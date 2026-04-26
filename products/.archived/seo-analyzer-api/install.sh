#!/bin/bash
# SEO Analyzer API - Installation Script
# Version: 2.0
# Validated: 2026-04-03

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗"
echo -e "║  SEO Analyzer API v2.0 - Installer     ║"
echo -e "╚════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠ Running as root (not recommended)${NC}"
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
else
    echo -e "${RED}✗ Unsupported OS: $OSTYPE${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Detected OS: ${OS}"

# Check Python version
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.6+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python found: ${PYTHON_VERSION}"

# Installation directory
INSTALL_DIR="/opt/seo-analyzer"
BIN_DIR="/usr/local/bin"

echo ""
echo -e "${YELLOW}📁 Installation directory: ${INSTALL_DIR}${NC}"
echo -e "${YELLOW}📁 Binary directory: ${BIN_DIR}${NC}"
echo ""

# Create installation directory
echo -e "${BLUE}→${NC} Creating installation directory..."
sudo mkdir -p "$INSTALL_DIR"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy main script
echo -e "${BLUE}→${NC} Copying seo_analyzer.py..."
sudo cp "$SCRIPT_DIR/seo_analyzer.py" "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/seo_analyzer.py"

# Create launcher script
echo -e "${BLUE}→${NC} Creating launcher script..."
sudo tee "$BIN_DIR/seo-api" > /dev/null <<'EOF'
#!/bin/bash
# SEO Analyzer API Launcher
exec python3 /opt/seo-analyzer/seo_analyzer.py "$@"
EOF

sudo chmod +x "$BIN_DIR/seo-api"

# Create uninstall script
echo -e "${BLUE}→${NC} Creating uninstall script..."
sudo tee "$INSTALL_DIR/uninstall.sh" > /dev/null <<'EOF'
#!/bin/bash
echo "Uninstalling SEO Analyzer API..."
sudo rm -rf /opt/seo-analyzer
sudo rm -f /usr/local/bin/seo-api
echo "✓ Uninstall complete"
EOF

sudo chmod +x "$INSTALL_DIR/uninstall.sh"

# Create README in install directory
echo -e "${BLUE}→${NC} Creating quick reference..."
sudo tee "$INSTALL_DIR/QUICKSTART.md" > /dev/null <<'EOF'
# SEO Analyzer API - Quick Start

## Start the API
```bash
seo-api
# or
python3 /opt/seo-analyzer/seo_analyzer.py
```

## API runs on: http://localhost:5055

## Quick Test
```bash
# Health check
curl http://localhost:5055/health

# Analyze single URL
curl -X POST http://localhost:5055/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Analyze batch (up to 50 URLs)
curl -X POST http://localhost:5055/analyze-batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://example.org"]}'

# Export results as JSON
curl http://localhost:5055/export?format=json

# Export results as CSV
curl http://localhost:5055/export?format=csv
```

## Stop the API
Press Ctrl+C in the terminal running the API.

## Uninstall
```bash
/opt/seo-analyzer/uninstall.sh
```
EOF

# Verify installation
echo ""
echo -e "${BLUE}→${NC} Verifying installation..."

if [ -f "$INSTALL_DIR/seo_analyzer.py" ]; then
    echo -e "${GREEN}✓${NC} Main script installed"
else
    echo -e "${RED}✗ Main script installation failed${NC}"
    exit 1
fi

if [ -x "$BIN_DIR/seo-api" ]; then
    echo -e "${GREEN}✓${NC} Launcher script installed"
else
    echo -e "${RED}✗ Launcher script installation failed${NC}"
    exit 1
fi

# Final output
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ Installation Complete!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}📖 Quick Start:${NC}"
echo ""
echo -e "  Start API:  ${GREEN}seo-api${NC}"
echo -e "  or:         ${GREEN}python3 /opt/seo-analyzer/seo_analyzer.py${NC}"
echo ""
echo -e "${YELLOW}📖 Documentation:${NC}"
echo ""
echo -e "  README:     ${GREEN}cat $SCRIPT_DIR/README.md${NC}"
echo -e "  Examples:   ${GREEN}cat $SCRIPT_DIR/examples.md${NC}"
echo ""
echo -e "${YELLOW}🔧 Uninstall:${NC}"
echo ""
echo -e "  ${GREEN}/opt/seo-analyzer/uninstall.sh${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✓ Ready to use!${NC}"
echo ""
