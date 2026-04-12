from pathlib import Path

from market_data_core.storage import dataset_id, dataset_partition_path, partition_years


def test_dataset_partition_path_for_curated_includes_adj() -> None:
    path = dataset_partition_path(
        root=Path("/tmp/data"),
        layer="curated",
        market="cn_equity",
        frequency="1d",
        symbol="000001.SZ",
        year=2026,
        adjustment="qfq",
    )
    assert "adj=qfq" in str(path)


def test_partition_years_inclusive() -> None:
    assert partition_years("2024-12-31", "2026-01-01") == [2024, 2025, 2026]


def test_dataset_id_builder() -> None:
    assert dataset_id("cn_equity", "30m", "raw") == "cn_equity_30m_raw"
