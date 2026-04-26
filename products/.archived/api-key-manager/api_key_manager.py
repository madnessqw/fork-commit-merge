#!/usr/bin/env python3
"""
API Key Manager CLI
Securely store, organize, and manage API keys with encryption.
Part of the Complete Developer Toolkit.
"""

import argparse
import json
import os
import sys
import getpass
import hashlib
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Simple encryption using Fernet-like approach (for demonstration - use proper encryption in production)
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

CONFIG_DIR = Path.home() / ".config" / "api-key-manager"
KEYS_FILE = CONFIG_DIR / "keys.enc"
MASTER_FILE = CONFIG_DIR / ".master"
SALT_FILE = CONFIG_DIR / ".salt"

class APIKeyManager:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.keys_file = KEYS_FILE
        self.master_file = MASTER_FILE
        self.salt_file = SALT_FILE
        self._ensure_config_dir()
        self._cipher = None
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        # Set restrictive permissions (Unix only)
        try:
            os.chmod(self.config_dir, 0o700)
        except:
            pass
    
    def _get_salt(self) -> bytes:
        """Get or create salt for key derivation."""
        if self.salt_file.exists():
            return base64.urlsafe_b64decode(self.salt_file.read_text().strip())
        else:
            import secrets
            salt = secrets.token_bytes(32)
            self.salt_file.write_text(base64.urlsafe_b64encode(salt).decode())
            try:
                os.chmod(self.salt_file, 0o600)
            except:
                pass
            return salt
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password."""
        if not CRYPTO_AVAILABLE:
            # Fallback to simple hash (not secure, for demo only)
            return hashlib.sha256((password + self._get_salt().hex()).encode()).digest()
        
        salt = self._get_salt()
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _get_cipher(self, password: str):
        """Get or create Fernet cipher."""
        if self._cipher is None and CRYPTO_AVAILABLE:
            key = self._derive_key(password)
            self._cipher = Fernet(key)
        return self._cipher
    
    def setup(self, password: Optional[str] = None) -> bool:
        """Initialize the key manager with a master password."""
        if self.master_file.exists():
            print("⚠️  API Key Manager already initialized.")
            return False
        
        if password is None:
            password = getpass.getpass("Create master password: ")
            confirm = getpass.getpass("Confirm master password: ")
            if password != confirm:
                print("❌ Passwords do not match.")
                return False
        
        if len(password) < 8:
            print("❌ Password must be at least 8 characters.")
            return False
        
        # Store password hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.master_file.write_text(password_hash)
        try:
            os.chmod(self.master_file, 0o600)
        except:
            pass
        
        # Initialize empty keys file
        self._save_keys({}, password)
        
        print("✅ API Key Manager initialized successfully!")
        print(f"📁 Keys stored in: {self.config_dir}")
        return True
    
    def _verify_password(self, password: str) -> bool:
        """Verify master password."""
        if not self.master_file.exists():
            return False
        stored_hash = self.master_file.read_text().strip()
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    
    def _load_keys(self, password: str) -> Dict:
        """Load and decrypt keys."""
        if not self.keys_file.exists():
            return {}
        
        try:
            if CRYPTO_AVAILABLE:
                cipher = self._get_cipher(password)
                encrypted_data = self.keys_file.read_bytes()
                decrypted_data = cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
            else:
                # Fallback: simple obfuscation
                data = self.keys_file.read_bytes()
                key = self._derive_key(password)
                decrypted = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
                return json.loads(decrypted.decode())
        except Exception as e:
            print(f"❌ Failed to decrypt keys. Wrong password?")
            return None
    
    def _save_keys(self, keys: Dict, password: str):
        """Encrypt and save keys."""
        data = json.dumps(keys, indent=2).encode()
        
        if CRYPTO_AVAILABLE:
            cipher = self._get_cipher(password)
            encrypted = cipher.encrypt(data)
            self.keys_file.write_bytes(encrypted)
        else:
            # Fallback: simple obfuscation
            key = self._derive_key(password)
            encrypted = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
            self.keys_file.write_bytes(encrypted)
        
        try:
            os.chmod(self.keys_file, 0o600)
        except:
            pass
    
    def add_key(self, name: str, key_value: str, service: str = "", 
                environment: str = "production", password: Optional[str] = None) -> bool:
        """Add a new API key."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized. Run 'api-key-manager setup' first.")
            return False
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return False
        
        keys = self._load_keys(password)
        if keys is None:
            return False
        
        if name in keys:
            print(f"⚠️  Key '{name}' already exists. Use 'update' to modify.")
            return False
        
        keys[name] = {
            "key": key_value,
            "service": service,
            "environment": environment,
            "created": datetime.now().isoformat(),
            "last_used": None
        }
        
        self._save_keys(keys, password)
        print(f"✅ Added key '{name}' for {service or 'unknown service'}")
        return True
    
    def get_key(self, name: str, password: Optional[str] = None, 
                copy_to_clipboard: bool = False) -> Optional[str]:
        """Retrieve an API key."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return None
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return None
        
        keys = self._load_keys(password)
        if keys is None:
            return None
        
        if name not in keys:
            print(f"❌ Key '{name}' not found.")
            return None
        
        key_data = keys[name]
        key_value = key_data["key"]
        
        # Update last used
        keys[name]["last_used"] = datetime.now().isoformat()
        self._save_keys(keys, password)
        
        if copy_to_clipboard:
            try:
                import pyperclip
                pyperclip.copy(key_value)
                print(f"✅ Key '{name}' copied to clipboard!")
            except ImportError:
                print("⚠️  pyperclip not installed. Key:")
                print(f"   {key_value}")
        else:
            print(f"🔑 Key '{name}':")
            print(f"   Service: {key_data.get('service', 'N/A')}")
            print(f"   Environment: {key_data.get('environment', 'N/A')}")
            print(f"   Value: {key_value}")
        
        return key_value
    
    def list_keys(self, service: Optional[str] = None, 
                  environment: Optional[str] = None,
                  password: Optional[str] = None) -> List[Dict]:
        """List all stored keys."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return []
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return []
        
        keys = self._load_keys(password)
        if keys is None:
            return []
        
        filtered_keys = []
        for name, data in keys.items():
            if service and data.get("service") != service:
                continue
            if environment and data.get("environment") != environment:
                continue
            filtered_keys.append({
                "name": name,
                **data,
                "key": "***" + data["key"][-4:] if len(data["key"]) > 4 else "****"
            })
        
        if not filtered_keys:
            print("📭 No keys found.")
            return []
        
        print(f"\n📋 Stored API Keys ({len(filtered_keys)} total):\n")
        print(f"{'Name':<20} {'Service':<15} {'Environment':<12} {'Created':<20} {'Key'}")
        print("-" * 90)
        for key in filtered_keys:
            created = key["created"][:10] if key.get("created") else "N/A"
            print(f"{key['name']:<20} {key.get('service', 'N/A'):<15} "
                  f"{key.get('environment', 'N/A'):<12} {created:<20} {key['key']}")
        
        return filtered_keys
    
    def update_key(self, name: str, key_value: Optional[str] = None,
                   service: Optional[str] = None, environment: Optional[str] = None,
                   password: Optional[str] = None) -> bool:
        """Update an existing key."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return False
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return False
        
        keys = self._load_keys(password)
        if keys is None:
            return False
        
        if name not in keys:
            print(f"❌ Key '{name}' not found.")
            return False
        
        if key_value:
            keys[name]["key"] = key_value
        if service:
            keys[name]["service"] = service
        if environment:
            keys[name]["environment"] = environment
        
        keys[name]["updated"] = datetime.now().isoformat()
        self._save_keys(keys, password)
        print(f"✅ Updated key '{name}'")
        return True
    
    def delete_key(self, name: str, password: Optional[str] = None) -> bool:
        """Delete a key."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return False
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return False
        
        keys = self._load_keys(password)
        if keys is None:
            return False
        
        if name not in keys:
            print(f"❌ Key '{name}' not found.")
            return False
        
        confirm = input(f"Delete key '{name}'? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Cancelled.")
            return False
        
        del keys[name]
        self._save_keys(keys, password)
        print(f"✅ Deleted key '{name}'")
        return True
    
    def generate_key(self, name: str, service: str = "", 
                     environment: str = "production", length: int = 32,
                     password: Optional[str] = None) -> Optional[str]:
        """Generate a secure random API key."""
        import secrets
        import string
        
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return None
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return None
        
        # Generate secure random key
        alphabet = string.ascii_letters + string.digits
        key_value = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        # Add prefix based on service
        prefix = service.lower().replace(" ", "_") if service else "key"
        key_value = f"{prefix}_{key_value}"
        
        return self.add_key(name, key_value, service, environment, password)
    
    def export_keys(self, filepath: str, password: Optional[str] = None) -> bool:
        """Export keys to encrypted file."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return False
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return False
        
        keys = self._load_keys(password)
        if keys is None:
            return False
        
        # Export with encryption
        export_data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "keys": keys
        }
        
        data = json.dumps(export_data, indent=2).encode()
        
        if CRYPTO_AVAILABLE:
            cipher = self._get_cipher(password)
            encrypted = cipher.encrypt(data)
            Path(filepath).write_bytes(encrypted)
        else:
            key = self._derive_key(password)
            encrypted = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
            Path(filepath).write_bytes(encrypted)
        
        print(f"✅ Exported {len(keys)} keys to {filepath}")
        return True
    
    def import_keys(self, filepath: str, password: Optional[str] = None,
                    overwrite: bool = False) -> bool:
        """Import keys from encrypted file."""
        if not self.master_file.exists():
            print("❌ API Key Manager not initialized.")
            return False
        
        if not Path(filepath).exists():
            print(f"❌ File not found: {filepath}")
            return False
        
        if password is None:
            password = getpass.getpass("Master password: ")
        
        if not self._verify_password(password):
            print("❌ Incorrect password.")
            return False
        
        try:
            if CRYPTO_AVAILABLE:
                cipher = self._get_cipher(password)
                encrypted_data = Path(filepath).read_bytes()
                decrypted_data = cipher.decrypt(encrypted_data)
                export_data = json.loads(decrypted_data.decode())
            else:
                data = Path(filepath).read_bytes()
                key = self._derive_key(password)
                decrypted = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
                export_data = json.loads(decrypted.decode())
            
            imported_keys = export_data.get("keys", {})
            existing_keys = self._load_keys(password) or {}
            
            if not overwrite:
                # Merge, keeping existing keys
                for name, key_data in imported_keys.items():
                    if name not in existing_keys:
                        existing_keys[name] = key_data
            else:
                existing_keys = imported_keys
            
            self._save_keys(existing_keys, password)
            print(f"✅ Imported {len(imported_keys)} keys from {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to import: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="🔐 API Key Manager - Securely manage your API keys",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s setup                          # Initialize the key manager
  %(prog)s add my-api --service Stripe    # Add a new key
  %(prog)s get my-api --copy              # Copy key to clipboard
  %(prog)s list                           # List all keys
  %(prog)s generate new-key --length 48   # Generate secure random key
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup
    setup_parser = subparsers.add_parser("setup", help="Initialize the key manager")
    
    # Add
    add_parser = subparsers.add_parser("add", help="Add a new API key")
    add_parser.add_argument("name", help="Key name/identifier")
    add_parser.add_argument("--service", "-s", default="", help="Service name")
    add_parser.add_argument("--env", "-e", default="production", help="Environment")
    
    # Get
    get_parser = subparsers.add_parser("get", help="Retrieve an API key")
    get_parser.add_argument("name", help="Key name")
    get_parser.add_argument("--copy", "-c", action="store_true", help="Copy to clipboard")
    
    # List
    list_parser = subparsers.add_parser("list", help="List all keys")
    list_parser.add_argument("--service", "-s", help="Filter by service")
    list_parser.add_argument("--env", "-e", help="Filter by environment")
    
    # Update
    update_parser = subparsers.add_parser("update", help="Update an existing key")
    update_parser.add_argument("name", help="Key name")
    update_parser.add_argument("--key", "-k", help="New key value")
    update_parser.add_argument("--service", "-s", help="New service name")
    update_parser.add_argument("--env", "-e", help="New environment")
    
    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete a key")
    delete_parser.add_argument("name", help="Key name")
    
    # Generate
    gen_parser = subparsers.add_parser("generate", help="Generate a secure random key")
    gen_parser.add_argument("name", help="Key name")
    gen_parser.add_argument("--service", "-s", default="", help="Service name")
    gen_parser.add_argument("--env", "-e", default="production", help="Environment")
    gen_parser.add_argument("--length", "-l", type=int, default=32, help="Key length")
    
    # Export
    export_parser = subparsers.add_parser("export", help="Export keys to file")
    export_parser.add_argument("filepath", help="Export file path")
    
    # Import
    import_parser = subparsers.add_parser("import", help="Import keys from file")
    import_parser.add_argument("filepath", help="Import file path")
    import_parser.add_argument("--overwrite", "-o", action="store_true", help="Overwrite existing keys")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = APIKeyManager()
    
    if args.command == "setup":
        manager.setup()
    elif args.command == "add":
        key_value = getpass.getpass("Enter API key: ")
        manager.add_key(args.name, key_value, args.service, args.env)
    elif args.command == "get":
        manager.get_key(args.name, copy_to_clipboard=args.copy)
    elif args.command == "list":
        manager.list_keys(service=args.service, environment=args.env)
    elif args.command == "update":
        key_value = None
        if args.key:
            key_value = getpass.getpass("Enter new API key: ")
        manager.update_key(args.name, key_value, args.service, args.env)
    elif args.command == "delete":
        manager.delete_key(args.name)
    elif args.command == "generate":
        manager.generate_key(args.name, args.service, args.env, args.length)
    elif args.command == "export":
        manager.export_keys(args.filepath)
    elif args.command == "import":
        manager.import_keys(args.filepath, overwrite=args.overwrite)


if __name__ == "__main__":
    main()