"""Canonical bar schema constants.

Aligned with docs/canonical_bar_contract.md.
"""

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
