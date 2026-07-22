"""Tkinter view for the Morning App Launcher workflow."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from ..controller import ApplicationController
from ..errors import ApplicationError


class MainWindow:
    def __init__(self, root: tk.Tk, controller: ApplicationController) -> None:
        self._root = root
        self._controller = controller
        self._listbox = tk.Listbox(root, width=88, height=24, activestyle="dotbox")
        self._build()
        self._refresh()

    def _build(self) -> None:
        self._root.title("Morning App Launcher")
        self._root.minsize(700, 500)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        frame = tk.Frame(self._root, padx=24, pady=24)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self._listbox.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 16))
        tk.Button(frame, text="Add application", command=self._add).grid(row=1, column=0)
        tk.Button(frame, text="Remove selected", command=self._remove).grid(row=1, column=1)
        tk.Button(frame, text="Open", command=self._open).grid(row=1, column=2)

        menu = tk.Menu(self._root)
        actions = tk.Menu(menu, tearoff=False)
        actions.add_command(label="Add application", command=self._add)
        actions.add_command(label="Open", command=self._open)
        actions.add_command(label="Remove selected", command=self._remove)
        actions.add_separator()
        actions.add_command(label="Exit", command=self._root.destroy)
        menu.add_cascade(label="Actions", menu=actions)
        self._root.configure(menu=menu)

    def _refresh(self) -> None:
        self._listbox.delete(0, tk.END)
        for application in self._controller.list_applications():
            self._listbox.insert(tk.END, str(application.path))

    def _selected_index(self) -> int | None:
        selection = self._listbox.curselection()  # type: ignore[no-untyped-call]
        return int(selection[0]) if selection else None

    def _add(self) -> None:
        selected = filedialog.askopenfilename(
            title="Select an application",
            filetypes=(("Applications", "*.exe"), ("All files", "*.*")),
        )
        if not selected:
            return
        try:
            self._controller.add(Path(selected))
        except ApplicationError as exc:
            messagebox.showerror("Unable to add application", str(exc), parent=self._root)
        else:
            self._refresh()

    def _remove(self) -> None:
        index = self._selected_index()
        if index is None:
            messagebox.showerror("Nothing selected", "Select an application to remove.")
            return
        if not messagebox.askyesno(
            "Remove application",
            "Remove the selected application from this list?",
            parent=self._root,
        ):
            return
        try:
            self._controller.remove(index)
        except ApplicationError as exc:
            messagebox.showerror("Unable to remove application", str(exc), parent=self._root)
        else:
            self._refresh()

    def _open(self) -> None:
        index = self._selected_index()
        try:
            if index is None:
                self._controller.launch_all()
            elif messagebox.askyesno(
                "Open application",
                "Open the selected application?",
                parent=self._root,
            ):
                self._controller.launch_one(index)
        except ApplicationError as exc:
            messagebox.showerror("Unable to open application", str(exc), parent=self._root)
        finally:
            self._listbox.selection_clear(0, tk.END)
