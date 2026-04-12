"""Canonical bar schema constants and helpers.

Aligned with docs/canonical_bar_contract.md.
"""

from __future__ import annotations

from market_data_core.core.constants import CANONICAL_TIMEZONE, CANONICAL_TIMESTAMP_ANCHOR

REQUIRED_BAR_COLUMNS = (
    "symbol",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "turnover_rate",
)

OPTIONAL_BAR_COLUMNS = (
    "amount",
    "vwap",
    "trade_count",
    "provider",
    "frequency",
)

BAR_PRIMARY_KEY = ("symbol", "timestamp")
ALL_KNOWN_BAR_COLUMNS = REQUIRED_BAR_COLUMNS + OPTIONAL_BAR_COLUMNS

SCHEMA_VERSION = 1
TIMESTAMP_TIMEZONE = CANONICAL_TIMEZONE
TIMESTAMP_ANCHOR = CANONICAL_TIMESTAMP_ANCHOR
