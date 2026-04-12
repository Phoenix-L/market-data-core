"""Calendar alignment checks for canonical bars."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from .sessions import coerce_shanghai_timestamp, is_session_aligned, session_open_anchors


def check_session_alignment(timestamps: list[datetime], frequency: str) -> list[str]:
    """Validate that each timestamp is on the CN A-share open-anchor grid."""
    misaligned = [ts for ts in timestamps if not is_session_aligned(ts, frequency)]
    if not misaligned:
        return []
    return [f"session_misaligned_timestamps: {len(misaligned)}"]


def check_missing_30m_bars(timestamps: list[datetime]) -> list[str]:
    """Flag missing 30m anchors per day (best-effort without holiday source)."""
    by_day: dict[date, set[datetime]] = defaultdict(set)
    for ts in timestamps:
        norm = coerce_shanghai_timestamp(ts)
        by_day[norm.date()].add(norm)

    missing_total = 0
    for day, day_ts in by_day.items():
        expected = set(session_open_anchors(day, "30m"))
        missing_total += len(expected - day_ts)

    if missing_total == 0:
        return []
    return [f"missing_30m_session_anchors: {missing_total}"]
