#!/usr/bin/env python3
"""
Text File Processor - Batch process text files with various operations
Part of the Python Automation Toolkit
"""

import os
import re
from pathlib import Path
import argparse


class TextProcessor:
    """Process text files with various transformations"""
    
    def __init__(self, directory, pattern='*.txt', recursive=False):
        self.directory = Path(directory).expanduser().resolve()
        self.pattern = pattern
        self.recursive = recursive
        self.processed = 0
        self.errors = 0
        
    def find_and_replace(self, search, replace, dry_run=False):
        """Find and replace text in all matching files"""
        print(f"\n📝 Find and Replace: '{search}' → '{replace}'")
        print(f"   Directory: {self.directory}")
        print(f"   Pattern: {self.pattern}")
        print(f"   Recursive: {self.recursive}")
        print(f"   Dry run: {dry_run}\n")
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                new_content = content.replace(search, replace)
                
                if content == new_content:
                    continue  # No changes
                
                if not dry_run:
                    file_path.write_text(new_content, encoding='utf-8')
                
                action = "[DRY RUN] Would update" if dry_run else "Updated"
                print(f"   {action}: {file_path.name} ({content.count(search)} replacements)")
                self.processed += 1
                
            except Exception as e:
                print(f"   ❌ Error processing {file_path.name}: {e}")
                self.errors += 1
        
        self._print_summary()
        
    def regex_replace(self, pattern, replacement, dry_run=False):
        """Regex find and replace"""
        print(f"\n🔍 Regex Replace: '{pattern}' → '{replacement}'")
        print(f"   Directory: {self.directory}")
        print(f"   Pattern: {self.pattern}")
        print(f"   Dry run: {dry_run}\n")
        
        regex = re.compile(pattern)
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                new_content = regex.sub(replacement, content)
                
                if content == new_content:
                    continue
                
                if not dry_run:
                    file_path.write_text(new_content, encoding='utf-8')
                
                matches = len(regex.findall(content))
                action = "[DRY RUN] Would update" if dry_run else "Updated"
                print(f"   {action}: {file_path.name} ({matches} replacements)")
                self.processed += 1
                
            except Exception as e:
                print(f"   ❌ Error processing {file_path.name}: {e}")
                self.errors += 1
        
        self._print_summary()
        
    def remove_empty_lines(self, dry_run=False):
        """Remove empty lines from files"""
        print(f"\n🧹 Remove Empty Lines")
        print(f"   Directory: {self.directory}\n")
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                new_lines = [line for line in lines if line.strip()]
                new_content = '\n'.join(new_lines)
                
                if content == new_content:
                    continue
                
                if not dry_run:
                    file_path.write_text(new_content, encoding='utf-8')
                
                removed = len(lines) - len(new_lines)
                action = "[DRY RUN] Would clean" if dry_run else "Cleaned"
                print(f"   {action}: {file_path.name} ({removed} empty lines removed)")
                self.processed += 1
                
            except Exception as e:
                print(f"   ❌ Error processing {file_path.name}: {e}")
                self.errors += 1
        
        self._print_summary()
        
    def trim_whitespace(self, dry_run=False):
        """Trim trailing whitespace from lines"""
        print(f"\n✂️  Trim Trailing Whitespace")
        print(f"   Directory: {self.directory}\n")
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                new_content = '\n'.join(line.rstrip() for line in content.split('\n'))
                
                if content == new_content:
                    continue
                
                if not dry_run:
                    file_path.write_text(new_content, encoding='utf-8')
                
                action = "[DRY RUN] Would trim" if dry_run else "Trimmed"
                print(f"   {action}: {file_path.name}")
                self.processed += 1
                
            except Exception as e:
                print(f"   ❌ Error processing {file_path.name}: {e}")
                self.errors += 1
        
        self._print_summary()
        
    def add_line_numbers(self, output_suffix='_numbered', dry_run=False):
        """Add line numbers to files"""
        print(f"\n🔢 Add Line Numbers")
        print(f"   Directory: {self.directory}\n")
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                numbered_lines = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
                new_content = '\n'.join(numbered_lines)
                
                output_path = file_path.parent / f"{file_path.stem}{output_suffix}{file_path.suffix}"
                
                if not dry_run:
                    output_path.write_text(new_content, encoding='utf-8')
                
                action = "[DRY RUN] Would create" if dry_run else "Created"
                print(f"   {action}: {output_path.name}")
                self.processed += 1
                
            except Exception as e:
                print(f"   ❌ Error processing {file_path.name}: {e}")
                self.errors += 1
        
        self._print_summary()
        
    def extract_emails(self, output_file='emails_found.txt'):
        """Extract email addresses from all files"""
        print(f"\n📧 Extract Email Addresses")
        print(f"   Directory: {self.directory}\n")
        
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = set()
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                found = email_pattern.findall(content)
                emails.update(found)
                
                if found:
                    print(f"   Found {len(found)} in: {file_path.name}")
                    
            except Exception as e:
                print(f"   ❌ Error reading {file_path.name}: {e}")
        
        if emails:
            output_path = self.directory / output_file
            output_path.write_text('\n'.join(sorted(emails)), encoding='utf-8')
            print(f"\n   💾 Saved {len(emails)} unique emails to: {output_file}")
        else:
            print("\n   No emails found")
            
    def extract_urls(self, output_file='urls_found.txt'):
        """Extract URLs from all files"""
        print(f"\n🔗 Extract URLs")
        print(f"   Directory: {self.directory}\n")
        
        url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
        urls = set()
        
        for file_path in self._get_files():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                found = url_pattern.findall(content)
                urls.update(found)
                
                if found:
                    print(f"   Found {len(found)} in: {file_path.name}")
                    
            except Exception as e:
                print(f"   ❌ Error reading {file_path.name}: {e}")
        
        if urls:
            output_path = self.directory / output_file
            output_path.write_text('\n'.join(sorted(urls)), encoding='utf-8')
            print(f"\n   💾 Saved {len(urls)} unique URLs to: {output_file}")
        else:
            print("\n   No URLs found")
        
    def _get_files(self):
        """Get list of files matching pattern"""
        if self.recursive:
            return list(self.directory.rglob(self.pattern))
        else:
            return list(self.directory.glob(self.pattern))
            
    def _print_summary(self):
        """Print processing summary"""
        print(f"\n📊 Summary:")
        print(f"   Processed: {self.processed}")
        print(f"   Errors: {self.errors}")


