"""Tushare client ownership boundary.

Will own token resolution and API client construction without repo-relative assumptions.
"""


def get_client() -> None:
    raise NotImplementedError("Tushare client wiring is deferred to extraction phase.")
