#!/usr/bin/env python3
"""
Smart File Organizer - Organize your downloads folder automatically
A standalone Python script for organizing cluttered directories

Usage:
    python file_organizer.py /path/to/directory
    python file_organizer.py ~/Downloads

Features:
    - Auto-categorizes files by type
    - Creates organized subdirectories
    - Handles duplicates intelligently
    - Shows before/after summary
    - Safe - can preview before moving
"""

import os
import sys
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# File type categories
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs', '.swift'],
    'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
    'Data': ['.json', '.xml', '.csv', '.yaml', '.yml', '.sql', '.db', '.sqlite'],
}

class FileOrganizer:
    def __init__(self, target_dir, dry_run=True):
        self.target_dir = Path(target_dir).expanduser().resolve()
        self.dry_run = dry_run
        self.stats = defaultdict(int)
        self.operations = []
        
        if not self.target_dir.exists():
            print(f"❌ Directory does not exist: {self.target_dir}")
            sys.exit(1)
    
    def get_category(self, file_path):
        """Determine file category based on extension"""
        ext = file_path.suffix.lower()
        for category, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                return category
        return 'Others'
    
    def organize(self):
        """Main organization logic"""
        print(f"\n{'='*60}")
        print(f"📁 Smart File Organizer")
        print(f"{'='*60}")
        print(f"Target: {self.target_dir}")
        print(f"Mode: {'PREVIEW' if self.dry_run else 'EXECUTE'}")
        print(f"{'='*60}\n")
        
        # Scan files
        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        
        if not files:
            print("✅ No files to organize!")
            return
        
        print(f"Found {len(files)} files to organize\n")
        
        # Categorize files
        categorized = defaultdict(list)
        for file_path in files:
            category = self.get_category(file_path)
            categorized[category].append(file_path)
        
        # Show preview
        print("📊 Organization Preview:")
        print("-" * 60)
        for category, file_list in sorted(categorized.items()):
            print(f"\n📂 {category} ({len(file_list)} files):")
            for f in file_list[:3]:  # Show first 3
                print(f"   • {f.name}")
            if len(file_list) > 3:
                print(f"   ... and {len(file_list) - 3} more")
        
        print("\n" + "-" * 60)
        
        # Execute moves
        if not self.dry_run:
            print("\n🚀 Executing organization...\n")
        
        for category, file_list in categorized.items():
            category_dir = self.target_dir / category
            
            if not self.dry_run:
                category_dir.mkdir(exist_ok=True)
            
            for file_path in file_list:
                dest = category_dir / file_path.name
                
                # Handle duplicates
                if dest.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dest = category_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
                
                if self.dry_run:
                    self.operations.append(f"Would move: {file_path.name} → {category}/")
                else:
                    try:
                        shutil.move(str(file_path), str(dest))
                        self.operations.append(f"Moved: {file_path.name} → {category}/")
                        self.stats[category] += 1
                    except Exception as e:
                        self.operations.append(f"❌ Failed: {file_path.name} - {e}")
        
        self.show_summary()
    
    def show_summary(self):
        """Display operation summary"""
        print(f"\n{'='*60}")
        print("📈 SUMMARY")
        print(f"{'='*60}")
        
        if self.dry_run:
            print("\n✅ PREVIEW MODE - No files were moved")
            print(f"Total operations that would occur: {len(self.operations)}\n")
            for op in self.operations[:10]:
                print(f"  {op}")
            if len(self.operations) > 10:
                print(f"  ... and {len(self.operations) - 10} more")
            print("\n💡 Run with --execute to actually organize files")
        else:
            print("\n✅ Organization complete!")
            print(f"\nFiles organized by category:")
            for category, count in sorted(self.stats.items()):
                print(f"  📂 {category}: {count} files")
            print(f"\nTotal files moved: {sum(self.stats.values())}")
        
        print(f"{'='*60}\n")


def main():
    print("\n" + "="*60)
    print("  Smart File Organizer v1.0")
    print("  Organize your cluttered directories with one command")
    print("="*60 + "\n")
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python file_organizer.py /path/to/directory")
        print("  python file_organizer.py ~/Downloads --execute")
        print("\nOptions:")
        print("  --execute    Actually move files (default is preview mode)")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    dry_run = "--execute" not in sys.argv
    
    # Run organizer
    organizer = FileOrganizer(target_dir, dry_run=dry_run)
    organizer.organize()


if __name__ == "__main__":
    main()
