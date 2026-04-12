# Market-Data Migration Inventory (aShare → `market-data-core`)

This inventory focuses on modules that either:
- already implement market-data concerns directly, or
- sit immediately adjacent to the data layer and create coupling risk during extraction.

Bucket legend:
- **CORE_MOVE_NOW**: generic data-layer logic ready to extract in Phase 0/1.
- **CORE_MOVE_LATER**: generic logic, but entangled enough to defer until interfaces stabilize.
- **KEEP_LOCAL**: aShare-specific orchestration, strategy, or Backtrader/runtime glue.
- **UNCLEAR**: not enough evidence yet; needs targeted review.

---

## 1) `src/ashare/data/providers/base.py`
- **Purpose**: Defines abstract provider contract (`DataProvider`) with normalized output schema.
- **Main classes/functions**: `DataProvider.fetch_daily`, `DataProvider.fetch_minute30`.
- **Key inputs/outputs**:
  - Input: `ts_code`, `start_date`, `end_date`.
  - Output: `pd.DataFrame` indexed by datetime with `open/high/low/close/volume/turnover_rate`.
- **Main dependencies/imports**: `abc`, `pandas`.
- **Main downstream consumers**: `src/ashare/data/providers/__init__.py`, concrete providers.
- **Coupling notes**: Interface is generic and reusable; minimal aShare coupling.
- **Initial bucket**: **CORE_MOVE_NOW**.

## 2) `src/ashare/data/providers/__init__.py`
- **Purpose**: Provider factory/registry, env-driven provider selection, singleton lifecycle.
- **Main classes/functions**: `get_provider()`, `reset_provider()`.
- **Key inputs/outputs**:
  - Input: env var `ASHARE_DATA_PROVIDER`.
  - Output: singleton `DataProvider` instance.
- **Main dependencies/imports**: `os`, `DataProvider`, concrete provider modules.
- **Main downstream consumers**: `src/ashare/data/loaders.py`, tests.
- **Coupling notes**: Generic, but env var naming is aShare-branded (`ASHARE_*`).
- **Initial bucket**: **CORE_MOVE_NOW** (rename env var namespace during extraction).

## 3) `src/ashare/data/providers/baostock_provider.py`
- **Purpose**: BaoStock adapter implementing provider contract for daily and 30-minute bars.
- **Main classes/functions**:
  - `BaoStockProvider`
  - `_ensure_login`, `_normalize_code`, `_get_shares_outstanding`
  - `fetch_daily`, `fetch_minute30`
- **Key inputs/outputs**:
  - Input: Tushare-style symbols (`000001.SZ`), date range.
  - Output: normalized OHLCV+turnover DataFrames.
- **Main dependencies/imports**: `baostock`, `pandas`, provider base.
- **Main downstream consumers**: provider factory, loaders.
- **Coupling notes**:
  - Generic provider logic overall.
  - Contains domain assumptions (A-share code formats, turnover derivation heuristics).
- **Initial bucket**: **CORE_MOVE_NOW**.

## 4) `src/ashare/data/providers/tushare_provider.py`
- **Purpose**: Tushare adapter implementing provider contract for daily + 30m bars.
- **Main classes/functions**: `TushareProvider.fetch_daily`, `TushareProvider.fetch_minute30`.
- **Key inputs/outputs**:
  - Input: Tushare symbol/date range.
  - Output: normalized OHLCV+turnover DataFrames.
- **Main dependencies/imports**: `pandas`, `get_pro` from `tushare_client`, provider base.
- **Main downstream consumers**: provider factory, loaders.
- **Coupling notes**:
  - Generic adapter logic.
  - Uses Tushare-specific endpoints (`daily`, `daily_basic`, `stk_mins`).
- **Initial bucket**: **CORE_MOVE_NOW**.

## 5) `src/ashare/data/tushare_client.py`
- **Purpose**: Token/env initialization and client construction for Tushare.
- **Main classes/functions**: `get_pro()`.
- **Key inputs/outputs**:
  - Input: env var `TUSHARE_TOKEN`, `.env` at project root.
  - Output: `ts.pro_api()` client.
