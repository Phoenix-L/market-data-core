"""Public provider boundary.

Phase 6 stable exports in this module are limited to:
- provider interface type (`DataProvider`)
- registry lifecycle helpers (`register_provider`, `get_provider`, `reset_provider`)

Concrete SDK adapters under `providers.baostock` and `providers.tushare` are
kept internal to preserve stable boundaries.
"""

from .base import DataProvider
from .registry import get_provider, register_provider, reset_provider

# Register built-in provider factories.
from .baostock import register_builtin as _register_baostock_builtin

_register_baostock_builtin()

__all__ = ["DataProvider", "get_provider", "register_provider", "reset_provider"]
