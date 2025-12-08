import type { ApiSuccess } from './api';

export interface WalletSource {
  source: string;
  type?: string;
  detail?: string;
  risk_level?: string;
  scam_category?: string;
  createdAt?: string;
  trusted?: boolean;
  score?: number;
}

export interface WalletSummary {
  address: string;
  networks: string[];
  risk_level?: string | null;
  risk_level_numeric: number;
  risk_score_numeric?: number | null;
  scam_categories: string[];
  domains: string[];
  first_seen?: string | null;
  last_seen?: string | null;
  sources: WalletSource[];
}

export interface WalletMetadata {
  description: string;
  version: string;
  date_generated: string;
  risk_categories: Record<string, string>;
  source_file: string;
  records: number;
  extracted_at: string;
}

export interface WalletVerifyResponseData {
  found: boolean;
  summary: WalletSummary | null;
  metadata: WalletMetadata;
}

export type WalletVerifyResponse = ApiSuccess<WalletVerifyResponseData>;
***