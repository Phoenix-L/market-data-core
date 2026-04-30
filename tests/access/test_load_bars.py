import pytest
pd = pytest.importorskip("pandas")


from market_data_core.access import load_30m, load_bars, load_daily, load_minute_30
from market_data_core.core.exceptions import ContractError
from market_data_core.providers import DataProvider, register_provider, reset_provider


class StubProvider(DataProvider):
    name = "stub"
    fetch_daily_calls = 0
    fetch_minute30_calls = 0

    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del symbol, start_date, end_date
        type(self).fetch_daily_calls += 1
        return _frame()

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del symbol, start_date, end_date
        type(self).fetch_minute30_calls += 1
        return _frame()


class BadProvider(DataProvider):
    name = "bad"

    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del symbol, start_date, end_date
        return pd.DataFrame({"symbol": ["000001.SZ"]})

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        return self.fetch_daily(symbol, start_date, end_date)


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


def _reset_stub_counts() -> None:
    StubProvider.fetch_daily_calls = 0
    StubProvider.fetch_minute30_calls = 0


def test_load_bars_fetch_path(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    _reset_stub_counts()
    register_provider("stub", StubProvider)

    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)
    monkeypatch.setattr("market_data_core.access.load.write_bars", lambda *args, **kwargs: None)

    df = load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="1d", provider="stub")
    assert list(df.columns)[:2] == ["symbol", "timestamp"]


def test_load_bars_cache_path(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    _reset_stub_counts()
    register_provider("stub", StubProvider)

    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr("market_data_core.access.load.read_bars", lambda *args, **kwargs: _frame())

    df = load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="1d", provider="stub")
    assert len(df) == 1
    assert StubProvider.fetch_daily_calls == 0


def test_load_bars_ignores_old_unversioned_cache_path(tmp_path) -> None:
    reset_provider()
    _reset_stub_counts()
    register_provider("stub", StubProvider)

    old_path = tmp_path / "stub" / "000001.SZ" / "1d" / "2026-01-01_2026-01-31.parquet"
    old_path.parent.mkdir(parents=True)
    _frame().to_parquet(old_path, index=False)

    df = load_bars(
        "000001.SZ",
        "2026-01-01",
        "2026-01-31",
        frequency="1d",
        provider="stub",
        data_root=str(tmp_path),
        use_cache=True,
    )

    assert len(df) == 1
    assert StubProvider.fetch_daily_calls == 1
    assert (tmp_path / "v2" / "stub" / "000001.SZ" / "1d" / "2026-01-01_2026-01-31.parquet").exists()


def test_load_bars_raises_contract_error_on_invalid_provider_output(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    register_provider("bad", BadProvider)
    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)

    with pytest.raises(ContractError, match="Loaded bars failed validation"):
        load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="1d", provider="bad")


def test_load_bars_unsupported_frequency(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    register_provider("stub", StubProvider)
    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)

    with pytest.raises(ValueError, match="Unsupported frequency"):
        load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="5m", provider="stub")


def test_wrapper_api_consistency(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_provider()
    register_provider("stub", StubProvider)
    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)
    monkeypatch.setattr("market_data_core.access.load.write_bars", lambda *args, **kwargs: None)

    df_daily = load_daily("000001.SZ", "2026-01-01", "2026-01-31", provider="stub")
    df_30m = load_30m("000001.SZ", "2026-01-01", "2026-01-31", provider="stub")
    df_legacy = load_minute_30("000001.SZ", "2026-01-01", "2026-01-31", provider="stub")

    assert list(df_daily.columns) == list(df_30m.columns)
    assert list(df_legacy.columns) == list(df_30m.columns)
