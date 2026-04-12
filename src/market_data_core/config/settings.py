"""Runtime settings scaffolding.

Owns only data-layer settings. Backtesting/runtime settings are out of scope.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class CoreSettings:
    """Minimal settings for early extraction waves."""

    market_data_root: str = os.getenv("MARKET_DATA_ROOT", ".data/market_data")
    default_provider: str = os.getenv("MARKET_DATA_PROVIDER", os.getenv("ASHARE_DATA_PROVIDER", "baostock"))
    timezone: str = "Asia/Shanghai"
