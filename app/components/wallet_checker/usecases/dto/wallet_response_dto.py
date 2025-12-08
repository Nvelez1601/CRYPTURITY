"""Wallet verification response DTOs."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class WalletSourceDTO(BaseModel):
    source: str
    type: Optional[str] = None
    detail: Optional[str] = None
    risk_level: Optional[str] = None
    scam_category: Optional[str] = None
    createdAt: Optional[str] = None
    trusted: Optional[bool] = None


class WalletRiskSummaryDTO(BaseModel):
    address: str
    networks: List[str]
    risk_level: Optional[str]
    risk_level_numeric: int
    risk_score_numeric: Optional[int] = None
    scam_categories: List[str]
    domains: List[str]
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    sources: List[WalletSourceDTO]


class WalletVerificationResponseDTO(BaseModel):
    found: bool
    summary: Optional[WalletRiskSummaryDTO] = None
    metadata: Dict[str, Any]
