#!/usr/bin/env python3
"""
Project Initializer CLI
One command to initialize a complete, production-ready project.
"""

import argparse
import os
from pathlib import Path

TEMPLATES = {
    "readme": {
        "minimal": """# {name}

{description}

## Installation
```bash
pip install {name}
```

## License
MIT
""",
        "standard": """# {name}

{description}

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
```bash
pip install {name}
```

## Contributing
Pull requests welcome!

## License
MIT
"""
    },
    "gitignore": {
        "python": """__pycache__/
*.py[cod]
build/
dist/
*.egg-info/
venv/
.env
.vscode/
.idea/
.pytest_cache/
.coverage
""",
        "node": """node_modules/
build/
dist/
.env
.vscode/
.idea/
coverage/
*.log
""",
        "go": """*.exe
*.test
vendor/
.env
.vscode/
.idea/
"""
    },
    "docker": {
        "python": """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "{name}"]
""",
        "node": """FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
"""
    },
    "github_actions": """name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    - name: Run tests
      run: pytest
""",
    "license_mit": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""
}

def create_project(args):
    """Create a new project with all selected components."""
    project_path = Path(args.name)
    
    if project_path.exists() and not args.force:
        print(f"Error: {args.name} already exists. Use --force to overwrite.")
        return False
    
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create README
    if args.readme:
        readme_content = TEMPLATES["readme"][args.readme_type].format(
            name=args.name,
            description=args.description or f"A {args.language} project"
        )
        (project_path / "README.md").write_text(readme_content)
        print(f"✓ Created README.md ({args.readme_type})")
    
    # Create .gitignore
    if args.gitignore and args.language in TEMPLATES["gitignore"]:
        gitignore_content = TEMPLATES["gitignore"][args.language]
        (project_path / ".gitignore").write_text(gitignore_content)
        print(f"✓ Created .gitignore ({args.language})")
    
    # Create Dockerfile
    if args.docker and args.language in TEMPLATES["docker"]:
        docker_content = TEMPLATES["docker"][args.language].format(name=args.name)
        (project_path / "Dockerfile").write_text(docker_content)
        print(f"✓ Created Dockerfile ({args.language})")
    
    # Create GitHub Actions workflow
    if args.github_actions:
        workflows_dir = project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        (workflows_dir / "ci.yml").write_text(TEMPLATES["github_actions"])
        print("✓ Created .github/workflows/ci.yml")
    
    # Create LICENSE
    if args.license:
        license_content = TEMPLATES["license_mit"].format(
            year=args.year,
            author=args.author or "Your Name"
        )
        (project_path / "LICENSE").write_text(license_content)
        print("✓ Created LICENSE (MIT)")
    
    # Create src directory
    if args.src_dir:
        src_dir = project_path / args.name.replace("-", "_")
        src_dir.mkdir(exist_ok=True)
        (src_dir / "__init__.py").write_text(f'"""{args.description or args.name}"""\n\n__version__ = "0.1.0"\n')
        print(f"✓ Created {src_dir}/ directory")
    
    # Create tests directory
    if args.tests_dir:
        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / f"test_{args.name.replace('-', '_')}.py").write_text("""import pytest

def test_example():
    assert True
""")
        print("✓ Created tests/ directory")
    
    # Create requirements.txt
    if args.requirements:
        (project_path / "requirements.txt").write_text("# Add your dependencies here\n")
        print("✓ Created requirements.txt")
    
    print(f"\n🎉 Project '{args.name}' initialized successfully!")
    print(f"   Location: {project_path.absolute()}")
    return True

def list_templates():
    """List available templates."""
    print("Available Templates:")
    print("\nREADME Types:")
    for t in TEMPLATES["readme"].keys():
        print(f"  - {t}")
    print("\nLanguages (for .gitignore, Dockerfile):")
    for lang in TEMPLATES["gitignore"].keys():
        print(f"  - {lang}")

def main():
    parser = argparse.ArgumentParser(
        description="Initialize a complete, production-ready project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  project-init my-project --language python
  project-init my-api --language node --readme-type api --docker
  project-init my-lib --all
        """
    )
    
    parser.add_argument("name", help="Project name")
    parser.add_argument("--description", "-d", help="Project description")
    parser.add_argument("--author", "-a", help="Author name")
    parser.add_argument("--language", "-l", default="python",
                       choices=["python", "node", "go", "rust", "java"],
                       help="Primary language (default: python)")
    parser.add_argument("--year", "-y", type=int, default=2026,
                       help="Copyright year (default: 2026)")
    
    # Component toggles
    parser.add_argument("--readme", action="store_true", default=True,
                       help="Create README.md (default: True)")
    parser.add_argument("--readme-type", default="standard",
                       choices=["minimal", "standard"],
                       help="README template type")
    parser.add_argument("--gitignore", action="store_true", default=True,
                       help="Create .gitignore (default: True)")
    parser.add_argument("--docker", action="store_true",
                       help="Create Dockerfile")
    parser.add_argument("--github-actions", "-gha", action="store_true",
                       help="Create GitHub Actions workflow")
    parser.add_argument("--license", action="store_true", default=True,
                       help="Create LICENSE file (default: True)")
    parser.add_argument("--src-dir", "-s", action="store_true",
                       help="Create src/ directory")
    parser.add_argument("--tests-dir", "-t", action="store_true",
                       help="Create tests/ directory")
    parser.add_argument("--requirements", "-r", action="store_true",
                       help="Create requirements.txt")
    parser.add_argument("--all", action="store_true",
                       help="Enable all components")
    parser.add_argument("--force", "-f", action="store_true",
                       help="Overwrite existing directory")
    parser.add_argument("--list-templates", action="store_true",
                       help="List available templates")
    
    args = parser.parse_args()
    
    if args.list_templates:
        list_templates()
        return
    
    # If --all is specified, enable all components
    if args.all:
        args.docker = True
        args.github_actions = True
        args.src_dir = True
        args.tests_dir = True
        args.requirements = True
    
    create_project(args)

if __name__ == "__main__":
    main()