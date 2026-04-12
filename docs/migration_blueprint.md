# Migration Blueprint: `aShare` → `market-data-core` (Phase 1 Contracts + Extraction Plan)

## 1) Goal

Establish `market-data-core` as the reusable market-data package for:
- provider adapters,
- canonical OHLCV contract,
- normalization/validation,
- calendar/session semantics,
- storage/access APIs.

Keep Backtrader, strategy logic, experiment/research orchestration in `aShare`.

---

## 2) Phase 1 contract prerequisites (must be accepted before extraction)

Extraction depends on these contracts being the source of truth:
1. `docs/canonical_bar_contract.md`
2. `docs/calendar_policy.md`
3. `docs/adjustment_policy.md`
4. `docs/storage_layout.md`
5. `docs/public_api_draft.md`
6. `docs/architecture.md`
7. `docs/repo_structure.md`

No module moves should happen without aligning behavior to these docs.

---

## 3) Module classification (from Phase 0 audit)

| Source module in `aShare` | Bucket | Decision |
|---|---|---|
| `src/ashare/data/providers/base.py` | CORE_MOVE_NOW | Move in wave 1 |
| `src/ashare/data/providers/__init__.py` | CORE_MOVE_NOW | Move in wave 1 |
| `src/ashare/data/providers/baostock_provider.py` | CORE_MOVE_NOW | Move in wave 1 |
| `src/ashare/data/providers/tushare_provider.py` | CORE_MOVE_NOW | Move in wave 1 |
| `src/ashare/data/cache.py` | CORE_MOVE_NOW | Move in wave 1 |
| `src/ashare/data/loaders.py` | CORE_MOVE_NOW | Move in wave 1 |
| `src/ashare/data/tushare_client.py` | CORE_MOVE_LATER | Split then move |
| `src/ashare/config/settings.py` (cache slice) | CORE_MOVE_LATER | Split then move |
| `src/ashare/sanitytests.py` | CORE_MOVE_LATER | Optional post-wave 1 |
| `src/ashare/data/normalizers.py` | KEEP_LOCAL | Keep in `aShare` |
| Engine/strategy/research modules | KEEP_LOCAL / UNCLEAR | Keep in `aShare` |

---

## 4) CORE_MOVE_NOW mapping (required detail)

## Item 1: `src/ashare/data/providers/base.py`
- **Target path**: `src/market_data_core/providers/base.py`
- **Contract dependencies**:
  - Canonical dataframe contract (`canonical_bar_contract.md`)
  - Frequency ids (`1d`, `30m`) and timestamp semantics (`calendar_policy.md`)
- **Extraction order**: `1`
- **Required source split/refactor before movement**: none
- **Notes**:
  - Keep method signatures close to existing to minimize migration churn.

## Item 2: `src/ashare/data/providers/__init__.py`
- **Target path**: `src/market_data_core/providers/registry.py` (+ `providers/__init__.py` re-export)
- **Contract dependencies**:
  - Public API naming in `public_api_draft.md`
  - Env compatibility policy (`ASHARE_DATA_PROVIDER` alias + neutral naming)
- **Extraction order**: `2`
- **Required source split/refactor before movement**:
  - Replace aShare-branded env assumptions with neutral primary env and compatibility fallback.
- **Notes**:
  - Preserve reset hook for tests.

## Item 3: `src/ashare/data/providers/baostock_provider.py`
- **Target path**: `src/market_data_core/providers/baostock.py`
- **Contract dependencies**:
  - Canonical columns/invariants (`canonical_bar_contract.md`)
  - Session/timestamp grid (`calendar_policy.md`)
- **Extraction order**: `3`
- **Required source split/refactor before movement**: none (path/import rewiring only)
- **Notes**:
  - Preserve current turnover derivation behavior in first move; improvements can be phase 2.

## Item 4: `src/ashare/data/providers/tushare_provider.py`
- **Target path**: `src/market_data_core/providers/tushare.py`
- **Contract dependencies**:
  - Canonical columns/invariants (`canonical_bar_contract.md`)
  - Adjustment naming alignment (`adjustment_policy.md`) where relevant
- **Extraction order**: `4`
- **Required source split/refactor before movement**:
  - Temporary import bridge to existing `aShare` tushare client until client split is complete.
- **Notes**:
  - Maintain existing daily + 30m normalization semantics for parity.

