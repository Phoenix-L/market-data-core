"""Minimal validate_bars usage example."""

from __future__ import annotations

import pandas as pd

from market_data_core.validation import validate_bars


if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "symbol": ["000001.SZ"],
            "timestamp": pd.to_datetime(["2026-01-05 09:30:00+08:00"]),
            "open": [10.0],
            "high": [10.2],
            "low": [9.8],
            "close": [10.1],
            "volume": [1000.0],
            "turnover_rate": [1.0],
        }
    )

    report = validate_bars(df, frequency="1d", strict=True)
    print(report)
