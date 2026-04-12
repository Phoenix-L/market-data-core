"""Shared exception hierarchy."""


class MarketDataCoreError(Exception):
    """Base exception for market-data-core errors."""


class ContractError(MarketDataCoreError):
    """Raised when a DataFrame violates the canonical contract."""


class ProviderError(MarketDataCoreError):
    """Raised for provider adapter/client errors."""


class NotReadyError(MarketDataCoreError):
    """Raised by placeholder modules that are intentional stubs."""