- **Main dependencies/imports**: `tushare`, `dotenv`, `pathlib`, `os`.
- **Main downstream consumers**: `tushare_provider.py`.
- **Coupling notes**:
  - Currently assumes aShare repository layout via `_PROJECT_ROOT = parents[3]`.
  - This is extraction-sensitive and should be made package-relative/configurable.
- **Initial bucket**: **CORE_MOVE_LATER** (or NOW with small refactor first).

## 6) `src/ashare/data/cache.py`
- **Purpose**: File-system cache helpers for provider data (parquet).
- **Main classes/functions**:
  - `_cache_file_path`
  - `cache_exists`, `load_from_cache`, `save_to_cache`
- **Key inputs/outputs**:
  - Input: `(provider, symbol, frequency, start, end)` key tuple + DataFrame.
  - Output: cached parquet path/DataFrame.
- **Main dependencies/imports**: `pathlib`, `pandas`, `ashare.config.settings.get_cache_dir`.
- **Main downstream consumers**: `loaders.py`, tests.
- **Coupling notes**:
  - Strongly reusable cache mechanism.
  - Coupled to aShare config namespace (`get_cache_dir`, env name).
- **Initial bucket**: **CORE_MOVE_NOW** (extract with config abstraction).

## 7) `src/ashare/data/loaders.py`
- **Purpose**: Public market-data API for this repo: load daily/30m with cache + schema validation.
- **Main classes/functions**:
  - `_provider_name`, `_validate_loaded_frame`
  - `load_daily`, `load_minute_30`
- **Key inputs/outputs**:
  - Input: symbol + date range + `use_cache`.
  - Output: validated normalized DataFrame.
- **Main dependencies/imports**: `pandas`, cache helpers, provider factory, `os`.
- **Main downstream consumers**:
  - CLI (`backtest`, `data fetch-ohlcv`),
  - experiment executor,
  - walk-forward,
  - sanity tests,
  - many test modules.
- **Coupling notes**:
  - This is the current central data access boundary.
  - Mostly generic, but function names and env constants are aShare-specific.
- **Initial bucket**: **CORE_MOVE_NOW**.

## 8) `src/ashare/data/normalizers.py`
- **Purpose**: Converts normalized pandas data into Backtrader feed objects.
- **Main classes/functions**: `PandasDataWithTurnover`, `to_backtrader_feed`.
- **Key inputs/outputs**:
  - Input: normalized OHLCV DataFrame.
  - Output: `bt.feeds.PandasData` (Backtrader-specific).
- **Main dependencies/imports**: `backtrader`, `pandas`, `re`.
- **Main downstream consumers**: `engine/runner.py`, tests.
- **Coupling notes**:
  - Explicitly tied to Backtrader runtime.
  - Violates target-scope rule for core repo (“should NOT own Backtrader adapters”).
- **Initial bucket**: **KEEP_LOCAL**.

## 9) `src/ashare/config/settings.py` (data-adjacent slice)
- **Purpose**: Global app settings; includes `get_cache_dir()` used by data cache.
- **Main classes/functions**: `get_cache_dir`, `BacktestConfig`.
- **Key inputs/outputs**:
  - Input: env `ASHARE_CACHE_DIR`.
  - Output: cache path string.
- **Main dependencies/imports**: `os`, `dataclasses`.
- **Main downstream consumers**:
  - Data cache uses `get_cache_dir`.
  - Engine/broker uses `BacktestConfig`.
- **Coupling notes**:
  - Mixed module: cache config (generic) + backtest broker settings (local).
- **Initial bucket**: **CORE_MOVE_LATER** (split required).

## 10) `src/ashare/sanitytests.py`
- **Purpose**: Integration checks for loader outputs/schemas.
- **Main classes/functions**:
  - `SanityCheckResult`
  - `run_loader_sanity_check`, `sanitycheck_daily`, `sanitycheck_minute30`
- **Key inputs/outputs**:
  - Input: loader args.
  - Output: structured pass/fail plus optional DataFrame.
