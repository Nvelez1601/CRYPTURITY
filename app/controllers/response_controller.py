"""Helpers to build consistent API responses."""
from __future__ import annotations

from typing import Any, Dict, Optional


class ResponseController:
    """Factory class to standardise API responses."""

    @staticmethod
    def success(message: str, data: Any) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": message,
            "data": data,
        }

    @staticmethod
    def failure(message: str, errors: Optional[Any] = None) -> Dict[str, Any]:
        response: Dict[str, Any] = {
            "status": "error",
            "message": message,
        }
        if errors is not None:
            response["errors"] = errors
        return response
