"""Parquet store placeholder.

No heavy persistence behavior is implemented in bootstrap phase.
"""


def read_bars(*_: object, **__: object) -> object:
    raise NotImplementedError("Parquet read implementation is deferred.")


def write_bars(*_: object, **__: object) -> object:
    raise NotImplementedError("Parquet write implementation is deferred.")
