#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator CLI
Generate production-ready CI/CD workflows in seconds.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Templates for different workflows
TEMPLATES = {
    "python-ci": {
        "name": "Python CI",
        "description": "Test Python code on multiple versions",
        "content": '''name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
'''
    },
    
    "node-ci": {
        "name": "Node.js CI",
        "description": "Test Node.js code on multiple versions",
        "content": '''name: Node.js CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x, 21.x]

    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint --if-present
    
    - name: Run tests
      run: npm test --if-present
    
    - name: Build
      run: npm run build --if-present
'''
    },
    
    "docker-publish": {
        "name": "Docker Publish",
        "description": "Build and publish Docker images",
        "content": '''name: Docker Publish

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
'''
    },
    
    "release-please": {
        "name": "Release Please",
        "description": "Automated versioning and releases",
        "content": '''name: Release Please

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/release-please-action@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          release-type: python
          package-name: your-package-name
'''
    },
    
    "dependabot": {
        "name": "Dependabot Auto-merge",
        "description": "Auto-merge dependency updates",
        "content": '''name: Dependabot Auto-merge

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: write
  pull-requests: write

jobs:
  dependabot:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v1
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"
      
      - name: Auto-merge Dependabot PRs
        if: steps.metadata.outputs.update-type == 'version-update:semver-patch' || steps.metadata.outputs.update-type == 'version-update:semver-minor'
        run: gh pr merge --auto --merge "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''
    },
    
    "pages-deploy": {
        "name": "GitHub Pages Deploy",
        "description": "Deploy static sites to GitHub Pages",
        "content": '''name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''
    }
}


def list_templates():
    """List all available workflow templates."""
    print("\n📋 Available Workflow Templates:\n")
    print(f"{'Template ID':<20} {'Name':<25} {'Description'}")
    print("-" * 80)
    for template_id, template in TEMPLATES.items():
        print(f"{template_id:<20} {template['name']:<25} {template['description']}")
    print()


def generate_workflow(template_id: str, output_path: str = None, project_name: str = None):
    """Generate a workflow file from a template."""
    if template_id not in TEMPLATES:
        print(f"❌ Error: Unknown template '{template_id}'")
        print(f"   Run with --list to see available templates")
        return False
    
    template = TEMPLATES[template_id]
    content = template['content']
    
    # Replace placeholders
    if project_name:
        content = content.replace('your-package-name', project_name)
    
    # Determine output path
    if output_path is None:
        # Create .github/workflows directory if it doesn't exist
        workflows_dir = Path('.github/workflows')
        workflows_dir.mkdir(parents=True, exist_ok=True)
        output_path = workflows_dir / f"{template_id}.yml"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the workflow file
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Generated workflow: {output_path}")
    print(f"   Template: {template['name']}")
    print(f"   Description: {template['description']}")
    return True


def interactive_mode():
    """Run in interactive mode."""
    print("\n🚀 GitHub Actions Workflow Generator\n")
    print("This tool will help you create production-ready CI/CD workflows.\n")
    
    # Show available templates
    list_templates()
    
    # Get template selection
    template_id = input("Enter template ID (or 'q' to quit): ").strip().lower()
    if template_id == 'q':
        return
    
    if template_id not in TEMPLATES:
        print(f"❌ Unknown template: {template_id}")
        return
    
    # Get project name
    project_name = input("Enter project name (optional, press Enter to skip): ").strip()
    if not project_name:
        project_name = None
    
    # Get output path
    custom_path = input("Custom output path (optional, press Enter for default): ").strip()
    output_path = custom_path if custom_path else None
    
    # Generate workflow
    generate_workflow(template_id, output_path, project_name)
    
    print("\n✨ Done! Your workflow is ready to use.")
    print("   Commit and push to see it in action on GitHub.")


def main():
    parser = argparse.ArgumentParser(
        description='Generate GitHub Actions workflows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                           # List all templates
  %(prog)s --template python-ci             # Generate Python CI workflow
  %(prog)s --template docker-publish --name myapp  # Generate with project name
  %(prog)s --interactive                    # Run interactive mode
        """
    )
    
    parser.add_argument('-t', '--template', 
                        help='Template ID to generate (use --list to see options)')
    parser.add_argument('-o', '--output', 
                        help='Output file path (default: .github/workflows/<template>.yml)')
    parser.add_argument('-n', '--name', 
                        help='Project name (replaces placeholders in template)')
    parser.add_argument('-l', '--list', 
                        action='store_true', 
                        help='List all available templates')
    parser.add_argument('-i', '--interactive', 
                        action='store_true', 
                        help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.list:
        list_templates()
        sys.exit(0)
    
    if args.interactive:
        interactive_mode()
        sys.exit(0)
    
    if args.template:
        success = generate_workflow(args.template, args.output, args.name)
        sys.exit(0 if success else 1)
    
    # No arguments - show help
    parser.print_help()
    sys.exit(0)


if __name__ == '__main__':
    main()