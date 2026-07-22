from __future__ import annotations

from pathlib import Path

import pytest

from morning_app_launcher.errors import InvalidApplicationPath, LaunchError
from morning_app_launcher.launcher import WindowsApplicationLauncher
from morning_app_launcher.models import Application


def test_launcher_success_uses_injected_boundary(tmp_path: Path) -> None:
    executable = tmp_path / "app.exe"
    executable.touch()
    calls: list[str] = []

    WindowsApplicationLauncher(calls.append).launch(Application(executable))

    assert calls == [str(executable)]


@pytest.mark.parametrize("kind", ["missing", "directory", "relative"])
def test_launcher_rejects_invalid_path_before_boundary(tmp_path: Path, kind: str) -> None:
    calls: list[str] = []
    if kind == "missing":
        path = tmp_path / "missing.exe"
    elif kind == "directory":
        path = tmp_path
    else:
        path = Path("relative.exe")

    with pytest.raises(InvalidApplicationPath):
        WindowsApplicationLauncher(calls.append).launch(Application(path))
    assert calls == []


def test_launcher_translates_operating_system_failure_without_path(tmp_path: Path) -> None:
    executable = tmp_path / "private-name.exe"
    executable.touch()

    def fail(_path: str) -> None:
        raise OSError("private operating-system detail")

    with pytest.raises(LaunchError) as captured:
        WindowsApplicationLauncher(fail).launch(Application(executable))

    assert str(executable) not in str(captured.value)
    assert "private operating-system detail" not in str(captured.value)
