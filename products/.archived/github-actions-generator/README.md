# GitHub Actions Generator CLI

Generate production-ready CI/CD workflows in seconds. Stop wrestling with YAML syntax and start shipping.

## 🎯 What It Does

Creates professional GitHub Actions workflows for:
- **Python projects** - Multi-version testing, linting, coverage
- **Node.js projects** - Build, test, lint across Node versions
- **Docker publishing** - Automated image builds and registry pushes
- **Release automation** - Version bumping and changelog generation
- **Dependency management** - Auto-merge Dependabot updates
- **Static site deployment** - GitHub Pages publishing

## 💡 Why You Need This

Writing GitHub Actions workflows is tedious and error-prone:
- YAML indentation nightmares
- Outdated action versions
- Missing best practices
- Hours of documentation reading

**This tool generates battle-tested workflows in seconds.**

## 🚀 Quick Start

### Interactive Mode (Recommended)
```bash
python github_actions_generator.py --interactive
```

### Command Line
```bash
# List all templates
python github_actions_generator.py --list

# Generate Python CI workflow
python github_actions_generator.py --template python-ci

# Generate with custom project name
python github_actions_generator.py --template release-please --name my-awesome-project

# Custom output path
python github_actions_generator.py --template docker-publish --output ./my-workflow.yml
```

## 📋 Available Templates

| Template | Purpose | Best For |
|----------|---------|----------|
| `python-ci` | Multi-version Python testing | Python libraries, Django, Flask |
| `node-ci` | Node.js build and test | React, Vue, Express apps |
| `docker-publish` | Build and push images | Containerized applications |
| `release-please` | Automated releases | Libraries with versioning |
| `dependabot` | Auto-merge updates | Maintained open source projects |
| `pages-deploy` | Deploy to GitHub Pages | Static sites, documentation |

## 📦 Installation

### Option 1: Direct Download
```bash
curl -O https://raw.githubusercontent.com/yourusername/devtools/main/products/github-actions-generator/github_actions_generator.py
chmod +x github_actions_generator.py
```

### Option 2: Full Bundle
```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/devtools/main/install.sh | bash
```

## 🎨 Features

### Python CI Workflow
- Tests on Python 3.9, 3.10, 3.11, 3.12
- pytest with coverage reporting
- flake8 linting
- Codecov integration

### Node.js CI Workflow
- Tests on Node 18, 20, 21
- npm ci for reproducible builds
- Automatic npm caching
- Lint and build steps

### Docker Publish Workflow
- Multi-platform builds with Buildx
- GitHub Container Registry (ghcr.io)
- Tag-based versioning
- Layer caching for speed

### Release Please Workflow
- Conventional commit parsing
- Automatic version bumping
- Changelog generation
- PR-based releases

### Dependabot Auto-merge
- Auto-approve patch updates
- Auto-approve minor updates
- Security-focused defaults

### GitHub Pages Deploy
- Static site deployment
- Jekyll support
- Custom domain ready

## 💰 Pricing

| Package | Price |
|---------|-------|
| Individual Tool | $9 |
| Complete Bundle (11 tools) | $49 |
| Team License (10 users) | $129 |

## 🛡️ Guarantee

30-day money-back guarantee. Not satisfied? Full refund, no questions.

## 📞 Support

- Email: support@yourdomain.com
- Issues: [GitHub Issues](https://github.com/yourusername/devtools/issues)

## 📄 License

MIT License - modify and distribute freely.

---

**Ready to automate your CI/CD?** [Get the Complete Bundle →]()
