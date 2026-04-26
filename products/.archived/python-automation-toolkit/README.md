# Python Automation Toolkit

A collection of powerful command-line tools to automate repetitive file and text operations. Save hours of manual work with these simple, fast utilities.

## 🚀 What's Included

### 1. File Organizer (`file_organizer.py`)
Automatically organize files by type, date, or size.

```bash
# Organize Downloads folder by file type
python file_organizer.py ~/Downloads --by-type

# Organize photos by month
python file_organizer.py ~/Photos --by-date --date-format "%Y-%m"

# Preview changes before applying
python file_organizer.py ~/Downloads --by-type --dry-run
```

**Features:**
- 📁 Organize by file type (Images, Documents, Videos, etc.)
- 📅 Organize by modification date
- 📊 Organize by file size
- 🔒 Duplicate file handling
- 👁️ Dry-run mode to preview changes

### 2. Bulk Renamer (`bulk_renamer.py`)
Rename hundreds of files in seconds with patterns, counters, and transformations.

```bash
# Sequential numbering
python bulk_renamer.py ~/Photos --pattern "vacation_{count:03d}.jpg"

# Regex replacement
python bulk_renamer.py ~/Files --regex "IMG_(\d+)" "Photo_\1"

# Add prefix/suffix
python bulk_renamer.py ~/Documents --prefix "2024_"
python bulk_renamer.py ~/Backups --suffix "_backup"

# Clean up filenames
python bulk_renamer.py ~/Downloads --lowercase
python bulk_renamer.py ~/Downloads --replace-spaces "_"
```

**Features:**
- 🔢 Pattern-based renaming with counters
- 🔍 Regex search and replace
- ➕ Add prefix/suffix
- 🔤 Convert case (lower/upper)
- 🔄 Replace spaces with custom characters

### 3. Directory Sync (`directory_sync.py`)
Keep directories synchronized with multiple modes.

```bash
# Mirror: Make backup identical to source
python directory_sync.py ~/Documents /backup/Documents --mirror

# Update: Copy only new/changed files
python directory_sync.py ~/Projects /backup/Projects --update

# Backup: Create timestamped backups before overwriting
python directory_sync.py ~/Important /backup/Important --backup
```

**Features:**
- 🔄 Mirror mode (exact copy, deletes extra files)
- ⬆️ Update mode (copy new/modified only)
- 💾 Backup mode (preserve old versions)
- 📊 Transfer statistics
- 👁️ Dry-run preview

### 4. Text Processor (`text_processor.py`)
Batch process text files with find/replace, extraction, and cleanup.

```bash
# Find and replace across all files
python text_processor.py ~/Code --find-replace "old_api" "new_api" --pattern "*.py"

# Regex replacement
python text_processor.py ~/Logs --regex "\d{4}-\d{2}-\d{2}" "[DATE]"

# Clean up files
python text_processor.py ~/Documents --remove-empty-lines
python text_processor.py ~/Code --trim-whitespace

# Extract data
python text_processor.py ~/Emails --extract-emails
python text_processor.py ~/Bookmarks --extract-urls
```

**Features:**
- 📝 Find and replace (simple or regex)
- 🧹 Remove empty lines
- ✂️ Trim trailing whitespace
- 📧 Extract email addresses
- 🔗 Extract URLs
- 🔍 Recursive processing

## 📦 Installation

### Option 1: Direct Download
```bash
# Download all files to a directory
cd ~/tools
# Save each .py file and make executable
chmod +x *.py
```

### Option 2: pip Installation (Coming Soon)
```bash
pip install python-automation-toolkit
```

## 🎯 Use Cases

### Photographers
```bash
# Organize photos by date
python file_organizer.py ~/Camera --by-date --date-format "%Y/%m"

# Rename with sequential numbers
python bulk_renamer.py ~/Camera/2024 --pattern "shoot_{count:04d}.jpg"
```

### Developers
```bash
# Sync project to backup
python directory_sync.py ~/Projects/myapp /backup/myapp --mirror

# Update copyright year across files
python text_processor.py ~/Projects --find-replace "2023" "2024" --pattern "*.py" --recursive
```

### Content Creators
```bash
# Organize downloads
python file_organizer.py ~/Downloads --by-type

# Clean up filenames
python bulk_renamer.py ~/Downloads --lowercase --replace-spaces "-"
```

### System Administrators
```bash
# Backup important directories
python directory_sync.py /var/www /backup/www --backup

# Extract all emails from log files
python text_processor.py /var/log --extract-emails --pattern "*.log"
```

## ⚡ Quick Start

1. **Download** all 4 Python files to a folder
2. **Make executable**: `chmod +x *.py` (Linux/Mac) or just run with `python` (Windows)
3. **Test with dry-run**: Most commands support `--dry-run` to preview changes
4. **Execute**: Run the actual command

## 🔧 Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 🛡️ Safety Features

- **Dry-run mode**: Preview all changes before applying
- **Duplicate handling**: Automatic renaming of duplicates
- **Error reporting**: Clear messages for any issues
- **Non-destructive**: Backup mode preserves old versions

## 💡 Tips

1. **Always use `--dry-run` first** to see what will happen
2. **Test on a small folder** before processing thousands of files
3. **Use quotes** for patterns containing spaces or special characters
4. **Backup important data** before bulk operations

## 📊 Comparison with Manual Work

| Task | Manual Time | With Toolkit | Time Saved |
|------|-------------|--------------|------------|
| Organize 1000 files | 2 hours | 10 seconds | 99.9% |
| Rename 500 photos | 1 hour | 5 seconds | 99.8% |
| Sync 10GB directory | Manual copy | 1 minute | 95% |
| Find/replace in 50 files | 30 minutes | 3 seconds | 99.8% |

## 📝 License

MIT License - Use freely for personal and commercial projects.

## 🤝 Support

- 📧 Email: support@example.com
- 🐛 Issues: github.com/yourusername/python-automation-toolkit/issues
- 💬 Discussions: github.com/yourusername/python-automation-toolkit/discussions

---

**Ready to save hours of manual work? Download now and automate!**
