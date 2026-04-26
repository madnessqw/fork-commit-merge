#!/usr/bin/env python3
"""
RustChain MCP Server Transfer Tools
Handles signed RTC transfers for the MCP wallet integration.

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
import requests

# Ed25519 for cryptographic operations
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey
    )
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class TransferManager:
    """Manages RTC transfers with Ed25519 signing."""
    
    def __init__(self, keystore_path: Optional[str] = None, 
                 api_endpoint: Optional[str] = None):
        """Initialize transfer manager."""
        if keystore_path is None:
            keystore_path = os.path.expanduser("~/.rustchain/mcp_wallets")
        self.keystore_path = Path(keystore_path)
        self.wallets_file = self.keystore_path / "wallets.json"
        
        # RustChain API endpoint
        self.api_endpoint = api_endpoint or os.getenv(
            "RUSTCHAIN_API", 
            "https://api.rustchain.org/v1"
        )
    
    def _load_wallets(self) -> Dict:
        """Load wallets from keystore."""
        try:
            with open(self.wallets_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _get_private_key(self, wallet_id: str) -> Optional[Ed25519PrivateKey]:
        """Load private key for a wallet."""
        if not CRYPTO_AVAILABLE:
            return None
        
        wallets = self._load_wallets()
        if wallet_id not in wallets:
            return None
        
        wallet_data = wallets[wallet_id]
        private_key_b64 = wallet_data.get("private_key_encrypted")
        if not private_key_b64:
            return None
        
        try:
            private_bytes = base64.b64decode(private_key_b64)
            return Ed25519PrivateKey.from_private_bytes(private_bytes)
        except Exception:
            return None
    
    def _sign_transfer(self, private_key: Ed25519PrivateKey,
                       recipient: str, amount: float,
                       nonce: int, timestamp: int) -> str:
        """Sign a transfer with Ed25519."""
        # Create transfer message
        message = json.dumps({
            "recipient": recipient,
            "amount": amount,
            "nonce": nonce,
            "timestamp": timestamp
        }, sort_keys=True)
        
        # Sign message
        signature = private_key.sign(message.encode('utf-8'))
        return base64.b64encode(signature).decode('utf-8')
    
    def wallet_transfer_signed(self, wallet_id: str, recipient: str,
                               amount: float, memo: Optional[str] = None) -> Dict[str, Any]:
        """
        Sign and submit an RTC transfer.
        
        Args:
            wallet_id: Source wallet ID
            recipient: Destination wallet ID
            amount: Amount of RTC to transfer
            memo: Optional memo
            
        Returns:
            Dict with transfer result
        """
        if not CRYPTO_AVAILABLE:
            return {
                "success": False,
                "error": "cryptography library not installed. Run: pip install cryptography"
            }
        
        # Validate inputs
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be greater than 0"
            }
        
        # Load private key
        private_key = self._get_private_key(wallet_id)
        if not private_key:
            return {
                "success": False,
                "error": f"Wallet {wallet_id} not found or private key unavailable"
            }
        
        # Get public key for sender identification
        public_key = private_key.public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        sender = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
        
        # Generate nonce and timestamp
        nonce = secrets.randbelow(2**32)
        timestamp = int(datetime.utcnow().timestamp())
        
        # Sign the transfer
        try:
            signature = self._sign_transfer(
                private_key, recipient, amount, nonce, timestamp
            )
        except Exception as e:
            return {
                "success": False,
                "error": f"Signing failed: {str(e)}"
            }
        
        # Build transfer payload
        transfer_payload = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "nonce": nonce,
            "timestamp": timestamp,
            "signature": signature,
            "memo": memo or ""
        }
        
        # Submit to RustChain API
        try:
            response = requests.post(
                f"{self.api_endpoint}/wallet/transfer/signed",
                json=transfer_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "transaction_id": result.get("transaction_id"),
                    "sender": sender,
                    "recipient": recipient,
                    "amount": amount,
                    "timestamp": timestamp,
                    "status": "pending",
                    "note": "Transfer submitted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code} - {response.text}",
                    "payload": transfer_payload
                }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "note": "Transfer signed but not submitted. Save payload for retry.",
                "signed_payload": transfer_payload
            }
    
    def prepare_transfer(self, wallet_id: str, recipient: str,
                         amount: float, memo: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepare a transfer without submitting (for offline signing).
        
        Args:
            wallet_id: Source wallet ID
            recipient: Destination wallet ID
            amount: Amount of RTC to transfer
            memo: Optional memo
            
        Returns:
            Dict with prepared transfer payload
        """
        if not CRYPTO_AVAILABLE:
            return {
                "success": False,
                "error": "cryptography library not installed"
            }
        
        # Load private key
        private_key = self._get_private_key(wallet_id)
        if not private_key:
            return {
                "success": False,
                "error": f"Wallet {wallet_id} not found"
            }
        
        # Get sender ID
        public_key = private_key.public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        sender = base64.urlsafe_b