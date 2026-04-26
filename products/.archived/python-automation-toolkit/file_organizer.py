#!/usr/bin/env python3
"""
Smart File Organizer - Automatically organize files by type, date, or custom rules
Part of the Python Automation Toolkit
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse


class FileOrganizer:
    """Organize files in a directory based on various rules"""
    
    FILE_TYPES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.rb', '.php'],
        'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
        'Data': ['.json', '.xml', '.csv', '.yaml', '.yml', '.sql', '.db', '.sqlite'],
    }
    
    def __init__(self, source_dir, dry_run=False):
        self.source_dir = Path(source_dir).expanduser().resolve()
        self.dry_run = dry_run
        self.stats = defaultdict(int)
        
    def organize_by_type(self):
        """Organize files into folders by file type"""
        print(f"\n📁 Organizing by type: {self.source_dir}")
        print(f"   Dry run: {self.dry_run}\n")
        
        for file_path in self.source_dir.iterdir():
            if not file_path.is_file():
                continue
                
            file_ext = file_path.suffix.lower()
            category = 'Others'
            
            for cat, extensions in self.FILE_TYPES.items():
                if file_ext in extensions:
                    category = cat
                    break
            
            target_dir = self.source_dir / category
            self._move_file(file_path, target_dir)
            
        self._print_stats()
        
    def organize_by_date(self, date_format='%Y-%m'):
        """Organize files into folders by modification date"""
        print(f"\n📅 Organizing by date: {self.source_dir}")
        print(f"   Date format: {date_format}")
        print(f"   Dry run: {self.dry_run}\n")
        
        for file_path in self.source_dir.iterdir():
            if not file_path.is_file():
                continue
                
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = mod_time.strftime(date_format)
            
            target_dir = self.source_dir / date_folder
            self._move_file(file_path, target_dir)
            
        self._print_stats()
        
    def organize_by_size(self):
        """Organize files into folders by size category"""
        print(f"\n📊 Organizing by size: {self.source_dir}")
        print(f"   Dry run: {self.dry_run}\n")
        
        size_categories = {
            'Small': (0, 1024 * 1024),  # < 1MB
            'Medium': (1024 * 1024, 100 * 1024 * 1024),  # 1MB - 100MB
            'Large': (100 * 1024 * 1024, float('inf')),  # > 100MB
        }
        
        for file_path in self.source_dir.iterdir():
            if not file_path.is_file():
                continue
                
            file_size = file_path.stat().st_size
            category = 'Others'
            
            for cat, (min_size, max_size) in size_categories.items():
                if min_size <= file_size < max_size:
                    category = cat
                    break
            
            target_dir = self.source_dir / category
            self._move_file(file_path, target_dir)
            
        self._print_stats()
        
    def _move_file(self, file_path, target_dir):
        """Move a file to the target directory"""
        try:
            if not self.dry_run:
                target_dir.mkdir(exist_ok=True)
                target_path = target_dir / file_path.name
                
                # Handle duplicates
                counter = 1
                while target_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(target_path))
            
            self.stats[target_dir.name] += 1
            action = "[DRY RUN] Would move" if self.dry_run else "Moved"
            print(f"   {action}: {file_path.name} → {target_dir.name}/")
            
        except Exception as e:
            print(f"   ❌ Error moving {file_path.name}: {e}")
            
    def _print_stats(self):
        """Print organization statistics"""
        if not self.stats:
            print("   No files to organize")
            return
            
        print(f"\n📈 Statistics:")
        print(f"   Total files: {sum(self.stats.values())}")
        for category, count in sorted(self.stats.items()):
            print(f"   {category}: {count} files")


def main():
    parser = argparse.ArgumentParser(
        description='Smart File Organizer - Organize your files automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Downloads --by-type              # Organize by file type
  %(prog)s ~/Downloads --by-date              # Organize by date
  %(prog)s ~/Downloads --by-size              # Organize by file size
  %(prog)s ~/Downloads --by-type --dry-run    # Preview changes
        """
    )
    
    parser.add_argument('directory', help='Directory to organize')
    parser.add_argument('--by-type', action='store_true', help='Organize by file type')
    parser.add_argument('--by-date', action='store_true', help='Organize by modification date')
    parser.add_argument('--by-size', action='store_true', help='Organize by file size')
    parser.add_argument('--date-format', default='%Y-%m', help='Date format for --by-date (default: %%Y-%%m)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without moving files')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"❌ Error: '{args.directory}' is not a valid directory")
        return 1
    
    # Require at least one organization method
    if not (args.by_type or args.by_date or args.by_size):
        print("❌ Error: Please specify --by-type, --by-date, or --by-size")
        return 1
    
    organizer = FileOrganizer(args.directory, dry_run=args.dry_run)
    
    if args.by_type:
        organizer.organize_by_type()
    elif args.by_date:
        organizer.organize_by_date(date_format=args.date_format)
    elif args.by_size:
        organizer.organize_by_size()
    
    return 0


if __name__ == '__main__':
    exit(main())
