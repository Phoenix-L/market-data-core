"""Schema-level validation checks for canonical bars."""

from __future__ import annotations

from typing import TYPE_CHECKING

from market_data_core.clean.dedupe import duplicate_key_count
from market_data_core.clean.quality_flags import DUPLICATE_PRIMARY_KEY, MISSING_REQUIRED_COLUMNS, NON_MONOTONIC_TIMESTAMP
from market_data_core.schema.bars import REQUIRED_BAR_COLUMNS

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def check_required_columns(df: "pd.DataFrame") -> list[str]:
    missing = [col for col in REQUIRED_BAR_COLUMNS if col not in df.columns]
    return [] if not missing else [f"{MISSING_REQUIRED_COLUMNS}: {', '.join(missing)}"]


def check_duplicate_keys(df: "pd.DataFrame") -> list[str]:
    dupes = duplicate_key_count(df)
    return [] if dupes == 0 else [f"{DUPLICATE_PRIMARY_KEY}: {dupes}"]


def check_monotonic_timestamp(df: "pd.DataFrame") -> list[str]:
    if not {"symbol", "timestamp"}.issubset(df.columns):
        return []
    for _, part in df.groupby("symbol", sort=False):
        if not part["timestamp"].is_monotonic_increasing:
            return [NON_MONOTONIC_TIMESTAMP]
    return []
