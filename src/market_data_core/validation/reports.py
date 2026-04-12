"""Validation report dataclass used by access and ingest layers."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, int | float] = field(default_factory=dict)
