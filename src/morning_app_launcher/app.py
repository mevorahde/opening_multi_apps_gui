"""GUI composition root. Importing this module does not create a window."""

from __future__ import annotations

import os
import tkinter as tk
from importlib import resources
from pathlib import Path
from tkinter import messagebox

from .controller import ApplicationController
from .errors import ApplicationError
from .gui.main_window import MainWindow
from .launcher import WindowsApplicationLauncher
from .operational_logging import create_operational_logger
from .storage import JsonApplicationStore, LegacyConfigurationMigrator, user_configuration_path

LEGACY_CONFIGURATION_FILENAME = "save.txt"


def build_controller() -> ApplicationController:
    configuration_path = user_configuration_path()
    store = JsonApplicationStore(configuration_path)
    migrator = LegacyConfigurationMigrator(Path.cwd() / LEGACY_CONFIGURATION_FILENAME, store)
    migrator.migrate()
    event_logger = create_operational_logger(configuration_path.parent / "logs")
    controller = ApplicationController(store, WindowsApplicationLauncher(), event_logger)
    controller.load()
    return controller


def _apply_icon(root: tk.Tk) -> None:
    try:
        resource_root = resources.files("morning_app_launcher.resources")
    except Exception:
        return
    if os.name == "nt":
        try:
            icon = resource_root.joinpath("morning-app-launcher.ico")
            with resources.as_file(icon) as icon_path:
                root.iconbitmap(default=str(icon_path))  # type: ignore[no-untyped-call]
            return
        except Exception:
            pass
    try:
        icon = resource_root.joinpath("morning-app-launcher.png")
        with resources.as_file(icon) as icon_path:
            photo = tk.PhotoImage(master=root, file=str(icon_path))
        root.iconphoto(True, photo)
        root._morning_app_launcher_icon = photo  # type: ignore[attr-defined]
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
