#!/usr/bin/env python3
"""
Duplicate File Finder - Find and optionally remove duplicate files.

Usage:
    python duplicate_finder.py /path/to/directory [--delete] [--min-size 1024]
"""

import os
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict


def hash_file(filepath: str, block_size: int = 65536) -> str:
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError):
        return None


def find_duplicates(directory: str, min_size: int = 0) -> dict:
    """Find duplicate files in directory."""
    path = Path(directory)
    if not path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    # Group files by size first (optimization)
    size_map = defaultdict(list)
    for file_path in path.rglob('*'):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size >= min_size:
                    size_map[size].append(file_path)
            except (OSError, IOError):
                continue
    
    # Hash files with same size
    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) > 1:  # Only hash if potential duplicates exist
            for file_path in files:
                file_hash = hash_file(str(file_path))
                if file_hash:
                    hash_map[file_hash].append(file_path)
    
    # Return only duplicates
    return {h: files for h, files in hash_map.items() if len(files) > 1}


def format_size(size_bytes: int) -> str:
    """Format file size for display."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    parser = argparse.ArgumentParser(description='Find duplicate files')
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('--delete', action='store_true', help='Delete duplicates (keep first)')
    parser.add_argument('--min-size', type=int, default=0, help='Minimum file size in bytes')
    parser.add_argument('--dry-run', action='store_true', help='Preview deletions without removing')
    
    args = parser.parse_args()
    
    print(f"Scanning: {args.directory}")
    print(f"Minimum file size: {format_size(args.min_size)}")
    print("This may take a while for large directories...\n")
    
    try:
        duplicates = find_duplicates(args.directory, args.min_size)
        
        if not duplicates:
            print("No duplicate files found!")
            return 0
        
        total_duplicates = 0
        total_wasted = 0
        
        for file_hash, files in duplicates.items():
            file_size = files[0].stat().st_size
            group_wasted = file_size * (len(files) - 1)
            total_duplicates += len(files) - 1
            total_wasted += group_wasted
            
            print(f"\nDuplicate group ({format_size(file_size)} each, {format_size(group_wasted)} wasted):")
            for i, file_path in enumerate(files):
                marker = " [KEEP]" if i == 0 else " [DELETE]" if args.delete else ""
                print(f"  {i+1}. {file_path}{marker}")
                
                if args.delete and i > 0:
                    if args.dry_run:
                        print(f"      [DRY RUN] Would delete: {file_path}")
                    else:
                        try:
                            os.remove(file_path)
                            print(f"      Deleted: {file_path}")
                        except OSError as e:
                            print(f"      Error deleting: {e}")
        
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Duplicate groups found: {len(duplicates)}")
        print(f"Duplicate files: {total_duplicates}")
        print(f"Space wasted: {format_size(total_wasted)}")
        
        if args.delete:
            action = "Would free" if args.dry_run else "Freed"
            print(f"{action}: {format_size(total_wasted)}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
