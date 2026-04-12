"""Data invariant checks for canonical bar frames."""

from __future__ import annotations

from typing import TYPE_CHECKING

from market_data_core.clean.quality_flags import INVALID_OHLC, NEGATIVE_TURNOVER_RATE, NEGATIVE_VOLUME

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def check_ohlc_invariants(df: "pd.DataFrame") -> list[str]:
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        return []
    bad = (
        (df["low"] > df[["open", "close"]].min(axis=1))
        | (df["high"] < df[["open", "close"]].max(axis=1))
        | (df["high"] < df["low"])
    )
    bad_count = int(bad.sum())
    return [] if bad_count == 0 else [f"{INVALID_OHLC}: {bad_count}"]


def check_non_negative_volume(df: "pd.DataFrame") -> list[str]:
    if "volume" not in df.columns:
        return []
    bad_count = int((df["volume"] < 0).sum())
    return [] if bad_count == 0 else [f"{NEGATIVE_VOLUME}: {bad_count}"]


def check_non_negative_turnover_rate(df: "pd.DataFrame") -> list[str]:
    if "turnover_rate" not in df.columns:
        return []
    non_null = df["turnover_rate"].dropna()
    bad_count = int((non_null < 0).sum())
    return [] if bad_count == 0 else [f"{NEGATIVE_TURNOVER_RATE}: {bad_count}"]


def check_timestamp_order(df: "pd.DataFrame") -> list[str]:
    if not {"symbol", "timestamp"}.issubset(df.columns):
        return []
    sorted_df = df.sort_values(["symbol", "timestamp"], kind="stable")
    return [] if sorted_df.index.equals(df.index) else ["non_monotonic_timestamp"]
