# Git Commit Message Generator CLI

Generate conventional commit messages with smart suggestions, templates, and interactive mode. Never struggle with commit messages again.

## Features

✨ **Smart Suggestions** - Analyzes your staged changes and suggests appropriate commit messages

🎯 **Conventional Commits** - Follows the conventional commits specification

📝 **Interactive Mode** - Guided step-by-step commit message creation

⚡ **Quick Mode** - One-liner commits when you know what you want

🔍 **Auto-Detection** - Automatically detects scope from changed files

## Installation

```bash
# Download the script
curl -O https://raw.githubusercontent.com/yourusername/commit-generator/main/commit_generator.py

# Make executable
chmod +x commit_generator.py

# Optional: Add to PATH
sudo mv commit_generator.py /usr/local/bin/commit-gen
```

## Usage

### Interactive Mode (Recommended)
```bash
python commit_generator.py
# or
commit-gen
```

Guides you through:
1. Commit type selection (feat, fix, docs, etc.)
2. Scope detection/auto-suggestion
3. Message templates or custom input
4. Optional body and footer

### Quick Mode
```bash
# Quick commit with type and message
commit-gen -q feat "add user authentication"

# With scope
commit-gen -q fix "resolve null pointer" -s api --commit

# Actually commit (adds --commit flag)
commit-gen -q feat "add dashboard" --commit
```

### Suggest Mode
```bash
# Get AI-like suggestions based on staged changes
commit-gen --suggest
```

Example output:
```
📝 Suggested commit messages:

  1. feat(auth): add login module
     Type: feat, Template: add

  2. fix(auth): resolve issue in auth module
     Type: fix, Template: fix

  3. refactor(auth): improve auth structure
     Type: refactor, Template: refactor
```

### List Commit Types
```bash
commit-gen --types
```

Output:
```
📋 Conventional Commit Types:

  feat       - A new feature
  fix        - A bug fix
  docs       - Documentation only changes
  style      - Code style changes (formatting, semicolons)
  refactor   - Code change that neither fixes a bug nor adds a feature
  perf       - Performance improvement
  test       - Adding or correcting tests
  chore      - Build process or auxiliary tool changes
  ci         - CI configuration changes
  build      - Build system or dependency changes
  revert     - Reverts a previous commit
```

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): resolve timeout issue` |
| `docs` | Documentation | `docs(readme): update install guide` |
| `style` | Code style | `style(css): fix indentation` |
| `refactor` | Refactoring | `refactor(core): simplify parser` |
| `perf` | Performance | `perf(query): optimize database calls` |
| `test` | Tests | `test(auth): add login tests` |
| `chore` | Maintenance | `chore(deps): update packages` |
| `ci` | CI/CD | `ci(github): add deploy workflow` |
| `build` | Build system | `build(docker): add multi-stage build` |
| `revert` | Revert | `revert: undo auth changes` |

## Why Conventional Commits?

1. **Automatic Changelogs** - Generate changelogs from commit history
2. **Semantic Versioning** - Automatically determine version bumps
3. **Clear History** - Easy to understand project evolution
4. **Better Collaboration** - Team members understand changes quickly
5. **CI/CD Integration** - Trigger workflows based on commit types

## Examples

```bash
# Feature with scope
feat(api): add user endpoints

# Bug fix without scope
fix: resolve memory leak

# Documentation with issue reference
docs: update API documentation

Closes #123

# Breaking change
feat(api): change response format

BREAKING CHANGE: response now includes metadata object
```

## Smart Detection

The tool automatically detects:
- **Scope** from directory structure (e.g., `src/auth/login.py` → scope: `auth`)
- **Type** from file patterns:
  - Test files → `test`
  - Documentation → `docs`
  - Config files → `chore`
  - New files → `feat`
  - Modifications → `fix`

## License

MIT - Feel free to use in personal and commercial projects.

## Support

Found an issue? Have a suggestion? 
- Open an issue on GitHub
- Email: support@yourdomain.com

---

**Price:** $5 (individual) | $29 (DevTools Bundle with 6 other CLI tools)
