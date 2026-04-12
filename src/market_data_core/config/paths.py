"""Path resolution helpers for storage/access modules."""

from pathlib import Path
from .settings import CoreSettings


def resolve_data_root(settings: CoreSettings | None = None) -> Path:
    """Resolve the shared data root for canonical datasets."""
    cfg = settings or CoreSettings()
    return Path(cfg.market_data_root)
