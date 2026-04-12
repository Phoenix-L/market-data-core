# Extraction Rules: `aShare` → `market-data-core`

## 1) What counts as “data layer” in this migration

Data layer includes logic that is:
- provider-facing (vendor API adapters, auth/client setup),
- schema-facing (canonical OHLCV(+extensions), type/index normalization, validation),
- time/calendar-facing (session handling, frequency conversion, resampling primitives),
- storage-facing (cache/read/write helpers for market bars),
- API-facing for data access (`load_*` functions or reusable service classes returning DataFrames).

Data layer **excludes** execution engine, strategy behavior, experiment/report orchestration, and any Backtrader object wiring.

---

## 2) What must move to `market-data-core`

1. Provider abstractions and registry/factory behavior.
2. BaoStock and Tushare adapters that output canonical DataFrames.
3. Canonical schema validation currently in loader-level checks.
4. Cache helpers and cache key conventions (with configurable root/env naming).
5. Reusable DataFrame loader API currently represented by `load_daily` and `load_minute_30`.

---

## 3) What must stay local in `aShare`

1. Backtrader adapters:
   - `PandasDataWithTurnover`
   - `to_backtrader_feed`
2. Engine-runner resampling tied to Backtrader graph semantics.
3. Strategy and signal logic.
4. Experiment orchestration and output pointer maintenance.
5. CLI flows tightly coupled to aShare runtime and research folder conventions.

---

## 4) Temporary rules during migration

1. **No behavior drift**
   - Keep current output schema and semantics stable during Phase 0.
2. **Compatibility shim first**
   - In aShare, introduce import shim layer if needed:
     - `ashare.data.loaders` re-exporting from `market_data_core`.
3. **One boundary object type**
   - Cross-repo boundary uses pandas DataFrame only (no Backtrader classes).
4. **Preserve env compatibility initially**
   - Support `ASHARE_DATA_PROVIDER` / `ASHARE_CACHE_DIR` temporarily; add neutral aliases later.
5. **Split before move when mixed concerns exist**
   - Example: separate cache config from backtest config before extraction.

---

## 5) Anti-patterns to avoid

1. Moving Backtrader dependencies into data-core.
2. Embedding aShare path conventions (`outputs/`, `data/research/ohlcv`) inside generic data package.
3. Letting provider adapters import strategy/engine modules.
4. Duplicating normalization rules in both repos (single source of truth required).
5. Hidden singleton/global state without reset hooks (hurts tests and multi-context usage).
6. Hard-coded repository-root assumptions (e.g., `.env` discovery based on parent-depth traversal).

---

## 6) Generic vs aShare-local examples

### Generic (move)
- `DataProvider` interface.
- Provider factory + registration.
- `fetch_daily` / `fetch_minute30` normalization logic.
- Cache key + parquet persistence helpers.
- Loader schema checks for OHLCV + `turnover_rate` + datetime index.

### aShare-local (keep)
- Converting DataFrame to `bt.feeds.PandasData`.
- Backtrader-specific timeframe inference for feed metadata.
- Strategy-specific data expectations enforced in runtime execution.
- CLI command that fetches CSV and then auto-runs regime backtest in local research folders.

---

## 7) Rule for ambiguous modules

If a module has both generic and local concerns:
1. Extract only pure data primitives first.
2. Keep orchestration/runtime code in aShare.
3. Add TODO markers and explicit split tickets.
4. Classify as `CORE_MOVE_LATER` until split is complete.
