"""Provider registry with compatibility env behavior."""

from __future__ import annotations

import os
from typing import Callable

from market_data_core.core.enums import Provider
from market_data_core.core.exceptions import ProviderError
from .base import DataProvider

ProviderFactory = Callable[[], DataProvider]

_PROVIDER_INSTANCE: DataProvider | None = None
_PROVIDER_FACTORIES: dict[str, ProviderFactory] = {}


def _provider_name_from_env() -> str:
    return os.getenv("MARKET_DATA_PROVIDER", os.getenv("ASHARE_DATA_PROVIDER", Provider.BAOSTOCK.value)).lower()


def register_provider(name: str, factory: ProviderFactory) -> None:
    """Register a provider factory by normalized name."""
    _PROVIDER_FACTORIES[name.lower()] = factory


def get_provider(name: str | None = None) -> DataProvider:
    """Return singleton provider instance.

    If `name` is None, provider name is resolved from environment.
    """
    global _PROVIDER_INSTANCE
    resolved = (name or _provider_name_from_env()).lower()
    if _PROVIDER_INSTANCE is not None and _PROVIDER_INSTANCE.name.lower() == resolved:
        return _PROVIDER_INSTANCE

    factory = _PROVIDER_FACTORIES.get(resolved)
    if factory is None:
        raise ProviderError(
            f"Unsupported provider: {resolved}. "
            f"Registered providers: {sorted(_PROVIDER_FACTORIES.keys()) or 'none'}"
        )

    _PROVIDER_INSTANCE = factory()
    return _PROVIDER_INSTANCE


def reset_provider() -> None:
    """Reset provider singleton for tests and process-local reconfiguration."""
    global _PROVIDER_INSTANCE
    _PROVIDER_INSTANCE = None
