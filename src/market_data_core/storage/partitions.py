"""Partition planning helpers."""

from __future__ import annotations

from datetime import datetime


def partition_years(start: str, end: str) -> list[int]:
    """Return inclusive year partitions for ISO-like date inputs."""
    start_year = datetime.fromisoformat(start).year
    end_year = datetime.fromisoformat(end).year
    if end_year < start_year:
        raise ValueError("end must be >= start")
    return list(range(start_year, end_year + 1))
