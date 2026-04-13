"""BaoStock fetch orchestration for canonical bar retrieval."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from market_data_core.core.exceptions import ProviderError

from .client import get_client

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


_DAILY_FIELDS = "date,open,high,low,close,volume,turn"
_MINUTE30_FIELDS = "date,time,open,high,low,close,volume"


def _to_baostock_code(symbol: str) -> str:
    """Convert canonical symbol like ``000001.SZ`` to ``sz.000001``."""
    if "." not in symbol:
        raise ProviderError(f"Invalid symbol format: {symbol}")

    code, exchange = symbol.split(".", 1)
    exchange = exchange.upper().strip()
    if exchange == "SZ":
        return f"sz.{code}"
    if exchange == "SH":
        return f"sh.{code}"
    raise ProviderError(f"Unsupported symbol exchange in {symbol}")


def _query_to_frame(query_result: Any) -> "pd.DataFrame":
    import pandas as pd

    error_code = str(getattr(query_result, "error_code", "0"))
    if error_code not in {"0", "0000"}:
        msg = str(getattr(query_result, "error_msg", "unknown query error"))
        raise ProviderError(f"BaoStock query failed: {msg}")

    fields = getattr(query_result, "fields", None)
    if not fields:
        raise ProviderError("BaoStock query result missing fields")

    if isinstance(fields, str):
        columns = [f.strip() for f in fields.split(",") if f.strip()]
    else:
        columns = [str(f).strip() for f in fields if str(f).strip()]

    rows: list[list[object]] = []
    while query_result.next():
        row_data = getattr(query_result, "get_row_data", None)
        if row_data is None:
            raise ProviderError("BaoStock query result missing get_row_data")
        rows.append(row_data())

    if not rows:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame(rows, columns=columns)


def fetch_daily_payload(symbol: str, start_date: str, end_date: str, client_factory: Any = get_client) -> "pd.DataFrame":
    """Fetch BaoStock daily payload as raw DataFrame."""
    code = _to_baostock_code(symbol)
    try:
        with client_factory() as bs:
            result = bs.query_history_k_data_plus(
                code=code,
                fields=_DAILY_FIELDS,
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="3",
            )
    except ProviderError:
        raise
    except Exception as exc:
        raise ProviderError(f"BaoStock daily fetch failed for {symbol}: {exc}") from exc

    return _query_to_frame(result)


def fetch_minute30_payload(symbol: str, start_date: str, end_date: str, client_factory: Any = get_client) -> "pd.DataFrame":
    """Fetch BaoStock 30m payload as raw DataFrame."""
    code = _to_baostock_code(symbol)
    try:
        with client_factory() as bs:
            result = bs.query_history_k_data_plus(
                code=code,
                fields=_MINUTE30_FIELDS,
                start_date=start_date,
                end_date=end_date,
                frequency="30",
                adjustflag="3",
            )
    except ProviderError:
        raise
    except Exception as exc:
        raise ProviderError(f"BaoStock 30m fetch failed for {symbol}: {exc}") from exc

    return _query_to_frame(result)
