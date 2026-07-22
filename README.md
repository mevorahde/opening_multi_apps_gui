# Morning App Launcher

Morning App Launcher is a small Windows desktop utility for maintaining and opening a
user-selected group of applications. It retains the original Tkinter workflow while separating
the GUI, use cases, persistence, and operating-system launch behavior.

## Status

This branch is a modernization foundation. It supports Python 3.10 through 3.13 on Windows.
Tkinter is supplied by the Python installation; the application has no third-party runtime
dependencies.

## Development

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m mypy
```

Run the application only when you intend to open its GUI:

```powershell
.\.venv\Scripts\morning-app-launcher.exe
```

Importing `morning_app_launcher` or its modules does not create a window or launch an
application.

## Desktop workflow

The responsive application list shows friendly names and a `Ready` or `Missing` status. You can
add multiple files, select multiple entries, remove stale entries, open selected ready entries,
open all ready entries, and refresh status without restarting. Missing entries remain removable
but cannot be launched. Batch launch results report counts without exposing full paths.

Keyboard shortcuts:

- `Enter`: open selected ready entries
- `Delete`: request removal of selected entries
- `Ctrl+O`: add applications
- `Ctrl+A`: select all entries
- `F5`: refresh status
- `Escape`: clear the current selection; native dialogs also support cancellation

## Configuration and migration

Configuration is versioned JSON stored below `%LOCALAPPDATA%\MorningAppLauncher`. If
`LOCALAPPDATA` is unavailable, the application uses the equivalent per-user Windows local
application-data location.

On first start, when no JSON configuration exists, the launcher looks for the legacy ignored
`save.txt` in the current working directory. It de-duplicates entries, writes JSON atomically,
and leaves the legacy file untouched. A failed migration never deletes or changes the legacy
file. Malformed or unsupported JSON is reported safely and is never overwritten automatically.
Stored application paths are not printed or logged.

Operational logs rotate below the same per-user application-data directory. They contain only
predefined event classifications and integer counts—never complete application paths or
configuration contents. Logging is fail-open: setup, write, rotation, or close failures do not
prevent startup or normal operation.

Both `save.txt` and local JSON configuration are excluded from Git.

## Safety and platform behavior

Only the concrete Windows launcher adapter can call `os.startfile`. Paths are validated before
launch, operating-system failures are translated into safe application errors, and tests inject
fakes instead of invoking the real adapter.

The Morning App Launcher icon is an original project asset created specifically for this project
with OpenAI image generation under the project owner's direction. The application prefers the
multi-resolution ICO on Windows and falls back to the transparent PNG when needed. Icon-loading
failure is cosmetic and never prevents startup.

## License

The source code is available under the [MIT License](LICENSE). No separate asset license is
declared for the original project icon.
