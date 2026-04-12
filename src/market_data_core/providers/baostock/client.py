"""BaoStock client ownership boundary.

Will own login/session lifecycle only.
"""


def get_client() -> None:
    """Placeholder BaoStock client builder."""
    raise NotImplementedError("BaoStock client wiring is deferred to extraction phase.")
