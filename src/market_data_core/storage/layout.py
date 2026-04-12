"""Storage layout helpers aligned to docs/storage_layout.md."""

from pathlib import Path


def canonical_partition_path(root: Path, market: str, frequency: str, symbol: str, year: int) -> Path:
    """Build canonical partition path without performing I/O."""
    return root / "canonical" / f"market={market}" / f"freq={frequency}" / f"symbol={symbol}" / f"year={year}"
