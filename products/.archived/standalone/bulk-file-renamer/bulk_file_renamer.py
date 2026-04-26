#!/usr/bin/env python3
"""
Bulk File Renamer - Advanced batch file renaming tool
Product #30 in the UniverseCreator standalone tool series
Features: Pattern matching, regex support, preview mode, undo, sequential numbering
"""

import os
import sys
import re
import json
import argparse
import glob
from datetime import datetime
from typing import List, Tuple, Optional


class BulkFileRenamer:
    """Advanced bulk file renaming with safety features."""

    def __init__(self):
        self.history_file = ".rename_history.json"
        self.operations = []

    def log_operation(self, old_path: str, new_path: str):
        """Log a rename operation for potential undo."""
        self.operations.append({
            "timestamp": datetime.now().isoformat(),
            "old_path": old_path,
            "new_path": new_path
        })

    def save_history(self):
        """Save operation history to file."""
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        history.extend(self.operations)
        with open(self.history_file, 'w') as f:
            json.dump(history[-100:], f, indent=2)

    def load_history(self) -> List[dict]:
        """Load operation history."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def preview_rename(self, files: List[str], pattern: str, replacement: str,
                       use_regex: bool = False) -> List[Tuple[str, str]]:
        """Preview rename operations without executing."""
        previews = []
        for file_path in files:
            filename = os.path.basename(file_path)
            if use_regex:
                new_filename = re.sub(pattern, replacement, filename)
            else:
                new_filename = filename.replace(pattern, replacement)
            if new_filename != filename:
                new_path = os.path.join(os.path.dirname(file_path), new_filename)
                previews.append((file_path, new_path))
        return previews

    def execute_rename(self, previews: List[Tuple[str, str]]) -> Tuple[int, List[str]]:
        """Execute rename operations."""
        success_count = 0
        errors = []
        for old_path, new_path in previews:
            try:
                os.rename(old_path, new_path)
                self.log_operation(old_path, new_path)
                success_count += 1
            except Exception as e:
                errors.append(f"Failed to rename {old_path}: {e}")
        if self.operations:
            self.save_history()
        return success_count, errors

    def undo_last(self, count: int = 1) -> Tuple[int, List[str]]:
        """Undo last N rename operations."""
        history = self.load_history()
        if not history:
            return 0, ["No operations to undo"]

        success_count = 0
        errors = []
        for op in reversed(history[-count:]):
            try:
                if os.path.exists(op["new_path"]):
                    os.rename(op["new_path"], op["old_path"])
                    success_count += 1
            except Exception as e:
                errors.append(f"Failed to undo {op['new_path']}: {e}")
        return success_count, errors

    def add_sequence(self, files: List[str], start: int = 1,
                     prefix: str = "", suffix: str = "",
                     extension: Optional[str] = None) -> List[Tuple[str, str]]:
        """Generate sequential filenames."""
        previews = []
        for i, file_path in enumerate(files, start):
            old_dir = os.path.dirname(file_path)
            old_ext = extension or os.path.splitext(file_path)[1]
            new_filename = f"{prefix}{i:03d}{suffix}{old_ext}"
            new_path = os.path.join(old_dir, new_filename)
            previews.append((file_path, new_path))
        return previews

    def add_timestamp(self, files: List[str],
                      prefix: str = "", suffix: str = "") -> List[Tuple[str, str]]:
        """Add timestamps to filenames."""
        previews = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file_path in files:
            old_dir = os.path.dirname(file_path)
            old_name, old_ext = os.path.splitext(os.path.basename(file_path))
            new_filename = f"{prefix}{old_name}_{timestamp}{suffix}{old_ext}"
            new_path = os.path.join(old_dir, new_filename)
            previews.append((file_path, new_path))
        return previews

    def change_case(self, files: List[str], case: str = "lower") -> List[Tuple[str, str]]:
        """Change filename case."""
        previews = []
        for file_path in files:
            old_dir = os.path.dirname(file_path)
            old_name, old_ext = os.path.splitext(os.path.basename(file_path))
            if case == "lower":
                new_name = old_name.lower()
            elif case == "upper":
                new_name = old_name.upper()
            elif case == "title":
                new_name = old_name.title()
            else:
                continue
            new_path = os.path.join(old_dir, f"{new_name}{old_ext}")
            if new_path != file_path:
                previews.append((file_path, new_path))
        return previews


def interactive_mode():
    """Run interactive renaming session."""
    print("\n" + "="*60)
    print("  BULK FILE RENAMER - Interactive Mode")
    print("  Product #30 by UniverseCreator")
    print("="*60 + "\n")

    renamer = BulkFileRenamer()

    # Get directory
    directory = input("📁 Enter directory path (default: current): ").strip()
    if not directory:
        directory = "."

    if not os.path.isdir(directory):
        print(f"❌ Directory not found: {directory}")
        return

    # Get file pattern
    pattern = input("🔍 File pattern (e.g., *.jpg, *.txt, *): ").strip() or "*"

    # Find files
    search_path = os.path.join(directory, pattern)
    files = sorted(glob.glob(search_path))
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        print(f"❌ No files found matching: {pattern}")
        return

    print(f"\n✅ Found {len(files)} files")

    # Show menu
    print("\n" + "-"*40)
    print("  RENAMING OPTIONS:")
    print("-"*40)
    print("  1. Replace text in filenames")
    print("  2. Regex pattern replace")
    print("  3. Add sequential numbering")
    print("  4. Add timestamp")
    print("  5. Change case (lower/upper/title)")
    print("  6. Undo last operation")
    print("-"*40)

    choice = input("\nSelect option (1-6): ").strip()

    previews = []

    if choice == "1":
        old_text = input("Text to replace: ")
        new_text = input("Replace with: ")
        previews = renamer.preview_rename(files, old_text, new_text)

    elif choice == "2":
        regex_pattern = input("Regex pattern: ")
        regex_replace = input("Replacement (use $1, $2 for groups): ")
        try:
            re.compile(regex_pattern)
            previews = renamer.preview_rename(files, regex_pattern, regex_replace, use_regex=True)
        except re.error as e:
            print(f"❌ Invalid regex: {e}")
            return

    elif choice == "3":
        start_num = int(input("Start number (default: 1): ") or "1")
        prefix = input("Prefix (optional): ")
        suffix = input("Suffix (optional): ")
        ext = input("New extension (optional, e.g., .jpg): ").strip() or None
        previews = renamer.add_sequence(files, start_num, prefix, suffix, ext)

    elif choice == "4":
        prefix = input("Prefix (optional): ")
        suffix = input("Suffix (optional): ")
        previews = renamer.add_timestamp(files, prefix, suffix)

    elif choice == "5":
        print("\nCase options: lower, upper, title")
        case_choice = input("Select case: ").strip().lower()
        if case_choice in ["lower", "upper", "title"]:
            previews = renamer.change_case(files, case_choice)
        else:
            print("❌ Invalid case option")
            return

    elif choice == "6":
        count = int(input("How many operations to undo (default: 1): ") or "1")
        success, errors = renamer.undo_last(count)
        print(f"\n✅ Undone {success} operations")
        if errors:
            for err in errors:
                print(f"⚠️  {err}")
        return

    else:
        print("❌ Invalid option")
        return

    # Show preview
    if not previews:
        print("\n⚠️  No files would be renamed with these settings")
        return

    print(f"\n📋 PREVIEW - {len(previews)} files will be renamed:")
    print("-" * 60)
    for old, new in previews[:10]:  # Show first 10
        old_name = os.path.basename(old)
        new_name = os.path.basename(new)
        print(f"  {old_name}")
        print(f"  → {new_name}")
        print()
    if len(previews) > 10:
        print(f"  ... and {len(previews) - 10} more files")

    # Confirm
    confirm = input("\n⚡ Execute these changes? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        success, errors = renamer.execute_rename(previews)
        print(f"\n✅ Successfully renamed {success} files")
        if errors:
            print(f"\n⚠️  Errors ({len(errors)}):")
            for err in errors:
                print(f"  - {err}")
    else:
        print("\n❌ Cancelled")


def main():
    """Main entry point with CLI support."""
    parser = argparse.ArgumentParser(
        description="Bulk File Renamer - Advanced batch renaming tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i                          # Interactive mode
  %(prog)s -d ./photos -p "*.jpg" -r "IMG" "Vacation"  # Replace text
  %(prog)s -d ./files --sequence --prefix "file_"      # Sequential numbering
  %(prog)s --undo 5                    # Undo last 5 operations
        """
    )

    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Run in interactive mode")
    parser.add_argument("-d", "--directory", default=".",
                        help="Directory to process (default: current)")
    parser.add_argument("-p", "--pattern", default="*",
                        help="File pattern to match (default: *)")
    parser.add_argument("-r", "--replace", nargs=2, metavar=("OLD", "NEW"),
                        help="Replace OLD with NEW in filenames")
    parser.add_argument("--regex", action="store_true",
                        help="Use regex pattern for replacement")
    parser.add_argument("--sequence", action="store_true",
                        help="Add sequential numbering")
    parser.add_argument("--start", type=int, default=1,
                        help="Starting number for sequence (default: 1)")
    parser.add_argument("--prefix", default="",
                        help="Prefix for sequence/timestamp")
    parser.add_argument("--suffix", default="",
                        help="Suffix for sequence/timestamp")
    parser.add_argument("--timestamp", action="store_true",
                        help="Add timestamp to filenames")
    parser.add_argument("--case", choices=["lower", "upper", "title"],
                        help="Change filename case")
    parser.add_argument("--undo", type=int, metavar="N",
                        help="Undo last N operations")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without executing")

    args = parser.parse_args()

    # Handle undo first
    if args.undo:
        renamer = BulkFileRenamer()
        success, errors = renamer.undo_last(args.undo)
        print(f"✅ Undone {success} operations")
        for err in errors:
            print(f"⚠️  {err}")
        return

    # Interactive mode
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return

    # CLI mode
    renamer = BulkFileRenamer()

    # Find files
    search_path = os.path.join(args.directory, args.pattern)
    files = sorted(glob.glob(search_path))
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        print(f"❌ No files found matching: {search_path}")
        return

    print(f"✅ Found {len(files)} files")

    # Generate previews based on operation
    previews = []

    if args.replace:
        old, new = args.replace
        previews = renamer.preview_rename(files, old, new, args.regex)

    elif args.sequence:
        previews = renamer.add_sequence(files, args.start, args.prefix, args.suffix)

    elif args.timestamp:
        previews = renamer.add_timestamp(files, args.prefix, args.suffix)

    elif args.case:
        previews = renamer.change_case(files, args.case)

    else:
        print("❌ No operation specified. Use --interactive or see --help")
        return

    # Show preview
    if not previews:
        print("⚠️  No files would be renamed")
        return

    print(f"\n📋 Preview ({len(previews)} files):")
    for old, new in previews[:5]:
        print(f"  {os.path.basename(old)} → {os.path.basename(new)}")
    if len(previews) > 5:
        print(f"  ... and {len(previews) - 5} more")

    # Execute or dry run
    if args.dry_run:
        print("\n🔍 Dry run - no changes made")
    else:
        confirm = input("\n⚡ Execute? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            success, errors = renamer.execute_rename(previews)
            print(f"✅ Renamed {success} files")
            for err in errors:
                print(f"⚠️  {err}")
        else:
            print("❌ Cancelled")


if __name__ == "__main__":
    main()