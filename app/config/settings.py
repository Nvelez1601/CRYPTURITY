"""Application settings and configuration helpers."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/"):
            return f"/{value}"
        return value.rstrip("/") or "/"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        return value.upper()

    @field_validator("dataset_path", mode="before")
    @classmethod
    def validate_dataset_path(cls, value: Path | str) -> Path:
        if isinstance(value, Path):
            return value.expanduser()
        return Path(value).expanduser()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
