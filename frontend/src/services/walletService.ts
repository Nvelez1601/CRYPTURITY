import { apiClient } from './apiClient';
import type {
  WalletMetadata,
  WalletVerifyResponse,
  WalletVerifyResponseData
} from '@/types/wallet';
import type { ApiSuccess } from '@/types/api';

const API_PREFIX = import.meta.env.VITE_API_PREFIX ?? '/api/v1';

export const walletService = {
  async verifyWallet(address: string): Promise<WalletVerifyResponseData> {
    const { data } = await apiClient.post<WalletVerifyResponse>(`${API_PREFIX}/wallets/verify`, {
      address
    });

    if (!data?.data) {
      throw new Error('Respuesta inválida del API');
    }

    return data.data;
  },

  async fetchMetadata(): Promise<WalletMetadata | null> {
    const { data } = await apiClient.get<ApiSuccess<WalletMetadata>>(
      `${API_PREFIX}/wallets/metadata`
    );
    return data?.data ?? null;
  }
};
