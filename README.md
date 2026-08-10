# Airlock

Airlock is a small Windows desktop utility for ending the workday. It previews
selected communication and distraction applications, asks for confirmation,
then closes only the exact processes shown.

## Current MVP

- Minimal Tkinter desktop interface
- JSON-configured executable targets
- Exact, case-insensitive executable-name matching
- Friendly application names and running status in the preview
- Exact process IDs shown in the confirmation dialog
- Graceful Windows `WM_CLOSE` request before forced fallback
- Clear `Closed`, `Not running`, and `Failed` results
- Responsive `Ending Workday…` and `Workday Ended ✓` button states
- Protected Windows-process denylist and PID-identity checks
- Unit tests that never terminate real processes

## Install from a fresh clone

Airlock requires Windows and Python 3.11 or newer. Run these commands from the
repository root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

`requirements.txt` contains runtime dependencies. `requirements-dev.txt` adds
the test and pinned build tools used by contributors.

Edit `airlock_settings.json` to select targets. The file must contain only an
`enabled_targets` list of complete executable names such as `Discord.exe`.

## Run and test from source

Run from the repository root so Airlock can find `airlock_settings.json`:

```powershell
.\.venv\Scripts\python.exe -m airlock
```

Run the automated tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

If pytest reports `PermissionError` for its temporary directory on Windows, use
a repository-local directory owned by the current PowerShell session:

```powershell
$airlockTestTemp = ".\.pytest_temp_user_$PID"

.\.venv\Scripts\python.exe -m pytest `
  --basetemp $airlockTestTemp `
  -p no:cacheprovider
```

Directories beginning with `.pytest_temp` are ignored by Git.

Tests use fake process objects and must never terminate real user processes.

## Documentation

- [Process-matching safety review](docs/PROCESS_MATCHING_SAFETY_REVIEW.md)
- [Program flow walkthrough](docs/PROGRAM_FLOW_WALKTHROUGH.md)

## Download and run the Windows release

You do not need Python to use the release version of Airlock.

1. Open the [latest Airlock release](https://github.com/Roineric/Airlock/releases/latest).
2. Download both `Airlock.exe` and `airlock_settings.json` into the same folder.
3. Open `airlock_settings.json` in Notepad and list the applications you want
   Airlock to close. Use each application's complete executable name, such as
   `Discord.exe`.
4. Save the settings file, then double-click `Airlock.exe` from that folder.

Keep `Airlock.exe` and `airlock_settings.json` together. Airlock reads its list
of applications from the settings file each time it starts.

The release notes include SHA-256 hashes that you can use to check that the
downloads are unchanged. In PowerShell, run:

```powershell
Get-FileHash .\Airlock.exe -Algorithm SHA256
Get-FileHash .\airlock_settings.json -Algorithm SHA256
```

Compare the displayed hashes with those in the release notes. Because Airlock
is not digitally signed, Windows may show a security warning the first time you
open it.

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
- The executable is unsigned and may trigger Windows security warnings

## License

Airlock is available under the [MIT License](LICENSE).
