"""Parquet-backed storage helpers for the active Cache Mode.

Active mode (Phase 6):
- cache path layout:
  ``<data_root>/<cache_contract_version>/<provider>/<symbol>/<frequency>/<start>_<end>.parquet``

Future mode (Phase 7+):
- canonical dataset partition + manifest model for direct loading.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from market_data_core.core.exceptions import NotReadyError
from market_data_core.storage.constants import CACHE_CONTRACT_VERSION

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def _pd():
    try:
        import pandas as pd  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise NotReadyError("pandas is required for storage read/write") from exc
    return pd


def resolve_data_root(data_root: str | None = None) -> Path:
    """Resolve data root with env compatibility fallback."""
    if data_root:
        return Path(data_root)
    env_root = os.getenv("MARKET_DATA_ROOT") or os.getenv("ASHARE_CACHE_DIR")
    return Path(env_root) if env_root else Path(".data/market_data")


def cache_file_path(provider: str, symbol: str, frequency: str, start: str, end: str, data_root: str | None = None) -> Path:
    """Return Cache Mode parquet path for one provider/symbol/range slice."""
    return resolve_data_root(data_root) / CACHE_CONTRACT_VERSION / provider / symbol / frequency / f"{start}_{end}.parquet"


def cache_exists(provider: str, symbol: str, frequency: str, start: str, end: str, data_root: str | None = None) -> bool:
    """Check whether a Cache Mode parquet artifact already exists."""
    return cache_file_path(provider, symbol, frequency, start, end, data_root).exists()


def read_bars(provider: str, symbol: str, frequency: str, start: str, end: str, data_root: str | None = None) -> "pd.DataFrame":
    """Read bars from Cache Mode parquet path."""
    pd = _pd()
    path = cache_file_path(provider, symbol, frequency, start, end, data_root)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def write_bars(
    df: "pd.DataFrame",
    provider: str,
    symbol: str,
    frequency: str,
    start: str,
    end: str,
    data_root: str | None = None,
) -> Path:
    """Write bars to Cache Mode parquet path."""
    path = cache_file_path(provider, symbol, frequency, start, end, data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(path, index=False)
    except ImportError as exc:  # pragma: no cover
        raise NotReadyError("Parquet support requires pyarrow or fastparquet") from exc
    return path
