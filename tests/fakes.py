from __future__ import annotations

from dataclasses import dataclass, field

from morning_app_launcher.models import Application
from morning_app_launcher.operational_logging import OperationalEvent


@dataclass
class FakeStore:
    applications: list[Application] = field(default_factory=list)
    save_calls: list[list[Application]] = field(default_factory=list)
    configuration_exists: bool = False

    def exists(self) -> bool:
        return self.configuration_exists

    def load(self) -> list[Application]:
        return list(self.applications)

    def save(self, applications: list[Application]) -> None:
        self.applications = list(applications)
        self.save_calls.append(list(applications))
        self.configuration_exists = True


@dataclass
class FakeLauncher:
    launched: list[Application] = field(default_factory=list)

    def launch(self, application: Application) -> None:
        self.launched.append(application)


@dataclass
class FakeEventLogger:
    events: list[tuple[OperationalEvent, dict[str, int]]] = field(default_factory=list)
    close_calls: int = 0

    def event(self, event: OperationalEvent, **counts: int) -> None:
        self.events.append((event, counts))

    def close(self) -> None:
        self.close_calls += 1