- **Main dependencies/imports**: `pandas`, dataclasses, `ashare.data.loaders`.
- **Main downstream consumers**: CLI `sanitytest` commands.
- **Coupling notes**:
  - Mostly generic loader validation patterns.
  - Entrypoints and messaging are currently aShare CLI-oriented.
- **Initial bucket**: **CORE_MOVE_LATER** (portable checks, but optional for Phase 0).

## 11) `src/ashare/cli.py` (data command slices)
- **Purpose**: User CLI entrypoint, includes data fetch/export command.
- **Main classes/functions (data-adjacent)**:
  - `data` click group
  - `fetch_ohlcv`
  - `_normalize_research_ohlcv`
- **Key inputs/outputs**:
  - Input: ticker/date/timeframe/options.
  - Output: CSVs under `data/research/ohlcv`, optional regime pipeline trigger.
- **Main dependencies/imports**: `click`, data loaders, research runner loading.
- **Main downstream consumers**: human operators, research pipeline.
- **Coupling notes**:
  - Highly aShare orchestration and folder-layout specific.
  - Not suitable for `market-data-core` runtime package.
- **Initial bucket**: **KEEP_LOCAL**.

## 12) `src/ashare/experiment/executor.py` (data ingestion touchpoint)
- **Purpose**: Experiment execution orchestrator.
- **Main data-layer touchpoint**: `symbol_data = {symbol: load_minute_30(...)}`.
- **Main dependencies/imports**: loaders + engine + experiment/report stack.
- **Main downstream consumers**: CLI experiment command, research workflow.
- **Coupling notes**: pure consumer of data API; strategy/experiment-specific.
- **Initial bucket**: **KEEP_LOCAL**.

## 13) `src/ashare/research/walk_forward.py` (data ingestion touchpoint)
- **Purpose**: Walk-forward optimization workflow.
- **Main data-layer touchpoint**: `full_df = load_minute_30(...)` then train/test slicing.
- **Main dependencies/imports**: loaders, engine runner, research utilities.
- **Coupling notes**: consumer only; research-specific orchestration.
- **Initial bucket**: **KEEP_LOCAL**.

## 14) `src/ashare/engine/runner.py` (normalizer consumer)
- **Purpose**: Backtest execution against Backtrader.
- **Main data-layer touchpoint**: `to_backtrader_feed(data_df, name=symbol)`.
- **Coupling notes**:
  - Backtrader runtime adapter boundary should remain in aShare.
  - Indicates where market-data-core boundary should stop (DataFrame API, before feed conversion).
- **Initial bucket**: **KEEP_LOCAL**.

## 15) `research/regime_state_machine/*.py` (adjacent research data usage)
- **Purpose**: Research-only feature engineering and state machine over exported OHLCV CSVs.
- **Main classes/functions**:
  - `regime_backtest.py`: `load_ohlcv_csv`, `run_regime_backtest`
  - `regime_features.py`: `validate_ohlcv`, `compute_regime_features`
  - `regime_rules.py`: state classification rules
- **Key inputs/outputs**: CSV-based `datetime/open/high/low/close/volume` flows.
- **Main dependencies/imports**: pandas/numpy; local research modules.
- **Coupling notes**:
  - May contain reusable validation/feature ideas.
  - Currently research-specific and not part of production data layer.
- **Initial bucket**: **UNCLEAR** (keep local for now; evaluate later as separate analytics package candidate).

---

## Split-required (identified during inventory)

1. **`src/ashare/config/settings.py`**
   - Split cache config from backtest broker config.
   - Generic slice: cache directory resolution.
   - Local slice: `BacktestConfig` and broker assumptions.

2. **`src/ashare/data/normalizers.py` vs `src/ashare/data/loaders.py` boundary**
   - Keep Backtrader feed adapter local.
   - Ensure extracted core exposes DataFrame-only API and no Backtrader dependency.

3. **`src/ashare/data/tushare_client.py`**
   - Remove hard-coded repo-root `.env` traversal (`parents[3]`), replace with explicit configuration in extracted package.
