"""GUI composition root. Importing this module does not create a window."""

from __future__ import annotations

import tkinter as tk
from importlib import resources
from pathlib import Path
from tkinter import messagebox

from .controller import ApplicationController
from .errors import ApplicationError
from .gui.main_window import MainWindow
from .launcher import WindowsApplicationLauncher
from .storage import JsonApplicationStore, LegacyConfigurationMigrator, user_configuration_path

LEGACY_CONFIGURATION_FILENAME = "save.txt"


def build_controller() -> ApplicationController:
    store = JsonApplicationStore(user_configuration_path())
    migrator = LegacyConfigurationMigrator(Path.cwd() / LEGACY_CONFIGURATION_FILENAME, store)
    migrator.migrate()
    controller = ApplicationController(store, WindowsApplicationLauncher())
    controller.load()
    return controller


def _apply_icon(root: tk.Tk) -> None:
    try:
        icon = resources.files("morning_app_launcher.resources").joinpath("favicon.ico")
        with resources.as_file(icon) as icon_path:
            root.iconbitmap(default=str(icon_path))  # type: ignore[no-untyped-call]
    except Exception:
        # The icon is cosmetic; startup must not depend on resource or Tk icon support.
        return


def main() -> int:
    root = tk.Tk()
    root.withdraw()
    try:
        controller = build_controller()
    except ApplicationError as exc:
        messagebox.showerror("Morning App Launcher", str(exc), parent=root)
        root.destroy()
        return 1

    _apply_icon(root)
    MainWindow(root, controller)
    root.deiconify()
    root.mainloop()
    return 0
