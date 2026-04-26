# PrivacyLayer React Integration Example

A complete React application demonstrating PrivacyLayer SDK integration for private blockchain transactions.

## Features

- 🔒 Private deposit/withdrawal flows
- 🎛️ Customizable privacy levels
- 📊 Transaction history with privacy indicators
- 🔔 Real-time status notifications
- 🎨 Tailwind CSS styling

## Quick Start

```bash
# Clone and install
cd examples/react
npm install

# Start development server
npm run dev
```

## Usage

```tsx
import { PrivacyProvider, usePrivacy } from './hooks/usePrivacy';

function App() {
  return (
    <PrivacyProvider config={{ network: 'testnet' }}>
      <DepositForm />
    </PrivacyProvider>
  );
}

function DepositForm() {
  const { deposit, balance, isLoading } = usePrivacy();

  const handleDeposit = async (amount: string) => {
    const tx = await deposit({
      amount,
      privacyLevel: 'high',
      recipient: '0x...'
    });
    console.log('Transaction:', tx.hash);
  };

  return (
    <form onSubmit={(e) => handleDeposit(e.target.amount.value)}>
      <input name="amount" placeholder="Amount (ETH)" />
      <button disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Deposit Privately'}
      </button>
    </form>
  );
}
```

## Components

- `DepositForm` — Private deposit with amount/privacy selection
- `WithdrawForm` — Secure withdrawal to any address
- `TransactionList` — Privacy-aware transaction history
- `PrivacySlider` — Visual privacy level selector
- `StatusBadge` — Real-time transaction status

## Configuration

```typescript
interface PrivacyConfig {
  network: 'mainnet' | 'testnet' | 'localhost';
  rpcUrl?: string;
  apiKey?: string;
  defaultPrivacyLevel: 'low' | 'medium' | 'high';
}
```

## Privacy Levels

| Level | Anonymity Set | Verification Time | Use Case |
|-------|---------------|-------------------|----------|
| Low | 10 users | ~2s | Quick transfers |
| Medium | 100 users | ~10s | Standard payments |
| High | 1000+ users | ~30s | Maximum privacy |

## License

MIT - Part of PrivacyLayer SDK Examples
