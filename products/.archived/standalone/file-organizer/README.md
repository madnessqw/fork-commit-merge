# Smart File Organizer

A lightweight Python script that automatically organizes cluttered directories by file type.

## Features

- **Auto-categorization**: Sorts files into Images, Documents, Videos, Audio, Archives, Code, Executables, Data, and Others
- **Safe preview mode**: See what would happen before actually moving files
- **Duplicate handling**: Automatically renames files if duplicates exist
- **Before/after summary**: Clear statistics on what was organized
- **No dependencies**: Pure Python, no external packages required

## Installation

No installation needed! Just download `file_organizer.py` and run it.

```bash
# Download
curl -O https://raw.githubusercontent.com/yourusername/file-organizer/main/file_organizer.py

# Or clone
git clone https://github.com/yourusername/file-organizer.git
```

## Usage

### Preview Mode (Recommended First)
```bash
python file_organizer.py ~/Downloads
```
This shows what would be organized without actually moving anything.

### Execute Organization
```bash
python file_organizer.py ~/Downloads --execute
```
This actually moves files into categorized folders.

### Organize Other Directories
```bash
python file_organizer.py ~/Desktop --execute
python file_organizer.py /path/to/any/folder --execute
```

## File Categories

| Category | Extensions |
|----------|-----------|
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico |
| Documents | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx |
| Videos | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| Audio | .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma |
| Archives | .zip, .rar, .7z, .tar, .gz, .bz2, .xz |
| Code | .py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .go, .rs, .swift |
| Executables | .exe, .msi, .dmg, .pkg, .deb, .rpm, .appimage |
| Data | .json, .xml, .csv, .yaml, .yml, .sql, .db, .sqlite |
| Others | Everything else |

## Example Output

```
============================================================
📁 Smart File Organizer
============================================================
Target: /home/user/Downloads
Mode: PREVIEW
============================================================

Found 47 files to organize

📊 Organization Preview:
------------------------------------------------------------

📂 Images (12 files):
   • screenshot_2024.png
   • meme.jpg
   • logo.svg
   ... and 9 more

📂 Documents (8 files):
   • report.pdf
   • notes.txt
   • budget.xlsx
   ... and 5 more

📂 Archives (5 files):
   • project_backup.zip
   • old_files.tar.gz
   ... and 3 more

...

============================================================
📈 SUMMARY
============================================================

✅ PREVIEW MODE - No files were moved
Total operations that would occur: 47

  Would move: screenshot_2024.png → Images/
  Would move: report.pdf → Documents/
  Would move: project_backup.zip → Archives/
  ...

💡 Run with --execute to actually organize files
============================================================
```

## Safety Features

1. **Preview by default**: Must explicitly use `--execute` to move files
2. **Duplicate handling**: Renames files instead of overwriting
3. **No recursion**: Only organizes the specified directory, not subdirectories
4. **Preserves structure**: Creates category folders, doesn't flatten hierarchy

## Use Cases

- Clean up your Downloads folder
- Organize project assets
- Sort camera photos by type
- Manage cluttered Desktop
- Archive old files by category

## License

MIT License - Feel free to use, modify, and distribute!

## Support

For issues or feature requests, please open an issue on GitHub.

---

**Built with ❤️ by UniverseCreator**
