import pytest

from market_data_core.core.exceptions import ProviderError
from market_data_core.providers import DataProvider, get_provider, register_provider, reset_provider


class _DummyProvider(DataProvider):
    name = "dummy"

    def fetch_daily(self, symbol: str, start_date: str, end_date: str):
        del symbol, start_date, end_date
        return object()

    def fetch_minute30(self, symbol: str, start_date: str, end_date: str):
        del symbol, start_date, end_date
        return object()


def test_register_and_get_provider() -> None:
    reset_provider()
    register_provider("dummy", _DummyProvider)
    provider = get_provider("dummy")
    assert provider.name == "dummy"


def test_get_provider_raises_for_unknown() -> None:
    reset_provider()
    with pytest.raises(ProviderError, match="Unsupported provider"):
        get_provider("not-registered")
