# Migration Blueprint: Extract `market-data-core` from `aShare`

## 1) Goal

Create a standalone repository `market-data-core` that owns reusable market-data functionality (provider adapters, schema normalization/validation, cache/load APIs), while keeping Backtrader and strategy execution concerns in `aShare`.

---

## 2) Migration principles

1. **DataFrame boundary**: extracted package returns canonical pandas DataFrames only.
2. **No strategy runtime in core**: core cannot depend on Backtrader or strategy modules.
3. **Conservative extraction**: move stable primitives first; defer entangled modules.
4. **Behavior preservation**: maintain current schema/column names and loader semantics.
5. **Explicit compatibility**: temporary aShare shims allowed to avoid breaking callers.

---

## 3) Bucket definitions

- **CORE_MOVE_NOW**: generic data-layer code with manageable coupling; extract first wave.
- **CORE_MOVE_LATER**: belongs in core but requires split/config cleanup first.
- **KEEP_LOCAL**: aShare runtime/research/backtrader-specific code.
- **UNCLEAR**: uncertain fit; needs additional architecture decision.

---

## 4) Current data flow summary

1. CLI/experiment/research entry points call `load_daily`/`load_minute_30`.
2. Loader resolves provider and cache, then fetches or reads cached data.
3. Provider adapter normalizes vendor payloads to canonical OHLCV+turnover DataFrame.
4. Loader validates schema and writes cache.
5. Engine converts DataFrame to Backtrader feed and does runtime resampling.

Clean cut line: after validated DataFrame return from loader; before Backtrader feed conversion.

---

## 5) Module-by-module classification

| Module | Bucket | Why |
|---|---|---|
| `src/ashare/data/providers/base.py` | CORE_MOVE_NOW | Pure generic provider contract. |
| `src/ashare/data/providers/__init__.py` | CORE_MOVE_NOW | Generic factory/registry with minor env rename needs. |
| `src/ashare/data/providers/baostock_provider.py` | CORE_MOVE_NOW | Provider adapter logic is core market-data functionality. |
| `src/ashare/data/providers/tushare_provider.py` | CORE_MOVE_NOW | Provider adapter logic is core market-data functionality. |
| `src/ashare/data/cache.py` | CORE_MOVE_NOW | Generic cache read/write and keying mechanism. |
| `src/ashare/data/loaders.py` | CORE_MOVE_NOW | Canonical data-access API and schema guardrails. |
| `src/ashare/data/tushare_client.py` | CORE_MOVE_LATER | Hard-coded repo-root `.env` pathing; split/config polish needed. |
| `src/ashare/config/settings.py` (cache slice) | CORE_MOVE_LATER | Mixed with backtest settings; must be split first. |
| `src/ashare/sanitytests.py` | CORE_MOVE_LATER | Generic validation helper but currently CLI-oriented. |
| `src/ashare/data/normalizers.py` | KEEP_LOCAL | Backtrader adapter; excluded by target scope. |
| `src/ashare/engine/runner.py` | KEEP_LOCAL | Runtime feed conversion/resampling and backtest execution. |
| `src/ashare/experiment/executor.py` | KEEP_LOCAL | Experiment orchestration only consumes loaders. |
| `src/ashare/research/walk_forward.py` | KEEP_LOCAL | Research orchestration only consumes loaders. |
| `src/ashare/cli.py` | KEEP_LOCAL | App CLI + local research pipeline wiring. |
| `research/regime_state_machine/*.py` | UNCLEAR | Research analytics; not core ingestion currently. |

---

## 6) Split-required modules

### A) `src/ashare/config/settings.py`
- **Generic slice to extract later**:
  - cache root resolution (`get_cache_dir`) and related env constants.
- **aShare-local slice to keep**:
  - `BacktestConfig` (commission/stamp duty/slippage assumptions for Backtrader broker).
- **Why split first**: data-core should not import broker/runtime settings.

### B) `src/ashare/data/tushare_client.py`
- **Generic slice to extract later**:
  - token lookup + client builder for Tushare API.
- **aShare-local slice to keep (if any)**:
  - repo-specific `.env` discovery assumptions (currently parent traversal).
- **Why split first**: avoid hard-coded source-repo layout in core package.

### C) `src/ashare/data/normalizers.py` (boundary clarification, not actual move)
- **Generic slice**: none currently (function is Backtrader-specific).
- **aShare-local slice**: entire file remains local.
- **Action**: do not move; ensure loader/core interface stays DataFrame-only.

---

## 7) Proposed target structure in `market-data-core`

```text
market_data_core/
  __init__.py
  providers/
    __init__.py              # factory/registry
    base.py                  # DataProvider ABC
    baostock.py              # BaoStock adapter
    tushare.py               # Tushare adapter
    tushare_client.py        # token/client (post-split)
  schema/
    canonical.py             # required columns, schema constants
    validation.py            # dataframe validation helpers
  cache/
    store.py                 # cache path/read/write helpers
    keys.py                  # request key conventions
  loaders/
    bars.py                  # load_daily/load_minute_30 style APIs
  config/
    settings.py              # provider/cache env config (core-scoped names)
```

