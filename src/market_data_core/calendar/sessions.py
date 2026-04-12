"""CN A-share session anchor utilities.

Public helpers in this module are stable for consumer repos.
"""

from __future__ import annotations

from datetime import date, datetime, time
from zoneinfo import ZoneInfo

ASIA_SHANGHAI = ZoneInfo("Asia/Shanghai")
CN_A_30M_OPEN_ANCHORS: tuple[time, ...] = (
    time(9, 30),
    time(10, 0),
    time(10, 30),
    time(11, 0),
    time(13, 0),
    time(13, 30),
    time(14, 0),
    time(14, 30),
)
CN_A_DAILY_OPEN_ANCHOR: time = time(9, 30)


def coerce_shanghai_timestamp(value: datetime) -> datetime:
    """Return timezone-aware timestamp normalized to Asia/Shanghai."""
    if value.tzinfo is None:
        return value.replace(tzinfo=ASIA_SHANGHAI)
    return value.astimezone(ASIA_SHANGHAI)


def session_open_anchors(trading_day: date, frequency: str) -> tuple[datetime, ...]:
    """Return canonical bar-open anchors for one CN A-share trading day."""
    if frequency == "1d":
        return (datetime.combine(trading_day, CN_A_DAILY_OPEN_ANCHOR, tzinfo=ASIA_SHANGHAI),)
    if frequency == "30m":
        return tuple(datetime.combine(trading_day, t, tzinfo=ASIA_SHANGHAI) for t in CN_A_30M_OPEN_ANCHORS)
    raise ValueError(f"Unsupported frequency for CN A-share sessions: {frequency}")


def is_session_aligned(value: datetime, frequency: str) -> bool:
    """Check whether timestamp lies on canonical open anchor grid."""
    ts = coerce_shanghai_timestamp(value)
    if frequency == "1d":
        return ts.timetz().replace(tzinfo=None) == CN_A_DAILY_OPEN_ANCHOR
    if frequency == "30m":
        return ts.timetz().replace(tzinfo=None) in CN_A_30M_OPEN_ANCHORS
    raise ValueError(f"Unsupported frequency for CN A-share sessions: {frequency}")
