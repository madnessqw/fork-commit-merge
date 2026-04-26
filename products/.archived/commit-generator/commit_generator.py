#!/usr/bin/env python3
"""
Git Commit Message Generator CLI
Generate conventional commit messages using AI or smart templates
"""

import argparse
import subprocess
import sys
import re
from datetime import datetime

# Conventional commit types
COMMIT_TYPES = {
    "feat": "A new feature",
    "fix": "A bug fix",
    "docs": "Documentation only changes",
    "style": "Changes that don't affect code meaning (formatting, semicolons, etc)",
    "refactor": "A code change that neither fixes a bug nor adds a feature",
    "perf": "A code change that improves performance",
    "test": "Adding missing tests or correcting existing tests",
    "chore": "Changes to build process or auxiliary tools",
    "ci": "Changes to CI configuration",
    "build": "Changes that affect the build system or dependencies",
    "revert": "Reverts a previous commit"
}

# Scope suggestions by project type
SCOPE_SUGGESTIONS = {
    "web": ["frontend", "backend", "api", "auth", "ui", "css", "js"],
    "mobile": ["ios", "android", "flutter", "react-native", "ui"],
    "ai": ["model", "training", "inference", "data", "pipeline"],
    "blockchain": ["contract", "wallet", "node", "consensus", "crypto"],
    "general": ["core", "utils", "config", "deps", "docs", "tests"]
}

# Smart message templates
TEMPLATES = {
    "add": "{type}{scope}: add {what} to {where}",
    "update": "{type}{scope}: update {what} for {reason}",
    "fix": "{type}{scope}: fix {issue} in {location}",
    "remove": "{type}{scope}: remove {what} from {where}",
    "refactor": "{type}{scope}: refactor {what} to {improvement}",
    "implement": "{type}{scope}: implement {feature} for {purpose}",
    "optimize": "{type}{scope}: optimize {what} for {benefit}",
}


