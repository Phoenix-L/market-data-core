from pathlib import Path

from market_data_core.schema.metadata import DatasetMetadata
from market_data_core.storage import build_manifest, read_manifest, write_manifest


def test_write_and_read_manifest_roundtrip(tmp_path: Path) -> None:
    metadata = DatasetMetadata(
        dataset_id="cn_equity_1d_raw",
        market="cn_equity",
        frequency="1d",
        adjustment_mode="raw",
        provider="baostock",
    )
    payload = build_manifest(metadata, row_count=10, symbol_count=1, min_timestamp="2026-01-01", max_timestamp="2026-01-31")

    manifest_path = write_manifest(tmp_path / "canonical/market=cn_equity/freq=1d", payload)
    loaded = read_manifest(manifest_path.parent)

    assert loaded["dataset_id"] == "cn_equity_1d_raw"
    assert loaded["row_count"] == 10
    assert "created_at_utc" in loaded
