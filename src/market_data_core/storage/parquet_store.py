"""Minimal Parquet-backed storage for canonical bars."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from market_data_core.core.exceptions import NotReadyError

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def _pd():
    try:
        import pandas as pd  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise NotReadyError("pandas is required for storage read/write") from exc
    return pd


def resolve_data_root(data_root: str | None = None) -> Path:
    if data_root:
        return Path(data_root)
    env_root = os.getenv("MARKET_DATA_ROOT") or os.getenv("ASHARE_CACHE_DIR")
    return Path(env_root) if env_root else Path(".data/market_data")


def cache_file_path(provider: str, symbol: str, frequency: str, start: str, end: str, data_root: str | None = None) -> Path:
    return resolve_data_root(data_root) / provider / symbol / frequency / f"{start}_{end}.parquet"


def cache_exists(provider: str, symbol: str, frequency: str, start: str, end: str, data_root: str | None = None) -> bool:
    return cache_file_path(provider, symbol, frequency, start, end, data_root).exists()


def read_bars(provider: str, symbol: str, frequency: str, start: str, end: str, data_root: str | None = None) -> "pd.DataFrame":
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
    path = cache_file_path(provider, symbol, frequency, start, end, data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(path, index=False)
    except ImportError as exc:  # pragma: no cover
        raise NotReadyError("Parquet support requires pyarrow or fastparquet") from exc
    return path
