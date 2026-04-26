# Project Initializer CLI

**One command to initialize a complete, production-ready project.**

Stop manually creating the same files for every new project. This tool generates everything you need in seconds.

## Features

- ✨ **README.md** - Professional templates (minimal, standard)
- 🔒 **.gitignore** - Language-specific ignore patterns
- 🐳 **Dockerfile** - Production-ready container configs
- ⚙️ **GitHub Actions** - CI/CD workflow templates
- 📄 **LICENSE** - MIT license with your name
- 📁 **Directory Structure** - src/, tests/ folders
- 📦 **requirements.txt** - Dependency management

## Installation

```bash
# Clone and install
git clone https://github.com/yourusername/project-init.git
cd project-init
pip install -e .

# Or copy the script directly
cp project_init.py /usr/local/bin/project-init
chmod +x /usr/local/bin/project-init
```

## Usage

### Quick Start

```bash
# Initialize a Python project
project-init my-project --language python

# Initialize with all components
project-init my-api --language node --all

# Custom description and author
project-init my-lib --description "A cool library" --author "Your Name"
```

### Examples

```bash
# Python project with Docker and CI/CD
project-init my-service --language python --docker --github-actions

# Node.js API project
project-init my-api --language node --readme-type api --docker --all

# Minimal Go project
project-init my-cli --language go --readme-type minimal
```

### Options

| Option | Description |
|--------|-------------|
| `--language`, `-l` | Primary language (python, node, go, rust, java) |
| `--description`, `-d` | Project description |
| `--author`, `-a` | Author name for LICENSE |
| `--readme-type` | README template (minimal, standard) |
| `--docker` | Create Dockerfile |
| `--github-actions`, `-gha` | Create CI workflow |
| `--src-dir`, `-s` | Create src/ directory |
| `--tests-dir`, `-t` | Create tests/ directory |
| `--requirements`, `-r` | Create requirements.txt |
| `--all` | Enable all components |
| `--force`, `-f` | Overwrite existing directory |
| `--list-templates` | Show available templates |

## What Gets Created

```
my-project/
├── README.md              # Professional project readme
├── .gitignore            # Language-specific ignores
├── LICENSE               # MIT license
├── Dockerfile            # (if --docker)
├── requirements.txt      # (if --requirements)
├── .github/
│   └── workflows/
│       └── ci.yml        # (if --github-actions)
├── my_project/           # (if --src-dir)
│   └── __init__.py
└── tests/                # (if --tests-dir)
    ├── __init__.py
    └── test_my_project.py
```

## Supported Languages

- **Python** - Full support (README, .gitignore, Dockerfile, CI)
- **Node.js** - Full support (README, .gitignore, Dockerfile, CI)
- **Go** - README, .gitignore
- **Rust** - README, .gitignore
- **Java** - README, .gitignore

## Time Savings

| Task | Manual Time | With Tool | Saved |
|------|-------------|-----------|-------|
| Create README | 15 min | 1 sec | 14.9 min |
| Create .gitignore | 10 min | 1 sec | 9.9 min |
| Create Dockerfile | 20 min | 1 sec | 19.9 min |
| Setup CI/CD | 30 min | 1 sec | 29.9 min |
| Create LICENSE | 5 min | 1 sec | 4.9 min |
| **Total** | **80 min** | **5 sec** | **~80 min** |

## Why Use This?

1. **Consistency** - Every project starts with the same professional structure
2. **Speed** - Go from idea to coding in seconds, not minutes
3. **Best Practices** - Templates follow industry standards
4. **No Dependencies** - Pure Python, no external packages needed

## License

MIT License - see LICENSE file for details.
