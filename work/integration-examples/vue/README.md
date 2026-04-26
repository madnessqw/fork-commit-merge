# PrivacyLayer Vue Integration Example

A Vue 3 composition API example for integrating PrivacyLayer SDK.

## Features

- 🔄 Reactive privacy state management
- 🎯 Composable functions for clean architecture
- 📱 Responsive design with Tailwind
- 🛡️ TypeScript support

## Quick Start

```bash
cd examples/vue
npm install
npm run dev
```

## Usage

```vue
<template>
  <div class="privacy-app">
    <DepositForm />
    <TransactionList />
  </div>
</template>

<script setup lang="ts">
import { usePrivacy } from './composables/usePrivacy';
import DepositForm from './components/DepositForm.vue';
import TransactionList from './components/TransactionList.vue';

const { init } = usePrivacy();

onMounted(() => {
  init({ network: 'testnet' });
});
</script>
```

## Composables

### usePrivacy
Main composable for SDK interaction:

```typescript
const { 
  deposit, 
  withdraw, 
  balance, 
  isLoading,
  transactions 
} = usePrivacy();
```

### usePrivacyLevel
Manage privacy preferences:

```typescript
const { level, setLevel, anonymitySet } = usePrivacyLevel();
```

## Components

- `DepositForm.vue` — Amount input with privacy selector
- `WithdrawForm.vue` — Secure withdrawal interface
- `TransactionList.vue` — History with privacy indicators
- `PrivacyBadge.vue` — Visual privacy level display

## License

MIT - Part of PrivacyLayer SDK Examples
