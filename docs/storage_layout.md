# Storage Layout and Persistence Conventions

## Purpose
Define stable storage semantics used by `market-data-core` in Phase 6, while separating active behavior from future dataset plans.

## 1) Two storage-facing modes

### Mode A: Cache Mode (**active, implemented**)

Used by `load_bars` today.

Path format:
`<data_root>/<cache_contract_version>/<provider>/<symbol>/<frequency>/<start>_<end>.parquet`

Current cache contract version:
`v2`

Characteristics:
- request-window keyed artifacts,
- versioned by semantic cache contract,
- simple read/write helpers,
- strict validation performed at load boundary.

The cache contract version is intentionally part of the active path. This prevents silent reuse of stale files created under an older timestamp convention, such as unversioned BaoStock 30m files with close/end-anchored timestamps.

### Mode B: Canonical Dataset Mode (**future, not implemented for load path**)

Planned partition format:
`canonical/market=<market>/freq=<freq>/symbol=<symbol>/year=<yyyy>/part-*.parquet`

Characteristics:
- dataset-oriented partitions,
- manifest-backed metadata,
- intended for future ingest/canonical-serving flow.

## 2) Shared data root assumptions

Data root is externalized via environment/config:
- Preferred env: `MARKET_DATA_ROOT`
- Compatibility alias (temporary): `ASHARE_CACHE_DIR`

Default (if unset): `.data/market_data`

With the active contract version, the default cache path is:
`.data/market_data/v2/<provider>/<symbol>/<frequency>/<start>_<end>.parquet`

## 3) Manifest and metadata expectations

Manifest helpers currently support JSON sidecars carrying fields such as:
- `dataset_id`, `market`, `frequency`, `adjustment_mode`, `provider`
- `schema_version`, `timezone`, `timestamp_anchor`
- `row_count`, `symbol_count`, `min_timestamp`, `max_timestamp`, `created_at_utc`

## 4) Access patterns for consumer repos

In Phase 6:
1. Use `market_data_core.access.load_bars` for request-window loads (Cache Mode).
2. Use `list_datasets` / `inspect_dataset` for manifest-based metadata discovery.
3. Treat canonical partition loading as future behavior.

## 5) Deferred/open decisions

- canonical partition read path in access layer,
- ingest materialization policy,
- potential catalog backend expansion.
