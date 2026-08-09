# Airlock

Airlock is a small Windows desktop utility for ending the workday. It previews
selected communication and distraction applications, asks for confirmation,
then closes only the exact processes shown.

## Current MVP

- Minimal Tkinter desktop interface
- JSON-configured executable targets
- Exact, case-insensitive executable-name matching
- Running-process and PID preview
- Confirmation before closure
- Graceful Windows `WM_CLOSE` request before forced fallback
- Clear `Closed`, `Not running`, and `Failed` results
- Protected Windows-process denylist and PID-identity checks
- Unit tests that never terminate real processes

## Installation

Airlock requires Windows and Python 3.11 or newer. From the repository root in
PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

Edit `airlock_settings.json` to select targets. The file must contain only an
`enabled_targets` list of complete executable names such as `Discord.exe`.

## Run from source

Run from the repository root so Airlock can find `airlock_settings.json`:

```powershell
.\.venv\Scripts\python.exe -m airlock
```

Run the tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Build an executable

Install PyInstaller in the virtual environment, then create a single windowed
executable:

```powershell
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\python.exe -m PyInstaller --onefile --windowed --name Airlock --paths src src\airlock\__main__.py
Copy-Item airlock_settings.json dist\airlock_settings.json
```

The output is `dist\Airlock.exe`. Keep `airlock_settings.json` beside it and
launch it with that directory as the working directory. PyInstaller builds are
platform-specific, so build the Windows executable on Windows. See the
[official PyInstaller usage guide](https://pyinstaller.org/en/stable/usage.html)
for other bundle options.

## Safety behavior

Airlock never uses partial-name or wildcard matching: `Discord.exe` does not
match `DiscordHelper.exe`. It rescans immediately before confirmation and acts
only on configured, previewed process objects. Protected Windows names are
rejected, and process identity is checked before any close request.

After confirmation, Airlock posts `WM_CLOSE` to matching top-level windows and
waits up to five seconds. It force-terminates only survivors, then waits up to
three seconds to verify exit. Permission errors, disappearing processes, and
timeouts are reported without crashing.

## Known limitations

- Windows only
- Targets are edited manually in JSON; there is no settings screen yet
- The settings file is resolved from the current working directory
- A process without a top-level window goes directly to forced fallback
- A save prompt still open after five seconds may be force-terminated, risking
  unsaved data
- Apps with differently named helpers may remain running or relaunch themselves
- Closure waits run on the GUI thread and may temporarily freeze the window
- The executable is unsigned and may trigger Windows security warnings
