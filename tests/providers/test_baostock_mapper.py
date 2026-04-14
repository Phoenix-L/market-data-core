import pytest

pd = pytest.importorskip("pandas")

from market_data_core.core.exceptions import ProviderError
from market_data_core.providers.baostock.mapper import map_to_canonical


def test_map_daily_payload_to_canonical() -> None:
    payload = pd.DataFrame(
        {
            "date": ["2026-01-03", "2026-01-02"],
            "open": [10.5, 10.0],
            "high": [10.6, 10.2],
            "low": [10.4, 9.8],
            "close": [10.55, 10.1],
            "volume": [2000, 1000],
            "turn": [1.3, 1.2],
        }
    )

    out = map_to_canonical(payload, symbol="000001.sz", frequency="1d")

    assert list(out.columns) == ["symbol", "timestamp", "open", "high", "low", "close", "volume", "turnover_rate"]
    assert out["symbol"].tolist() == ["000001.SZ", "000001.SZ"]
    assert out["timestamp"].is_monotonic_increasing
    assert str(out["timestamp"].dt.tz) == "Asia/Shanghai"


def test_map_minute30_payload_to_canonical() -> None:
    payload = pd.DataFrame(
        {
            "time": ["2026010210000000", "2026010209300000"],
            "open": [10.1, 10.0],
            "high": [10.3, 10.2],
            "low": [10.0, 9.9],
            "close": [10.2, 10.1],
            "volume": [1200, 1000],
        }
    )

    out = map_to_canonical(payload, symbol="000001.SZ", frequency="30m")

    assert out["timestamp"].is_monotonic_increasing
    assert str(out["timestamp"].dt.tz) == "Asia/Shanghai"
    assert out["turnover_rate"].isna().all()


def test_map_minute30_payload_invalid_compact_time_raises_provider_error() -> None:
    payload = pd.DataFrame(
        {
            "time": ["202601020930000"],
            "open": [10.0],
            "high": [10.2],
            "low": [9.8],
            "close": [10.1],
            "volume": [1000],
        }
    )

    with pytest.raises(ProviderError, match="invalid format"):
        map_to_canonical(payload, symbol="000001.SZ", frequency="30m")


def test_map_payload_missing_columns_raises_provider_error() -> None:
    payload = pd.DataFrame({"date": ["2026-01-02"], "open": [10.0]})

    with pytest.raises(ProviderError, match="missing columns"):
        map_to_canonical(payload, symbol="000001.SZ", frequency="1d")


def test_map_payload_invalid_timestamp_raises_provider_error() -> None:
    payload = pd.DataFrame(
        {
            "date": ["bad-ts"],
            "open": [10.0],
            "high": [10.2],
            "low": [9.8],
            "close": [10.1],
            "volume": [1000],
        }
    )

    with pytest.raises(ProviderError, match="timestamp parse failed"):
        map_to_canonical(payload, symbol="000001.SZ", frequency="1d")


def test_map_payload_duplicate_keys_raises_provider_error() -> None:
    payload = pd.DataFrame(
        {
            "time": ["2026-01-02 09:30:00", "2026-01-02 09:30:00"],
            "open": [10.0, 10.1],
            "high": [10.2, 10.3],
            "low": [9.8, 10.0],
            "close": [10.1, 10.2],
            "volume": [1000, 1200],
        }
    )

    with pytest.raises(ProviderError, match="duplicate"):
        map_to_canonical(payload, symbol="000001.SZ", frequency="30m")
