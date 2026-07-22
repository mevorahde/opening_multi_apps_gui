"""Application-launching boundary and Windows implementation."""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Protocol

from .errors import InvalidApplicationPath, LaunchError
from .models import Application


class ApplicationLauncher(Protocol):
    def launch(self, application: Application) -> None:
        """Open one application or raise a safe application error."""


class WindowsApplicationLauncher:
    """Validate and open applications using the Windows shell."""

    def __init__(self, start_file: Callable[[str], None] | None = None) -> None:
        self._start_file = start_file

    def launch(self, application: Application) -> None:
        path = application.path
        if not path.is_absolute() or not path.exists() or not path.is_file():
            raise InvalidApplicationPath("The selected application is missing or invalid.")
        try:
            if self._start_file is not None:
                self._start_file(str(path))
            else:
                os.startfile(str(path))
        except OSError as exc:
            raise LaunchError("Windows could not open the selected application.") from exc
