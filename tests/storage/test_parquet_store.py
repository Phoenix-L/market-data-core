from market_data_core.storage.parquet_store import cache_file_path


def test_cache_file_path_layout() -> None:
    path = cache_file_path(
        provider="baostock",
        symbol="000001.SZ",
        frequency="1d",
        start="2026-01-01",
        end="2026-01-31",
        data_root="/tmp/mdata",
    )
    assert str(path).endswith("/baostock/000001.SZ/1d/2026-01-01_2026-01-31.parquet")
