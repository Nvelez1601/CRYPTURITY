"""Application settings and configuration helpers."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Centralised application settings loaded from environment variables."""

    app_name: str = Field(default="Crypturity Wallet Risk API", alias="APP_NAME")
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")
    dataset_path: Path = Field(
        default=Path("app/repositories/data/wallet_risk_dataset.json"),
        alias="DATASET_PATH",
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    risk_level_scale: Dict[str, int] = Field(
        default_factory=lambda: {
            "BAJO": 25,
            "MEDIO": 50,
            "ALTO": 75,
            "CRÍTICO": 100,
        }
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("api_prefix")
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/"):
            return f"/{value}"
        return value.rstrip("/") or "/"

    @validator("log_level")
    def validate_log_level(cls, value: str) -> str:
        return value.upper()

    @validator("dataset_path")
    def validate_dataset_path(cls, value: Path) -> Path:
        return value.expanduser()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()  # type: ignore[arg-type]
