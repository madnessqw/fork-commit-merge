#!/bin/bash
# GitHub Pages Deployment Script for UniverseCreator Tools
# Run this script to deploy the landing page to GitHub Pages

set -e

echo "🚀 UniverseCreator GitHub Pages Deployer"
echo "=================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) not found. Install with: sudo apt install gh"
    echo "   Then run: gh auth login"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "⚠️  Not logged into GitHub. Please run: gh auth login"
    exit 1
fi

# Get GitHub username
USERNAME=$(gh api user -q '.login')
echo "✅ Authenticated as: $USERNAME"

# Create repo if it doesn't exist
echo "📦 Checking for repository..."
if ! gh repo view "$USERNAME/UniverseCreator-tools" &> /dev/null; then
    echo "🆕 Creating new repository: UniverseCreator-tools"
    gh repo create UniverseCreator-tools --public --description "15 CLI tools for developers" --homepage "https://$USERNAME.github.io/UniverseCreator-tools/"
    echo "✅ Repository created"
else
    echo "✅ Repository already exists"
fi

# Initialize git if needed
if [ ! -d .git ]; then
    echo "🔧 Initializing git repository..."
    git init
    git branch -M main
fi

# Add remote
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 Adding remote origin..."
    git remote add origin "https://github.com/$USERNAME/UniverseCreator-tools.git"
fi

# Commit and push
echo "📤 Deploying to GitHub Pages..."
git add .
git commit -m "Deploy landing page - Cycle 21" || echo "Nothing to commit"
git push -u origin main --force

# Enable GitHub Pages
echo "🌐 Enabling GitHub Pages..."
gh api repos/$USERNAME/UniverseCreator-tools/pages \
  --method POST \
  --input - <<< '{"source":{"branch":"main","path":"/"}}' 2>/dev/null || echo "Pages may already be enabled"

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo "======================="
echo "🌐 Your site will be live at: https://$USERNAME.github.io/UniverseCreator-tools/"
echo "⏱️  It may take 2-5 minutes to propagate"
echo ""
echo "Next steps:"
echo "1. Visit your site (wait a few minutes if 404)"
echo "2. Share the link on social media"
echo "3. Set up Gumroad for payments"
echo ""
echo "Built with ❤️ by UniverseCreator (Cycle 21)"
