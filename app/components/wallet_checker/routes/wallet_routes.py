"""API routes for wallet verification."""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.config.settings import Settings, get_settings
from app.controllers.response_controller import ResponseController
from app.components.wallet_checker.services.wallet_service import WalletService
from app.components.wallet_checker.usecases.dto.wallet_request_dto import WalletQueryDTO
from app.components.wallet_checker.usecases.verify_wallet_usecase import (
    WalletVerificationUseCase,
)
from app.repositories.wallet_repository import WalletRepository

router = APIRouter(prefix="/wallets", tags=["Wallet Checker"])


@lru_cache(maxsize=1)
def _get_use_case_cached() -> WalletVerificationUseCase:
    settings = get_settings()
    repository = WalletRepository(settings.dataset_path)
    service = WalletService(repository, settings)
    return WalletVerificationUseCase(service)


def get_use_case(_: Settings = Depends(get_settings)) -> WalletVerificationUseCase:
    """FastAPI dependency to share the cached use case instance."""

    return _get_use_case_cached()


@router.post(
    "/verify",
    summary="Verifica una wallet y devuelve su diagnóstico",
)
async def verify_wallet(
    payload: WalletQueryDTO,
    use_case: WalletVerificationUseCase = Depends(get_use_case),
) -> Dict[str, Any]:
    """Return wallet diagnostic information if present in the dataset."""

    result = use_case.execute(payload)
    message = (
        "Wallet encontrada en el dataset de riesgo"
        if result.found
        else "Wallet no encontrada en el dataset"
    )
    return ResponseController.success(message, jsonable_encoder(result))


@router.get(
    "/metadata",
    summary="Obtiene información del dataset cargado",
)
async def dataset_metadata(
    use_case: WalletVerificationUseCase = Depends(get_use_case),
) -> Dict[str, Any]:
    """Expose dataset metadata for monitoring purposes."""

    metadata = use_case.metadata()
    return ResponseController.success("Metadata recuperada", metadata)
