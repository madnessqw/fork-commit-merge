#!/usr/bin/env python3
"""
File Organizer - Automatically organize files by type/extension.

Usage:
    python file_organizer.py /path/to/directory [--dry-run]
"""

import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict


FILE_CATEGORIES = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs'],
    'data': ['.json', '.xml', '.csv', '.yaml', '.yml', '.sql', '.db'],
}


def get_category(extension: str) -> str:
    """Get category for a file extension."""
    ext_lower = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext_lower in extensions:
            return category
    return 'others'


def organize_files(directory: str, dry_run: bool = False) -> dict:
    """Organize files in directory by category."""
    path = Path(directory)
    if not path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    stats = defaultdict(int)
    
    for file_path in path.iterdir():
        if file_path.is_file():
            category = get_category(file_path.suffix)
            target_dir = path / category
            
            if not dry_run:
                target_dir.mkdir(exist_ok=True)
                
                # Handle duplicate filenames
                target_file = target_dir / file_path.name
                counter = 1
                while target_file.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    target_file = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(target_file))
            
            stats[category] += 1
            print(f"{'[DRY RUN] ' if dry_run else ''}Moved: {file_path.name} -> {category}/")
    
    return dict(stats)


def main():
    parser = argparse.ArgumentParser(description='Organize files by type')
    parser.add_argument('directory', help='Directory to organize')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without moving files')
    
    args = parser.parse_args()
    
    print(f"Organizing files in: {args.directory}")
    if args.dry_run:
        print("DRY RUN MODE - No files will be moved\n")
    
    try:
        stats = organize_files(args.directory, args.dry_run)
        
        print("\n" + "="*40)
        print("SUMMARY")
        print("="*40)
        total = sum(stats.values())
        for category, count in sorted(stats.items()):
            print(f"  {category}: {count} files")
        print(f"  TOTAL: {total} files")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
