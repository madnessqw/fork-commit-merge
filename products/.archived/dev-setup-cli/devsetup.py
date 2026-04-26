#!/usr/bin/env python3
"""
DevSetup CLI - One-Command Development Environment Setup
Automates the tedious parts of starting new projects.
"""

import argparse
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

__version__ = "1.0.0"

# Preset configurations
PRESETS = {
    "mern": {
        "name": "MERN Stack",
        "description": "MongoDB + Express + React + Node.js",
        "languages": ["node"],
        "databases": ["mongodb"],
        "tools": ["docker", "eslint", "prettier"],
        "packages": {
            "frontend": ["react", "react-dom", "vite", "@vitejs/plugin-react"],
            "backend": ["express", "mongoose", "cors", "dotenv"]
        }
    },
    "django": {
        "name": "Django Stack",
        "description": "Django + PostgreSQL + Celery",
        "languages": ["python"],
        "databases": ["postgres"],
        "tools": ["docker", "black", "flake8"],
        "packages": ["django", "psycopg2-binary", "celery", "redis", "djangorestframework"]
    },
    "nextjs": {
        "name": "Next.js Full Stack",
        "description": "Next.js + TypeScript + Tailwind + Prisma",
        "languages": ["node"],
        "databases": ["postgres"],
        "tools": ["docker", "typescript", "tailwind", "prisma"],
        "packages": ["next", "react", "react-dom", "typescript", "@types/node", "@types/react", "tailwindcss", "prisma", "@prisma/client"]
    },
    "fastapi": {
        "name": "FastAPI Stack",
        "description": "FastAPI + PostgreSQL + Alembic",
        "languages": ["python"],
        "databases": ["postgres"],
        "tools": ["docker", "black", "pytest", "alembic"],
        "packages": ["fastapi", "uvicorn", "sqlalchemy", "alembic", "psycopg2-binary", "pydantic", "python-dotenv"]
    },
    "go-api": {
        "name": "Go API Stack",
        "description": "Go + Gin + PostgreSQL",
        "languages": ["go"],
        "databases": ["postgres"],
        "tools": ["docker", "air"],
        "packages": ["github.com/gin-gonic/gin", "github.com/joho/godotenv", "github.com/lib/pq"]
    },
    "rust-web": {
        "name": "Rust Web Stack",
        "description": "Rust + Axum + PostgreSQL",
        "languages": ["rust"],
        "databases": ["postgres"],
        "tools": ["docker", "cargo-watch"],
        "packages": ["axum", "tokio", "sqlx", "serde", "serde_json", "dotenvy"]
    },
    "ml": {
        "name": "ML Development",
        "description": "Python + PyTorch + Jupyter + Docker",
        "languages": ["python"],
        "databases": [],
        "tools": ["docker", "jupyter", "conda"],
        "packages": ["torch", "torchvision", "jupyter", "numpy", "pandas", "matplotlib", "scikit-learn"]
    },
    "blockchain": {
        "name": "Blockchain Dev",
        "description": "Hardhat + Ethers.js + TypeScript",
        "languages": ["node"],
        "databases": [],
        "tools": ["hardhat", "typescript", "eslint"],
        "packages": ["hardhat", "ethers", "@nomicfoundation/hardhat-toolbox", "@typechain/hardhat", "typescript", "ts-node"]
    }
}

