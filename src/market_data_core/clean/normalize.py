"""Generic normalization helpers for canonical bar DataFrames."""

from __future__ import annotations

from typing import TYPE_CHECKING

from market_data_core.schema.bars import BAR_PRIMARY_KEY

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def _pd():
    import pandas as pd  # type: ignore

    return pd


def normalize_columns(df: "pd.DataFrame") -> "pd.DataFrame":
    out = df.copy()
    out.columns = [str(col).strip().lower() for col in out.columns]
    return out


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def normalize_timestamp_column(df: "pd.DataFrame", tz: str = "Asia/Shanghai") -> "pd.DataFrame":
    pd = _pd()
    out = df.copy()
    ts = pd.to_datetime(out["timestamp"])
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize(tz)
    else:
        ts = ts.dt.tz_convert(tz)
    out["timestamp"] = ts
    return out


def sort_by_key(df: "pd.DataFrame") -> "pd.DataFrame":
    return df.sort_values(list(BAR_PRIMARY_KEY), kind="stable").reset_index(drop=True)
