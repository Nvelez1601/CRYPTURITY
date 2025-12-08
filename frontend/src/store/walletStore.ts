import { defineStore } from 'pinia';
import { ref } from 'vue';
import { walletService } from '@/services/walletService';
import type { WalletMetadata, WalletSummary } from '@/types/wallet';

export const useWalletStore = defineStore('wallet', () => {
  const summary = ref<WalletSummary | null>(null);
  const lastQuery = ref<string | null>(null);
  const metadata = ref<WalletMetadata | null>(null);
  const errorMessage = ref<string | null>(null);

  const loadMetadata = async () => {
    try {
      const data = await walletService.fetchMetadata();
      metadata.value = data;
    } catch (error) {
      console.error('No se pudo cargar metadata', error);
    }
  };

  const verifyWallet = async (address: string) => {
    errorMessage.value = null;
    try {
      const { found, summary: summaryData, metadata: payloadMetadata } =
        await walletService.verifyWallet(address);

      lastQuery.value = address;
      metadata.value = payloadMetadata;

      if (!found || !summaryData) {
        summary.value = null;
        errorMessage.value = 'Wallet no encontrada en el dataset.';
        return;
      }

      summary.value = summaryData;
    } catch (error) {
      console.error('Error verificando wallet', error);
      summary.value = null;
      errorMessage.value = 'No se pudo verificar la wallet. Intenta nuevamente.';
      throw error;
    }
  };

  return {
    summary,
    metadata,
    lastQuery,
    errorMessage,
    verifyWallet,
    loadMetadata
  };
});
