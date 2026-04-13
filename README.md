# market-data-core

`market-data-core` is the reusable market-data foundation package shared by `aShare` and future consumer repositories.

## Current phase

This repository is in **Phase 6 (contract hardening + consumer readiness)**.

### Implemented (Phase 6 stable)
- canonical bar schema constants and validation entrypoint,
- CN A-share session anchor helpers and alignment checks,
- provider registry boundary with compatibility env behavior,
- storage layout/manifests helpers and dataset inspection APIs,
- load API boundary (`load_bars`, `load_daily`, `load_30m`, `load_minute_30`) in **Cache Mode**.

### Deferred (future phase)
- concrete BaoStock/Tushare SDK adapters,
- ingest orchestration pipelines,
- full transform layer (`resample`, `adjust`) implementation,
- canonical dataset loading path from partitioned datasets.

## Public API Contract

The following import surfaces are the **stable public contract** in Phase 6:

- `market_data_core.access`
  - `load_bars`, `load_daily`, `load_30m`, `load_minute_30`
  - `list_datasets`, `inspect_dataset`
- `market_data_core.validation`
  - `validate_bars`, `ValidationReport`
- `market_data_core.calendar`
  - session anchor helpers and alignment checks
- `market_data_core.storage`
  - storage layout/manifests helper functions
- `market_data_core.providers`
  - provider boundary types + registry (`DataProvider`, `register_provider`, `get_provider`, `reset_provider`)

Everything else should be treated as **internal, experimental, or deferred** unless promoted here in a later phase.

## Storage and loading modes

`market-data-core` currently defines two storage-facing modes:

1. **Cache Mode (active, implemented)**
   - Used by `load_bars`.
   - Path format: `<data_root>/<provider>/<symbol>/<frequency>/<start>_<end>.parquet`.

2. **Canonical Dataset Mode (future, not implemented for load path)**
   - Uses partition + manifest conventions (`canonical/market=.../freq=.../symbol=.../year=...`).
   - Planned for a future phase (Phase 7+).

## Scope guardrails

This package does **not** own:
- Backtrader integration,
- strategy/signal/research orchestration,
- experiment/report workflows.

## Package layout

See:
- `docs/architecture.md`
- `docs/public_api_draft.md`
- `docs/storage_layout.md`
- `docs/provider_contract.md`
- `docs/consumer_api.md`

Code is under `src/market_data_core/` and tests under `tests/`.
