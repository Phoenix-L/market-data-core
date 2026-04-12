"""Typed ingest request models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IngestRequest:
    symbol: str
    start: str
    end: str
    frequency: str
    provider: str | None = None
