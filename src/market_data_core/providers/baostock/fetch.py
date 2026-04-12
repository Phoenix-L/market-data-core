"""BaoStock fetch orchestration scaffolding.

TODO: split daily vs 30m fetch paths and keep API-free pure mapping where possible.
"""


def fetch_bars(*_: object, **__: object) -> object:
    raise NotImplementedError("BaoStock fetch is deferred to extraction phase.")
