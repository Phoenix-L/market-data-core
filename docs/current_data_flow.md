# Current Data Flow in `aShare`

## High-level flow (concise)

1. **Entry points call loaders**
   - CLI backtest/data commands, experiment executor, and walk-forward call `load_daily` / `load_minute_30`.
2. **Loader resolves provider and cache**
   - Loader picks provider (`baostock` or `tushare`) via env and singleton factory.
   - Loader checks cache path by `(provider, symbol, frequency, start, end)`.
3. **Provider fetch + normalize**
   - Provider adapter fetches raw vendor data and normalizes to canonical columns/index.
4. **Loader validation + optional persistence**
   - Loader validates required schema (`open/high/low/close/volume/turnover_rate`, datetime index) and writes cache.
5. **Downstream consumption**
   - Strategy/backtest paths consume normalized DataFrames.
   - Backtrader runner converts DataFrame to Backtrader feed (`to_backtrader_feed`) and may resample to daily feed in-engine.

---

## Detailed narrative

### 1) Fetch/ingestion entry points

Primary ingestion entrypoints are:
- `ashare.cli backtest` → `load_minute_30(...)`
- `ashare.cli data fetch-ohlcv` → `load_daily(...)` or `load_minute_30(...)`
- `ashare.experiment.executor.execute_experiment_spec` → bulk `load_minute_30(...)` by symbol
- `ashare.research.walk_forward.run_walk_forward` → one `load_minute_30(...)` then date slicing
- `ashare.sanitytests` wrappers call both loaders for integration checks

These all centralize on `src/ashare/data/loaders.py`, making it the practical ingestion façade.

### 2) Provider selection and lifecycle

`src/ashare/data/providers/__init__.py` selects provider using `ASHARE_DATA_PROVIDER` (default `baostock`).
- Factory lazily initializes singleton provider instance.
- `reset_provider()` exists for tests and provider switching scenarios.

### 3) Cache path and read/write behavior

`src/ashare/data/cache.py` builds cache file path:

`<cache_root>/<provider>/<symbol>/<frequency>/<start>_<end>.parquet`

Where `cache_root` comes from `get_cache_dir()` in `config/settings.py` (env override `ASHARE_CACHE_DIR`).

Loader behavior:
- If `use_cache=True` and cache exists → read parquet and validate schema.
- Otherwise fetch from provider, validate, then write parquet (best effort; parquet engine ImportError is swallowed).

### 4) Normalization and validation

Normalization currently happens mostly in provider adapters:
- Rename provider-specific columns to canonical names.
- Parse/construct datetime index.
- Sort index ascending.
- Attach/derive `turnover_rate`.

Validation occurs in loader `_validate_loaded_frame(...)`:
- non-empty DataFrame
- required columns present
- index is `DatetimeIndex`
- sorted ascending (sorts if needed)

### 5) Provider-specific details

#### BaoStock path
- Converts code format `000001.SZ` → `sz.000001`.
- Daily bars: `query_history_k_data_plus(... frequency='d')`.
- 30m bars: `query_history_k_data_plus(... frequency='30')`.
- Turnover logic:
  - Preferred: derive from shares outstanding (`query_profit_data`) and volume.
  - Minute bars map daily turnover onto intraday bars; fallback heuristic if daily fetch fails.
- Maintains login/logout session state.

#### Tushare path
- Uses tokenized `pro_api` client from `tushare_client.get_pro()`.
- Daily bars: merge `daily` and `daily_basic(turnover_rate)`.
- 30m bars: fetch `stk_mins(freq='30min')`, map `daily_basic.turnover_rate` by date and ffill.

### 6) Resampling/alignment location

Resampling for strategy execution is currently **not** in data loaders/providers.
- In `engine.runner.run_backtest`, after converting DataFrame to Backtrader feed, engine optionally calls `cerebro.resampledata(... Days, 1)` for strategies needing daily MA logic.

This is a key architectural boundary: runtime/backtesting resampling is coupled to Backtrader, not generic data utilities.

### 7) Storage/export/read paths beyond cache

- Data utility command (`data fetch-ohlcv`) exports normalized DataFrames to CSV under `data/research/ohlcv`.
- Optional regime pipeline reads those CSVs via `research/regime_state_machine/regime_backtest.py`.
- This export pipeline is research orchestration and path-convention-heavy; it is not core provider/cache infrastructure.

---

## Recommended clean boundary for `market-data-core`

### Should be inside `market-data-core`
- Provider contract + provider registry/factory.
- BaoStock/Tushare provider adapters.
- Canonical schema enforcement and validation.
- Cache keying + filesystem cache helper abstractions.
- DataFrame-centric loader API (daily/30m + future frequencies).

### Should remain in `aShare`
- Backtrader feed conversion (`to_backtrader_feed`, custom feed lines).
- Engine-runner resampling tied to Backtrader execution graph.
- Strategy/experiment/research orchestration and output folder conventions.
- CLI commands that orchestrate strategy workflows and regime research pipeline.

### Boundary contract (recommended)
- **Input into aShare runtime**: canonical `pd.DataFrame` market bars from `market-data-core`.
- **Output from data-core**: no engine objects, no strategy objects, no experiment artifacts.
