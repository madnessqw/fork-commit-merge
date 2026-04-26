# PrivacyLayer Integration Examples

Complete integration examples for popular frameworks and platforms.

## Overview

This directory contains working examples for:
- **React** — Hooks-based integration with TypeScript
- **Vue** — Composition API with reactive state
- **Angular** — RxJS-based service architecture
- **Node.js CLI** — Command-line interface for automation
- **Python** — Python SDK for data pipelines and backend

## Quick Start

Each example is self-contained with its own README:

```bash
# React
cd react && npm install && npm run dev

# Vue
cd vue && npm install && npm run dev

# Angular
cd angular && npm install && ng serve

# Node.js CLI
cd nodejs-cli && npm install && npm run build

# Python
cd python && pip install -r requirements.txt && python example.py
```

## Common Patterns

All examples demonstrate:
1. SDK initialization with configuration
2. Private deposit with privacy level selection
3. Secure withdrawal to any address
4. Balance checking
5. Transaction history with privacy indicators

## Privacy Levels

| Level | Anonymity | Time | Best For |
|-------|-----------|------|----------|
| Low | 10 users | ~2s | Quick transfers |
| Medium | 100 users | ~10s | Standard use |
| High | 1000+ users | ~30s | Maximum privacy |

## Configuration

All examples support environment-based configuration:

```bash
export PRIVACYLAYER_NETWORK=testnet  # or mainnet
export PRIVACYLAYER_API_KEY=your-key
export PRIVACYLAYER_RPC_URL=https://...
```

## License

MIT - Part of PrivacyLayer SDK
