# Consumer API Guide (Phase 6)

This guide documents what downstream repos can rely on today.

## Install

```bash
pip install -e .
```

For tests/examples:

```bash
pip install -e .[dev]
```

## Stable public modules

- `market_data_core.access`
- `market_data_core.validation`
- `market_data_core.calendar`
- `market_data_core.storage`
- `market_data_core.providers` (registry + interface)

## Load bars

Use `load_bars` (or wrappers `load_daily`, `load_30m`, `load_minute_30`).

Important:
- Phase 6 load path uses Cache Mode storage.
- A registered provider implementation is required.

## Validate data

Use `validate_bars(df, frequency, strict=True)`.

- `strict=True`: contract violations are errors.
- `strict=False`: selected issues are warnings.

## Inspect datasets

Use:
- `list_datasets(data_root=...)`
- `inspect_dataset(dataset_id, data_root=...)`

These APIs read manifest sidecars discovered under the data root.

## Guaranteed vs not guaranteed

Guaranteed in Phase 6:
- public function names exported from stable modules,
- strict validation behavior,
- calendar anchor behavior for `1d`/`30m`,
- manifest inspection/listing behavior.

Not guaranteed in Phase 6:
- concrete provider SDK adapters,
- ingest pipelines,
- transform/resample/adjust implementation,
- canonical partition read path through `load_bars`.