def main():
    parser = argparse.ArgumentParser(
        description='Text File Processor - Batch process text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Documents --find-replace "old" "new" --pattern "*.txt"
  %(prog)s ~/Logs --regex "\\d{4}-\\d{2}-\\d{2}" "[DATE]" --recursive
  %(prog)s ~/Code --remove-empty-lines --pattern "*.py"
  %(prog)s ~/Data --trim-whitespace
  %(prog)s ~/Emails --extract-emails
  %(prog)s ~/Bookmarks --extract-urls
        """
    )
    
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('--pattern', default='*.txt', help='File pattern (default: *.txt)')
    parser.add_argument('--recursive', action='store_true', help='Process subdirectories')
    parser.add_argument('--find-replace', nargs=2, metavar=('SEARCH', 'REPLACE'), help='Simple find and replace')
    parser.add_argument('--regex', nargs=2, metavar=('PATTERN', 'REPLACEMENT'), help='Regex find and replace')
    parser.add_argument('--remove-empty-lines', action='store_true', help='Remove empty lines')
    parser.add_argument('--trim-whitespace', action='store_true', help='Trim trailing whitespace')
    parser.add_argument('--extract-emails', action='store_true', help='Extract email addresses')
    parser.add_argument('--extract-urls', action='store_true', help='Extract URLs')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"❌ Error: '{args.directory}' is not a valid directory")
        return 1
    
    processor = TextProcessor(args.directory, pattern=args.pattern, recursive=args.recursive)
    
    if args.find_replace:
        processor.find_and_replace(args.find_replace[0], args.find_replace[1], dry_run=args.dry_run)
    elif args.regex:
        processor.regex_replace(args.regex[0], args.regex[1], dry_run=args.dry_run)
    elif args.remove_empty_lines:
        processor.remove_empty_lines(dry_run=args.dry_run)
    elif args.trim_whitespace:
        processor.trim_whitespace(dry_run=args.dry_run)
    elif args.extract_emails:
        processor.extract_emails()
    elif args.extract_urls:
        processor.extract_urls()
    else:
        print("❌ Error: Please specify an operation")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
