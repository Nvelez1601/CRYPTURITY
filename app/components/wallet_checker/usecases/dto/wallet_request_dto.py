"""Wallet verification request DTO."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WalletQueryDTO(BaseModel):
    """Incoming payload to request wallet verification."""

    address: str = Field(..., min_length=4, description="Dirección de la wallet a evaluar")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "address": "0x47ce0c6ac56edb84e2ad330bec0b500ad6e71bee",
            }
        },
    )
