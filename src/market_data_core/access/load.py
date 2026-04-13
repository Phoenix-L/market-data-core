"""Stable load APIs (Phase 6) built on Cache Mode storage.

Important contract note:
- ``load_bars`` currently operates in **Cache Mode** only
  (`provider/symbol/frequency/start_end.parquet`).
- Canonical dataset partition loading is a future phase concern.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from market_data_core.core.exceptions import ContractError
from market_data_core.providers import get_provider
from market_data_core.storage.parquet_store import cache_exists, read_bars, write_bars
from market_data_core.validation import validate_bars

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def load_bars(
    symbol: str,
    start: str,
    end: str,
    frequency: str,
    adjustment: str = "raw",
    source_preference: str = "canonical",
    provider: str | None = None,
    use_cache: bool = True,
    data_root: str | None = None,
) -> "pd.DataFrame":
    """Load canonical bars for one symbol via provider + Cache Mode storage.

    Parameters ``adjustment`` and ``source_preference`` are retained for
    compatibility but are not active in Phase 6 behavior.
    """
    del adjustment, source_preference
    resolved_provider = get_provider(provider)
    provider_name = resolved_provider.name.lower()

    if use_cache and cache_exists(provider_name, symbol, frequency, start, end, data_root):
        df = read_bars(provider_name, symbol, frequency, start, end, data_root)
    else:
        if frequency == "1d":
            df = resolved_provider.fetch_daily(symbol=symbol, start_date=start, end_date=end)
        elif frequency == "30m":
            df = resolved_provider.fetch_minute30(symbol=symbol, start_date=start, end_date=end)
        else:
            raise ValueError(f"Unsupported frequency: {frequency}")
        if use_cache:
            write_bars(df, provider_name, symbol, frequency, start, end, data_root)

    report = validate_bars(df, frequency=frequency, strict=True)
    if not report.ok:
        raise ContractError(f"Loaded bars failed validation: {report.errors}")
    return df


def load_daily(*_: object, **kwargs: object) -> "pd.DataFrame":
    """Compatibility wrapper for ``load_bars(..., frequency='1d')``."""
    return load_bars(*_, frequency="1d", **kwargs)


def load_30m(*_: object, **kwargs: object) -> "pd.DataFrame":
    """Compatibility wrapper for ``load_bars(..., frequency='30m')``."""
    return load_bars(*_, frequency="30m", **kwargs)


def load_minute_30(*_: object, **kwargs: object) -> "pd.DataFrame":
    """Legacy compatibility alias retained for migration from aShare."""
    return load_30m(*_, **kwargs)
