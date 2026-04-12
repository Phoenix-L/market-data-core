# Public API Draft (Phase 1)

## Goals
- Keep API surface small and stable.
- Return pandas DataFrames only.
- Separate ingest/write concerns from read/load concerns.

Namespace shown as `market_data_core`.

---

## 1) Ingest APIs

```python
from market_data_core.ingest import ingest_bars
```

```python
def ingest_bars(
    symbol: str,
    start: str,
    end: str,
    frequency: str,
    provider: str | None = None,
    write_layer: str = "canonical",
    data_root: str | None = None,
    validate_strict: bool = True,
) -> "IngestResult":
    """Fetch from provider, normalize, validate, and persist."""
```

`IngestResult` should include:
- resolved provider
- row counts fetched/written
- output dataset path(s)
- validation summary

---

## 2) Load APIs

```python
from market_data_core.access import load_bars, load_daily, load_30m
```

```python
def load_bars(
    symbol: str,
    start: str,
    end: str,
    frequency: str,
    adjustment: str = "raw",
    source_preference: str = "canonical",
    provider: str | None = None,
    use_cache: bool = True,
    data_root: str | None = None,
) -> pd.DataFrame:
    """Load canonical bars with optional read-time adjustment."""
```

Convenience wrappers:
- `load_daily(...)` → `frequency="1d"`
- `load_30m(...)` → `frequency="30m"`

Compatibility rule:
- Maintain close behavior to current `aShare` `load_daily` / `load_minute_30` in Phase 1.

---

## 3) Validation APIs

```python
from market_data_core.validation import validate_bars
```

```python
def validate_bars(
    df: pd.DataFrame,
    frequency: str,
    market: str = "cn_equity",
    strict: bool = True,
) -> "ValidationReport":
    """Validate canonical bar contract and calendar alignment."""
```

`ValidationReport`:
- `ok: bool`
- `errors: list[str]`
- `warnings: list[str]`
- `stats: dict[str, int | float]`

---

## 4) Transform APIs

```python
from market_data_core.transform import resample_bars, apply_adjustment
```

```python
def resample_bars(
    df: pd.DataFrame,
    to_frequency: str,
    market: str = "cn_equity",
    session_policy: str = "strict",
) -> pd.DataFrame:
    """Session-aware OHLCV resampling."""
```

```python
def apply_adjustment(
    df: pd.DataFrame,
    mode: str,
    factors: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Apply raw/qfq/hfq adjustment while preserving contract."""
```

---

## 5) Dataset inspection APIs

```python
from market_data_core.access import inspect_dataset, list_datasets
```

```python
def list_datasets(data_root: str | None = None) -> list[str]:
    """List available dataset ids."""
```

```python
def inspect_dataset(
    dataset_id: str,
    data_root: str | None = None,
) -> "DatasetProfile":
    """Return metadata profile (coverage, symbols, schema, freshness)."""
```

`DatasetProfile` should include:
- dataset metadata contract fields from `storage_layout.md`
- sample schema
- min/max timestamps
- symbol coverage summary

---

## 6) Deliberate exclusions from public API

- Backtrader feed conversion.
- Strategy-oriented feature generation.
- Experiment orchestration helpers.
- Research report generation.

---

## 7) Stability policy

- Functions above become Phase 1 "supported" surface.
- New parameters must be additive with safe defaults.
- Breaking signature changes require a documented migration note.
