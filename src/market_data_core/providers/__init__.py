"""Public provider boundary.

Phase 6 stable exports in this module are limited to:
- provider interface type (`DataProvider`)
- registry lifecycle helpers (`register_provider`, `get_provider`, `reset_provider`)

Concrete SDK adapters under `providers.baostock` and `providers.tushare` are
intentionally deferred.
"""

from .base import DataProvider
from .registry import get_provider, register_provider, reset_provider

__all__ = ["DataProvider", "get_provider", "register_provider", "reset_provider"]
