"""Use case for verifying a wallet risk profile."""
from __future__ import annotations

from typing import Optional

from app.components.wallet_checker.services.wallet_service import WalletService
from app.components.wallet_checker.usecases.dto.wallet_request_dto import WalletQueryDTO
from app.components.wallet_checker.usecases.dto.wallet_response_dto import (
    WalletRiskSummaryDTO,
    WalletVerificationResponseDTO,
)


class WalletVerificationUseCase:
    """Coordinate the wallet verification workflow."""

    def __init__(self, service: WalletService):
        self._service = service

    def execute(self, payload: WalletQueryDTO) -> WalletVerificationResponseDTO:
        summary_data = self._service.fetch_wallet_summary(payload.address)
        metadata = self._service.get_metadata()

        if summary_data is None:
            return WalletVerificationResponseDTO(found=False, summary=None, metadata=metadata)

        summary_dto = WalletRiskSummaryDTO(**summary_data)
        return WalletVerificationResponseDTO(found=True, summary=summary_dto, metadata=metadata)

    def metadata(self) -> dict:
        """Expose dataset metadata to the outside world."""

        return self._service.get_metadata()
