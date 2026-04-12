from market_data_core.core.enums import AdjustmentMode, Frequency, Market


def test_enum_values() -> None:
    assert Market.CN_EQUITY.value == "cn_equity"
    assert Frequency.DAILY_1D.value == "1d"
    assert AdjustmentMode.RAW.value == "raw"
