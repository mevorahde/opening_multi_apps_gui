from __future__ import annotations

import os
from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True)
def forbid_real_startfile(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    def forbidden_startfile(_path: str) -> None:
        raise AssertionError("A test attempted to call the real operating-system launcher.")

    monkeypatch.setattr(os, "startfile", forbidden_startfile, raising=False)
    yield
