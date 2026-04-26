#!/usr/bin/env python3
"""
Directory Sync Tool - Sync two directories with various modes
Part of the Python Automation Toolkit
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import argparse


class DirectorySync:
    """Synchronize two directories with various sync modes"""
    
    def __init__(self, source, destination, dry_run=False, verbose=False):
        self.source = Path(source).expanduser().resolve()
        self.destination = Path(destination).expanduser().resolve()
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            'copied': 0,
            'updated': 0,
            'deleted': 0,
            'skipped': 0,
            'errors': 0,
            'bytes_transferred': 0
        }
        
    def sync_mirror(self):
        """
        Mirror mode: Make destination identical to source
        Copies new files, updates modified files, deletes extra files
        """
        print(f"\n🔄 Mirror Sync: {self.source} → {self.destination}")
        print(f"   Dry run: {self.dry_run}\n")
        
        if not self.dry_run:
            self.destination.mkdir(parents=True, exist_ok=True)
        
        # Track all files in destination for deletion check
        dest_files = set()
        
        # Walk through source and sync to destination
        for src_path in self._walk_files(self.source):
            rel_path = src_path.relative_to(self.source)
            dst_path = self.destination / rel_path
            dest_files.add(dst_path)
            
            self._sync_file(src_path, dst_path)
        
        # Remove files in destination that don't exist in source
        for dst_path in self._walk_files(self.destination):
            if dst_path not in dest_files:
                self._delete_file(dst_path)
        
        self._print_stats()
        
    def sync_update(self):
        """
        Update mode: Copy new and modified files only
        Never deletes files from destination
        """
        print(f"\n⬆️  Update Sync: {self.source} → {self.destination}")
        print(f"   Dry run: {self.dry_run}\n")
        
        if not self.dry_run:
            self.destination.mkdir(parents=True, exist_ok=True)
        
        for src_path in self._walk_files(self.source):
            rel_path = src_path.relative_to(self.source)
            dst_path = self.destination / rel_path
            
            self._sync_file(src_path, dst_path)
        
        self._print_stats()
        
    def sync_backup(self, backup_dir=None):
        """
        Backup mode: Create timestamped backup before overwriting
        """
        if backup_dir is None:
            backup_dir = self.destination.parent / f"{self.destination.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n💾 Backup Sync: {self.source} → {self.destination}")
        print(f"   Backup to: {backup_dir}")
        print(f"   Dry run: {self.dry_run}\n")
        
        if not self.dry_run:
            self.destination.mkdir(parents=True, exist_ok=True)
            Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        for src_path in self._walk_files(self.source):
            rel_path = src_path.relative_to(self.source)
            dst_path = self.destination / rel_path
            
            # Backup existing file if it will be overwritten
            if dst_path.exists() and self._files_differ(src_path, dst_path):
                backup_path = Path(backup_dir) / rel_path
                self._backup_file(dst_path, backup_path)
            
            self._sync_file(src_path, dst_path)
        
        self._print_stats()
        
    def _walk_files(self, directory):
        """Generator to walk all files in directory"""
        if not directory.exists():
            return
        for path in directory.rglob('*'):
            if path.is_file():
                yield path
                
    def _sync_file(self, src_path, dst_path):
        """Sync a single file from source to destination"""
        try:
            # Check if destination exists and is up to date
            if dst_path.exists():
                if not self._files_differ(src_path, dst_path):
                    if self.verbose:
                        print(f"   ⏭️  Skipped (identical): {src_path.name}")
                    self.stats['skipped'] += 1
                    return
                action = "Updated"
                self.stats['updated'] += 1
            else:
                action = "Copied"
                self.stats['copied'] += 1
            
            if not self.dry_run:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
            
            file_size = src_path.stat().st_size
            self.stats['bytes_transferred'] += file_size
            
            size_str = self._format_bytes(file_size)
            dry_str = "[DRY RUN] Would " if self.dry_run else ""
            print(f"   {dry_str}{action}: {src_path.name} ({size_str})")
            
        except Exception as e:
            print(f"   ❌ Error syncing {src_path.name}: {e}")
            self.stats['errors'] += 1
            
    def _delete_file(self, path):
        """Delete a file from destination"""
        try:
            if not self.dry_run:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
            
            dry_str = "[DRY RUN] Would delete" if self.dry_run else "Deleted"
            print(f"   {dry_str}: {path.name}")
            self.stats['deleted'] += 1
            
        except Exception as e:
            print(f"   ❌ Error deleting {path.name}: {e}")
            self.stats['errors'] += 1
            
    def _backup_file(self, src_path, backup_path):
        """Backup a file before overwriting"""
        try:
            if not self.dry_run:
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, backup_path)
            
            dry_str = "[DRY RUN] Would backup" if self.dry_run else "Backed up"
            print(f"   💾 {dry_str}: {src_path.name}")
            
        except Exception as e:
            print(f"   ❌ Error backing up {src_path.name}: {e}")
            
    def _files_differ(self, path1, path2):
        """Check if two files differ by size and modification time"""
        try:
            stat1 = path1.stat()
            stat2 = path2.stat()
            return stat1.st_size != stat2.st_size or stat1.st_mtime != stat2.st_mtime
        except:
            return True
            
    def _format_bytes(self, size):
        """Format byte size to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"
        
    def _print_stats(self):
        """Print sync statistics"""
        print(f"\n📊 Sync Statistics:")
        print(f"   Copied: {self.stats['copied']}")
        print(f"   Updated: {self.stats['updated']}")
        print(f"   Deleted: {self.stats['deleted']}")
        print(f"   Skipped: {self.stats['skipped']}")
        print(f"   Errors: {self.stats['errors']}")
        print(f"   Total transferred: {self._format_bytes(self.stats['bytes_transferred'])}")


def main():
    parser = argparse.ArgumentParser(
        description='Directory Sync Tool - Sync directories with multiple modes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Documents /backup/Documents --mirror
  %(prog)s ~/Projects /backup/Projects --update
  %(prog)s ~/Important /backup/Important --backup --backup-dir ~/Backups
  %(prog)s ~/Test /backup/Test --mirror --dry-run --verbose
        """
    )
    
    parser.add_argument('source', help='Source directory')
    parser.add_argument('destination', help='Destination directory')
    parser.add_argument('--mirror', action='store_true', help='Mirror mode (delete extra files)')
    parser.add_argument('--update', action='store_true', help='Update mode (copy new/modified only)')
    parser.add_argument('--backup', action='store_true', help='Backup mode (backup before overwrite)')
    parser.add_argument('--backup-dir', help='Custom backup directory')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate source
    if not os.path.isdir(args.source):
        print(f"❌ Error: Source '{args.source}' is not a valid directory")
        return 1
    
    # Require exactly one mode
    modes = [args.mirror, args.update, args.backup]
    if sum(modes) != 1:
        print("❌ Error: Please specify exactly one mode (--mirror, --update, or --backup)")
        return 1
    
    sync = DirectorySync(args.source, args.destination, dry_run=args.dry_run, verbose=args.verbose)
    
    if args.mirror:
        sync.sync_mirror()
    elif args.update:
        sync.sync_update()
    elif args.backup:
        sync.sync_backup(backup_dir=args.backup_dir)
    
    return 0


if __name__ == '__main__':
    exit(main())
