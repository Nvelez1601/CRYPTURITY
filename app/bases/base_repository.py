"""Base repository definition to handle dataset loading."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class BaseRepository(ABC):
    """Abstract base repository with memoised dataset loading."""

    def __init__(self, dataset_path: Path):
        self._dataset_path = dataset_path
        self._dataset_cache: Optional[Dict[str, Any]] = None

    @property
    def dataset_path(self) -> Path:
        return self._dataset_path

    def load_dataset(self) -> Dict[str, Any]:
        if self._dataset_cache is None:
            self._dataset_cache = self._read_dataset()
        return self._dataset_cache

    @abstractmethod
    def _read_dataset(self) -> Dict[str, Any]:
        """Load the dataset from the underlying source."""

        raise NotImplementedError
