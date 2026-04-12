"""Contract helpers.

TODO(phase2): move strict validation engine from placeholder checks in validation/.
"""

from dataclasses import dataclass
from .bars import REQUIRED_BAR_COLUMNS


@dataclass(frozen=True)
class BarContract:
    required_columns: tuple[str, ...] = REQUIRED_BAR_COLUMNS
    timestamp_anchor: str = "open"
    timezone: str = "Asia/Shanghai"
