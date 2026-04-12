"""Provider registry with compatibility env behavior."""

from __future__ import annotations
import os
from typing import Optional

from market_data_core.core.exceptions import ProviderError
from market_data_core.core.enums import Provider
from .base import DataProvider

_PROVIDER_INSTANCE: Optional[DataProvider] = None


def _provider_name_from_env() -> str:
    return os.getenv("MARKET_DATA_PROVIDER", os.getenv("ASHARE_DATA_PROVIDER", Provider.BAOSTOCK.value)).lower()


def get_provider() -> DataProvider:
    """Return singleton provider instance.

    TODO(phase2): wire concrete provider constructors after extraction.
    """
    global _PROVIDER_INSTANCE
    if _PROVIDER_INSTANCE is None:
        name = _provider_name_from_env()
        if name not in {Provider.BAOSTOCK.value, Provider.TUSHARE.value}:
            raise ProviderError(f"Unsupported provider: {name}")
        raise NotImplementedError("Provider wiring is pending extraction in a later phase.")
    return _PROVIDER_INSTANCE


def reset_provider() -> None:
    """Reset provider singleton for tests and process-local reconfiguration."""
    global _PROVIDER_INSTANCE
    _PROVIDER_INSTANCE = None
