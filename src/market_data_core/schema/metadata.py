"""Dataset metadata model scaffolding."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetMetadata:
    dataset_id: str
    market: str
    frequency: str
    adjustment_mode: str
    schema_version: int = 1
