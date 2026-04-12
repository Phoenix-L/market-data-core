# Proposed Repository Structure (`market-data-core`)

## 1) Top-level structure

```text
market-data-core/
  pyproject.toml
  README.md
  docs/
  src/
  tests/
  scripts/
  .data/                  # local dev only (gitignored)
```

Notes:
- Keep repository minimal; avoid adding app-specific folders from `aShare`.
- `scripts/` is optional for operational utilities (backfill, validation runs).

---

## 2) `src/` package structure

```text
src/market_data_core/
  __init__.py
  core/
    __init__.py
    errors.py
    types.py
    constants.py

  schema/
    __init__.py
    canonical.py
    contracts.py

  providers/
    __init__.py
    base.py
    registry.py
    baostock.py
    tushare.py
    tushare_client.py      # may be placeholder until split complete

  clean/
    __init__.py
    normalize.py

  calendar/
    __init__.py
    sessions.py
    align.py

  validation/
    __init__.py
    bars.py
    report.py

  transform/
    __init__.py
    resample.py
    adjust.py

  storage/
    __init__.py
    layout.py
    manifest.py
    parquet_store.py

  ingest/
    __init__.py
    bars.py

  access/
    __init__.py
    load.py
    inspect.py

  cli/
    __init__.py
    main.py
```

---

## 3) `docs/` structure

```text
docs/
  module_inventory.md          # existing Phase 0 input
  current_data_flow.md         # existing Phase 0 input
  extraction_rules.md          # existing Phase 0 input
  migration_blueprint.md       # updated plan of record

  architecture.md
  canonical_bar_contract.md
  calendar_policy.md
  adjustment_policy.md
  storage_layout.md
  public_api_draft.md
  repo_structure.md
```

---

## 4) `tests/` structure

```text
tests/
  contract/
    test_canonical_contract.py
    test_calendar_alignment.py
  providers/
    test_provider_registry.py
    test_baostock_adapter.py
    test_tushare_adapter.py
  storage/
    test_parquet_store.py
    test_manifest.py
  access/
    test_load_daily.py
    test_load_30m.py
  integration/
    test_ingest_to_load_smoke.py
```

Testing priorities:
- Contract and invariants first.
- Provider adapters second.
- End-to-end ingest/load smoke third.

---

## 5) Modules to create first vs placeholders

## Create first (implementation-ready in extraction wave 1)
1. `providers/base.py`
2. `providers/registry.py` (or `providers/__init__.py` factory)
3. `providers/baostock.py`
4. `providers/tushare.py`
5. `storage/parquet_store.py` (cache + canonical persistence)
6. `validation/bars.py`
7. `access/load.py`
8. `schema/canonical.py`

## Keep as placeholders in early phases
- `transform/adjust.py` (interface only if factor pipeline not moved yet)
- `ingest/bars.py` (thin wrapper initially)
- `cli/main.py` (optional minimal commands)
- `providers/tushare_client.py` (placeholder until split from aShare path assumptions)

---

## 6) Packaging and namespace guidance

- Use package name: `market_data_core`.
- Keep imports absolute within package.
- Avoid compatibility aliases in deep modules; isolate legacy shims in `access/load.py` if needed.

This structure keeps scope narrow and supports safe phased extraction from `aShare`.
