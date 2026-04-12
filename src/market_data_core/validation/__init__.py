"""Validation entrypoints for canonical bar DataFrames."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .data_checks import (
    check_non_negative_turnover_rate,
    check_non_negative_volume,
    check_ohlc_invariants,
    check_timestamp_order,
)
from .reports import ValidationReport
from .schema_checks import check_duplicate_keys, check_monotonic_timestamp, check_required_columns

if TYPE_CHECKING:  # pragma: no cover
    import pandas as pd


def validate_bars(
    df: "pd.DataFrame",
    frequency: str,
    market: str = "cn_equity",
    strict: bool = True,
) -> ValidationReport:
    del market, frequency
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(check_required_columns(df))
    errors.extend(check_duplicate_keys(df))
    errors.extend(check_monotonic_timestamp(df))
    errors.extend(check_timestamp_order(df))
    errors.extend(check_ohlc_invariants(df))
    errors.extend(check_non_negative_volume(df))

    turnover_issues = check_non_negative_turnover_rate(df)
    (errors if strict else warnings).extend(turnover_issues)

    return ValidationReport(ok=not errors, errors=errors, warnings=warnings, stats={"rows": len(df), "columns": len(df.columns)})


__all__ = ["ValidationReport", "validate_bars"]
