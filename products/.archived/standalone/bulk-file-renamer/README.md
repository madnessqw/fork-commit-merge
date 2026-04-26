# Bulk File Renamer

**Product #30** in the UniverseCreator standalone tool series

A powerful, safe, and user-friendly bulk file renaming tool with preview mode, undo functionality, and advanced pattern matching.

## Features

✅ **Multiple Rename Modes:**
- Text replacement (simple find/replace)
- Regex pattern matching
- Sequential numbering with custom prefix/suffix
- Timestamp insertion
- Case conversion (lower/upper/title)

✅ **Safety Features:**
- Preview mode — see changes before applying
- Undo history — reverse any operation
- Dry-run support — test without risk
- History persistence — last 100 operations saved

✅ **Flexible Usage:**
- Interactive mode with guided prompts
- CLI mode for scripting and automation
- File pattern matching (globs)
- Directory-specific operations

## Installation

```bash
# Download the script
curl -O https://raw.githubusercontent.com/yourusername/bulk-file-renamer/main/bulk_file_renamer.py

# Make executable
chmod +x bulk_file_renamer.py

# Run
python3 bulk_file_renamer.py
```

## Usage

### Interactive Mode
```bash
python3 bulk_file_renamer.py -i
```

### CLI Examples

**Replace text in filenames:**
```bash
python3 bulk_file_renamer.py -d ./photos -p "*.jpg" -r "IMG" "Vacation"
```

**Regex pattern replacement:**
```bash
python3 bulk_file_renamer.py -d ./docs --regex "doc_(\d+)" "Document_$1"
```

**Sequential numbering:**
```bash
python3 bulk_file_renamer.py -d ./files --sequence --prefix "file_" --start 1
```

**Add timestamp:**
```bash
python3 bulk_file_renamer.py -d ./backups --timestamp --prefix "backup_"
```

**Change case:**
```bash
python3 bulk_file_renamer.py -d ./files --case lower
```

**Preview changes (dry run):**
```bash
python3 bulk_file_renamer.py -d ./photos -r "old" "new" --dry-run
```

**Undo last 5 operations:**
```bash
python3 bulk_file_renamer.py --undo 5
```

## Use Cases

- **Photography:** Rename camera files (IMG_0001.jpg → Vacation_001.jpg)
- **Development:** Standardize file naming conventions
- **Data Organization:** Add timestamps to backup files
- **Content Creation:** Batch rename assets for projects
- **System Administration:** Standardize log file names

## Safety

- Always uses preview mode first
- Changes are logged and reversible
- History stored in `.rename_history.json`
- Original files preserved until rename confirmed

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)

## License

MIT License - Free for personal and commercial use

---

*Built by UniverseCreator - An autonomous economic organism*
