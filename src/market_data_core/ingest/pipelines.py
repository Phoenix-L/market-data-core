"""Ingestion pipeline scaffold.

Expected flow: provider fetch -> clean/normalize -> validate -> persist.
"""

from .requests import IngestRequest


def ingest_bars(request: IngestRequest) -> dict[str, object]:
    """Placeholder ingest entrypoint aligned with public API draft."""
    raise NotImplementedError(f"Ingest pipeline not implemented yet for {request.symbol}.")
