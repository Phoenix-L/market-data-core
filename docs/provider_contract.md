# Provider Contract (Phase 6)

This document defines the **stable provider interface boundary** for `market-data-core`.

## Status

- **Implemented**: provider interface (`DataProvider`) + registry lifecycle (`register_provider`, `get_provider`, `reset_provider`).
- **Deferred**: concrete BaoStock/Tushare SDK adapters.

## Interface

Providers must implement:
- `fetch_daily(symbol, start_date, end_date) -> pd.DataFrame`
- `fetch_minute30(symbol, start_date, end_date) -> pd.DataFrame`

## Output dataframe requirements

Required columns:
- `symbol`
- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `turnover_rate`

Column semantics follow `docs/canonical_bar_contract.md`.

## Timestamp and timezone requirements

- `timestamp` values must be timezone-aware.
- Canonical timezone is `Asia/Shanghai`.
- Values must align to session open anchors for the requested frequency (`1d` or `30m`).

## Ordering and key expectations

- Rows should be sorted ascending by timestamp for each symbol.
- `(symbol, timestamp)` keys should be unique.

## Missing data and null behavior

- Required columns must exist.
- `turnover_rate` may be null when source cannot provide/derive a value.
- Optional columns may be present but are not required.

## Error behavior

- Provider transport/data errors should raise explicit exceptions.
- Providers must not return malformed dataframes and rely on downstream silent repair.
- `load_bars` enforces strict validation and raises `ContractError` on validation failures.

## Consumer note

In Phase 6, providers are commonly injected by consumer repos via registry registration in process.
