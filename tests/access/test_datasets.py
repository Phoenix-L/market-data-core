from pathlib import Path

import pytest

from market_data_core.access.datasets import inspect_dataset, list_datasets
from market_data_core.schema.metadata import DatasetMetadata
from market_data_core.storage import build_manifest, write_manifest



def test_list_and_inspect_dataset(tmp_path: Path) -> None:
    metadata = DatasetMetadata(
        dataset_id="cn_equity_1d_raw",
        market="cn_equity",
        frequency="1d",
        adjustment_mode="raw",
        provider="baostock",
    )
    manifest = build_manifest(metadata, row_count=100, symbol_count=2, min_timestamp="2026-01-01", max_timestamp="2026-01-31")
    write_manifest(tmp_path / "canonical/market=cn_equity/freq=1d/symbol=000001.SZ/year=2026", manifest)

    assert list_datasets(str(tmp_path)) == ["cn_equity_1d_raw"]
    profile = inspect_dataset("cn_equity_1d_raw", str(tmp_path))
    assert profile["symbol_count"] == 2


def test_list_datasets_empty_root_returns_empty(tmp_path: Path) -> None:
    assert list_datasets(str(tmp_path / "does_not_exist")) == []


def test_inspect_dataset_missing_root_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Data root does not exist"):
        inspect_dataset("cn_equity_1d_raw", str(tmp_path / "missing"))


def test_inspect_dataset_not_found_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Dataset not found"):
        inspect_dataset("cn_equity_1d_raw", str(tmp_path))
