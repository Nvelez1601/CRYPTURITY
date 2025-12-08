"""Service layer for wallet risk verification."""
from __future__ import annotations

from typing import Any, Dict, Optional

from app.config.settings import Settings
from app.repositories.wallet_repository import WalletRepository


class WalletService:
    """Encapsulates wallet risk business logic."""

    def __init__(self, repository: WalletRepository, settings: Settings):
        self._repository = repository
        self._settings = settings
        self._risk_scale = settings.risk_level_scale

    def get_metadata(self) -> Dict[str, Any]:
        return self._repository.get_metadata()

    def fetch_wallet_summary(self, address: str) -> Optional[Dict[str, Any]]:
        wallet = self._repository.get_wallet(address)
        if wallet is None:
            return None
        canonical_address = wallet.get("address", address)
        risk_level = wallet.get("risk_level")
        risk_score = wallet.get("risk_score")

        risk_level_numeric = self._risk_scale.get(risk_level or "BAJO", 0)
        risk_score_numeric: Optional[int] = None
        if isinstance(risk_score, (int, float)):
            risk_score_numeric = int(round(risk_score * 100))

        summary: Dict[str, Any] = {
            "address": canonical_address,
            "networks": sorted(wallet.get("networks", [])),
            "risk_level": risk_level,
            "risk_level_numeric": risk_level_numeric,
            "risk_score_numeric": risk_score_numeric,
            "scam_categories": sorted(wallet.get("scam_categories", [])),
            "domains": sorted(wallet.get("domains", [])),
            "first_seen": wallet.get("first_seen"),
            "last_seen": wallet.get("last_seen"),
            "sources": wallet.get("sources", []),
        }

        return summary
