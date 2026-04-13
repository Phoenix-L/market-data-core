"""BaoStock provider package."""

from __future__ import annotations

from market_data_core.providers.registry import register_provider

from .provider import BaoStockProvider


def register_builtin() -> None:
    """Register BaoStock provider factory in the global registry."""
    register_provider("baostock", BaoStockProvider)


__all__ = ["BaoStockProvider", "register_builtin"]
