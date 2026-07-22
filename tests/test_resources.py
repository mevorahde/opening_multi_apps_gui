from importlib import resources

import pytest

from morning_app_launcher import app


def test_icon_is_available_as_a_package_resource() -> None:
    icon = resources.files("morning_app_launcher.resources").joinpath("favicon.ico")

    assert icon.is_file()
    assert icon.read_bytes().startswith(b"\x00\x00\x01\x00")


def test_icon_loading_failure_is_nonfatal(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_to_find_resources(_package: str) -> None:
        raise RuntimeError("simulated resource failure")

    monkeypatch.setattr(app.resources, "files", fail_to_find_resources)

    app._apply_icon(object())  # type: ignore[arg-type]
