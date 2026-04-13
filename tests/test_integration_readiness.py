"""Smoke coverage for stable consumer-facing entrypoints."""

from datetime import date

import pytest

from market_data_core.access import inspect_dataset, list_datasets, load_bars
from market_data_core.calendar import is_session_aligned, session_open_anchors
from market_data_core.providers import DataProvider, register_provider, reset_provider
from market_data_core.validation import validate_bars

pd = pytest.importorskip("pandas")


class _SmokeProvider(DataProvider):
    name = "smoke"

    def fetch_daily(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        del start_date, end_date
        return pd.DataFrame(
            {
                "symbol": [symbol],
                "timestamp": pd.to_datetime(["2026-01-06 09:30:00+08:00"]),
                "open": [1.0],
                "high": [1.2],
                "low": [0.9],
                "close": [1.1],
                "volume": [10.0],
                "turnover_rate": [0.1],
            }
        )

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        return self.fetch_daily(symbol, start_date, end_date)


def test_public_entrypoints_smoke(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    reset_provider()
    register_provider("smoke", _SmokeProvider)

    monkeypatch.setattr("market_data_core.access.load.cache_exists", lambda *args, **kwargs: False)
    monkeypatch.setattr("market_data_core.access.load.write_bars", lambda *args, **kwargs: None)

    df = load_bars("000001.SZ", "2026-01-01", "2026-01-31", frequency="1d", provider="smoke")
    report = validate_bars(df, frequency="1d")

    anchors = session_open_anchors(date(2026, 1, 6), "1d")
    assert is_session_aligned(anchors[0], "1d")
    assert report.ok

    assert list_datasets(str(tmp_path)) == []
    with pytest.raises(FileNotFoundError):
        inspect_dataset("cn_equity_1d_raw", str(tmp_path))
