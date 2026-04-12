"""Enum definitions aligned to contract docs."""

from enum import Enum


class StrEnum(str, Enum):
    """Simple string enum base for Python 3.10 compatibility."""


class Market(StrEnum):
    CN_EQUITY = "cn_equity"


class Frequency(StrEnum):
    DAILY_1D = "1d"
    MIN_30 = "30m"


class AdjustmentMode(StrEnum):
    RAW = "raw"
    QFQ = "qfq"
    HFQ = "hfq"


class Provider(StrEnum):
    BAOSTOCK = "baostock"
    TUSHARE = "tushare"
