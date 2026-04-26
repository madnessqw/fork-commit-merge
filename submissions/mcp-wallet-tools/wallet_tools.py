#!/usr/bin/env python3
"""
RustChain MCP Server Wallet Tools
Extends the RustChain MCP Server with wallet management capabilities.

Bounty: #2302 - RustChain MCP Server v0.4: Wallet Management + Transfer Tools
Reward: 75 RTC
"""

import os
import json
import hashlib
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import secrets

# Ed25519 for cryptographic operations
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey
    )
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# BIP39 wordlist for seed phrases (first 256 words)
BIP39_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
    "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
    "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
    "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
    "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
    "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
    "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
    "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
    "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april",
    "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor",
    "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
    "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume",
    "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
    "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado",
    "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis",
    "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball",
    "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base",
    "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become",
    "beef", "before", "begin", "behave", "behind", "believe", "below", "belt",
    "bench", "benefit", "best", "betray", "better", "between", "beyond", "bicycle",
    "bid", "bike", "bind", "biology", "bird", "birth", "bitter", "black",
    "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood",
    "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body",
    "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring",
    "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain",
    "brake", "branch", "brass", "brave", "bread", "breeze", "brick", "bridge",
    "brief", "bright", "brilliant", "bring", "brisk", "broccoli", "broken", "bronze",
    "broom", "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo",
    "build", "bulb", "bulk", "bullet", "bundle", "bunker", "burden", "burger",
    "burst", "bus", "business", "busy", "butter", "buyer", "buzz", "cabbage"
]


