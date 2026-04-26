#!/usr/bin/env python3
"""
PrivacyLayer Python SDK Example
Demonstrates deposit, withdrawal, balance checking, and transaction history.
"""

import os
import asyncio
from privacylayer import PrivacySDK, PrivacyConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Synchronous example"""
    # Initialize SDK
    config = PrivacyConfig(
        network=os.getenv('PRIVACYLAYER_NETWORK', 'testnet'),
        api_key=os.getenv('PRIVACYLAYER_API_KEY'),
        rpc_url=os.getenv('PRIVACYLAYER_RPC_URL'),
        default_privacy_level='medium'
    )
    
    sdk = PrivacySDK(config)
    print(f"Connected to {config.network}")
    
    # Check balance
    balance = sdk.get_balance()
    print(f"Private Balance: {balance} ETH")
    
    # Make a private deposit
    print("\nInitiating private deposit...")
    result = sdk.deposit(
        amount='0.1',
        privacy_level='high',
        recipient='0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
    )
    print(f"Deposit successful!")
    print(f"  Transaction Hash: {result.hash}")
    print(f"  Privacy Level: High (1000+ anonymity set)")
    print(f"  Estimated Confirmation: ~30 seconds")
    
    # Get transaction history
    print("\nTransaction History:")
    transactions = sdk.get_history(limit=5)
    for tx in transactions:
        status_emoji = '✅' if tx.status == 'confirmed' else '⏳' if tx.status == 'pending' else '❌'
        print(f"  {status_emoji} {tx.type.upper()}: {tx.amount} ETH "
              f"({tx.privacy_level} privacy) - {tx.hash[:12]}...")

async def async_example():
    """Asynchronous example"""
    config = PrivacyConfig(network='testnet')
    sdk = PrivacySDK(config)
    
    # Concurrent operations
    print("\nRunning concurrent operations...")
    
    tasks = [
        sdk.get_balance_async(),
        sdk.get_history_async(limit=3),
        # sdk.deposit_async(amount='0.05', privacy_level='low')  # Uncomment to test
    ]
    
    balance, history = await asyncio.gather(*tasks)
    
    print(f"Balance: {balance} ETH")
    print(f"Recent transactions: {len(history)}")

def batch_example():
    """Batch operations example"""
    from privacylayer import batch_deposit
    
    # Define batch recipients
    recipients = [
        {'address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb', 'amount': '0.05'},
        {'address': '0x8ba1f109551bD432803012645Hac136c82C3e8C', 'amount': '0.1'},
        {'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7', 'amount': '0.075'},
    ]
    
    print(f"\nProcessing batch deposit to {len(recipients)} recipients...")
    results = batch_deposit(
        recipients=recipients,
        privacy_level='medium'
    )
    
    successful = sum(1 for r in results if r.success)
    print(f"Batch complete: {successful}/{len(recipients)} successful")
    
    for result in results:
        status = '✅' if result.success else '❌'
        print(f"  {status} {result.recipient}: {result.hash or result.error}")

def analyze_privacy_levels():
    """Compare privacy levels"""
    sdk = PrivacySDK(network='testnet')
    
    print("\nPrivacy Level Comparison:")
    print("-" * 60)
    print(f"{'Level':<10} {'Anonymity Set':<15} {'Time':<10} {'Fee':<10}")
    print("-" * 60)
    
    levels = [
        ('Low', 10, '~2s', '0.1%'),
        ('Medium', 100, '~10s', '0.5%'),
        ('High', 1000, '~30s', '1.0%'),
    ]
    
    for level, anonymity, time, fee in levels:
        print(f"{level:<10} {anonymity:<15} {time:<10} {fee:<10}")
    
    print("-" * 60)
    print("Higher privacy = larger anonymity set = better protection")

if __name__ == '__main__':
    print("=" * 60)
    print("PrivacyLayer Python SDK Example")
    print("=" * 60)
    
    # Run synchronous examples
    main()
    analyze_privacy_levels()
    
    # Run async example
    asyncio.run(async_example())
    
    # Uncomment to test batch operations
    # batch_example()
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)
