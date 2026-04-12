# market-data-core

`market-data-core` is the reusable market-data foundation package extracted from `aShare` planning work.

## Current phase

This repository is in **bootstrap/skeleton phase**:
- contracts and boundaries are documented,
- package/module landing zones exist,
- only light scaffolding is implemented.

No real provider API integration or ingestion business logic is implemented yet.

## What this repo will own

- provider adapters
- canonical OHLCV schema and metadata contracts
- validation and calendar/session checks
- storage/access API boundaries
- transform boundaries (resample/adjust)
- minimal operational CLI

## What is intentionally deferred

- Backtrader integration
- strategy/signal/research orchestration
- full ingest pipelines
- production-grade persistence implementations

## Package layout

See:
- `docs/architecture.md`
- `docs/repo_structure.md`
- `docs/public_api_draft.md`

Code is under `src/market_data_core/` and tests under `tests/`.
