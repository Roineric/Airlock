# Airlock — Technical Notes

## Current stack

- Python 3.11 or newer
- standard-library `tkinter` for the Windows GUI
- `psutil` for process discovery, identity checks, waiting, and termination
- JSON for local enabled-target settings
- `pytest` for automated tests
- PyInstaller 6.22.0 for Windows release builds

Dependencies are split by purpose:

- `requirements.txt` contains runtime dependencies;
- `requirements-dev.txt` adds testing and pinned build dependencies; and
- `pyproject.toml` contains package metadata and the runtime dependency.

## Architecture

- `gui.py` owns presentation, confirmation, and background-worker coordination.
- `settings.py` loads and validates exact executable targets.
- `processes.py` discovers and closes only exact, previewed process objects.
- `windows.py` contains the Windows `WM_CLOSE` wrapper.

Process handling remains separate from the GUI so tests can use fake process
objects without opening windows or terminating real applications.

## Settings

Airlock reads `airlock_settings.json` from the current working directory. The
file contains only an `enabled_targets` list of complete `.exe` names. Friendly
application labels are a display-layer concern; exact executable names remain
the process-control identity.

## Release build

The PyInstaller CLI documented in `README.md` is authoritative. PyInstaller is
pinned in `requirements-dev.txt`. Generated `.spec`, `build/`, and `dist/`
outputs are ignored. Release binaries and their external settings file are
published as GitHub Release assets with SHA-256 hashes in the release notes.

## Current safety limitation

After a five-second graceful wait, survivors are force-terminated automatically.
A future safety improvement should report survivors and require a second explicit
confirmation before force termination.
