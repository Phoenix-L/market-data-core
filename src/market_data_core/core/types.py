"""Typed dataclasses used across module boundaries."""

from dataclasses import dataclass
from .enums import AdjustmentMode, Frequency, Market


@dataclass(frozen=True)
class BarRequest:
    symbol: str
    start: str
    end: str
    frequency: Frequency
    market: Market = Market.CN_EQUITY
    adjustment: AdjustmentMode = AdjustmentMode.RAW


@dataclass(frozen=True)
class DatasetRef:
    dataset_id: str
    market: Market
    frequency: Frequency
    adjustment: AdjustmentMode = AdjustmentMode.RAW
