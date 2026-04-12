# market-data-core

`market-data-core` is the reusable market-data foundation package extracted from `aShare` planning work.

## Current phase

This repository is in **Phase 3 (first extraction wave)**:
- canonical schema constants are implemented,
- baseline validation checks are implemented,
- basic normalization/dedupe helpers are implemented,
- provider registry + compatibility env behavior is implemented,
- minimal cache-backed load API is implemented.

Still intentionally deferred:
- concrete BaoStock/Tushare adapter wiring,
- full ingest pipeline,
- dataset inspection and rich manifests,
- advanced calendar and adjustment transforms.

## What this repo owns

- provider adapter contracts and registry
- canonical OHLCV schema and metadata contracts
- validation entrypoints for shared bar invariants
- generic normalization/dedupe helpers
- storage/access API boundaries

## What is intentionally deferred

- Backtrader integration
- strategy/signal/research orchestration
- full ingest pipelines
- production-grade persistence orchestration and cataloging

## Package layout

See:
- `docs/architecture.md`
- `docs/repo_structure.md`
- `docs/public_api_draft.md`

Code is under `src/market_data_core/` and tests under `tests/`.