## Item 5: `src/ashare/data/cache.py`
- **Target path**: `src/market_data_core/storage/parquet_store.py`
- **Contract dependencies**:
  - Storage partitioning/naming (`storage_layout.md`)
  - Manifest metadata minima (`storage_layout.md`)
- **Extraction order**: `5`
- **Required source split/refactor before movement**:
  - Decouple from `ashare.config.settings.get_cache_dir`.
  - Read `MARKET_DATA_ROOT` first; support legacy alias during transition.
- **Notes**:
  - Keep read/write behavior conservative; no format switch in wave 1.

## Item 6: `src/ashare/data/loaders.py`
- **Target path**: `src/market_data_core/access/load.py`
- **Contract dependencies**:
  - Public load API (`public_api_draft.md`)
  - Validation strictness (`canonical_bar_contract.md`, `calendar_policy.md`)
- **Extraction order**: `6`
- **Required source split/refactor before movement**:
  - Rewire imports to core providers + storage + validation modules.
  - Add compatibility wrappers (`load_daily`, `load_30m` and optional alias `load_minute_30`).
- **Notes**:
  - This is the critical boundary for `aShare` consumers.

---

## 5) Tightened first extraction wave (actionable sequence)

## Wave 1A: foundation move (no behavior changes)
1. Move `providers/base.py`.
2. Move provider registry/factory module with env compatibility aliasing.
3. Add schema constants + validator skeleton (`schema/canonical.py`, `validation/bars.py`) matching current loader checks.

**Exit check**:
- Existing provider unit tests (or equivalent smoke checks) pass unchanged via compatibility imports.

## Wave 1B: provider adapter move
4. Move BaoStock adapter.
5. Move Tushare adapter (using temporary bridge to old tushare client if needed).

**Exit check**:
- Daily and 30m fetch parity verified on sample symbols/date ranges against pre-move outputs (row count, columns, timestamp monotonicity).

## Wave 1C: storage + loader boundary move
6. Move cache/store logic to `storage/parquet_store.py` with root-config abstraction.
7. Move loader API to `access/load.py` and preserve compatibility wrappers in `aShare`.

**Exit check**:
- `aShare` callers import through shim without behavior regressions.
- Cache read/write path works with both neutral and legacy env configuration.

## Wave 1D: stabilization
8. Add dataset inspection minimal API (`access/inspect.py`) over existing storage metadata.
9. Freeze Phase 1 API signatures and document migration notes.

**Exit check**:
- Contract docs and code behavior match; extraction wave can be declared complete.

---

## 6) CORE_MOVE_LATER plan

## `src/ashare/data/tushare_client.py`
- **Target**: `src/market_data_core/providers/tushare_client.py`
- **Prerequisite**: remove hard-coded repo-root `.env` discovery (`parents[3]` style coupling).
- **Suggested approach**: explicit token resolution priority: function arg > env var > optional dotenv load at cwd/data-root.

## `src/ashare/config/settings.py` (cache slice)
- **Target**: `src/market_data_core/core/constants.py` and/or `core/types.py`
- **Prerequisite**: split backtest broker settings from data-root/provider env settings.

## `src/ashare/sanitytests.py`
- **Target**: `src/market_data_core/validation/smoke.py` (optional)
- **Prerequisite**: remove CLI/output formatting coupling.

---

## 7) Risk controls

1. **Schema drift risk**
   - Control: strict validation on write path; explicit schema version in metadata.
2. **Config compatibility risk**
   - Control: temporary support for legacy `ASHARE_*` env vars with deprecation note.
3. **Provider parity risk**
   - Control: sample parity checks per provider/frequency before deleting old code paths.
4. **Boundary leakage risk**
   - Control: ban Backtrader imports in `market-data-core` CI checks.

---

## 8) Phase 1 done criteria

Phase 1 extraction is done when:
1. All CORE_MOVE_NOW modules are moved to target paths listed above.
2. `aShare` consumes moved loaders via compatibility shim or direct imports without behavior regression.
3. Backtrader/feed/strategy/research modules remain in `aShare`.
4. Contract docs listed in Section 2 are reflected in implementation and tests.
5. Open issues for CORE_MOVE_LATER items are tracked with owners before Phase 2 starts.

---

## 9) Open decisions requiring manual judgment before Phase 2

1. Final neutral env var names and deprecation timeline for `ASHARE_*` aliases.
2. Whether adjustment factors are sourced from one provider or merged precedence rules.
3. Whether to materialize adjusted datasets in curated layer by default for 30m workloads.
4. Choice of manifest/catalog backend beyond simple JSON sidecars.
