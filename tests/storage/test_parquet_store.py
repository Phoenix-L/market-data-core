import pytest

pd = pytest.importorskip("pandas")

from market_data_core.core.exceptions import ContractError
from market_data_core.storage.constants import CACHE_CONTRACT_VERSION
from market_data_core.storage.parquet_store import cache_file_path, read_bars, write_bars
from market_data_core.validation import validate_bars


def test_cache_file_path_layout() -> None:
    path = cache_file_path(
        provider="baostock",
        symbol="000001.SZ",
        frequency="1d",
        start="2026-01-01",
        end="2026-01-31",
        data_root="/tmp/mdata",
    )
    assert str(path).endswith(f"/{CACHE_CONTRACT_VERSION}/baostock/000001.SZ/1d/2026-01-01_2026-01-31.parquet")


def test_cache_file_path_does_not_use_old_unversioned_layout() -> None:
    path = cache_file_path(
        provider="baostock",
        symbol="000001.SZ",
        frequency="30m",
        start="2026-01-01",
        end="2026-01-31",
        data_root="/tmp/mdata",
    )

    assert "/v2/baostock/000001.SZ/30m/" in str(path)
    assert str(path) != "/tmp/mdata/baostock/000001.SZ/30m/2026-01-01_2026-01-31.parquet"


def test_30m_cache_roundtrip_preserves_canonical_open_anchors(tmp_path) -> None:
    df = pd.DataFrame(
        {
            "symbol": ["000001.SZ", "000001.SZ"],
            "timestamp": pd.to_datetime(["2026-01-05 09:30:00+08:00", "2026-01-05 10:00:00+08:00"]),
            "open": [10.0, 10.1],
            "high": [10.2, 10.3],
            "low": [9.9, 10.0],
            "close": [10.1, 10.2],
            "volume": [1000, 1200],
            "turnover_rate": [1.1, 1.2],
        }
    )

    path = write_bars(df, "baostock", "000001.SZ", "30m", "2026-01-05", "2026-01-05", str(tmp_path))
    assert f"/{CACHE_CONTRACT_VERSION}/" in path.as_posix()

    cached = read_bars("baostock", "000001.SZ", "30m", "2026-01-05", "2026-01-05", str(tmp_path))
    report = validate_bars(cached, frequency="30m", strict=True)

    assert report.ok
    assert cached["timestamp"].dt.strftime("%H:%M").tolist() == ["09:30", "10:00"]


def test_stale_close_anchor_30m_cache_fixture_fails_validation() -> None:
    stale = pd.DataFrame(
        {
            "symbol": ["000001.SZ", "000001.SZ"],
            "timestamp": pd.to_datetime(["2026-01-05 14:30:00+08:00", "2026-01-05 15:00:00+08:00"]),
            "open": [10.0, 10.1],
            "high": [10.2, 10.3],
            "low": [9.9, 10.0],
            "close": [10.1, 10.2],
            "volume": [1000, 1200],
            "turnover_rate": [1.1, 1.2],
        }
    )

    report = validate_bars(stale, frequency="30m", strict=True)

    assert not report.ok
    assert any("session_misaligned_timestamps" in error for error in report.errors)
