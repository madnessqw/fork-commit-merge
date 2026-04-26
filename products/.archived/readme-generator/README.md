# README Generator CLI

Generate professional README files in seconds. Stop wasting time on documentation.

## Features

- 🚀 **4 Templates**: Standard, Minimal, Comprehensive, API-focused
- 🎨 **Interactive Mode**: Guided setup for perfect READMEs
- 📁 **JSON Config**: Batch generate from project configs
- ⚡ **Quick Mode**: One-liner generation for fast workflows
- 🎯 **Smart Defaults**: Sensible defaults for all fields

## Installation

```bash
# Clone and use directly
git clone <repo-url>
cd readme-generator
python readme_generator.py --help

# Or install globally
pip install readme-generator-cli
```

## Usage

### Interactive Mode (Recommended)

```bash
python readme_generator.py --interactive
```

Follow the prompts to create a perfect README tailored to your project.

### Quick Mode

```bash
python readme_generator.py --name "My Project" --desc "A cool tool" --template comprehensive
```

### From JSON Config

```bash
python readme_generator.py --json project.json --output README.md
```

Example `project.json`:
```json
{
  "name": "My Awesome Project",
  "description": "Does amazing things",
  "template": "comprehensive",
  "features": "- Fast\n- Reliable\n- Easy to use",
  "install_command": "pip install my-project",
  "usage_example": "my-project run",
  "license": "MIT",
  "author": "Your Name"
}
```

## Templates

| Template | Best For | Length |
|----------|----------|--------|
| `minimal` | Simple tools, prototypes | Short |
| `standard` | Most projects | Medium |
| `comprehensive` | Open source, libraries | Long |
| `api` | APIs, services | Medium |

## Examples

### Minimal Template
```bash
python readme_generator.py --name "Todo CLI" --desc "Simple todo manager" --template minimal
```

### API Template
```bash
python readme_generator.py --interactive
# Select template: api
```

## License

MIT License - see LICENSE file for details.

---

**Stop procrastinating on documentation. Generate your README now.**
