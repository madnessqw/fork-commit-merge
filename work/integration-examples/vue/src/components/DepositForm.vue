<template>
  <div class="p-6 bg-white rounded-lg shadow-md max-w-md">
    <h2 class="text-2xl font-bold mb-4">Private Deposit</h2>
    <div class="mb-4 text-sm text-gray-600">
      Balance: {{ balance }} ETH
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium mb-1">Amount (ETH)</label>
        <input
          v-model="amount"
          type="number"
          step="0.001"
          class="w-full px-3 py-2 border rounded-md"
          placeholder="0.1"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Privacy Level</label>
        <select
          v-model="privacyLevel"
          class="w-full px-3 py-2 border rounded-md"
        >
          <option value="low">Low (Fast, ~2s)</option>
          <option value="medium">Medium (Balanced, ~10s)</option>
          <option value="high">High (Maximum, ~30s)</option>
        </select>
      </div>

      <button
        type="submit"
        :disabled="isLoading || !amount"
        class="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isLoading ? 'Processing...' : 'Deposit Privately' }}
      </button>
    </form>

    <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-700 rounded">{{ error }}</div>
    <div v-if="success" class="mt-4 p-3 bg-green-100 text-green-700 rounded">{{ success }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { usePrivacy } from '../composables/usePrivacy';

const { deposit, balance, isLoading, error } = usePrivacy();

const amount = ref('');
const privacyLevel = ref<'low' | 'medium' | 'high'>('medium');
const success = ref<string | null>(null);

const handleSubmit = async () => {
  success.value = null;
  
  try {
    const result = await deposit({
      amount: amount.value,
      privacyLevel: privacyLevel.value,
      recipient: '0x...' // Get from wallet in real app
    });
    success.value = `Deposit successful! TX: ${result.hash.slice(0, 10)}...`;
    amount.value = '';
  } catch (err) {
    // Error handled by composable
  }
};
</script>
