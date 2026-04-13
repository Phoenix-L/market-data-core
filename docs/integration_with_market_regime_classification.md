# Integration with `market-regime-classification` (Phase 6)

This note describes the recommended integration pattern for downstream regime workflows.

## Recommended boundary

`market-regime-classification` should depend on `market-data-core` for:
- loading canonical bars via `market_data_core.access`,
- validating incoming frames via `market_data_core.validation`,
- optional metadata discovery via dataset inspection APIs.

It should not depend on internal modules under `market_data_core.*` outside the stable public list.

## Typical startup sequence

1. Register a provider implementation using `register_provider(...)`.
2. Call `load_bars(...)` / `load_30m(...)`.
3. Re-validate with `validate_bars(...)` when data quality gates are needed.
4. Use `inspect_dataset(...)` to report dataset metadata in diagnostics.

## Current limitations (intentional)

- No built-in BaoStock/Tushare adapters in Phase 6.
- No ingest orchestration in this package.
- No transform (`resample` / `adjust`) implementation.

## Migration safety note

`load_minute_30` remains available as a compatibility alias for existing integrations.
