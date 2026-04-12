"""Manifest helpers for dataset metadata sidecars."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from market_data_core.schema.metadata import DatasetMetadata


MANIFEST_FILE_NAME = "_manifest.json"


def build_manifest(metadata: DatasetMetadata, row_count: int, symbol_count: int, min_timestamp: str, max_timestamp: str) -> dict[str, Any]:
    """Build dataset manifest payload from strongly-typed metadata."""
    payload = asdict(metadata)
    payload.update(
        {
            "row_count": int(row_count),
            "symbol_count": int(symbol_count),
            "min_timestamp": min_timestamp,
            "max_timestamp": max_timestamp,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )
    return payload


def write_manifest(partition_path: Path, manifest: dict[str, Any]) -> Path:
    """Write manifest JSON sidecar under the partition path."""
    partition_path.mkdir(parents=True, exist_ok=True)
    manifest_path = partition_path / MANIFEST_FILE_NAME
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return manifest_path


def read_manifest(partition_path: Path) -> dict[str, Any]:
    """Read manifest sidecar from a partition path."""
    manifest_path = partition_path / MANIFEST_FILE_NAME
    return json.loads(manifest_path.read_text())
