"""Quick script to exercise the wallet verification flow."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.wallet_checker.services.wallet_service import WalletService
from app.components.wallet_checker.usecases.dto.wallet_request_dto import WalletQueryDTO
from app.components.wallet_checker.usecases.verify_wallet_usecase import (
    WalletVerificationUseCase,
)
from app.config.settings import get_settings
from app.repositories.wallet_repository import WalletRepository


def build_use_case() -> WalletVerificationUseCase:
    settings = get_settings()
    repository = WalletRepository(settings.dataset_path)
    service = WalletService(repository, settings)
    return WalletVerificationUseCase(service)


def main() -> None:
    """Ejecuta una demo con wallets sanas y maliciosas."""

    use_case = build_use_case()
    sample_addresses = {
        "malicious_btc": "bc1qdc9gnr2tqfm78lqhxunapaw605qhkpsq36ysr6",
        "malicious_eth": "0x47ce0c6ac56edb84e2ad330bec0b500ad6e71bee",
        "benign_btc": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
        "benign_eth": "0x000000000000000000000000000000000000dead",
    }

    for label, address in sample_addresses.items():
        payload = WalletQueryDTO(address=address)
        result = use_case.execute(payload)
        print("\n== Resultado para", label, "==")
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
