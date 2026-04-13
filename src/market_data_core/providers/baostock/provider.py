"""Concrete BaoStock provider implementation for Phase 6.5."""

from __future__ import annotations

from typing import Any

from market_data_core.providers.base import DataProvider

from .fetch import fetch_daily_payload, fetch_minute30_payload
from .mapper import map_to_canonical


class BaoStockProvider(DataProvider):
    """BaoStock adapter implementing the stable provider contract."""

    name = "baostock"

    def __init__(self, client_factory: Any = None):
        self._client_factory = client_factory

    def fetch_daily(self, symbol: str, start_date: str, end_date: str):
        kwargs = {"symbol": symbol, "start_date": start_date, "end_date": end_date}
        if self._client_factory is not None:
            kwargs["client_factory"] = self._client_factory
        payload = fetch_daily_payload(**kwargs)
        return map_to_canonical(payload, symbol=symbol, frequency="1d")

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str):
        kwargs = {"symbol": symbol, "start_date": start_date, "end_date": end_date}
        if self._client_factory is not None:
            kwargs["client_factory"] = self._client_factory
        payload = fetch_minute30_payload(**kwargs)
        return map_to_canonical(payload, symbol=symbol, frequency="30m")
