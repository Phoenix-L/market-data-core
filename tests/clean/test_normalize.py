import pytest
pd = pytest.importorskip("pandas")


from market_data_core.clean.normalize import normalize_columns, normalize_symbol


def test_normalize_columns_lower_strip() -> None:
    df = pd.DataFrame({" Open ": [1.0], "HIGH": [2.0]})
    out = normalize_columns(df)
    assert list(out.columns) == ["open", "high"]


def test_normalize_symbol_upper_strip() -> None:
    assert normalize_symbol(" 000001.sz ") == "000001.SZ"
