# DevSetup CLI - One-Command Development Environment Setup

🚀 **Spin up complete dev environments in seconds, not hours.**

Stop wasting time configuring Node.js, Python, Docker, databases, and tools. One command = ready to code.

## What It Does

```bash
# Full stack with one command
devsetup node python docker postgres redis

# Or use presets
devsetup --preset mern       # MongoDB + Express + React + Node
devsetup --preset django     # Python + Django + PostgreSQL
devsetup --preset nextjs     # Next.js + TypeScript + Tailwind + Prisma
```

## Features

✅ **Multi-Language Support**: Node.js, Python, Go, Rust, Ruby  
✅ **Database Setup**: PostgreSQL, MySQL, MongoDB, Redis  
✅ **Docker Integration**: Auto-generates docker-compose.yml  
✅ **VS Code Config**: Extensions, settings, launch configs  
✅ **Git Setup**: .gitignore templates, pre-commit hooks  
✅ **CI/CD Ready**: GitHub Actions workflows generated  
✅ **Cross-Platform**: Linux, macOS, Windows (WSL)  

## Installation

```bash
# Via pip
pip install devsetup-cli

# Or download standalone
curl -sSL https://get.devsetup.dev | bash
```

## Quick Start

```bash
# Create a new project directory
devsetup --init my-project --preset nextjs
cd my-project
npm run dev  # Already configured and ready!
```

## Presets Available

| Preset | Stack | Use Case |
|--------|-------|----------|
| `mern` | Mongo + Express + React + Node | Full-stack web apps |
| `django` | Django + PostgreSQL + Celery | Python web apps |
| `nextjs` | Next.js + TypeScript + Prisma | Modern React apps |
| `fastapi` | FastAPI + PostgreSQL + Alembic | Python APIs |
| `go-api` | Go + Gin + PostgreSQL | High-performance APIs |
| `rust-web` | Rust + Axum + PostgreSQL | Systems programming |
| `ml` | Python + PyTorch + Jupyter + Docker | Machine learning |
| `blockchain` | Hardhat + Ethers.js + TypeScript | Web3 development |

## Pricing

- **Free**: 3 presets, basic setup
- **Pro** ($9): All 15+ presets, Docker compose, CI/CD templates
- **Team** ($29): Everything + custom presets, team sharing

## Why DevSetup?

| Task | Manual Time | With DevSetup |
|------|-------------|---------------|
| Node.js + TypeScript project | 30 min | 10 sec |
| Full MERN stack | 2 hours | 30 sec |
| ML environment (PyTorch + CUDA) | 4 hours | 1 min |
| Blockchain dev setup | 1 hour | 20 sec |

**Your time is worth more than $9/hour.**

---

Built with ❤️ by developers, for developers.
