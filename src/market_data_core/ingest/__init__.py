"""Ingest surface (deferred).

`ingest_bars` is intentionally not implemented in Phase 6 and remains outside
stable consumer guarantees.
"""

from .requests import IngestRequest
from .pipelines import ingest_bars

__all__ = ["IngestRequest", "ingest_bars"]
