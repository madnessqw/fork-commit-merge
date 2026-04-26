# 🔐 API Key Manager CLI

Securely store, organize, and manage your API keys with encryption. Never lose or expose your API keys again.

## Features

- 🔒 **Military-grade encryption** - Keys encrypted at rest using PBKDF2 + Fernet
- 🏷️ **Smart organization** - Tag keys by service and environment
- 🔍 **Quick search** - Find keys instantly by name, service, or environment
- 📋 **Clipboard integration** - Copy keys without revealing them
- 🔄 **Import/Export** - Backup and migrate your keys securely
- 🎲 **Key generation** - Generate secure random API keys
- 🔐 **Master password** - Single password protects all your keys

## Installation

```bash
# Download the script
curl -O https://raw.githubusercontent.com/yourusername/api-key-manager/main/api_key_manager.py

# Make it executable
chmod +x api_key_manager.py

# Optional: Install to PATH
mv api_key_manager.py /usr/local/bin/api-key-manager
```

### Optional Dependencies

For enhanced security and clipboard support:

```bash
pip install cryptography pyperclip
```

## Quick Start

```bash
# 1. Initialize (set your master password)
api-key-manager setup

# 2. Add your first API key
api-key-manager add stripe-prod --service "Stripe" --env production

# 3. List all keys
api-key-manager list

# 4. Retrieve a key
api-key-manager get stripe-prod

# 5. Copy to clipboard
api-key-manager get stripe-prod --copy
```

## Commands

### `setup` - Initialize the key manager
```bash
api-key-manager setup
```
Sets up encrypted storage in `~/.config/api-key-manager/`

### `add` - Store a new API key
```bash
api-key-manager add <name> --service <service> --env <environment>
api-key-manager add stripe-prod --service "Stripe" --env production
```

### `get` - Retrieve an API key
```bash
api-key-manager get <name>
api-key-manager get stripe-prod --copy  # Copy to clipboard
```

### `list` - View all stored keys
```bash
api-key-manager list
api-key-manager list --service Stripe
api-key-manager list --env production
```

### `update` - Modify an existing key
```bash
api-key-manager update <name> --key <new-value> --service <new-service>
api-key-manager update stripe-prod --env staging
```

### `delete` - Remove a key
```bash
api-key-manager delete <name>
```

### `generate` - Create a secure random key
```bash
api-key-manager generate <name> --service <service> --length 32
api-key-manager generate my-api-key --service "MyApp" --length 48
```

### `export` - Backup your keys
```bash
api-key-manager export backup.enc
```
Creates an encrypted backup file you can store safely.

### `import` - Restore from backup
```bash
api-key-manager import backup.enc
```

## Security

- **Encryption**: Uses PBKDF2 key derivation with 100,000 iterations + Fernet symmetric encryption
- **Storage**: Keys stored in `~/.config/api-key-manager/` with 600 permissions (owner only)
- **Memory**: Keys only decrypted when retrieved, never logged
- **Master Password**: SHA-256 hashed, never stored in plain text

## Use Cases

- **Development teams** - Share API keys securely across team members
- **Freelancers** - Manage multiple client API keys
- **DevOps** - Organize production/staging/test keys
- **Security-conscious developers** - Never commit keys to git again

## Pricing

**$9** - One-time purchase, lifetime updates

Or get the **Complete Developer Toolkit** (8 tools) for **$39** (35% off)

## Requirements

- Python 3.7+
- Optional: `cryptography` for enhanced encryption
- Optional: `pyperclip` for clipboard support

## License

MIT License - See LICENSE file for details
