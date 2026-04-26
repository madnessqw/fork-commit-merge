#!/usr/bin/env python3
"""
Environment Variable Manager CLI
Manage .env files, secrets, and environment configurations
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def get_env_path(project_path=None):
    """Get the path to .env file."""
    if project_path:
        return Path(project_path) / ".env"
    return Path(".env")


def load_env_file(env_path):
    """Load .env file into dictionary."""
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def save_env_file(env_path, env_vars):
    """Save dictionary to .env file."""
    with open(env_path, 'w') as f:
        f.write(f"# Environment Variables\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
        for key, value in sorted(env_vars.items()):
            if ' ' in value or ';' in value:
                f.write(f'{key}="{value}"\n')
            else:
                f.write(f"{key}={value}\n")


def cmd_init(args):
    """Initialize a new .env file with common templates."""
    env_path = get_env_path(args.path)
    
    if env_path.exists() and not args.force:
        print(f"❌ {env_path} already exists. Use --force to overwrite.")
        return 1
    
    templates = {
        'web': {
            'NODE_ENV': 'development',
            'PORT': '3000',
            'DATABASE_URL': '',
            'JWT_SECRET': '',
            'API_KEY': ''
        },
        'python': {
            'PYTHON_ENV': 'development',
            'DEBUG': 'True',
            'DATABASE_URL': '',
            'SECRET_KEY': '',
            'REDIS_URL': ''
        },
        'docker': {
            'COMPOSE_PROJECT_NAME': 'myapp',
            'POSTGRES_USER': 'user',
            'POSTGRES_PASSWORD': '',
            'POSTGRES_DB': 'myapp'
        },
        'minimal': {}
    }
    
    template = templates.get(args.template, {})
    save_env_file(env_path, template)
    
    print(f"✅ Created {env_path} with {args.template} template")
    print(f"   Edit the file and add your actual values")
    return 0


def cmd_get(args):
    """Get a specific environment variable."""
    env_path = get_env_path(args.path)
    env_vars = load_env_file(env_path)
    
    if args.key:
        if args.key in env_vars:
            value = env_vars[args.key]
            if args.mask and len(value) > 4:
                print(f"{args.key}={value[:2]}{'*' * (len(value) - 4)}{value[-2:]}")
            else:
                print(f"{args.key}={value}")
        else:
            print(f"❌ Variable '{args.key}' not found")
            return 1
    else:
        # List all variables
        if not env_vars:
            print("No environment variables set")
            return 0
        
        print(f"\n🌍 Environment Variables ({len(env_vars)} total):\n")
        for key, value in sorted(env_vars.items()):
            if args.mask and len(value) > 4:
                display_value = f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"
            else:
                display_value = value
            print(f"  {key:30} = {display_value}")
        print()
    
    return 0


def cmd_set(args):
    """Set an environment variable."""
    env_path = get_env_path(args.path)
    env_vars = load_env_file(env_path)
    
    env_vars[args.key] = args.value
    save_env_file(env_path, env_vars)
    
    print(f"✅ Set {args.key}={args.value[:2]}{'*' * (len(args.value) - 4) if len(args.value) > 4 else ''}")
    return 0


def cmd_unset(args):
    """Remove an environment variable."""
    env_path = get_env_path(args.path)
    env_vars = load_env_file(env_path)
    
    if args.key in env_vars:
        del env_vars[args.key]
        save_env_file(env_path, env_vars)
        print(f"✅ Removed {args.key}")
    else:
        print(f"❌ Variable '{args.key}' not found")
        return 1
    
    return 0


def cmd_generate(args):
    """Generate secure random values."""
    import secrets
    import string
    
    if args.type == 'secret':
        value = secrets.token_hex(args.length or 32)
    elif args.type == 'password':
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        value = ''.join(secrets.choice(chars) for _ in range(args.length or 16))
    elif args.type == 'api_key':
        prefix = args.key.upper().replace('_', '')[:4] if args.key else 'API'
        value = f"{prefix}_{secrets.token_urlsafe(args.length or 24)}"
    else:
        print(f"❌ Unknown type: {args.type}")
        return 1
    
    if args.key:
        env_path = get_env_path(args.path)
        env_vars = load_env_file(env_path)
        env_vars[args.key] = value
        save_env_file(env_path, env_vars)
        print(f"✅ Generated and set {args.key}")
    else:
        print(f"Generated {args.type}: {value}")
    
    return 0


def cmd_sync(args):
    """Sync environment variables to shell."""
    env_path = get_env_path(args.path)
    env_vars = load_env_file(env_path)
    
    if args.format == 'export':
        for key, value in env_vars.items():
            print(f'export {key}="{value}"')
    elif args.format == 'json':
        import json
        print(json.dumps(env_vars, indent=2))
    elif args.format == 'yaml':
        for key, value in env_vars.items():
            print(f"{key}: \"{value}\"")
    
    return 0


def cmd_validate(args):
    """Validate .env file for common issues."""
    env_path = get_env_path(args.path)
    issues = []
    
    if not env_path.exists():
        print(f"❌ {env_path} does not exist")
        return 1
    
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    env_vars = load_env_file(env_path)
    
    # Check for empty values
    for key, value in env_vars.items():
        if not value:
            issues.append(f"⚠️  {key} is empty")
    
    # Check for common secrets that should be secure
    sensitive_keys = ['password', 'secret', 'key', 'token', 'api']
    for key, value in env_vars.items():
        if any(s in key.lower() for s in sensitive_keys):
            if value and len(value) < 8:
                issues.append(f"⚠️  {key} looks like a secret but is too short ({len(value)} chars)")
    
    # Check for .env in git
    gitignore_path = env_path.parent / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            if '.env' not in f.read():
                issues.append("⚠️  .env is not in .gitignore - secrets may be committed!")
    else:
        issues.append("⚠️  No .gitignore found - create one with .env listed")
    
    if issues:
        print(f"\n🔍 Found {len(issues)} issue(s) in {env_path}:\n")
        for issue in issues:
            print(f"  {issue}")
        print()
        return 1
    else:
        print(f"✅ {env_path} looks good!")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Environment Variable Manager - Secure .env management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init                    # Create .env with web template
  %(prog)s get                     # List all variables
  %(prog)s get DATABASE_URL        # Get specific variable
  %(prog)s set API_KEY abc123      # Set a variable
  %(prog)s generate secret API_KEY # Generate secure secret
  %(prog)s validate                # Check for