# Gitignore templates
GITIGNORE_TEMPLATES = {
    "node": """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# Build
dist/
build/
.next/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/*
!.vscode/extensions.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
""",
    "python": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
""",
    "go": """# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
""",
    "rust": """# Rust
/target/
**/*.rs.bk
Cargo.lock

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""
}

# Docker Compose templates
DOCKER_COMPOSE_TEMPLATE = """version: '3.8'

services:
{services}

volumes:
{volumes}
"""

DB_SERVICES = {
    "postgres": """  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-dev}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-dev}
      POSTGRES_DB: ${DB_NAME:-app}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
""",
    "mongodb": """  mongodb:
    image: mongo:7-jammy
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${DB_USER:-dev}
      MONGO_INITDB_ROOT_PASSWORD: ${DB_PASSWORD:-dev}
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
""",
    "mysql": """  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD:-root}
      MYSQL_DATABASE: ${DB_NAME:-app}
      MYSQL_USER: ${DB_USER:-dev}
      MYSQL_PASSWORD: ${DB_PASSWORD:-dev}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
""",
    "redis": """  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
"""
}

DB_VOLUMES = {
    "postgres": "  postgres_data:",
    "mongodb": "  mongodb_data:",
    "mysql": "  mysql_data:",
    "redis": "  redis_data:"
}


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")
    print("=" * 50)


def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_info(text: str):
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def print_warning(text: str):
    print(f"{Colors.WARNING}⚠ {text}{Colors.END}")


def print_error(text: str):
    print(f"{Colors.FAIL}✗ {text}{Colors.END}")


def run_command(cmd: List[str], cwd: Optional[str] = None) -> bool:
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        return False


def check_command(cmd: str) -> bool:
    """Check if a command is available."""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_directory_structure(base_path: Path, preset: Dict) -> None:
    """Create the project directory structure."""
    print_info("Creating directory structure...")
    
    # Create base directories
    dirs = ["src", "docs", "scripts", "config"]
    if "docker" in preset.get("tools", []):
        dirs.append("docker")
    
    for dir_name in dirs:
        (base_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    print_success("Directory structure created")


def create_gitignore(base_path: Path, languages: List[str]) -> None:
    """Create .gitignore file."""
    print_info("Creating .gitignore...")
    
    gitignore_content = ""
    for lang in languages:
        if lang in GITIGNORE_TEMPLATES:
            gitignore_content += f"# {lang.upper()}\n"
            gitignore_content += GITIGNORE_TEMPLATES[lang] + "\n"
    
    (base_path / ".gitignore").write_text(gitignore_content)
    print_success(".gitignore created")


def create_docker_compose(base_path: Path, databases: List[str]) -> None:
    """Create docker-compose.yml for databases."""
    if not databases:
        return
    
    print_info("Creating docker-compose.yml...")
    
    services = ""
    volumes = ""
    
    for db in databases:
        if db in DB_SERVICES:
            services += DB_SERVICES[db] + "\n"
        if db in DB_VOLUMES:
            volumes += DB_VOLUMES[db] + "\n"
    
    compose_content = DOCKER_COMPOSE_TEMPLATE.format(
        services=services,
        volumes=volumes
    )
    
    (base_path / "docker-compose.yml").write_text(compose_content)
    print_success("docker-compose.yml created")


def create_env_file(base_path: Path, databases: List[str]) -> None:
    """Create .env.example file."""
    print_info("Creating .env.example...")
    
    env_content = """# Development Environment Variables
NODE_ENV=development
"""
    
    if databases:
        env_content += """
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=dev
DB_PASSWORD=dev
DB_NAME=app
"""
    
    (base_path / ".env.example").write_text(env_content)
    (base_path / ".env").write_text(env_content.replace("=dev", "=changeme"))
    print_success("Environment files created")


def setup_node_project(base_path: Path, preset: Dict, project_name: str) -> None:
    """Setup a Node.js project."""
    print_info("Setting up Node.js project...")
    
    # Create package.json
    package_json = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"Generated with DevSetup CLI - {preset['name']}",
        "main": "src/index.js",
        "scripts": {
            "dev": "node src/index.js",
            "start": "node src/index.js",
            "test": "echo 'Error: no test specified' && exit 1"
        },
        "keywords": [],
        "author": "",
        "license": "MIT",
        "dependencies": {},
        "devDependencies": {}
    }
    
    # Add TypeScript if needed
    if "typescript" in preset.get("tools", []):
        package_json["scripts"]["dev"] = "ts-node src/index.ts"
        package_json["scripts"]["build"] = "tsc"
        package_json["main"] = "dist/index.js"
    
    # Add packages
    packages = preset.get("packages", [])
    if isinstance(packages, dict):
        packages = packages.get("backend", [])
    
    for pkg in packages:
        package_json["dependencies"][pkg] = "latest"
    
    (base_path / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # Create basic entry file
    if "typescript" in preset.get("tools", []):
        (base_path / "src" / "index.ts").write_text("""console.log('Hello from DevSetup!');
""")
    else:
        (base_path / "src" / "index.js").write_text("""console.log('Hello from DevSetup!');
""")
    
    print_success("Node.js project initialized")


def setup_python_project(base_path: Path, preset: Dict, project_name: str) -> None:
    """Setup a Python project."""
    print_info("Setting up Python project...")
    
    # Create requirements.txt
    packages = preset.get("packages", [])
    if isinstance(packages, dict):
        packages = packages.get("backend", [])
    
    requirements = "\n".join(packages) if packages else "# Add your dependencies here"
    (base_path / "requirements.txt").write_text(requirements + "\n")
    
    # Create basic Python file
    (base_path / "src" / "main.py").write_text("""def main():
    print("Hello from DevSetup!")

if __name__ == "__main__":
    main()
""")
    
    print_success("Python project initialized")


def setup_go_project(base_path: Path, preset: Dict, project_name: str) -> None:
    """Setup a Go project."""
    print_info("Setting up Go project...")
    
    # Initialize Go module
    run_command(["go", "mod", "init", project_name], cwd=str(base_path))
    
    # Create basic Go file
    (base_path / "main.go").write_text("""package main

import "fmt"

func main() {
    fmt.Println("Hello from DevSetup!")
}
""")
    
    print_success("Go project initialized")


def setup_rust_project(base_path: Path, preset: Dict, project_name: str) -> None:
    """Setup a Rust project."""
    print_info("Setting up Rust project...")
    
    # Initialize Cargo project
    run_command(["cargo", "init", "--name", project_name], cwd=str(base_path))
    
    print_success("Rust project initialized")


def create_readme(base_path: Path, preset: Dict, project_name: str) -> None:
    """Create project README."""
    readme_content = f"""# {project_name}

Generated with DevSetup CLI - {preset['name']}

## Quick Start

```bash
# Install dependencies
"""
    
    if "node" in preset.get("languages", []):
        readme_content += "npm install\n\n# Run development server\nnpm run dev\n"
    elif "python" in preset.get("languages", []):
        readme_content += "pip install -r requirements.txt\n\n# Run\npython src/main.py\n"
    elif "go" in preset.get("languages", []):
        readme_content += "go mod tidy\n\n# Run\ngo run main.go\n"
    elif "rust" in preset.get("languages", []):
        readme_content += "cargo build\n\n# Run\ncargo run\n"
    
    readme_content += """```

## Project Structure

```
.
├── src/            # Source code
├── docs/           # Documentation
├── scripts/        # Utility scripts
├── config/         # Configuration files
└── README.md       # This file
```

## Environment Setup

1. Copy `.env.example` to `.env`
2. Update the values as needed
"""
    
    if preset.get("databases"):
        readme_content += """
3. Start databases with Docker:
   ```bash
   docker-compose up -d
   ```
"""
    
    (base_path / "README.md").write_text(readme_content)
    print_success("README.md created")


def list_presets():
    """List all available presets."""
    print_header("Available Presets")
    
    for key, preset in PRESETS.items():
        print(f"{Colors.BOLD}{key:12}{Colors.END} - {preset['name']}")
        print(f"{' ' * 12}  {preset['description']}")
        print()


def apply_preset(preset_name: str, project_path: Path, project_name: str) -> bool:
    """Apply a preset to create a project."""
    if preset_name not in PRESETS:
        print_error(f"Unknown preset: {preset_name}")
        print_info(f"Run 'devsetup --list' to see available presets")
        return False
    
    preset = PRESETS[preset_name]
    
    print_header(f"Setting up {preset['name']}")
    print_info(f"Project: {project_name}")
    print_info(f"Location: {project_path}")
    print()
    
    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    create_directory_structure(project_path, preset)
    
    # Create .gitignore
    create_gitignore(project_path, preset.get("languages", []))
    
    # Create docker-compose if databases
    if preset.get("databases"):
        create_docker_compose(project_path, preset["databases"])
    
    # Create environment files
    create_env_file(project_path, preset.get("databases", []))
    
    # Setup language-specific project
    for lang in preset.get("languages", []):
        if lang == "node":
            setup_node_project(project_path, preset, project_name)
        elif lang == "python":
            setup_python_project(project_path, preset, project_name)
        elif lang == "go":
            setup_go_project(project_path, preset, project_name)
        elif lang == "rust":
            setup_rust_project(project_path, preset, project_name)
    
    # Create README
    create_readme(project_path, preset, project_name)
    
    print()
    print_header("Setup Complete!")
    print_success(f"Project '{project_name}' is ready at {project_path}")
    print()
    print_info("Next steps:")
    print(f"  cd {project_path}")
    
    if preset.get("databases"):
        print("  docker-compose up -d")
    
    if "node" in preset.get("languages", []):
        print("  npm install")
        print("  npm run dev")
    elif "python" in preset.get("languages", []):
        print("  pip install -r requirements.txt")
        print("  python src/main.py")
    elif "go" in preset.get("languages", []):
        print("  go run main.go")
    elif "rust" in preset.get("languages", []):
        print("  cargo run")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="DevSetup CLI - One-command development environment setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devsetup --list                    # List all available presets
  devsetup --preset nextjs my-app    # Create Next.js project
  devsetup --init my-app --preset django  # Initialize in new directory
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--list", "-l", action="store_true", help="List available presets")
    parser.add_argument("--preset", "-p", help="Preset to use")
    parser.add_argument("--init", "-i", action="store_true", help="Create new directory for project")
    parser.add_argument("name", nargs="?", help="Project name/directory")
    
    args = parser.parse_args()
    
    # List presets
    if args.list:
        list_presets()
        return 0
    
    # Validate arguments
    if not args.preset:
        print_error("No preset specified. Use --preset or --list")
        return 1
    
    if not args.name:
        print_error("No project name specified")
        return 1
    
    # Determine project path
    if args.init:
        project_path = Path.cwd() / args.name
    else:
        project_path = Path(args.name).resolve()
    
    # Apply preset
    success = apply_preset(args.preset, project_path, args.name)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
