# Environment Variable Manager CLI

Securely manage `.env` files, generate secrets, and validate environment configurations.

## Features

- **Initialize** - Create `.env` files with templates (web, Python, Docker)
- **Get/Set** - Read and write environment variables
- **Generate** - Create secure secrets, passwords, and API keys
- **Validate** - Check for common security issues
- **Sync** - Export to shell, JSON, or YAML formats

## Installation

```bash
pip install env-manager-cli
# or
curl -sSL https://install.example.com/env-manager | bash
```

## Quick Start

```bash
# Create a new .env file
env-manager init --template web

# List all variables
env-manager get

# Set a variable
env-manager set DATABASE_URL postgresql://localhost/mydb

# Generate a secure secret
env-manager generate secret JWT_SECRET

# Validate your .env
env-manager validate
```

## Commands

### `init` - Initialize .env file
```bash
env-manager init --template web      # Web app template
env-manager init --template python   # Python app template
env-manager init --template docker   # Docker Compose template
```

### `get` - Read variables
```bash
env-manager get                      # List all
env-manager get DATABASE_URL         # Get specific
env-manager get --mask               # Mask secrets
```

### `set` / `unset` - Modify variables
```bash
env-manager set API_KEY abc123
env-manager unset OLD_VAR
```

### `generate` - Create secure values
```bash
env-manager generate secret SESSION_SECRET
env-manager generate password ADMIN_PASS --length 32
env-manager generate api_key STRIPE_KEY
```

### `validate` - Security check
```bash
env-manager validate
# Checks:
# - Empty values
# - Short secrets
# - .env in .gitignore
```

### `sync` - Export formats
```bash
env-manager sync --format export     # Shell exports
env-manager sync --format json       # JSON output
env-manager sync --format yaml       # YAML output
```

## Pricing

- **Individual**: $9
- **Complete Bundle** (14 tools): $49 (50% off)
- **Team License**: $129

## Why This Tool?

Managing environment variables manually is error-prone and insecure. This CLI:
- Prevents accidental secret commits
- Generates cryptographically secure values
- Validates configurations automatically
- Works with any project type
