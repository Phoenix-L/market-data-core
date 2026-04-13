"""Minimal load_bars usage example with an in-process stub provider."""

from __future__ import annotations

import pandas as pd

from market_data_core.access import load_bars
from market_data_core.providers import DataProvider, register_provider, reset_provider


class ExampleProvider(DataProvider):
    name = "example"

    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del start_date, end_date
        return pd.DataFrame(
            {
                "symbol": [symbol],
                "timestamp": pd.to_datetime(["2026-01-05 09:30:00+08:00"]),
                "open": [10.0],
                "high": [10.2],
                "low": [9.8],
                "close": [10.1],
                "volume": [1000.0],
                "turnover_rate": [1.0],
            }
        )

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        return self.fetch_daily(symbol, start_date, end_date)


if __name__ == "__main__":
    reset_provider()
    register_provider("example", ExampleProvider)

    bars = load_bars(
        symbol="000001.SZ",
        start="2026-01-01",
        end="2026-01-31",
        frequency="1d",
        provider="example",
        use_cache=False,
    )
    print(bars)
