from market_data_core.schema.bars import REQUIRED_BAR_COLUMNS


def test_required_bar_columns_contains_expected_fields() -> None:
    assert REQUIRED_BAR_COLUMNS[:3] == ("symbol", "timestamp", "open")
    assert "turnover_rate" in REQUIRED_BAR_COLUMNS