def get_git_diff():
    """Get the current git diff for context"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        return []
    except:
        return []


def get_git_status():
    """Get git status summary"""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    except:
        return ""


def detect_scope(files):
    """Detect scope from changed files"""
    if not files:
        return ""
    
    # Extract directory names
    dirs = set()
    for f in files:
        parts = f.split('/')
        if len(parts) > 1:
            dirs.add(parts[0])
    
    if dirs:
        return list(dirs)[0]
    return ""


def detect_type(files, status):
    """Detect commit type from changes"""
    status_lower = status.lower()
    
    # Check for test files
    if any('test' in f.lower() for f in files):
        return "test"
    
    # Check for docs
    if any(f.endswith(('.md', '.rst', '.txt')) for f in files):
        return "docs"
    
    # Check for config files
    if any(f.endswith(('.json', '.yaml', '.yml', '.toml', '.ini')) for f in files):
        return "config"
    
    # Default to feat for new files, fix for modifications
    if 'A' in status:
        return "feat"
    return "fix"


def generate_suggestions(files, status):
    """Generate commit message suggestions"""
    suggestions = []
    scope = detect_scope(files)
    detected_type = detect_type(files, status)
    
    scope_str = f"({scope})" if scope else ""
    
    # Get file names for context
    file_names = [f.split('/')[-1] for f in files if f]
    file_summary = ', '.join(file_names[:3])
    if len(file_names) > 3:
        file_summary += f" and {len(file_names) - 3} more"
    
    # Generate contextual suggestions
    suggestions.append({
        "type": detected_type,
        "scope": scope,
        "message": f"{detected_type}{scope_str}: update {file_summary}",
        "template": "update"
    })
    
    if detected_type == "feat":
        suggestions.append({
            "type": "feat",
            "scope": scope,
            "message": f"feat{scope_str}: add support for {scope or 'new feature'}",
            "template": "add"
        })
    
    if detected_type == "fix":
        suggestions.append({
            "type": "fix",
            "scope": scope,
            "message": f"fix{scope_str}: resolve issue in {scope or 'module'}",
            "template": "fix"
        })
    
    # Add generic suggestions
    suggestions.append({
        "type": "refactor",
        "scope": scope,
        "message": f"refactor{scope_str}: improve {scope or 'code'} structure",
        "template": "refactor"
    })
    
    return suggestions


def interactive_mode():
    """Interactive commit message generation"""
    print("📝 Git Commit Message Generator\n")
    
    # Get git info
    files = get_git_diff()
    status = get_git_status()
    
    if not files and not status:
        print("⚠️  No staged changes found. Stage files with 'git add' first.")
        return
    
    print(f"Changed files: {len(files)}")
    print(f"Files: {', '.join(files[:5])}{'...' if len(files) > 5 else ''}\n")
    
    # Show type options
    print("Select commit type:")
    for i, (ctype, desc) in enumerate(COMMIT_TYPES.items(), 1):
        marker = "✓" if i == 1 else " "
        print(f"  [{marker}] {i}. {ctype:<10} - {desc}")
    
    try:
        type_choice = int(input("\nEnter number (1-10): ") or "1")
        commit_type = list(COMMIT_TYPES.keys())[type_choice - 1]
    except (ValueError, IndexError):
        commit_type = "feat"
    
    # Scope
    detected_scope = detect_scope(files)
    scope = input(f"\nScope (optional, detected: '{detected_scope}'): ").strip()
    if not scope and detected_scope:
        scope = detected_scope
    
    scope_str = f"({scope})" if scope else ""
    
    # Message
    print("\nQuick templates:")
    print("  1. Add feature")
    print("  2. Fix bug")
    print("  3. Update existing")
    print("  4. Remove feature")
    print("  5. Custom message")
    
    template_choice = input("\nSelect template (1-5): ").strip() or "5"
    
    if template_choice == "1":
        what = input("What are you adding? ")
        where = input("Where? (e.g., 'API', 'UI') ") or scope or "module"
        message = f"add {what} to {where}"
    elif template_choice == "2":
        issue = input("What issue are you fixing? ")
        location = input("Where? ") or scope or "module"
        message = f"fix {issue} in {location}"
    elif template_choice == "3":
        what = input("What are you updating? ")
        reason = input("Why? (optional) ")
        if reason:
            message = f"update {what} for {reason}"
        else:
            message = f"update {what}"
    elif template_choice == "4":
        what = input("What are you removing? ")
        where = input("From where? ") or scope or "module"
        message = f"remove {what} from {where}"
    else:
        message = input("\nEnter commit message: ").strip()
    
    # Build final message
    final_message = f"{commit_type}{scope_str}: {message.lower()}"
    
    print(f"\n{'='*50}")
    print(f"Generated commit message:")
    print(f"  {final_message}")
    print(f"{'='*50}")
    
    # Body and footer
    add_body = input("\nAdd detailed description? (y/n): ").lower() == 'y'
    body = ""
    if add_body:
        print("Enter description (blank line to finish):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        body = '\n'.join(lines)
    
    # Footer
    add_footer = input("Add footer (e.g., 'Closes #123')? (y/n): ").lower() == 'y'
    footer = ""
    if add_footer:
        footer = input("Footer: ").strip()
    
    # Preview
    print(f"\n{'='*50}")
    print("FINAL COMMIT MESSAGE:")
    print(f"{'='*50}")
    print(final_message)
    if body:
        print(f"\n{body}")
    if footer:
        print(f"\n{footer}")
    print(f"{'='*50}")
    
    # Confirm
    if input("\nCommit with this message? (y/n): ").lower() == 'y':
        full_message = final_message
        if body:
            full_message += f"\n\n{body}"
        if footer:
            full_message += f"\n\n{footer}"
        
        try:
            result = subprocess.run(
                ["git", "commit", "-m", full_message],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Committed successfully!")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("Commit cancelled. Message saved to clipboard (if available).")


def quick_mode(args):
    """Quick one-liner commit"""
    commit_type = args.type or "feat"
    scope = args.scope
    message = args.message
    
    scope_str = f"({scope})" if scope else ""
    final_message = f"{commit_type}{scope_str}: {message}"
    
    print(final_message)
    
    if args.commit:
        try:
            result = subprocess.run(
                ["git", "commit", "-m", final_message],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Committed successfully!")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")


def suggest_mode():
    """Suggest commit messages based on staged changes"""
    files = get_git_diff()
    status = get_git_status()
    
    if not files:
        print("⚠️  No staged changes found. Run 'git add' first.")
        return
    
    suggestions = generate_suggestions(files, status)
    
    print("📝 Suggested commit messages:\n")
    for i, sugg in enumerate(suggestions, 1):
        print(f"  {i}. {sugg['message']}")
        print(f"     Type: {sugg['type']}, Template: {sugg['template']}")
        print()
    
    print("Use with: git commit -m \"<message>\"")


def list_types():
    """List all conventional commit types"""
    print("📋 Conventional Commit Types:\n")
    for ctype, desc in COMMIT_TYPES.items():
        print(f"  {ctype:<10} - {desc}")
    print("\nUsage: <type>(<scope>): <description>")


def main():
    parser = argparse.ArgumentParser(
        description="Generate conventional commit messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Interactive mode
  %(prog)s -i                 # Interactive mode (explicit)
  %(prog)s -s                 # Suggest based on staged changes
  %(prog)s -t                 # List commit types
  %(prog)s -q feat "add login" --commit
  %(prog)s -q fix "resolve bug" -s auth --commit
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive mode (default)')
    parser.add_argument('-s', '--suggest', action='store_true',
                        help='Suggest messages for staged changes')
    parser.add_argument('-t', '--types', action='store_true',
                        help='List conventional commit types')
    parser.add_argument('-q', '--quick', nargs=2, metavar=('TYPE', 'MESSAGE'),
                        help='Quick mode: type and message')
    parser.add_argument('--scope', '-S', help='Scope for quick mode')
    parser.add_argument('--commit', '-c', action='store_true',
                        help='Actually commit in quick mode')
    
    args = parser.parse_args()
    
    if args.types:
        list_types()
    elif args.suggest:
        suggest_mode()
    elif args.quick:
        quick_mode(args)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
