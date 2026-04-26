#!/bin/bash

# Complete Developer Toolkit - Unified Installer
# Installs all 13 CLI tools in one command

set -e

echo "🛠️  Complete Developer Toolkit Installer"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Installation directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Check if directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}⚠️  $INSTALL_DIR is not in your PATH${NC}"
    echo "Add this to your shell profile (.bashrc, .zshrc, etc):"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Tools to install
TOOLS=(
    "bounty-hunter-cli/bounty_hunter.py:bounty-hunter"
    "dev-setup-cli/dev_setup.py:devsetup"
    "code-review-cli/code_review.py:codereview"
    "github-bounty-scraper/bounty_scraper.py:bounty-scraper"
    "readme-generator/readme_generator.py:readme-gen"
    "gitignore-generator/gitignore_generator.py:gitignore-gen"
    "commit-generator/commit_generator.py:commit-gen"
    "docker-compose-generator/docker_compose_generator.py:docker-compose-gen"
    "api-key-manager/api_key_manager.py:api-key-manager"
    "github-actions-generator/gh_actions_generator.py:gha-gen"
    "project-init/project_initializer.py:project-init"
    "api-tester/api_tester.py:api-tester"
    "db-schema-generator/db_schema_generator.py:db-schema-gen"
)

# Download and install each tool
BASE_URL="https://raw.githubusercontent.com/yourusername/devtoolkit/main/products"

install_tool() {
    local path="$1"
    local name="$2"
    local target="$INSTALL_DIR/$name"
    
    echo -n "Installing $name... "
    
    if curl -fsSL "$BASE_URL/$path" -o "$target" 2>/dev/null; then
        chmod +x "$target"
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC} (offline mode - copy manually)"
    fi
}

echo "Installing 13 developer tools to $INSTALL_DIR..."
echo ""

for tool in "${TOOLS[@]}"; do
    IFS=':' read -r path name <<< "$tool"
    install_tool "$path" "$name"
done

echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Tools installed:"
echo "  • bounty-hunter      - Find GitHub bounties"
echo "  • devsetup           - Environment setup"
echo "  • codereview         - Automated code review"
echo "  • bounty-scraper     - Batch bounty processing"
echo "  • readme-gen         - README generator"
echo "  • gitignore-gen      - .gitignore generator"
echo "  • commit-gen         - Commit message generator"
echo "  • docker-compose-gen - Docker Compose generator"
echo "  • api-key-manager    - API key management"
echo "  • gha-gen            - GitHub Actions generator"
echo "  • project-init       - Project initializer"
echo "  • api-tester         - API testing tool"
echo "  • db-schema-gen      - Database schema generator"
echo ""
echo "Run any tool with --help to get started:"
echo "  bounty-hunter --help"
echo ""
echo "📚 Documentation: https://github.com/yourusername/devtoolkit"
echo "💰 Get the complete bundle: https://gumroad.com/your-product"
