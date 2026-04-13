"""Provider interface contract.

This module defines the provider boundary used by `market_data_core.access.load`.
Concrete adapters are intentionally deferred; consumers can register their own
providers via `market_data_core.providers.register_provider`.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


class DataProvider(ABC):
    """Provider contract for canonical bar fetches.

    Required output contract for both fetch methods:
    - Return a pandas ``DataFrame`` with required canonical columns:
      ``symbol, timestamp, open, high, low, close, volume, turnover_rate``.
    - ``timestamp`` values must be timezone-aware and aligned to Asia/Shanghai
      open-anchor semantics expected by ``validate_bars``.
    - Rows should be sorted in ascending ``timestamp`` order per symbol.
    - Missing provider data should be represented as empty frames or nullable
      optional fields; silent schema drift is not allowed.

    Error behavior:
    - Provider-level failures should raise explicit exceptions (for example
      ``ProviderError`` from ``market_data_core.core.exceptions``) rather than
      returning malformed frames.
    """

    name: str

    @abstractmethod
    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> "pd.DataFrame":
        """Fetch canonical 1d bars for ``symbol`` in the inclusive date range."""
        raise NotImplementedError

    @abstractmethod
    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> "pd.DataFrame":
        """Fetch canonical 30m bars for ``symbol`` in the inclusive date range."""
        raise NotImplementedError
