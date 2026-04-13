import os

import pytest

pd = pytest.importorskip("pandas")

from market_data_core.access import load_bars
from market_data_core.providers import register_provider, reset_provider
from market_data_core.providers.baostock.provider import BaoStockProvider


pytestmark = pytest.mark.skipif(
    os.getenv("MDCF_RUN_BAOSTOCK_LIVE") != "1",
    reason="Set MDCF_RUN_BAOSTOCK_LIVE=1 to enable BaoStock live smoke test.",
)


def test_baostock_live_smoke_roundtrip(tmp_path) -> None:
    pytest.importorskip("baostock")

    reset_provider()
    register_provider("baostock", BaoStockProvider)

    df_fetch = load_bars(
        symbol="000001.SZ",
        start="2026-01-05",
        end="2026-01-09",
        frequency="1d",
        provider="baostock",
        use_cache=True,
        data_root=str(tmp_path),
    )

    df_cache = load_bars(
        symbol="000001.SZ",
        start="2026-01-05",
        end="2026-01-09",
        frequency="1d",
        provider="baostock",
        use_cache=True,
        data_root=str(tmp_path),
    )

    assert not df_fetch.empty
    pd.testing.assert_frame_equal(df_fetch, df_cache, check_dtype=False)
