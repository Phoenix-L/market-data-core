import pytest
pd = pytest.importorskip("pandas")


from market_data_core.validation import validate_bars


def _valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "symbol": ["000001.SZ", "000001.SZ"],
            "timestamp": pd.to_datetime(["2026-01-02 09:30:00+08:00", "2026-01-03 09:30:00+08:00"]),
            "open": [10.0, 10.5],
            "high": [10.2, 10.6],
            "low": [9.8, 10.4],
            "close": [10.1, 10.55],
            "volume": [1000.0, 2000.0],
            "turnover_rate": [1.2, 1.3],
        }
    )


def test_validate_bars_ok() -> None:
    report = validate_bars(_valid_frame(), frequency="1d")
    assert report.ok
    assert report.errors == []


def test_validate_bars_detects_missing_required_column() -> None:
    df = _valid_frame().drop(columns=["volume"])
    report = validate_bars(df, frequency="1d")
    assert not report.ok
    assert any("missing_required_columns" in err for err in report.errors)


def test_validate_bars_detects_duplicate_key() -> None:
    df = _valid_frame().copy()
    df.loc[1, "timestamp"] = df.loc[0, "timestamp"]
    report = validate_bars(df, frequency="1d")
    assert not report.ok
    assert any("duplicate_primary_key" in err for err in report.errors)


def test_validate_bars_detects_ohlc_issue() -> None:
    df = _valid_frame()
    df.loc[0, "low"] = 11.0
    report = validate_bars(df, frequency="1d")
    assert not report.ok
    assert any("invalid_ohlc_invariant" in err for err in report.errors)


def test_validate_bars_detects_negative_volume() -> None:
    df = _valid_frame()
    df.loc[0, "volume"] = -1.0
    report = validate_bars(df, frequency="1d")
    assert not report.ok
    assert any("negative_volume" in err for err in report.errors)


def test_validate_bars_turnover_warning_in_permissive_mode() -> None:
    df = _valid_frame()
    df.loc[0, "turnover_rate"] = -0.1
    report = validate_bars(df, frequency="1d", strict=False)
    assert report.ok
    assert any("negative_turnover_rate" in warn for warn in report.warnings)


def test_validate_bars_flags_session_alignment_for_30m() -> None:
    df = _valid_frame()
    df["timestamp"] = pd.to_datetime(["2026-01-02 12:00:00+08:00", "2026-01-03 10:00:00+08:00"])
    report = validate_bars(df, frequency="30m")
    assert not report.ok
    assert any("session_misaligned_timestamps" in err for err in report.errors)


def test_validate_bars_warns_missing_30m_anchors() -> None:
    df = pd.DataFrame(
        {
            "symbol": ["000001.SZ", "000001.SZ"],
            "timestamp": pd.to_datetime(["2026-01-05 09:30:00+08:00", "2026-01-05 10:00:00+08:00"]),
            "open": [10.0, 10.1],
            "high": [10.2, 10.3],
            "low": [9.8, 10.0],
            "close": [10.1, 10.2],
            "volume": [1000.0, 1200.0],
            "turnover_rate": [1.0, 1.1],
        }
    )
    report = validate_bars(df, frequency="30m", strict=True)
    assert report.ok
    assert any("missing_30m_session_anchors" in warn for warn in report.warnings)