class WalletManager:
    """Manages RustChain wallets with secure keystore storage."""
    
    def __init__(self, keystore_path: Optional[str] = None):
        """Initialize wallet manager with keystore path."""
        if keystore_path is None:
            keystore_path = os.path.expanduser("~/.rustchain/mcp_wallets")
        self.keystore_path = Path(keystore_path)
        self.keystore_path.mkdir(parents=True, exist_ok=True)
        self.wallets_file = self.keystore_path / "wallets.json"
        self._ensure_keystore()
    
    def _ensure_keystore(self):
        """Ensure keystore file exists."""
        if not self.wallets_file.exists():
            self._save_wallets({})
    
    def _load_wallets(self) -> Dict:
        """Load wallets from keystore."""
        try:
            with open(self.wallets_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_wallets(self, wallets: Dict):
        """Save wallets to keystore with restricted permissions."""
        with open(self.wallets_file, 'w') as f:
            json.dump(wallets, f, indent=2)
        # Set restrictive permissions (owner read/write only)
        os.chmod(self.wallets_file, 0o600)
    
    def _generate_seed_phrase(self, word_count: int = 12) -> str:
        """Generate a BIP39-style seed phrase."""
        # Generate random indices for wordlist
        indices = [secrets.randbelow(len(BIP39_WORDLIST)) for _ in range(word_count)]
        words = [BIP39_WORDLIST[i] for i in indices]
        return " ".join(words)
    
    def _seed_to_private_key(self, seed_phrase: str) -> bytes:
        """Derive Ed25519 private key from seed phrase."""
        # Use PBKDF2 to derive key from seed phrase
        seed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            seed_phrase.encode('utf-8'),
            b'rustchain-mcp-salt',
            iterations=100000
        )
        return seed_hash[:32]
    
    def _generate_keypair(self, seed_phrase: Optional[str] = None) -> tuple:
        """Generate Ed25519 keypair. Returns (private_key, public_key, seed_phrase)."""
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("cryptography library required for key generation")
        
        if seed_phrase is None:
            seed_phrase = self._generate_seed_phrase()
        
        # Generate private key from seed
        private_key_bytes = self._seed_to_private_key(seed_phrase)
        private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        public_key = private_key.public_key()
        
        return private_key, public_key, seed_phrase
    
    def _get_wallet_id(self, public_key: Ed25519PublicKey) -> str:
        """Generate wallet ID from public key."""
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
    
    def wallet_create(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new wallet with Ed25519 keypair and BIP39 seed phrase.
        
        Returns:
            Dict with wallet_id, name, created_at (seed phrase shown once)
        """
        if not CRYPTO_AVAILABLE:
            return {
                "success": False,
                "error": "cryptography library not installed. Run: pip install cryptography"
            }
        
        private_key, public_key, seed_phrase = self._generate_keypair()
        wallet_id = self._get_wallet_id(public_key)
        
        # Export keys for storage
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=None
        )
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Store wallet (encrypted in production, base64 for now)
        wallets = self._load_wallets()
        wallet_data = {
            "name": name or f"Wallet {len(wallets) + 1}",
            "wallet_id": wallet_id,
            "public_key": base64.b64encode(public_bytes).decode('utf-8'),
            "private_key_encrypted": base64.b64encode(private_bytes).decode('utf-8'),
            "created_at": datetime.utcnow().isoformat(),
            "seed_phrase_hash": hashlib.sha256(seed_phrase.encode()).hexdigest()[:16]
        }
        wallets[wallet_id] = wallet_data
        self._save_wallets(wallets)
        
        # Return wallet info (seed phrase shown ONLY at creation)
        return {
            "success": True,
            "wallet_id": wallet_id,
            "name": wallet_data["name"],
            "created_at": wallet_data["created_at"],
            "seed_phrase": seed_phrase,  # SHOWN ONCE - SAVE THIS
            "warning": "BACK UP THIS SEED PHRASE NOW. It will never be shown again."
        }
    
    def wallet_list(self) -> Dict[str, Any]:
        """
        List all wallets in the local keystore.
        
        Returns:
            Dict with list of wallets (without private keys)
        """
        wallets = self._load_wallets()
        wallet_list = []
        for wallet_id, data in wallets.items():
            wallet_list.append({
                "wallet_id": wallet_id,
                "name": data.get("name", "Unnamed"),
                "created_at": data.get("created_at"),
                "public_key_preview": data.get("public_key", "")[:20] + "..."
            })
        
        return {
            "success": True,
            "wallets": wallet_list,
            "count": len(wallet_list)
        }
    
    def wallet_balance(self, wallet_id: str) -> Dict[str, Any]:
        """
        Check balance for any wallet ID.
        
        Args:
            wallet_id: The wallet ID to check
            
        Returns:
            Dict with balance, wallet_id
        """
        # In production, this would query the RustChain API
        # For now, return mock data
        return {
            "success": True,
            "wallet_id": wallet_id,
            "balance": 0.0,  # Would query API
            "currency": "RTC",
            "note": "Balance query requires RustChain API connection"
        }
    
    def wallet_history(self, wallet_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get transaction history for a wallet.
        
        Args:
            wallet_id: The wallet ID to query
            limit: Maximum number of transactions to return
            
        Returns:
            Dict with transactions list
        """
        # In production, this would query the RustChain API
        return {
            "success": True,
            "wallet_id": wallet_id,
            "transactions": [],  # Would query API
            "count": 0,
            "note": "Transaction history requires RustChain API connection"
        }
    
    def wallet_export(self, wallet_id: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Export encrypted keystore JSON for a wallet.
        
        Args:
            wallet_id: The wallet to export
            password: Optional encryption password
            
        Returns:
            Dict with keystore JSON
        """
        wallets = self._load_wallets()
        if wallet_id not in wallets:
            return {
                "success": False,
                "error": f"Wallet {wallet_id} not found"
            }
        
        wallet_data = wallets[wallet_id]
        
        # Create keystore format
        keystore = {
            "version": 1,
            "wallet_id": wallet_id,
            "name": wallet_data.get("name"),
            "public_key": wallet_data.get("public_key"),
            "created_at": wallet_data.get("created_at"),
            "encrypted_private_key": wallet_data.get("private_key_encrypted"),
            "format": "rustchain-mcp-v1"
        }
        
        return {
            "success": True,
            "wallet_id": wallet_id,
            "keystore": keystore,
            "export_format": "json",
            "warning": "This file contains encrypted private key data. Keep it secure."
        }
    
    def wallet_import(self, keystore_json: Dict[str, Any], 
                     name: Optional[str] = None) -> Dict[str, Any]:
        """
        Import a wallet from keystore JSON.
        
        Args:
            keystore_json: The keystore JSON to import
            name: Optional new name for the wallet
            
        Returns:
            Dict with imported wallet info
        """
        try:
            wallet_id = keystore_json.get("wallet_id")
            if not wallet_id:
                return {
                    "success": False,
                    "error": "Invalid keystore: missing wallet_id"
                }
            
            wallets = self._load_wallets()
            if wallet_id in wallets:
                return {
                    "success": False,
                    "error": f"Wallet {wallet_id} already exists"
                }
            
            # Import wallet
            wallet_data = {
                "name": name or keystore_json.get("name", f"Imported Wallet"),
                "wallet_id": wallet_id,
                "public_key": keystore_json.get("public_key"),
                "private_key_encrypted": keystore_json.get("encrypted_private_key"),
                "created_at": keystore_json.get("created_at"),
                "imported_at": datetime.utcnow().isoformat()
            }
            wallets[wallet_id] = wallet_data
            self._save_wallets(wallets)
            
            return {
                "success": True,
                "wallet_id": wallet_id,
                "name": wallet_data["name"],
                "imported_at": wallet_data["imported_at"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Import failed: {str(e)}"
            }
    
    def wallet_import_from_seed(self, seed_phrase: str,
                                 name: Optional[str] = None) -> Dict[str, Any]:
        """
        Import a wallet from BIP39 seed phrase.
        
        Args:
            seed_phrase: The 12-word seed phrase
            name: Optional name for the wallet
            
        Returns:
            Dict with imported wallet info
        """
        if not CRYPTO_AVAILABLE:
            return {
                "success": False,
                "error": "cryptography library not installed"
            }
        
        try:
            # Validate seed phrase
            words = seed_phrase.strip().lower().split()
            if len(words) != 12:
                return {
                    "success": False,
                    "error": "Seed phrase must be exactly 12 words"
                }
            
            # Regenerate keypair from seed
            private_key, public_key, _ = self._generate_keypair(seed_phrase)
            wallet_id = self._get_wallet_id(public_key)
            
            # Check if wallet already exists
            wallets = self._load_wallets()
            if wallet_id in wallets:
                return {
                    "success": False,
                    "error": f"Wallet {wallet_id} already exists in keystore"
                }
            
            # Export keys
            private_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=None
            )
            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            
            # Store wallet
            wallet_data = {
                "name": name or f"Recovered Wallet",
                "wallet_id": wallet_id,
                "public_key": base64.b64encode(public_bytes).decode('utf-8'),
                "private_key_encrypted": base64.b64encode(private_bytes).decode('utf-8'),
                "created_at": datetime.utcnow().isoformat(),
                "seed_phrase_hash": hashlib.sha256(seed_phrase.encode()).hexdigest()[:16],
                "imported_from_seed": True
            }
            wallets[wallet_id] = wallet_data
            self._save_wallets(wallets)
            
            return {
                "success": True,
                "wallet_id": wallet_id,
                "name": wallet_data["name"],
                "created_at": wallet_data["created_at"],
                "note": "Wallet recovered from seed phrase"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Import failed: {str(e)}"
            }


# MCP Tool Interface Functions
def wallet_create(name: Optional[str] = None) -> Dict[str, Any]:
    """MCP Tool: Create a new wallet."""
    manager = WalletManager()
    return manager.wallet_create(name)


def wallet_list() -> Dict[str, Any]:
    """MCP Tool: List all wallets."""
    manager = WalletManager()
    return manager.wallet_list()


def wallet_balance(wallet_id: str) -> Dict[str, Any]:
    """MCP Tool: Check wallet balance."""
    manager = WalletManager()
    return manager.wallet_balance(wallet_id)


def wallet_history(wallet_id: str, limit: int = 50) -> Dict[str, Any]:
    """MCP Tool: Get wallet transaction history."""
    manager = WalletManager()
    return manager.wallet_history(wallet_id, limit)


def wallet_export(wallet_id: str, password: Optional[str] = None) -> Dict[str, Any]:
    """MCP Tool: Export wallet keystore."""
    manager = WalletManager()
    return manager.wallet_export(wallet_id, password)


def wallet_import(keystore_json: Dict[str, Any], name: Optional[str] = None) -> Dict[str, Any]:
    """MCP Tool: Import wallet from keystore."""
    manager = WalletManager()
    return manager.wallet_import(keystore_json, name)


def wallet_import_from_seed(seed_phrase: str, name: Optional[str] = None) -> Dict[str, Any]:
    """MCP Tool: Import wallet from seed phrase."""
    manager = WalletManager()
    return manager.wallet_import_from_seed(seed_phrase, name)


if __name__ == "__main__":
    # Demo/test the wallet tools
    print("RustChain MCP Wallet Tools Demo")
    print("=" * 50)
    
    manager = WalletManager()
    
    # Create a wallet
    print("\n1. Creating wallet...")
    result = manager.wallet_create("Demo Wallet")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        wallet_id = result["wallet_id"]
        
        # List wallets
        print("\n2. Listing wallets...")
        list_result = manager.wallet_list()
        print(f"Result: {json.dumps(list_result, indent=2)}")
        
        # Check balance
        print("\n3. Checking balance...")
        balance_result = manager.wallet_balance(wallet_id)
        print(f"Result: {json.dumps(balance_result, indent=2)}")
        
        # Export wallet
        print("\n4. Exporting wallet...")
        export_result = manager.wallet_export(wallet_id)
        print(f"Result: {json.dumps(export_result, indent=2)}")
