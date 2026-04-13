"""BaoStock payload-to-canonical mapping utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from market_data_core.calendar import ASIA_SHANGHAI, CN_A_DAILY_OPEN_ANCHOR
from market_data_core.core.exceptions import ProviderError
from market_data_core.schema.bars import REQUIRED_BAR_COLUMNS

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def _parse_timestamp(df: "pd.DataFrame", frequency: str) -> "pd.Series":
    import pandas as pd

    if frequency == "1d":
        if "date" not in df.columns:
            raise ProviderError("BaoStock daily payload missing 'date' column")
        series = pd.to_datetime(df["date"], errors="raise")
        return series.dt.tz_localize(ASIA_SHANGHAI).dt.normalize() + pd.Timedelta(
            hours=CN_A_DAILY_OPEN_ANCHOR.hour,
            minutes=CN_A_DAILY_OPEN_ANCHOR.minute,
        )

    if frequency == "30m":
        if "time" in df.columns:
            series = pd.to_datetime(df["time"], errors="raise")
        elif "date" in df.columns:
            series = pd.to_datetime(df["date"], errors="raise")
        else:
            raise ProviderError("BaoStock 30m payload missing both 'time' and 'date' columns")

        if series.dt.tz is None:
            return series.dt.tz_localize(ASIA_SHANGHAI)
        return series.dt.tz_convert(ASIA_SHANGHAI)

    raise ProviderError(f"Unsupported frequency for mapping: {frequency}")


def _require_columns(df: "pd.DataFrame", columns: set[str], payload_name: str) -> None:
    missing = sorted(columns - set(df.columns))
    if missing:
        raise ProviderError(f"BaoStock {payload_name} payload missing columns: {', '.join(missing)}")


def map_to_canonical(payload: "pd.DataFrame", symbol: str, frequency: str) -> "pd.DataFrame":
    """Map BaoStock payload DataFrame to canonical bars.

    Raises ``ProviderError`` on any malformed payload or contract-unsafe condition.
    """
    import pandas as pd

    if not isinstance(payload, pd.DataFrame):
        raise ProviderError("BaoStock payload must be a pandas DataFrame")

    if payload.empty:
        return pd.DataFrame(columns=REQUIRED_BAR_COLUMNS)

    payload_name = "daily" if frequency == "1d" else "30m"
    _require_columns(payload, {"open", "high", "low", "close", "volume"}, payload_name)

    df = payload.copy()
    df["symbol"] = symbol.upper()

    try:
        df["timestamp"] = _parse_timestamp(df, frequency)
    except Exception as exc:
        if isinstance(exc, ProviderError):
            raise
        raise ProviderError(f"BaoStock {payload_name} timestamp parse failed: {exc}") from exc

    for col in ["open", "high", "low", "close", "volume"]:
        try:
            df[col] = pd.to_numeric(df[col], errors="raise")
        except Exception as exc:
            raise ProviderError(f"BaoStock {payload_name} non-numeric column '{col}': {exc}") from exc

    if "turn" in df.columns:
        try:
            df["turnover_rate"] = pd.to_numeric(df["turn"], errors="raise")
        except Exception as exc:
            raise ProviderError(f"BaoStock {payload_name} non-numeric column 'turn': {exc}") from exc
    elif "turnover_rate" in df.columns:
        try:
            df["turnover_rate"] = pd.to_numeric(df["turnover_rate"], errors="raise")
        except Exception as exc:
            raise ProviderError(f"BaoStock {payload_name} invalid 'turnover_rate': {exc}") from exc
    else:
        df["turnover_rate"] = pd.NA

    out = df.loc[:, list(REQUIRED_BAR_COLUMNS)].copy()
    out = out.sort_values(["symbol", "timestamp"], kind="stable").reset_index(drop=True)

    if out.duplicated(["symbol", "timestamp"]).any():
        raise ProviderError("BaoStock payload contains duplicate (symbol, timestamp) keys")

    return out
