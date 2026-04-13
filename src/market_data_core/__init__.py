"""Top-level package exports for market-data-core.

Phase 6 policy:
- Only package identity constants are exported at the root.
- Stable runtime APIs live in explicit public modules (`access`, `validation`,
  `calendar`, `storage`, `providers`).
"""

from .core.constants import PACKAGE_NAME, PACKAGE_VERSION

__all__ = ["PACKAGE_NAME", "PACKAGE_VERSION"]
