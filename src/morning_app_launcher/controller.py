"""Use cases shared by the GUI and isolated tests."""

from __future__ import annotations

from pathlib import Path

from .errors import DuplicateApplication, InvalidApplicationPath, InvalidSelection
from .launcher import ApplicationLauncher
from .models import Application, deduplicate
from .storage import ApplicationStore


class ApplicationController:
    def __init__(self, store: ApplicationStore, launcher: ApplicationLauncher) -> None:
        self._store = store
        self._launcher = launcher
        self._applications: list[Application] = []

    def load(self) -> tuple[Application, ...]:
        self._applications = deduplicate(self._store.load())
        return self.list_applications()

    def list_applications(self) -> tuple[Application, ...]:
        return tuple(self._applications)

    def add(self, path: Path) -> Application:
        application = Application.from_text(str(path))
        if not path.is_absolute() or not path.exists() or not path.is_file():
            raise InvalidApplicationPath("The selected application is missing or invalid.")
        if any(existing.identity == application.identity for existing in self._applications):
            raise DuplicateApplication("The selected application is already in the list.")
        updated = [*self._applications, application]
        self._store.save(updated)
        self._applications = updated
        return application

    def remove(self, index: int) -> Application:
        if index < 0 or index >= len(self._applications):
            raise InvalidSelection("Select an application to remove.")
        removed = self._applications[index]
        updated = [
            application
            for position, application in enumerate(self._applications)
            if position != index
        ]
        self._store.save(updated)
        self._applications = updated
        return removed

    def launch_one(self, index: int) -> None:
        if index < 0 or index >= len(self._applications):
            raise InvalidSelection("Select an application to open.")
        self._launcher.launch(self._applications[index])

    def launch_all(self) -> None:
        if not self._applications:
            raise InvalidSelection("Add an application before opening the list.")
        for application in self._applications:
            self._launcher.launch(application)
