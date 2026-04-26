import React, { useState } from 'react';
import { usePrivacy } from '../hooks/usePrivacy';

export const DepositForm: React.FC = () => {
  const { deposit, balance, isLoading, error } = usePrivacy();
  const [amount, setAmount] = useState('');
  const [privacyLevel, setPrivacyLevel] = useState<'low' | 'medium' | 'high'>('medium');
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(null);
    
    try {
      const result = await deposit({
        amount,
        privacyLevel,
        recipient: await getRecipientAddress()
      });
      setSuccess(`Deposit successful! TX: ${result.hash.slice(0, 10)}...`);
      setAmount('');
    } catch (err) {
      // Error handled by hook
    }
  };

  const getRecipientAddress = async () => {
    // In real app, get from wallet or input
    return '0x...';
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md max-w-md">
      <h2 className="text-2xl font-bold mb-4">Private Deposit</h2>
      <div className="mb-4 text-sm text-gray-600">
        Balance: {balance} ETH
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Amount (ETH)</label>
          <input
            type="number"
            step="0.001"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="0.1"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Privacy Level</label>
          <select
            value={privacyLevel}
            onChange={(e) => setPrivacyLevel(e.target.value as 'low' | 'medium' | 'high')}
            className="w-full px-3 py-2 border rounded-md"
          >
            <option value="low">Low (Fast, ~2s)</option>
            <option value="medium">Medium (Balanced, ~10s)</option>
            <option value="high">High (Maximum, ~30s)</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={isLoading || !amount}
          className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Processing...' : 'Deposit Privately'}
        </button>
      </form>

      {error && <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      {success && <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">{success}</div>}
    </div>
  );
};
