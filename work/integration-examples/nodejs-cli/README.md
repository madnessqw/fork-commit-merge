# PrivacyLayer Node.js CLI Example

A command-line interface for PrivacyLayer operations — perfect for automation and scripting.

## Features

- 🖥️ Interactive CLI prompts
- 📜 Scriptable commands
- 🔐 Secure key management
- 📊 Batch operations support

## Installation

```bash
cd examples/nodejs-cli
npm install
npm link  # Optional: make globally available
```

## Usage

### Interactive Mode
```bash
privacy-cli deposit
privacy-cli withdraw
privacy-cli balance
privacy-cli history
```

### Script Mode
```bash
# Deposit with all parameters
privacy-cli deposit --amount 0.5 --privacy high --recipient 0x...

# Check balance
privacy-cli balance --json

# Export transaction history
privacy-cli history --format csv --output txs.csv
```

## Configuration

Create `.privacyrc.json`:

```json
{
  "network": "testnet",
  "rpcUrl": "https://...",
  "apiKey": "your-api-key",
  "defaultPrivacyLevel": "medium"
}
```

## Commands

| Command | Description | Options |
|---------|-------------|---------|
| `deposit` | Make private deposit | `--amount`, `--privacy`, `--recipient` |
| `withdraw` | Withdraw funds | `--amount`, `--recipient` |
| `balance` | Check private balance | `--json` |
| `history` | List transactions | `--format`, `--output`, `--limit` |
| `config` | Manage settings | `--set`, `--get`, `--list` |

## Examples

```bash
# Quick deposit
privacy-cli deposit -a 1.0 -p high

# Batch withdraw from file
privacy-cli batch-withdraw --file payouts.csv

# Monitor pending transactions
privacy-cli watch --interval 30
```

## License

MIT - Part of PrivacyLayer SDK Examples
