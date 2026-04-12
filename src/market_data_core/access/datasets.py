"""Dataset inspection APIs over storage manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_data_core.storage.manifests import MANIFEST_FILE_NAME, read_manifest
from market_data_core.storage.parquet_store import resolve_data_root


def list_datasets(data_root: str | None = None) -> list[str]:
    """List dataset ids discovered from manifest sidecars."""
    root = resolve_data_root(data_root)
    if not root.exists():
        return []

    dataset_ids: set[str] = set()
    for manifest_path in root.rglob(MANIFEST_FILE_NAME):
        data = read_manifest(manifest_path.parent)
        dataset_id = str(data.get("dataset_id", "")).strip()
        if dataset_id:
            dataset_ids.add(dataset_id)
    return sorted(dataset_ids)


def inspect_dataset(dataset_id: str, data_root: str | None = None) -> dict[str, Any]:
    """Return latest manifest payload for requested dataset id."""
    root = resolve_data_root(data_root)
    if not root.exists():
        raise FileNotFoundError(f"Data root does not exist: {root}")

    matches: list[Path] = []
    for manifest_path in root.rglob(MANIFEST_FILE_NAME):
        data = read_manifest(manifest_path.parent)
        if data.get("dataset_id") == dataset_id:
            matches.append(manifest_path.parent)

    if not matches:
        raise FileNotFoundError(f"Dataset not found: {dataset_id}")

    latest = max(matches, key=lambda p: p.stat().st_mtime)
    return read_manifest(latest)
