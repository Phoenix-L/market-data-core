"""Duplicate-key handling policies for (symbol, timestamp)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from market_data_core.schema.bars import BAR_PRIMARY_KEY

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def drop_duplicate_keys(df: "pd.DataFrame", keep: str = "last") -> "pd.DataFrame":
    return df.drop_duplicates(subset=list(BAR_PRIMARY_KEY), keep=keep).reset_index(drop=True)


def duplicate_key_count(df: "pd.DataFrame") -> int:
    return int(df.duplicated(subset=list(BAR_PRIMARY_KEY), keep=False).sum())
