from __future__ import annotations

from pathlib import Path

import pytest

from morning_app_launcher.controller import ApplicationController
from morning_app_launcher.errors import (
    DuplicateApplication,
    InvalidApplicationPath,
    InvalidSelection,
)
from morning_app_launcher.models import Application

from .fakes import FakeLauncher, FakeStore


def make_controller() -> tuple[ApplicationController, FakeStore, FakeLauncher]:
    store = FakeStore()
    launcher = FakeLauncher()
    return ApplicationController(store, launcher), store, launcher


def test_load_list_add_and_remove(tmp_path: Path) -> None:
    controller, store, _launcher = make_controller()
    application_path = tmp_path / "app.exe"
    application_path.touch()

    assert controller.load() == ()
    added = controller.add(application_path)

    assert added == Application(application_path)
    assert controller.list_applications() == (added,)
    assert store.applications == [added]
    assert controller.remove(0) == added
    assert controller.list_applications() == ()


def test_add_rejects_duplicate(tmp_path: Path) -> None:
    controller, _store, _launcher = make_controller()
    application_path = tmp_path / "app.exe"
    application_path.touch()
    controller.add(application_path)

    with pytest.raises(DuplicateApplication):
        controller.add(application_path)


@pytest.mark.parametrize("kind", ["missing", "directory", "relative"])
def test_add_rejects_missing_or_invalid_paths(tmp_path: Path, kind: str) -> None:
    controller, _store, _launcher = make_controller()
    if kind == "missing":
        path = tmp_path / "missing.exe"
    elif kind == "directory":
        path = tmp_path
    else:
        path = Path("relative.exe")

    with pytest.raises(InvalidApplicationPath):
        controller.add(path)


def test_remove_rejects_invalid_selection() -> None:
    controller, _store, _launcher = make_controller()

    with pytest.raises(InvalidSelection):
        controller.remove(0)


def test_launch_one_and_all_use_only_injected_launcher(tmp_path: Path) -> None:
    controller, store, launcher = make_controller()
    applications = [Application(tmp_path / "one.exe"), Application(tmp_path / "two.exe")]
    store.applications = applications
    controller.load()

    controller.launch_one(1)
    controller.launch_all()

    assert launcher.launched == [applications[1], *applications]


def test_launch_empty_list_is_safe() -> None:
    controller, _store, launcher = make_controller()

    with pytest.raises(InvalidSelection):
        controller.launch_all()
    assert launcher.launched == []
