# Python Automation Cheat Sheet

## Quick Reference for Common Tasks

---

## File Operations

### Check if File Exists
```python
from pathlib import Path

# Method 1: pathlib (recommended)
file = Path("document.txt")
if file.exists():
    print("File exists")

# Method 2: os
import os
if os.path.exists("document.txt"):
    print("File exists")
```

### Get File Info
```python
from pathlib import Path

file = Path("document.pdf")
print(file.name)        # document.pdf
print(file.stem)        # document
print(file.suffix)      # .pdf
print(file.parent)      # Directory containing file
print(file.stat().st_size)      # Size in bytes
print(file.stat().st_mtime)     # Last modified time
```

### List Directory Contents
```python
from pathlib import Path

directory = Path(".")

# All items
for item in directory.iterdir():
    print(item)

# Only files
for file in directory.glob("*"):
    if file.is_file():
        print(file.name)

# Only Python files
for py_file in directory.glob("*.py"):
    print(py_file.name)

# Recursive search
for file in directory.rglob("*.txt"):
    print(file)
```

### Read/Write Files
```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Write file
with open("output.txt", "w") as f:
    f.write("Hello, World!")

# Append to file
with open("log.txt", "a") as f:
    f.write("\nNew entry")

# Read CSV
import csv
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Write CSV
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", "30"])
```

---

## String Operations

### Common String Methods
```python
text = "  Hello, World!  "

text.strip()           # Remove whitespace
text.lower()           # hello, world!
text.upper()           # HELLO, WORLD!
text.replace("World", "Python")  # Hello, Python!
text.split(",")        # ['  Hello', ' World!  ']
",".join(["a", "b", "c"])  # a,b,c
text.find("World")     # 9 (index)
text.count("l")        # 3
```

### Regular Expressions
```python
import re

# Search for pattern
match = re.search(r"\d+", "File123.txt")
if match:
    print(match.group())  # 123

# Find all matches
emails = re.findall(r"[\w.]+@[\w.]+\.\w+", text)

# Replace
new_text = re.sub(r"\d+", "NUM", "File123.txt")  # FileNUM.txt

# Common patterns
email_pattern = r"[\w.]+@[\w.]+\.\w+"
url_pattern = r"https?://[^\s]+"
phone_pattern = r"\d{3}-\d{3}-\d{4}"
```

---

## Date and Time

### Working with Dates
```python
from datetime import datetime, timedelta
import time

# Current time
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Parse date from string
date = datetime.strptime("2024-03-15", "%Y-%m-%d")

# File modification time
from pathlib import Path
file = Path("document.txt")
mtime = datetime.fromtimestamp(file.stat().st_mtime)

# Time differences
yesterday = now - timedelta(days=1)
last_week = now - timedelta(weeks=1)

# Sleep/pause
print("Waiting...")
time.sleep(5)  # Sleep for 5 seconds
print("Done!")
```

---

## Error Handling

### Try/Except Patterns
```python
# Basic try/except
try:
    with open("file.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
except Exception as e:
    print(f"Error: {e}")

# With finally
try:
    file = open("data.txt", "r")
    data = file.read()
finally:
    file.close()

# Context manager (recommended)
with open("data.txt", "r") as file:
    data = file.read()
```

---

## Common Automation Tasks

### Organize Files by Extension
```python
from pathlib import Path
import shutil

def organize_by_extension(directory="."):
    path = Path(directory)
    for file in path.iterdir():
        if file.is_file():
            ext = file.suffix[1:] or "no_extension"
            folder = path / ext
            folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(folder / file.name))
```

### Rename Files with Pattern
```python
from pathlib import Path

def bulk_rename(directory, pattern="file_{:03d}"):
    path = Path(directory)
    files = sorted([f for f in path.iterdir() if f.is_file()])
    
    for i, file in enumerate(files, 1):
        new_name = pattern.format(i) + file.suffix
        file.rename(path / new_name)
```

### Find Duplicate Files
```python
import hashlib
from pathlib import Path
from collections import defaultdict

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    hashes = defaultdict(list)
    for file in Path(directory).rglob("*"):
        if file.is_file():
            file_hash = get_file_hash(file)
            hashes[file_hash].append(file)
    
    return [files for files in hashes.values() if len(files) > 1]
```

### Process Text Files
```python
def find_replace_in_files(directory, find_text, replace_text):
    for file in Path(directory).rglob("*.txt"):
        content = file.read_text()
        new_content = content.replace(find_text, replace_text)
        file.write_text(new_content)
```

---

## Command Line Arguments

### Using sys.argv
```python
import sys

# script.py arg1 arg2
script_name = sys.argv[0]
first_arg = sys.argv[1] if len(sys.argv) > 1 else None
second_arg = sys.argv[2] if len(sys.argv) > 2 else None
```

### Using argparse (recommended)
```python
import argparse

parser = argparse.ArgumentParser(description="File processor")
parser.add_argument("input", help="Input file")
parser.add_argument("-o", "--output", help="Output file")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()

print(f"Input: {args.input}")
print(f"Output: {args.output}")
print(f"Verbose: {args.verbose}")
```

---

## Environment Variables

```python
import os

# Get environment variable
api_key = os.getenv("API_KEY")
home = os.getenv("HOME")

# Get with default
port = os.getenv("PORT", "8080")

# Set environment variable
os.environ["MY_VAR"] = "value"

# Load from .env file
from pathlib import Path

def load_env(filepath=".env"):
    env_path = Path(filepath)
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
```

---

## JSON Operations

```python
import json

# Read JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Write JSON file
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

# Parse JSON string
json_string = '{"name": "Alice", "age": 30}'
parsed = json.loads(json_string)

# Convert to JSON string
data = {"name": "Bob", "age": 25}
json_string = json.dumps(data, indent=2)
```

---

## Running External Commands

```python
import subprocess

# Run command
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)

# With error handling
try:
    result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

#