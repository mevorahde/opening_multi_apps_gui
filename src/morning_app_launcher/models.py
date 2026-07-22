"""Domain models and path identity helpers."""

from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .errors import InvalidApplicationPath


@dataclass(frozen=True, slots=True)
class Application:
    """A configured application path."""

    path: Path

    @classmethod
    def from_text(cls, value: str) -> Application:
        if not isinstance(value, str) or not value.strip() or "\x00" in value:
            raise InvalidApplicationPath("The application path is invalid.")
        return cls(Path(value.strip()))

    @property
    def identity(self) -> str:
        return os.path.normcase(str(self.path.resolve(strict=False)))


def deduplicate(applications: Iterable[Application]) -> list[Application]:
    """Preserve order while removing path-equivalent entries."""

    result: list[Application] = []
    identities: set[str] = set()
    for application in applications:
        if application.identity not in identities:
            identities.add(application.identity)
            result.append(application)
    return result
