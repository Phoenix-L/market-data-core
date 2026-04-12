def test_package_imports() -> None:
    import market_data_core

    assert market_data_core.PACKAGE_NAME == "market-data-core"
