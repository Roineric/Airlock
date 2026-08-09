# Airlock — Repository Explanation

## Purpose

Airlock is a small local Windows utility that creates an explicit transition
from work time to off-duty time by closing selected applications.

## Repository layout

```text
Airlock/
|-- airlock_settings.json
|-- requirements.txt
|-- requirements-dev.txt
|-- pyproject.toml
|-- README.md
|-- src/airlock/
|   |-- __init__.py
|   |-- __main__.py
|   |-- gui.py
|   |-- processes.py
|   |-- settings.py
|   `-- windows.py
|-- tests/
|   |-- test_gui.py
|   |-- test_processes.py
|   `-- test_settings.py
`-- docs/
```

## How the components connect

`python -m airlock` enters through `__main__.py` and calls `gui.main()`. The GUI
loads exact executable targets through `settings.py`, then asks `processes.py`
for exact running matches. The interface translates those targets into friendly
application names for display while retaining exact executable names internally.

Immediately before closure, Airlock refreshes the process list and asks for user
confirmation. The confirmation includes exact process IDs. Slow closure work
runs on a daemon worker thread, and results return to Tkinter's main thread
through a queue.

`processes.py` requests graceful window closure through `windows.py`, waits for
exit, and currently force-terminates verified survivors after five seconds.
Process identity and protected-name checks prevent stale or unsafe targets from
reaching termination.

## Settings and release files

The root `airlock_settings.json` is the source settings file. Release builds copy
it beside `Airlock.exe`; it is not bundled into the executable. Generated build
outputs stay out of Git and are attached to GitHub Releases with recorded hashes.

## Tests

The test suite mirrors the source modules. Process tests use fake objects and
injected functions, so automated tests never close real user processes. GUI
tests exercise state transitions and text output without opening a real window.

## Current boundary

The MVP intentionally has no scheduler, tray mode, cloud service, accounts, or
settings editor. The highest-priority future safety change is a separate
confirmation before force-closing graceful-shutdown survivors.
