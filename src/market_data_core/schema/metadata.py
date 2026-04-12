"""Dataset metadata model for canonical bar persistence."""

from __future__ import annotations

from dataclasses import dataclass

from market_data_core.core.constants import CANONICAL_TIMEZONE, CANONICAL_TIMESTAMP_ANCHOR


@dataclass(frozen=True)
class DatasetMetadata:
    dataset_id: str
    market: str
    frequency: str
    adjustment_mode: str
    provider: str
    schema_version: int = 1
    timezone: str = CANONICAL_TIMEZONE
    timestamp_anchor: str = CANONICAL_TIMESTAMP_ANCHOR
