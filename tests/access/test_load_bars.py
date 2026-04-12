import pytest
pd = pytest.importorskip("pandas")


from market_data_core.access import load_bars
from market_data_core.providers import DataProvider, register_provider, reset_provider


class StubProvider(DataProvider):
    name = "stub"

    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del symbol, start_date, end_date
        return _frame()

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del symbol, start_date, end_date
        return _frame()


def _frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "symbol": ["000001.SZ"],
            "timestamp": pd.to_datetime(["2026-01-02 09:30:00+08:00"]),
            "open": [10.0],
            "high": [10.2],
            "low": [9.8],
            "close": [10.1],
            "volume": [1000.0],
            "turnover_rate": [1.2],
        }
    )


def test_load_bars_fetch_path(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    register_provider("stub", StubProvider)

    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)
    monkeypatch.setattr("market_data_core.access.load.write_bars", lambda *args, **kwargs: None)

    df = load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="1d", provider="stub")
    assert list(df.columns)[:2] == ["symbol", "timestamp"]


def test_load_bars_unsupported_frequency(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    register_provider("stub", StubProvider)
    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)

    with pytest.raises(ValueError, match="Unsupported frequency"):
        load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="5m", provider="stub")
