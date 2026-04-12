"""Load APIs aligned to docs/public_api_draft.md."""


def load_bars(*_: object, **__: object) -> object:
    """Placeholder canonical loader API."""
    raise NotImplementedError("load_bars is deferred to extraction wave 1C.")


def load_daily(*_: object, **__: object) -> object:
    """Convenience wrapper for 1d bars."""
    return load_bars(*_, frequency="1d", **__)


def load_30m(*_: object, **__: object) -> object:
    """Convenience wrapper for 30m bars."""
    return load_bars(*_, frequency="30m", **__)
