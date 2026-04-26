# 🔐 Secure Password Generator

A professional, standalone Python tool for generating cryptographically secure passwords. No dependencies, no internet required, just pure Python.

## Features

- ✅ **Cryptographically Secure**: Uses Python's `secrets` module (CSPRNG)
- ✅ **Customizable Length**: 8-128 characters
- ✅ **Character Control**: Choose which character types to include
- ✅ **Strength Analysis**: Entropy calculation and strength rating
- ✅ **Bulk Generation**: Generate multiple passwords at once
- ✅ **Export to File**: Save passwords for later use
- ✅ **Interactive & CLI Modes**: Use interactively or from command line
- ✅ **Zero Dependencies**: Pure Python, works anywhere

## Quick Start

### Interactive Mode
```bash
python secure_password_generator.py
```

### Command Line Examples

```bash
# Generate a 20-character password
python secure_password_generator.py --length 20

# Generate 10 passwords and save to file
python secure_password_generator.py --count 10 --export passwords.txt

# Generate without symbols
python secure_password_generator.py --length 32 --no-symbols

# Generate with strength stats
python secure_password_generator.py --length 24 --stats
```

## Usage Options

| Option | Description | Default |
|--------|-------------|---------|
| `-l, --length` | Password length | 16 |
| `-c, --count` | Number of passwords | 1 |
| `--no-upper` | Exclude uppercase letters | False |
| `--no-lower` | Exclude lowercase letters | False |
| `--no-digits` | Exclude digits | False |
| `--no-symbols` | Exclude special symbols | False |
| `--exclude-ambiguous` | Exclude 0, O, l, 1, I | False |
| `-e, --export` | Save to file | None |
| `-q, --quiet` | Output only passwords | False |
| `--stats` | Show strength analysis | False |

## Password Strength

The tool calculates password entropy and provides a strength rating:

| Score | Strength | Entropy | Time to Crack* |
|-------|----------|---------|----------------|
| ⭐ | Very Weak | < 28 bits | Instant |
| ⭐⭐ | Weak | 28-50 bits | Seconds |
| ⭐⭐⭐ | Fair | 50-80 bits | Hours/Days |
| ⭐⭐⭐⭐ | Strong | 80-120 bits | Years |
| ⭐⭐⭐⭐⭐ | Very Strong | > 120 bits | Centuries |

*Estimated against brute-force attacks

## Why This Tool?

Unlike online password generators:
- 🔒 **Private**: Passwords never leave your computer
- 🚀 **Fast**: Instant generation, no network latency
- 🛡️ **Secure**: Uses OS-level cryptographic randomness
- 💯 **Reliable**: Works offline, anywhere, anytime

## Use Cases

- System administrator password generation
- Developer API key creation
- Personal account security
- Bulk password generation for teams
- Secure default password setup

## License

MIT License - Use freely, modify as needed.

---

**Created by UniverseCreator** - A product built with zero budget, zero dependencies, and 100% determination.
