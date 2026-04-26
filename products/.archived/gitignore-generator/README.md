# .gitignore Generator

Create perfect .gitignore files for any project in seconds.

## Features

- 🎯 **10+ Templates**: Python, Node.js, Go, Rust, Java, Flutter, Unity, Docker, Web
- 🔗 **Smart Combinations**: Fullstack, ML, Mobile, DevOps, Game dev presets
- 💬 **Interactive Mode**: Guided selection for perfect matches
- ⚡ **Quick Mode**: One command, instant .gitignore
- 📝 **Custom Rules**: Add your own patterns easily

## Installation

```bash
# Direct usage
python gitignore_generator.py --help

# Or install
pip install gitignore-generator-cli
```

## Usage

### Interactive Mode (Recommended)

```bash
python gitignore_generator.py --interactive
```

### Quick Generation

```bash
# Single template
python gitignore_generator.py python

# Multiple templates
python gitignore_generator.py python node web

# Combination preset
python gitignore_generator.py fullstack
```

### List All Templates

```bash
python gitignore_generator.py --list
```

## Templates

| Template | Description |
|----------|-------------|
| `python` | Python, virtualenv, pytest |
| `node` | Node.js, npm, yarn |
| `go` | Go binaries, vendor |
| `rust` | Cargo, target directory |
| `java` | Maven, Gradle, IntelliJ |
| `web` | General web development |
| `flutter` | Flutter/Dart projects |
| `unity` | Unity game projects |
| `docker` | Docker, env files |
| `base` | OS files, IDE configs |

## Combinations

| Combination | Includes |
|-------------|----------|
| `fullstack` | Node + Python + Web |
| `ml` | Python + Base |
| `mobile` | Flutter + Base |
| `devops` | Docker + Base |
| `game` | Unity + Base |

## Examples

### Python Project
```bash
python gitignore_generator.py python
```

### Full-Stack Web App
```bash
python gitignore_generator.py fullstack
# or
python gitignore_generator.py node python web
```

### Machine Learning
```bash
python gitignore_generator.py ml
```

## License

MIT License

---

**Never commit the wrong files again.**
