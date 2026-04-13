# Public API Contract (Phase 6)

## Status

This document now represents the Phase 6 **contract-locked** public API.

Implemented and stable:
- `market_data_core.access`
- `market_data_core.validation`
- `market_data_core.calendar`
- `market_data_core.storage`
- `market_data_core.providers` (registry boundary only)

Deferred (not stable):
- `market_data_core.ingest`
- `market_data_core.transform`
- concrete SDK adapters under provider subpackages

## 1) Stable load APIs (implemented)

```python
from market_data_core.access import load_bars, load_daily, load_30m, load_minute_30
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
    """Load canonical bars with strict validation via Cache Mode pathing."""
```

Compatibility wrappers:
- `load_daily(...)` → `frequency="1d"`
- `load_30m(...)` → `frequency="30m"`
- `load_minute_30(...)` compatibility alias for `aShare` migration path

## 2) Stable validation APIs (implemented)

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
    """Validate schema, invariants, and CN A-share session alignment."""
```

`ValidationReport` fields:
- `ok: bool`
- `errors: list[str]`
- `warnings: list[str]`
- `stats: dict[str, int | float]`

## 3) Stable dataset metadata APIs (implemented)

```python
from market_data_core.access import list_datasets, inspect_dataset
```

```python
def list_datasets(data_root: str | None = None) -> list[str]:
    """List dataset ids discovered from storage manifests."""
```

```python
def inspect_dataset(dataset_id: str, data_root: str | None = None) -> dict[str, object]:
    """Return latest manifest payload for dataset id."""
```

## 4) Stable calendar/session APIs (implemented)

```python
from market_data_core.calendar import session_open_anchors, is_session_aligned
```

## 5) Storage mode contract

Two explicitly documented modes:
1. **Cache Mode (active in Phase 6)**
   - used by `load_bars`
   - `<data_root>/<provider>/<symbol>/<frequency>/<start>_<end>.parquet`
2. **Canonical Dataset Mode (future phase)**
   - partition + manifest model
   - not used by `load_bars` yet

## 6) Stability policy

- APIs listed above are Phase 6 stable for consumer repos.
- New parameters must be additive with safe defaults.
- Breaking changes require migration notes and compatibility strategy.
