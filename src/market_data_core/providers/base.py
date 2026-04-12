"""Provider abstraction.

Concrete adapters must return canonical DataFrames per contract docs.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


class DataProvider(ABC):
    """Minimal provider contract for Phase 1 extraction."""

    name: str

    @abstractmethod
    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> "pd.DataFrame":
        raise NotImplementedError

    @abstractmethod
    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> "pd.DataFrame":
        raise NotImplementedError
