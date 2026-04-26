# PrivacyLayer Python Integration Example

Python SDK integration for PrivacyLayer — ideal for data pipelines, automation, and backend services.

## Features

- 🐍 Pythonic API design
- 📊 Pandas integration for transaction analysis
- 🔧 Async/await support
- 🧪 Jupyter notebook examples

## Installation

```bash
cd examples/python
pip install -r requirements.txt
```

## Quick Start

```python
from privacylayer import PrivacySDK

# Initialize
sdk = PrivacySDK(
    network='testnet',
    api_key='your-api-key'
)

# Make private deposit
result = sdk.deposit(
    amount='0.5',
    privacy_level='high',
    recipient='0x...'
)
print(f"Transaction: {result.hash}")

# Check balance
balance = sdk.get_balance()
print(f"Balance: {balance} ETH")
```

## Async Usage

```python
import asyncio
from privacylayer import PrivacySDK

async def main():
    sdk = PrivacySDK(network='testnet')
    
    # Concurrent operations
    deposit_task = sdk.deposit_async(amount='1.0', privacy_level='medium')
    balance_task = sdk.get_balance_async()
    
    result, balance = await asyncio.gather(deposit_task, balance_task)
    print(f"Deposited: {result.hash}, Balance: {balance}")

asyncio.run(main())
```

## Jupyter Notebook

See `examples.ipynb` for interactive tutorials:
- Privacy level comparison
- Transaction pattern analysis
- Batch operations

## Scripts

### Batch Deposit
```python
from privacylayer import batch_deposit

recipients = [
    {'address': '0x...', 'amount': '0.1'},
    {'address': '0x...', 'amount': '0.2'},
]

results = batch_deposit(recipients, privacy_level='medium')
```

### Transaction Analysis
```python
import pandas as pd
from privacylayer import PrivacySDK

sdk = PrivacySDK()
txs = sdk.get_history()

df = pd.DataFrame(txs)
print(df.groupby('privacyLevel')['amount'].sum())
```

## Configuration

Environment variables:
```bash
export PRIVACYLAYER_NETWORK=testnet
export PRIVACYLAYER_API_KEY=your-key
export PRIVACYLAYER_RPC_URL=https://...
```

## License

MIT - Part of PrivacyLayer SDK Examples
