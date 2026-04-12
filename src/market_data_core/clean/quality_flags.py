"""Quality flag semantics for diagnostics and manifests."""

from __future__ import annotations

MISSING_REQUIRED_COLUMNS = "missing_required_columns"
DUPLICATE_PRIMARY_KEY = "duplicate_primary_key"
NON_MONOTONIC_TIMESTAMP = "non_monotonic_timestamp"
INVALID_OHLC = "invalid_ohlc_invariant"
NEGATIVE_VOLUME = "negative_volume"
NEGATIVE_TURNOVER_RATE = "negative_turnover_rate"
