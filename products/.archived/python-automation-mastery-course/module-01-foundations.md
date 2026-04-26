# Module 1: Foundations of Python Automation

## Day 1-3: Getting Started with Automation

---

## Welcome to Python Automation Mastery!

In this module, we'll lay the groundwork for everything you'll learn in this course. By the end of these three days, you'll understand the core concepts of automation and have your environment set up for success.

---

## What Is Automation?

Automation is the process of making a system operate automatically with minimal human intervention. In Python, this means writing scripts that:

- Perform repetitive tasks for you
- Process data at scale
- Monitor systems and respond to events
- Integrate different tools and services

### Why Python for Automation?

1. **Readable syntax** - Easy to write and maintain
2. **Rich ecosystem** - Thousands of libraries for any task
3. **Cross-platform** - Works on Windows, Mac, and Linux
4. **Great for beginners** - Gentle learning curve
5. **Production-ready** - Used by companies worldwide

---

## Day 1: Setting Up Your Environment

### Installing Python

**Windows:**
1. Download from python.org
2. Run installer (check "Add to PATH")
3. Verify: `python --version`

**Mac:**
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Verify
python3 --version
```

### Setting Up Your Workspace

Create a dedicated folder for your automation projects:

```bash
mkdir ~/automation-projects
cd ~/automation-projects
python3 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Essential Tools

1. **VS Code** - Free, powerful code editor
2. **Git** - Version control (optional but recommended)
3. **Terminal/Command Prompt** - Your automation command center

---

## Day 2: Python Basics for Automation

### Variables and Data Types

```python
# Strings - text data
filename = "report_2024.pdf"
folder_name = "Documents"

# Integers - whole numbers
file_count = 150
retry_attempts = 3

# Floats - decimal numbers
file_size_mb = 2.5
progress_percent = 75.5

# Booleans - True/False
is_valid = True
needs_backup = False

# Lists - collections of items
file_list = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
folder_paths = ["/home/user/docs", "/home/user/pics"]

# Dictionaries - key-value pairs
file_info = {
    "name": "report.pdf",
    "size": 2048,
    "created": "2024-01-15"
}
```

### Control Flow

```python
# If statements - making decisions
if file_size > 100:
    print("Large file detected")
elif file_size > 50:
    print("Medium file")
else:
    print("Small file")

# For loops - iterating over collections
for filename in file_list:
    print(f"Processing: {filename}")

# While loops - repeating until condition is met
attempts = 0
while attempts < 3:
    print(f"Attempt {attempts + 1}")
    attempts += 1
```

### Functions

```python
def process_file(filename):
    """Process a single file."""
    print(f"Processing {filename}...")
    # Processing logic here
    return True

def get_file_size(filepath):
    """Get the size of a file in bytes."""
    import os
    return os.path.getsize(filepath)

# Using functions
process_file("document.pdf")
size = get_file_size("document.pdf")
```

---

## Day 3: Working with Files and Directories

### The `os` Module

The `os` module provides a way to interact with the operating system:

```python
import os

# Get current working directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# List files in a directory
files = os.listdir(".")
for file in files:
    print(file)

# Check if file exists
if os.path.exists("document.txt"):
    print("File exists")

# Check if it's a file or directory
if os.path.isfile("document.txt"):
    print("It's a file")

if os.path.isdir("Documents"):
    print("It's a directory")

# Create a directory
os.makedirs("new_folder", exist_ok=True)

# Rename a file
os.rename("old_name.txt", "new_name.txt")

# Delete a file
os.remove("temp_file.txt")

# Join paths (cross-platform)
full_path = os.path.join("Documents", "Projects", "script.py")
```

### The `pathlib` Module (Modern Approach)

`pathlib` is the modern, object-oriented way to work with paths:

```python
from pathlib import Path

# Create path objects
current_dir = Path.cwd()
documents = Path.home() / "Documents"

# List files
for file in documents.iterdir():
    if file.is_file():
        print(f"File: {file.name}")
    elif file.is_dir():
        print(f"Directory: {file.name}")

# Check existence
config_file = Path("config.json")
if config_file.exists():
    print("Config exists")

# Create directories
new_folder = Path("output") / "reports"
new_folder.mkdir(parents=True, exist_ok=True)

# Get file info
file_path = Path("document.pdf")
print(f"Name: {file_path.name}")
print(f"Extension: {file_path.suffix}")
print(f"Parent: {file_path.parent}")
print(f"Size: {file_path.stat().st_size} bytes")
```

### Reading and Writing Files

```python
# Reading files
with open("document.txt", "r") as file:
    content = file.read()

# Reading line by line
with open("log.txt", "r") as file:
    for line in file:
        print(line.strip())

# Writing files
with open("output.txt", "w") as file:
    file.write("Hello, Automation!")

# Appending to files
with open("log.txt", "a") as file:
    file.write("\nNew log entry")

# Reading CSV files
import csv
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

---

## Error Handling

Automation scripts need to handle errors gracefully:

```python
try:
    # Attempt to open file
    with open("document.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Permission denied!")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Cleanup code here")

# Practical example
def safe_read_file(filepath):
    """Read a file safely with error handling."""
    try:
        with open(filepath, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return None
    except PermissionError:
        print(f"Warning: No permission to read {filepath}")
        return None
```

---

## Your First Automation Script

Let's create a simple script that organizes files by extension:

```python
#!/usr/bin/env python3
"""
Simple File Organizer
Organizes files in a directory by their extensions.
"""

import os
import shutil
from pathlib import Path

def organize_by_extension(directory="."):
    """Organize files by extension."""
    dir_path = Path(directory)
    
    # Create organized folder
    organized = dir_path / "organized"
    organized.mkdir(exist_ok=True)
    
    # Process each file
    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.name != "organize.py":
            # Get file extension
            extension = file_path.suffix[1:] or "no_extension"
            
            # Create folder for this extension
            ext_folder = organized / extension
            ext_folder.mkdir(exist_ok=True)
            
            # Move file
            destination = ext_folder / file_path.name
            shutil.move(str(file_path), str(destination))
            print(f"Moved: {file_path.name} -> {extension}/")

if __name__ == "__main__":
    organize_by_extension()
    print("