#!/bin/bash
# Developer Tools Bundle Installer
# Installs all 9 CLI tools with one command

set -e

INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"

echo "🚀 Developer Tools Bundle Installer"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if install directory exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Creating install directory: $INSTALL_DIR${NC}"
    mkdir -p "$INSTALL_DIR"
fi

# Products to install
PRODUCTS=(
    "bounty-hunter-cli/bounty_hunter_cli.py:bounty-hunter"
    "dev-setup-cli/dev_setup_cli.py:dev-setup"
    "code-review-cli/code_review_cli.py:code-review"
    "github-bounty-scraper/github_bounty_scraper.py:bounty-scraper"
    "readme-generator/readme_generator.py:readme-gen"
    "gitignore-generator/gitignore_generator.py:gitignore-gen"
    "commit-generator/commit_generator.py:commit-gen"
    "docker-compose-generator/docker_compose_generator.py:dcompose-gen"
    "api-tester/api_tester.py:api-tester"
    "api-key-manager/api_key_manager.py:api-key-manager"
    "github-actions-generator/github_actions_generator.py:actions-gen"
    "project-init/project_init.py:project-init"
)

installed=0
failed=0

echo "Installing 12 CLI tools to $INSTALL_DIR..."
echo ""

for product in "${PRODUCTS[@]}"; do
    IFS=':' read -r source_file cmd_name <<< "$product"
    source_path="$(dirname "$0")/$source_file"
    target_path="$INSTALL_DIR/$cmd_name"
    
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        chmod +x "$target_path"
        echo -e "${GREEN}✓${NC} Installed: $cmd_name"
        ((installed++))
    else
        echo -e "${RED}✗${NC} Failed: $cmd_name (source not found)"
        ((failed++))
    fi
done

echo ""
echo "=================================="
echo -e "${GREEN}Installed: $installed tools${NC}"
if [ $failed -gt 0 ]; then
    echo -e "${RED}Failed: $failed tools${NC}"
fi
echo ""

# Add to PATH if needed
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Adding $INSTALL_DIR to PATH...${NC}"
    
    # Add to .bashrc
    if [ -f "$BASHRC" ]; then
        echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$BASHRC"
        echo -e "${GREEN}✓${NC} Added to .bashrc"
    fi
    
    # Add to .zshrc
    if [ -f "$ZSHRC" ]; then
        echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$ZSHRC"
        echo -e "${GREEN}✓${NC} Added to .zshrc"
    fi
    
    echo ""
    echo -e "${YELLOW}⚠️  Please run: source ~/.bashrc (or ~/.zshrc)${NC}"
    echo "   Or restart your terminal to use the commands."
else
    echo -e "${GREEN}✓${NC} $INSTALL_DIR is already in PATH"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Available commands:"
echo "  bounty-hunter    - Find GitHub issues with bounties"
echo "  dev-setup        - Automated development environment setup"
echo "  code-review      - Multi-language code review assistant"
echo "  bounty-scraper   - Scrape GitHub for bounty opportunities"
echo "  readme-gen       - Generate professional README files"
echo "  gitignore-gen    - Generate .gitignore for any tech stack"
echo "  commit-gen       - Generate conventional commit messages"
echo "  dcompose-gen     - Generate docker-compose.yml files"
echo "  api-key-manager  - Securely manage API keys with encryption"
echo "  api-tester       - Test REST APIs with detailed reports"
echo "  actions-gen      - Generate GitHub Actions workflows"
echo "  project-init     - Initialize complete projects with one command"
echo ""
echo "Run any command with --help for usage information."
