"""BaoStock client ownership boundary.

This module owns BaoStock SDK lifecycle concerns only.
"""

from __future__ import annotations

from typing import Any

from market_data_core.core.exceptions import ProviderError


class BaoStockSession:
    """Small wrapper to ensure logout is always attempted."""

    def __init__(self, bs_module: Any):
        self._bs = bs_module

    def __enter__(self) -> Any:
        login_result = self._bs.login()
        code = str(getattr(login_result, "error_code", "0"))
        if code not in {"0", "0000"}:
            msg = str(getattr(login_result, "error_msg", "unknown login error"))
            raise ProviderError(f"BaoStock login failed: {msg}")
        return self._bs

    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            self._bs.logout()
        except Exception:
            # Never mask the primary exception.
            pass
        return False


def get_client() -> BaoStockSession:
    """Return a managed BaoStock session context manager."""
    try:
        import baostock as bs  # type: ignore
    except ModuleNotFoundError as exc:
        raise ProviderError("BaoStock SDK is not installed.") from exc

    return BaoStockSession(bs)
