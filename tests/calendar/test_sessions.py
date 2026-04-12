from datetime import date, datetime

from market_data_core.calendar import (
    ASIA_SHANGHAI,
    check_missing_30m_bars,
    check_session_alignment,
    is_session_aligned,
    session_open_anchors,
)


def test_session_open_anchors_30m_count() -> None:
    anchors = session_open_anchors(date(2026, 1, 5), "30m")
    assert len(anchors) == 8
    assert anchors[0].hour == 9 and anchors[0].minute == 30
    assert anchors[-1].hour == 14 and anchors[-1].minute == 30


def test_is_session_aligned_respects_lunch_break() -> None:
    assert is_session_aligned(datetime(2026, 1, 5, 10, 0, tzinfo=ASIA_SHANGHAI), "30m")
    assert not is_session_aligned(datetime(2026, 1, 5, 12, 0, tzinfo=ASIA_SHANGHAI), "30m")


def test_missing_30m_bars_flags_gaps() -> None:
    ts = [
        datetime(2026, 1, 5, 9, 30, tzinfo=ASIA_SHANGHAI),
        datetime(2026, 1, 5, 10, 0, tzinfo=ASIA_SHANGHAI),
    ]
    issues = check_missing_30m_bars(ts)
    assert any("missing_30m_session_anchors" in item for item in issues)


def test_session_alignment_reports_misaligned() -> None:
    issues = check_session_alignment([datetime(2026, 1, 5, 12, 0, tzinfo=ASIA_SHANGHAI)], "30m")
    assert issues == ["session_misaligned_timestamps: 1"]
