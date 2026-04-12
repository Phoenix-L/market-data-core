"""Storage layout helpers aligned to docs/storage_layout.md."""

from __future__ import annotations

from pathlib import Path


def canonical_partition_path(root: Path, market: str, frequency: str, symbol: str, year: int) -> Path:
    """Build canonical partition path without performing I/O."""
    return root / "canonical" / f"market={market}" / f"freq={frequency}" / f"symbol={symbol}" / f"year={year}"


def dataset_partition_path(
    root: Path,
    layer: str,
    market: str,
    frequency: str,
    symbol: str,
    year: int,
    adjustment: str = "raw",
) -> Path:
    """Build partition path for canonical/curated datasets."""
    if layer not in {"raw", "canonical", "curated"}:
        raise ValueError(f"Unsupported layer: {layer}")

    path = root / layer / f"market={market}" / f"freq={frequency}" / f"symbol={symbol}" / f"year={year}"
    if layer == "curated":
        path = root / layer / f"adj={adjustment}" / f"market={market}" / f"freq={frequency}" / f"symbol={symbol}" / f"year={year}"
    return path


def dataset_id(market: str, frequency: str, adjustment: str = "raw") -> str:
    """Build stable dataset id used in manifests and access APIs."""
    return f"{market}_{frequency}_{adjustment}"