Notes:
- Keep names close to current APIs in first migration to reduce churn.
- Backtrader adapters explicitly remain outside this package.

---

## 8) First extraction wave (recommended)

### Scope (Wave 1)
Move these modules first:
1. `src/ashare/data/providers/base.py`
2. `src/ashare/data/providers/__init__.py`
3. `src/ashare/data/providers/baostock_provider.py`
4. `src/ashare/data/providers/tushare_provider.py`
5. `src/ashare/data/cache.py`
6. `src/ashare/data/loaders.py`

### For each CORE_MOVE item

#### CORE_MOVE_NOW items

1) **`src/ashare/data/providers/base.py`**
- Reason: stable interface definition.
- Target in core: `market_data_core/providers/base.py`.
- Prerequisite split/refactor: none.
- Important dependencies: `pandas` only.
- Recommended extraction order: **1**.

2) **`src/ashare/data/providers/__init__.py`**
- Reason: central provider lookup lifecycle.
- Target in core: `market_data_core/providers/__init__.py`.
- Prerequisite split/refactor: adapt env naming (`ASHARE_DATA_PROVIDER` compatibility alias).
- Important dependencies: provider base + concrete adapters.
- Recommended extraction order: **2**.

3) **`src/ashare/data/providers/baostock_provider.py`**
- Reason: concrete generic ingestion adapter.
- Target in core: `market_data_core/providers/baostock.py`.
- Prerequisite split/refactor: module path updates only.
- Important dependencies: `baostock`, `pandas`, provider base.
- Recommended extraction order: **3**.

4) **`src/ashare/data/providers/tushare_provider.py`**
- Reason: concrete generic ingestion adapter.
- Target in core: `market_data_core/providers/tushare.py`.
- Prerequisite split/refactor: temporary bridge to existing `tushare_client` until that module moves.
- Important dependencies: `pandas`, `tushare_client`.
- Recommended extraction order: **4**.

5) **`src/ashare/data/cache.py`**
- Reason: reusable storage primitive.
- Target in core: `market_data_core/cache/store.py`.
- Prerequisite split/refactor: decouple from `ashare.config.settings.get_cache_dir`.
- Important dependencies: `pandas`, path utils.
- Recommended extraction order: **5**.

6) **`src/ashare/data/loaders.py`**
- Reason: current public data-access façade used widely in aShare.
- Target in core: `market_data_core/loaders/bars.py`.
- Prerequisite split/refactor: import rewiring to core-local provider/cache modules.
- Important dependencies: provider factory, cache store, schema validation.
- Recommended extraction order: **6**.

#### CORE_MOVE_LATER items

7) **`src/ashare/data/tushare_client.py`**
- Reason for later: repo-root `.env` path assumption is brittle in standalone package.
- Target in core: `market_data_core/providers/tushare_client.py`.
- Prerequisite refactor/split: replace `parents[3]` lookup with explicit config/env loading strategy.
- Important dependencies: `tushare`, `dotenv`.
- Recommended extraction order: after Wave 1 stabilization (**7**).

8) **`src/ashare/config/settings.py` (cache slice)**
- Reason for later: mixed with backtesting broker config.
- Target in core: `market_data_core/config/settings.py` (cache/provider-only concerns).
- Prerequisite refactor/split: isolate `get_cache_dir` and related constants into a data-only module.
- Important dependencies: env handling only.
- Recommended extraction order: with/after `tushare_client` hardening (**8**).

9) **`src/ashare/sanitytests.py`**
- Reason for later: useful reusable smoke checks, but not required for minimal core extraction.
- Target in core: `market_data_core/testing/sanity.py` (optional helper layer).
- Prerequisite refactor/split: remove aShare CLI assumptions; keep loader-agnostic.
- Important dependencies: pandas + loader callable signatures.
- Recommended extraction order: optional post-Phase 0 (**9**).

---

## 9) Risks

1. **Env/config compatibility drift**
   - Existing callers depend on `ASHARE_*` env vars and cache location behavior.
2. **Hidden provider behavior contracts**
   - Downstream code assumes columns and sorted datetime index exactly as today.
3. **Turnover-rate semantics mismatch**
   - BaoStock/Tushare derive/map turnover differently; subtle changes could alter strategy behavior.
4. **Singleton provider state**
   - Shared process state can surprise tests or multi-provider workflows.
5. **Backtrader boundary leakage**
   - Risk of accidentally moving feed conversion code into core.
6. **Path/layout assumptions**
   - `tushare_client` currently assumes source-repo structure for `.env` loading.

---

## 10) Exit criteria for Phase 0

Phase 0 is complete when all are true:

1. `market-data-core` contains provider base/factory, BaoStock/Tushare adapters, cache helpers, and loader API.
2. `aShare` imports data access from core (directly or via compatibility shim) with no behavior regressions in existing loader-facing tests.
3. Backtrader normalizers and engine runtime remain fully in aShare.
4. Cache path/provider env behavior is documented and backward-compatible (or explicitly migrated with clear fallback).
5. Known split tasks (`tushare_client` pathing and config split) are tracked with owners and accepted as Phase 1 follow-ups.
