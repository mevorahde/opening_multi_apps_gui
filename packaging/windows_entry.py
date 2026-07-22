"""PyInstaller entry point; importing it has no GUI side effects."""

from morning_app_launcher.app import main

if __name__ == "__main__":
    raise SystemExit(main())
