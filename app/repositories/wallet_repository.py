"""Repository responsible for wallet risk lookups."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from app.bases.base_repository import BaseRepository


class WalletRepository(BaseRepository):
    """Access wallet risk data stored in a JSON dataset."""

    def __init__(self, dataset_path: Path):
        super().__init__(dataset_path)
        self._metadata: Dict[str, Any] = {}
        self._wallets: Dict[str, Any] = {}
        self._address_index: Dict[str, str] = {}

    def _read_dataset(self) -> Dict[str, Any]:
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"El dataset no existe en la ruta esperada: {self.dataset_path}"
            )
        data = json.loads(self.dataset_path.read_text(encoding="utf-8"))
        self._metadata = data.get("metadata", {})
        self._wallets = data.get("wallets", {})
        self._address_index = {}
        for address in self._wallets.keys():
            self._address_index[address] = address
            if address.lower().startswith("0x"):
                self._address_index[address.lower()] = address
        return data

    def get_metadata(self) -> Dict[str, Any]:
        self.load_dataset()
        return self._metadata

    def get_wallet(self, address: str) -> Optional[Dict[str, Any]]:
        self.load_dataset()
        normalized = address.strip()
        candidate_key = self._address_index.get(normalized)
        if candidate_key is None and normalized.lower().startswith("0x"):
            candidate_key = self._address_index.get(normalized.lower())
        if candidate_key is None:
            return None
        wallet_data = self._wallets.get(candidate_key)
        if wallet_data is None:
            return None
        enriched = dict(wallet_data)
        enriched.setdefault("address", candidate_key)
        return enriched

    def wallet_exists(self, address: str) -> bool:
        return self.get_wallet(address) is not None

    def list_wallets(self) -> Dict[str, Any]:
        self.load_dataset()
        return {
            address: {**data, "address": address}
            for address, data in self._wallets.items()
        }
