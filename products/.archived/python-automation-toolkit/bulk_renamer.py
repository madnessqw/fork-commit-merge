#!/usr/bin/env python3
"""
Bulk File Renamer - Rename multiple files with patterns, counters, and transformations
Part of the Python Automation Toolkit
"""

import os
import re
from pathlib import Path
import argparse


class BulkRenamer:
    """Bulk rename files with various patterns and rules"""
    
    def __init__(self, directory, dry_run=False):
        self.directory = Path(directory).expanduser().resolve()
        self.dry_run = dry_run
        self.renamed = 0
        self.errors = 0
        
    def rename_with_pattern(self, pattern, start=1, files=None):
        """Rename files with a pattern containing {count} placeholder"""
        print(f"\n🔢 Pattern Rename: {pattern}")
        print(f"   Directory: {self.directory}")
        print(f"   Start: {start}")
        print(f"   Dry run: {self.dry_run}\n")
        
        if files is None:
            files = sorted([f for f in self.directory.iterdir() if f.is_file()])
        
        counter = start
        for file_path in files:
            new_name = pattern.format(count=counter)
            new_path = file_path.parent / new_name
            
            self._rename_file(file_path, new_path)
            counter += 1
            
        self._print_summary()
        
    def regex_rename(self, pattern, replacement, files=None):
        """Rename files using regex search and replace"""
        print(f"\n🔍 Regex Rename: '{pattern}' → '{replacement}'")
        print(f"   Directory: {self.directory}")
        print(f"   Dry run: {self.dry_run}\n")
        
        regex = re.compile(pattern)
        
        if files is None:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        for file_path in files:
            new_name = regex.sub(replacement, file_path.name)
            if new_name == file_path.name:
                continue
                
            new_path = file_path.parent / new_name
            self._rename_file(file_path, new_path)
            
        self._print_summary()
        
    def add_prefix(self, prefix, files=None):
        """Add prefix to filenames"""
        print(f"\n➕ Add Prefix: '{prefix}'")
        print(f"   Directory: {self.directory}\n")
        
        if files is None:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        for file_path in files:
            new_name = prefix + file_path.name
            new_path = file_path.parent / new_name
            self._rename_file(file_path, new_path)
            
        self._print_summary()
        
    def add_suffix(self, suffix, files=None):
        """Add suffix to filenames (before extension)"""
        print(f"\n➕ Add Suffix: '{suffix}'")
        print(f"   Directory: {self.directory}\n")
        
        if files is None:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        for file_path in files:
            new_name = f"{file_path.stem}{suffix}{file_path.suffix}"
            new_path = file_path.parent / new_name
            self._rename_file(file_path, new_path)
            
        self._print_summary()
        
    def change_case(self, case='lower', files=None):
        """Change filename case"""
        print(f"\n🔤 Change Case: {case}")
        print(f"   Directory: {self.directory}\n")
        
        if files is None:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        for file_path in files:
            if case == 'lower':
                new_name = file_path.name.lower()
            elif case == 'upper':
                new_name = file_path.name.upper()
            else:
                continue
                
            new_path = file_path.parent / new_name
            self._rename_file(file_path, new_path)
            
        self._print_summary()
        
    def replace_spaces(self, replacement='_', files=None):
        """Replace spaces in filenames"""
        print(f"\n🔄 Replace Spaces: ' ' → '{replacement}'")
        print(f"   Directory: {self.directory}\n")
        
        if files is None:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        for file_path in files:
            new_name = file_path.name.replace(' ', replacement)
            if new_name == file_path.name:
                continue
                
            new_path = file_path.parent / new_name
            self._rename_file(file_path, new_path)
            
        self._print_summary()
        
    def _rename_file(self, old_path, new_path):
        """Perform the actual rename"""
        try:
            # Handle duplicates
            counter = 1
            original_new_path = new_path
            while new_path.exists() and new_path != old_path:
                stem = original_new_path.stem
                suffix = original_new_path.suffix
                new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            if old_path == new_path:
                return
            
            if not self.dry_run:
                old_path.rename(new_path)
            
            action = "[DRY RUN] Would rename" if self.dry_run else "Renamed"
            print(f"   {action}: {old_path.name} → {new_path.name}")
            self.renamed += 1
            
        except Exception as e:
            print(f"   ❌ Error renaming {old_path.name}: {e}")
            self.errors += 1
            
    def _print_summary(self):
        """Print rename summary"""
        print(f"\n📊 Summary:")
        print(f"   Renamed: {self.renamed}")
        print(f"   Errors: {self.errors}")


def main():
    parser = argparse.ArgumentParser(
        description='Bulk File Renamer - Rename multiple files at once',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Photos --pattern "vacation_{count:03d}.jpg"
  %(prog)s ~/Files --regex "IMG_(\\d+)" "Photo_\\1"
  %(prog)s ~/Docs --prefix "2024_"
  %(prog)s ~/Backups --suffix "_backup"
  %(prog)s ~/Downloads --lowercase
  %(prog)s ~/Downloads --replace-spaces "-"
        """
    )
    
    parser.add_argument('directory', help='Directory containing files to rename')
    parser.add_argument('--pattern', help='Pattern with {count} placeholder')
    parser.add_argument('--regex', nargs=2, metavar=('PATTERN', 'REPLACEMENT'), help='Regex pattern and replacement')
    parser.add_argument('--prefix', help='Add prefix to filenames')
    parser.add_argument('--suffix', help='Add suffix to filenames')
    parser.add_argument('--lowercase', action='store_true', help='Convert to lowercase')
    parser.add_argument('--uppercase', action='store_true', help='Convert to uppercase')
    parser.add_argument('--replace-spaces', metavar='CHAR', help='Replace spaces with character')
    parser.add_argument('--start', type=int, default=1, help='Starting number for counter (default: 1)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without renaming')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"❌ Error: '{args.directory}' is not a valid directory")
        return 1
    
    # Require exactly one operation
    operations = [
        args.pattern is not None,
        args.regex is not None,
        args.prefix is not None,
        args.suffix is not None,
        args.lowercase,
        args.uppercase,
        args.replace_spaces is not None
    ]
    
    if sum(operations) != 1:
        print("❌ Error: Please specify exactly one renaming operation")
        return 1
    
    renamer = BulkRenamer(args.directory, dry_run=args.dry_run)
    
    if args.pattern:
        renamer.rename_with_pattern(args.pattern, start=args.start)
    elif args.regex:
        renamer.regex_rename(args.regex[0], args.regex[1])
    elif args.prefix:
        renamer.add_prefix(args.prefix)
    elif args.suffix:
        renamer.add_suffix(args.suffix)
    elif args.lowercase:
        renamer.change_case('lower')
    elif args.uppercase:
        renamer.change_case('upper')
    elif args.replace_spaces:
        renamer.replace_spaces(args.replace_spaces)
    
    return 0


if __name__ == '__main__':
    exit(main())
