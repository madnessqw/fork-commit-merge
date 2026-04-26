import { ref, computed } from 'vue';
import { PrivacySDK, PrivacyConfig, DepositParams, WithdrawParams } from '@privacylayer/sdk';

interface Transaction {
  hash: string;
  type: 'deposit' | 'withdraw';
  amount: string;
  privacyLevel: string;
  timestamp: number;
  status: 'pending' | 'confirmed' | 'failed';
}

const sdk = ref<PrivacySDK | null>(null);
const balance = ref('0');
const isLoading = ref(false);
const error = ref<string | null>(null);
const transactions = ref<Transaction[]>([]);

export function usePrivacy() {
  const init = (config: PrivacyConfig) => {
    sdk.value = new PrivacySDK(config);
    refreshBalance();
  };

  const deposit = async (params: DepositParams): Promise<{ hash: string }> => {
    if (!sdk.value) throw new Error('SDK not initialized');
    
    isLoading.value = true;
    error.value = null;
    
    try {
      const result = await sdk.value.deposit(params);
      await refreshBalance();
      await refreshTransactions();
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Deposit failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const withdraw = async (params: WithdrawParams): Promise<{ hash: string }> => {
    if (!sdk.value) throw new Error('SDK not initialized');
    
    isLoading.value = true;
    error.value = null;
    
    try {
      const result = await sdk.value.withdraw(params);
      await refreshBalance();
      await refreshTransactions();
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Withdrawal failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const refreshBalance = async () => {
    if (!sdk.value) return;
    balance.value = await sdk.value.getBalance();
  };

  const refreshTransactions = async () => {
    if (!sdk.value) return;
    transactions.value = await sdk.value.getHistory();
  };

  return {
    init,
    deposit,
    withdraw,
    balance: computed(() => balance.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    transactions: computed(() => transactions.value),
    refreshBalance,
    refreshTransactions
  };
}
