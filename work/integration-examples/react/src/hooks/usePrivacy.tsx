import React, { createContext, useContext, useState, useCallback } from 'react';
import { PrivacySDK, PrivacyConfig, DepositParams, WithdrawParams } from '@privacylayer/sdk';

interface PrivacyContextType {
  sdk: PrivacySDK | null;
  balance: string;
  isLoading: boolean;
  error: string | null;
  deposit: (params: DepositParams) => Promise<{ hash: string }>;
  withdraw: (params: WithdrawParams) => Promise<{ hash: string }>;
  getTransactionHistory: () => Promise<Transaction[]>;
}

interface Transaction {
  hash: string;
  type: 'deposit' | 'withdraw';
  amount: string;
  privacyLevel: string;
  timestamp: number;
  status: 'pending' | 'confirmed' | 'failed';
}

const PrivacyContext = createContext<PrivacyContextType | null>(null);

export const PrivacyProvider: React.FC<{ config: PrivacyConfig; children: React.ReactNode }> = ({ config, children }) => {
  const [sdk] = useState(() => new PrivacySDK(config));
  const [balance, setBalance] = useState('0');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deposit = useCallback(async (params: DepositParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await sdk.deposit(params);
      await refreshBalance();
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Deposit failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [sdk]);

  const withdraw = useCallback(async (params: WithdrawParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await sdk.withdraw(params);
      await refreshBalance();
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Withdrawal failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [sdk]);

  const getTransactionHistory = useCallback(async () => {
    return await sdk.getHistory();
  }, [sdk]);

  const refreshBalance = async () => {
    const bal = await sdk.getBalance();
    setBalance(bal);
  };

  return (
    <PrivacyContext.Provider value={{ sdk, balance, isLoading, error, deposit, withdraw, getTransactionHistory }}>
      {children}
    </PrivacyContext.Provider>
  );
};

export const usePrivacy = () => {
  const context = useContext(PrivacyContext);
  if (!context) throw new Error('usePrivacy must be used within PrivacyProvider');
  return context;
};
