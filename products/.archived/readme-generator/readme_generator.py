#!/usr/bin/env python3
"""
README Generator CLI - Professional README files in seconds
A tool for developers who hate writing documentation
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


TEMPLATES = {
    "standard": """# {name}

{description}

## Features

{features}

## Installation

```bash
{install_command}
```

## Usage

```bash
{usage_example}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the {license} License.
""",

    "minimal": """# {name}

{description}

## Quick Start

```bash
{install_command}
{usage_example}
```

## License

{license}
""",

    "comprehensive": """# {name}

<p align="center">
  <b>{tagline}</b>
</p>

<p align="center">
  {badges}
</p>

---

## 🚀 Features

{features}

## 📦 Installation

### Prerequisites

{prerequisites}

### Install

```bash
{install_command}
```

## 💡 Usage

### Basic Usage

```bash
{usage_example}
```

### Advanced Options

{advanced_usage}

## 🛠️ Configuration

{configuration}

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the {license} License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

{acknowledgments}

---

<p align="center">
  Made with ❤️ by {author}
</p>
""",

    "api": """# {name}

{description}

## API Reference

{api_docs}

## Authentication

{auth_info}

## Rate Limits

{rate_limits}

## Examples

{examples}

## License

{license}
"""
}


def generate_badges(github_user, github_repo, license_name):
    """Generate common badges for README"""
    badges = []
    if github_user and github_repo:
        badges.append(f"![Build](https://img.shields.io/github/workflow/status/{github_user}/{github_repo}/CI)")
        badges.append(f"![License](https://img.shields.io/github/license/{github_user}/{github_repo})")
        badges.append(f"![Stars](https://img.shields.io/github/stars/{github_user}/{github_repo})")
    if license_name:
        badges.append(f"![License: {license_name}](https://img.shields.io/badge/License-{license_name}-blue.svg)")
    return "\n  ".join(badges)


def interactive_mode():
    """Interactive mode for collecting project info"""
    print("📝 README Generator - Interactive Mode")
    print("=" * 50)
    
    data = {}
    data["name"] = input("Project name: ").strip()
    data["description"] = input("Short description: ").strip()
    data["tagline"] = input("Tagline (one-liner): ").strip()
    
    print("\nSelect template:")
    print("1. standard - Balanced detail")
    print("2. minimal - Quick and simple")
    print("3. comprehensive - Full documentation")
    print("4. api - API/service focused")
    
    template_choice = input("Choice (1-4): ").strip()
    template_map = {"1": "standard", "2": "minimal", "3": "comprehensive", "4": "api"}
    data["template"] = template_map.get(template_choice, "standard")
    
    data["features"] = input("Key features (comma-separated): ").strip()
    data["features"] = "\n".join([f"- {f.strip()}" for f in data["features"].split(",")])
    
    data["install_command"] = input("Install command: ").strip() or f"pip install {data['name'].lower()}"
    data["usage_example"] = input("Usage example: ").strip() or f"{data['name'].lower()} --help"
    data["license"] = input("License (MIT/Apache/GPL): ").strip() or "MIT"
    data["author"] = input("Author name: ").strip()
    
    if data["template"] == "comprehensive":
        data["prerequisites"] = input("Prerequisites: ").strip() or "None"
        data["advanced_usage"] = input("Advanced usage example: ").strip() or "See documentation"
        data["configuration"] = input("Configuration details: ").strip() or "No configuration required"
        data["acknowledgments"] = input("Acknowledgments: ").strip() or "Thanks to all contributors"
        
        github_user = input("GitHub username (optional): ").strip()
        github_repo = input("GitHub repo name (optional): ").strip()
        data["badges"] = generate_badges(github_user, github_repo, data["license"])
    
    if data["template"] == "api":
        data["api_docs"] = input("API docs URL or summary: ").strip()
        data["auth_info"] = input("Authentication method: ").strip()
        data["rate_limits"] = input("Rate limit info: ").strip() or "100 requests/minute"
        data["examples"] = input("Code examples: ").strip()
    
    return data


def generate_readme(data):
    """Generate README from template and data"""
    template_name = data.get("template", "standard")
    template = TEMPLATES.get(template_name, TEMPLATES["standard"])
    
    try:
        return template.format(**data)
    except KeyError as e:
        missing_key = str(e).strip("'")
        data[missing_key] = ""
        return generate_readme(data)


def main():
    parser = argparse.ArgumentParser(
        description="Generate professional README files instantly",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --interactive              # Interactive mode
  %(prog)s --json project.json        # From JSON file
  %(prog)s --name "My Project" --desc "A cool tool"  # Quick mode
        """
    )
    
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--json", "-j", metavar="FILE", help="Read config from JSON file")
    parser.add_argument("--output", "-o", metavar="FILE", default="README.md", help="Output file")
    parser.add_argument("--template", "-t", choices=["standard", "minimal", "comprehensive", "api"], 
                        default="standard", help="README template")
    
    # Quick mode arguments
    parser.add_argument("--name", "-n", help="Project name")
    parser.add_argument("--desc", "-d", help="Project description")
    parser.add_argument("--license", "-l", default="MIT", help="License type")
    
    args = parser.parse_args()
    
    # Collect data
    if args.interactive:
        data = interactive_mode()
    elif args.json:
        with open(args.json, 'r') as f:
            data = json.load(f)
    elif args.name:
        data = {
            "name": args.name,
            "description": args.desc or f"{args.name} - A great project",
            "template": args.template,
            "features": "- Core functionality\n- Easy to use\n- Well documented",
            "install_command": f"pip install {args.name.lower()}",
            "usage_example": f"{args.name.lower()} --help",
            "license": args.license,
            "author": "Your Name"
        }
    else:
        parser.print_help()
        sys.exit(1)
    
    # Generate README
    readme = generate_readme(data)
    
    # Write output
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        f.write(readme)
    
    print(f"✅ README generated: {output_path.absolute()}")
    print(f"   Template: {data.get('template', 'standard')}")
    print(f"   Length: {len(readme)} characters")


if __name__ == "__main__":
    main()
