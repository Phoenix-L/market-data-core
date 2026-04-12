"""Persistence handoff scaffolding for ingest flow."""


def persist_canonical_frame(*_: object, **__: object) -> None:
    raise NotImplementedError("Persistence handoff is deferred to extraction phase.")
