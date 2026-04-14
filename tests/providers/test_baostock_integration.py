import pytest

pd = pytest.importorskip("pandas")

from market_data_core.access import load_bars
from market_data_core.core.exceptions import ProviderError
from market_data_core.providers import register_provider, reset_provider
from market_data_core.providers.baostock.provider import BaoStockProvider


class _FakeQueryResult:
    def __init__(self, fields: list[str], rows: list[list[str]], error_code: str = "0", error_msg: str = ""):
        self.fields = fields
        self.error_code = error_code
        self.error_msg = error_msg
        self._rows = rows
        self._idx = -1

    def next(self) -> bool:
        self._idx += 1
        return self._idx < len(self._rows)

    def get_row_data(self) -> list[str]:
        return self._rows[self._idx]


class _FakeBaoStockClient:
    def __init__(self, mode: str = "ok"):
        self.mode = mode

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def query_history_k_data_plus(self, code: str, fields: str, start_date: str, end_date: str, frequency: str, adjustflag: str):
        del code, start_date, end_date, adjustflag
        if self.mode == "error":
            return _FakeQueryResult(fields.split(","), [], error_code="1", error_msg="boom")

        if frequency == "d":
            return _FakeQueryResult(
                fields.split(","),
                [
                    ["2026-01-03", "10.5", "10.6", "10.4", "10.55", "2000", "1.3"],
                    ["2026-01-02", "10.0", "10.2", "9.8", "10.1", "1000", "1.2"],
                ],
            )

        return _FakeQueryResult(
            fields.split(","),
            [
                ["2026-01-02", "2026-01-02 10:00:00", "10.1", "10.3", "10.0", "10.2", "1200"],
                ["2026-01-02", "2026-01-02 09:30:00", "10.0", "10.2", "9.9", "10.1", "1000"],
            ],
        )


class _ClosedAwareQueryResult:
    def __init__(self, fields: list[str], rows: list[list[str]], is_closed):
        self.fields = fields
        self.error_code = "0"
        self.error_msg = ""
        self._rows = rows
        self._idx = -1
        self._is_closed = is_closed

    def next(self) -> bool:
        if self._is_closed():
            raise OSError(9, "Bad file descriptor")
        self._idx += 1
        return self._idx < len(self._rows)

    def get_row_data(self) -> list[str]:
        return self._rows[self._idx]


class _ExitOrderClient:
    def __init__(self):
        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._closed = True
        return False

    def query_history_k_data_plus(self, code: str, fields: str, start_date: str, end_date: str, frequency: str, adjustflag: str):
        del code, start_date, end_date, adjustflag, frequency
        return _ClosedAwareQueryResult(
            fields.split(","),
            [["2026-01-02", "10.0", "10.2", "9.8", "10.1", "1000", "1.2"]],
            is_closed=lambda: self._closed,
        )


def _provider_factory_ok():
    return BaoStockProvider(client_factory=lambda: _FakeBaoStockClient(mode="ok"))


def _provider_factory_error():
    return BaoStockProvider(client_factory=lambda: _FakeBaoStockClient(mode="error"))


def test_load_bars_baostock_fetch_then_cache_roundtrip(tmp_path) -> None:
    reset_provider()
    register_provider("baostock", _provider_factory_ok)

    df_fetch = load_bars(
        symbol="000001.SZ",
        start="2026-01-01",
        end="2026-01-31",
        frequency="1d",
        provider="baostock",
        use_cache=True,
        data_root=str(tmp_path),
    )

    df_cache = load_bars(
        symbol="000001.SZ",
        start="2026-01-01",
        end="2026-01-31",
        frequency="1d",
        provider="baostock",
        use_cache=True,
        data_root=str(tmp_path),
    )

    pd.testing.assert_frame_equal(df_fetch, df_cache, check_dtype=False)


def test_load_bars_baostock_minute30_passes_validation(tmp_path) -> None:
    reset_provider()
    register_provider("baostock", _provider_factory_ok)

    df = load_bars(
        symbol="000001.SZ",
        start="2026-01-01",
        end="2026-01-31",
        frequency="30m",
        provider="baostock",
        use_cache=True,
        data_root=str(tmp_path),
    )

    assert len(df) == 2
    assert df["timestamp"].is_monotonic_increasing


def test_baostock_provider_query_error_raises_provider_error() -> None:
    reset_provider()
    register_provider("baostock", _provider_factory_error)

    with pytest.raises(ProviderError, match="BaoStock query failed"):
        load_bars(
            symbol="000001.SZ",
            start="2026-01-01",
            end="2026-01-31",
            frequency="1d",
            provider="baostock",
            use_cache=False,
        )


def test_baostock_result_consumed_before_client_exit() -> None:
    reset_provider()
    register_provider("baostock", lambda: BaoStockProvider(client_factory=_ExitOrderClient))

    df = load_bars(
        symbol="000001.SZ",
        start="2026-01-01",
        end="2026-01-31",
        frequency="1d",
        provider="baostock",
        use_cache=False,
    )

    assert len(df) == 1
