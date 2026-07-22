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

## Configuration and migration

Configuration is versioned JSON stored below `%LOCALAPPDATA%\MorningAppLauncher`. If
`LOCALAPPDATA` is unavailable, the application uses the equivalent per-user Windows local
application-data location.

On first start, when no JSON configuration exists, the launcher looks for the legacy ignored
`save.txt` in the current working directory. It de-duplicates entries, writes JSON atomically,
and leaves the legacy file untouched. A failed migration never deletes or changes the legacy
file. Malformed or unsupported JSON is reported safely and is never overwritten automatically.
Stored application paths are not printed or logged.

Both `save.txt` and local JSON configuration are excluded from Git.

## Safety and platform behavior

Only the concrete Windows launcher adapter can call `os.startfile`. Paths are validated before
launch, operating-system failures are translated into safe application errors, and tests inject
fakes instead of invoking the real adapter.

The icon is retained from the earlier project as a package resource with its bytes unchanged.
Its ownership and licensing provenance have not been established; this project makes no claim
about either. Icon-loading failure is nonfatal.

## License

The source code is available under the [MIT License](LICENSE). This license statement does not
assert ownership of the bundled icon.
