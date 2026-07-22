from __future__ import annotations

import importlib
import os
import sys
import tkinter

import pytest


def test_imports_create_no_gui_and_launch_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"tk": 0, "launch": 0}

    def forbidden_tk(*_args: object, **_kwargs: object) -> None:
        calls["tk"] += 1
        raise AssertionError("Import created a Tk root.")

    def forbidden_launch(_path: str) -> None:
        calls["launch"] += 1
        raise AssertionError("Import launched an application.")

    monkeypatch.setattr(tkinter, "Tk", forbidden_tk)
    monkeypatch.setattr(os, "startfile", forbidden_launch, raising=False)

    modules = [
        "morning_app_launcher",
        "morning_app_launcher.models",
        "morning_app_launcher.storage",
        "morning_app_launcher.launcher",
        "morning_app_launcher.controller",
        "morning_app_launcher.operational_logging",
        "morning_app_launcher.gui.presentation",
        "morning_app_launcher.gui.main_window",
        "morning_app_launcher.app",
    ]
    for name in modules:
        sys.modules.pop(name, None)
        importlib.import_module(name)

    assert calls == {"tk": 0, "launch": 0}
