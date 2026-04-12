# market-data-core

`market-data-core` is the reusable market-data foundation package shared by `aShare` and future consumer repos.

## Current phase

This repository is in **Phase 5 (wave 2 expansion + contract tightening)**.

Implemented and stable for consumers:
- canonical bar schema constants and validation entrypoint,
- CN A-share session anchor helpers and alignment checks,
- provider registry boundary with compatibility env behavior,
- storage layout/manifests helpers and dataset inspection APIs,
- load API boundary (`load_bars`, `load_daily`, `load_30m`, `load_minute_30`).

Still intentionally deferred:
- concrete BaoStock/Tushare SDK adapters,
- ingest orchestration pipelines,
- full transform layer (`resample`, `adjust`) implementation.

## Public package boundaries

Prefer importing from these modules:
- `market_data_core.access`
- `market_data_core.validation`
- `market_data_core.calendar`
- `market_data_core.storage`
- `market_data_core.providers`

Internal helpers may evolve faster and are not guaranteed as stable imports.

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

Code is under `src/market_data_core/` and tests under `tests/`.
