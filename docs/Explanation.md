# Airlock: complete beginner-friendly and nerdy repository tour

This document explains the Airlock repository as it exists on **2026-08-09**. It covers every human-authored file, every executable line of Python, the important punctuation and language features, the generated files, the complete runtime path, the test strategy, and the known limitations.

The repository currently contains a working v0.1 MVP. The planning notes saying that implementation has not begun are older historical context, not the present state.

## 1. What Airlock does

Airlock is a small local Windows desktop application. It reads a reviewed list of executable names, scans the running processes for exact matches, previews those matches, asks the user for confirmation, terminates the previewed processes, and reports the result.

The entire runtime path is:

```text
PowerShell command: python -m airlock
    |
    v
src/airlock/__main__.py
    |
    v
gui.main()
    |
    +-- creates the Tk root window
    +-- loads airlock_settings.json through settings.py
    +-- builds AirlockApp
    +-- scans processes through processes.py
    +-- enters Tk's event loop
            |
            +-- Refresh Preview -> scan and display exact matches
            |
            +-- End Workday -> rescan -> confirm -> terminate -> report
```

The most important architectural boundary is this:

```text
GUI (display and user events)
        |
        +--> settings.py (read and validate configuration)
        |
        +--> processes.py (inspect and terminate processes)
```

The GUI does not contain the dangerous process-control implementation. That separation allows the process layer to be tested with fake objects rather than real Windows processes.

## 2. Repository tree

```text
AIRLOCK/
|-- .git/
|-- .pytest_cache/
|-- .venv/
|-- .vscode/
|   `-- launch.json
|-- docs/
|   |-- Explanation.md
|   |-- Process_Targets.md
|   |-- Project_Home.md
|   |-- Scope_and_Vision.md
|   `-- Tech_Notes.md
|-- src/
|   |-- airlock/
|   |   |-- __init__.py
|   |   |-- __main__.py
|   |   |-- gui.py
|   |   |-- processes.py
|   |   |-- settings.py
|   |   `-- windows.py
|   `-- airlock.egg-info/
|-- tests/
|   |-- test_processes.py
|   `-- test_settings.py
|-- .gitignore
|-- AGENTS.md
|-- README.md
|-- airlock_settings.json
|-- pyproject.toml
`-- requirements.txt
```

Folders beginning with a dot are conventionally hidden or tool-owned. Source files belong in `src`; tests belong in `tests`; project prose belongs in `docs`.

## 3. Root-level project files

### 3.1 `.gitignore`

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.py[cod]
*.egg-info/
```

Line 1 ignores `.venv/`, the local virtual environment. It contains a Python interpreter and installed packages. It is large, machine-specific, and reproducible from the dependency declarations.

Line 2 ignores every directory literally named `__pycache__`. Python creates these to hold compiled bytecode.

Line 3 ignores pytest's cache. Pytest records convenience data such as its last failures there; it is not application source.

Line 4 is a glob pattern. The bracket expression `[cod]` means one character chosen from `c`, `o`, or `d`, so this ignores `.pyc`, `.pyo`, and `.pyd` files.

Line 5 ignores directories such as `airlock.egg-info`. Setuptools generates this package metadata during installation.

The final blank line is harmless and is conventional for text files. Git can track empty directories only indirectly, through files inside them.

### 3.2 `AGENTS.md`

This is the repository's contributor contract. It guides humans and coding agents; Python never imports or executes it.

- Lines 1-5 define the product and lock the MVP stack to Python, standard `tkinter`, `psutil`, JSON, and pytest.
- Lines 7-16 define the intended directory structure and require process termination to remain separate from GUI code. The current code follows this rule.
- Lines 18-28 list PowerShell setup, run, and test commands and require new setup steps to be reflected in the README.
- Lines 30-32 define four-space indentation, Python naming conventions, type-hint guidance, short functions, and useful comments.
- Lines 34-36 contain the central safety requirements: tests must use mocks/fakes; matching must be exact; system processes must be rejected; targets must be previewed; expected OS errors must not crash the app; only enabled targets may be persisted.
- Lines 38-40 describe concise imperative Git commits and small pull requests. There are currently no commits.
- Lines 42-44 define the inspect, state, implement, test, explain workflow.
- Lines 46-63 rank the planning documents. `AGENTS.md` has priority over older plans and forbids accidental implementation of future phases.

There are two stale statements: line 9 says no application code exists, but the MVP now exists; line 54 references `docs/MVP_BUILD_PLAN.md`, which is not present. Those are documentation inconsistencies, not runtime failures.

### 3.3 `README.md`

The README is the short user/developer entry point.

- Line 1 provides the project title.
- Lines 3-5 state the purpose and two user-safety gates: an explicit click and a confirmation.
- Lines 7-15 show setup. `py -m venv .venv` asks the Windows Python launcher to create an isolated environment. Calling `.venv\Scripts\python.exe` explicitly guarantees subsequent commands use that environment. `pip install -r requirements.txt` installs dependencies. `pip install -e .` installs Airlock in editable mode, meaning edits under `src` become active without reinstalling after every edit.
- Lines 17-21 show the run command. `-m airlock` asks Python to execute the package's `__main__.py`.
- Lines 23-25 explain exact-match previewing and configuration.
- Lines 27-33 show the test command and state the no-real-termination test guarantee.

The README is intentionally compact; this document supplies the deep explanation.

### 3.4 `requirements.txt`

```text
psutil>=7.2,<8
pytest>=9,<10
```

Line 1 requests psutil version 7.2 or newer while refusing the potentially breaking major version 8. `>=` is the inclusive lower bound; `<` is the exclusive upper bound.

Line 2 does the same for pytest major version 9. Psutil is required at runtime. Pytest is required only while developing/testing, but keeping both in one file is a reasonable simplification for this tiny MVP.

### 3.5 `pyproject.toml`

TOML is a configuration language. Square-bracket headings open tables, strings use quotes, and arrays use square brackets.

- Lines 1-3 define the build system. Pip uses `setuptools.build_meta` to build/install the project and needs setuptools 77 or later.
- Lines 5-10 define installable package metadata: name `airlock`, version `0.1.0`, description, Python 3.11 minimum, and psutil runtime dependency.
- Lines 12-13 tell setuptools to discover packages beneath `src`. This is called the **src layout**.
- Lines 15-17 configure pytest. `pythonpath = ["src"]` makes `import airlock` resolve to the source tree during tests. `testpaths = ["tests"]` limits automatic test discovery to the tests directory.

Psutil appears in both this file and `requirements.txt`: this file declares what installed Airlock needs; the requirements file prepares the complete small development environment.

### 3.6 `airlock_settings.json`

```json
{
  "enabled_targets": [
    "Discord.exe",
    "Telegram.exe",
    "WhatsApp.Root.exe",
    "RingCentral.exe",
    "EpicGamesLauncher.exe",
    "upc.exe"
  ]
}
```

Line 1 opens a JSON object. Line 2 creates its only allowed key, `enabled_targets`, whose value is an array. Lines 3-8 are exact Windows executable names. Line 9 closes the array and line 10 closes the object.

Commas separate array values. The final value has no trailing comma because strict JSON does not allow one. JSON strings use double quotes.

Steam is intentionally absent, so it is disabled. Airlock stores no theme, history, credentials, schedule, or other state. Configuration order is retained in the GUI and result display.

### 3.7 `.vscode/launch.json`

This file is a Visual Studio Code debugger profile written as JSON with comments (technically JSONC).

- Line 1 opens the object.
- Lines 2-4 are VS Code's generated help comments.
- Line 5 declares debugger schema version `0.2.0`; this is not Airlock's version.
- Line 6 begins a list of debug configurations.
- Lines 7-15 define one profile.
- Line 8 sets its debugger type to `node`.
- Line 9 says to launch a new program.
- Line 10 gives it the generic display name `Launch Program`.
- Lines 11-13 tell the Node debugger to skip Node internals.
- Line 14 tries to execute the currently open file.
- Lines 16-17 close the array and root object.

This profile is stale or accidental: Airlock is Python, not Node.js. It does not affect README-based execution, but pressing this VS Code debug profile is not the supported way to launch Airlock.

## 4. The `src/airlock` Python package

### 4.1 `__init__.py`

```python
"""Airlock desktop utility."""

__version__ = "0.1.0"
```

Line 1 is the package docstring. Triple quotes create a string; because it is the first statement, Python exposes it as `airlock.__doc__`.

Line 2 is blank for readability.

Line 3 assigns the version string to `__version__`. The double underscores indicate a conventional special metadata name. It duplicates the version in `pyproject.toml`, which is acceptable here but can drift if only one copy is updated.

The file also makes `airlock` a conventional package rather than an arbitrary directory.

### 4.2 `__main__.py`

```python
from airlock.gui import main


if __name__ == "__main__":
    main()
```

Line 1 imports the `main` function from `gui.py`. Importing `gui` also evaluates its top-level imports and defines its constant, class, and function, but it does not create a Tk window yet.

Lines 2-3 are the standard two blank lines before a top-level construct.

Line 4 is the **name guard**. When Python runs this module as the program entry point, the special variable `__name__` equals `"__main__"`. If a test merely imports the module, the condition is false.

Line 5 calls `main`. Parentheses mean “invoke this callable now.” This tiny file is why `python -m airlock` works.

### 4.3 `settings.py`

This module converts an editable local file into a validated list that the rest of the program can trust.

#### Lines 1-2: imports

```python
import json
from pathlib import Path
```

`json` is Python's standard parser. `Path` is an object-oriented path type. `from ... import ...` imports only the named object into this module's namespace.

#### Lines 5-18: protected names

`PROTECTED_PROCESS_NAMES` is uppercase because it is a module-level constant. `frozenset(...)` creates an immutable set. Sets provide direct membership checks and discard duplicates.

The inner braces create a set literal. Each string is stored lowercase because comparisons use `casefold()`:

- `csrss.exe`: Client/Server Runtime Subsystem.
- `dwm.exe`: Desktop Window Manager.
- `explorer.exe`: desktop, taskbar, and file shell.
- `lsass.exe`: Local Security Authority process.
- `services.exe`: Service Control Manager.
- `smss.exe`: Session Manager.
- `svchost.exe`: shared host used by Windows services.
- `system`: the Windows System process name as commonly reported.
- `wininit.exe`: Windows initialization.
- `winlogon.exe`: interactive sign-in/session process.

The closing parentheses complete the multiline constructor call. This denylist is a second safety layer, not a complete inventory of every dangerous Windows process.

#### Lines 21-22: application-specific exception

```python
class SettingsError(ValueError):
    """Raised when the local settings file is unsafe or malformed."""
```

`class` defines a new type. The parentheses mean it inherits from `ValueError`, because invalid settings are invalid values. The indented string is its class docstring. The class needs no extra methods; its distinct type lets the GUI catch settings failures specifically.

#### Lines 25-30: reading and parsing

```python
def load_enabled_targets(path: Path) -> list[str]:
```

`def` creates a function. `path: Path` is an input type hint. `-> list[str]` says the intended return value is a list containing strings. Hints help readers and tools but are not runtime enforcement by themselves.

The docstring summarizes the contract. The `try` block reads UTF-8 text and passes it to `json.loads`, which converts JSON into Python dictionaries, lists, and primitive values.

The `except` tuple catches filesystem errors (`OSError`) and malformed JSON (`JSONDecodeError`) as `error`. It raises a `SettingsError` with context. The f-string inserts the path and original error. `from error` preserves exception chaining, so a traceback still shows the root cause.

#### Lines 32-37: exact document shape

The first `if` requires a dictionary and exactly one key. Python's `or` short-circuits, so if `data` is not a dictionary, `set(data)` is not needed. For a dictionary, `set(data)` produces its keys. The set must equal `{"enabled_targets"}` exactly; missing or extra keys fail.

Line 35 retrieves the value. Lines 36-37 require it to be a list and require every element to be a string. `all(...)` consumes the generator expression and returns true only if every item passes `isinstance(item, str)`. An empty list passes because it contains no counterexample.

#### Lines 39-52: normalization and safety checks

`normalized: list[str] = []` creates the output list. `seen: set[str] = set()` creates an initially empty set for case-insensitive duplicate detection.

The `for` loop visits each configured target in order. `strip()` removes leading/trailing whitespace. `casefold()` makes a comparison form suitable for case-insensitive matching.

Line 44 rejects an empty cleaned value or one not ending in `.exe`, ignoring case. `not` negates truth; `or` means either condition is sufficient. Line 45 uses `{target!r}` so the error shows Python's representation, making invisible whitespace easier to spot.

Lines 46-47 reject protected names. Lines 48-50 append only the first spelling of a case-insensitive duplicate and remember its folded form. Line 52 returns the clean, ordered list.

Current limitation: merely ending in `.exe` does not prove the value is a plain basename. A string containing a path separator or wildcard could pass validation, although exact process-name matching means it normally would not match a real process name.

### 4.4 `processes.py`

This is the process-workflow boundary and the most safety-sensitive module. The raw Windows message call lives in `windows.py`.

#### Lines 1-6: imports

`dataclass` generates boilerplate methods for small data containers. `Iterable` describes any input that can be iterated, not only lists. `psutil` supplies the real process API and typed OS exceptions. The protected-name set is reused from settings so validation and runtime filtering share one source.

#### Lines 9-20: result records

`@dataclass(frozen=True)` is a decorator. It transforms each following class into an immutable data record with a generated initializer, representation, and equality behavior.

`ProcessMatch` carries the configured target spelling, PID, and live psutil Process object. A PID is the operating system's numeric **process identifier**. Keeping the object captured at preview time is what makes later termination preview-bound.

`ProcessResult` carries a target, a short status (`Closed`, `Not running`, or `Failed`), and human-readable detail. Neither record contains behavior; they transport structured data between layers.

#### Lines 23-50: finding targets

`find_target_processes` accepts target strings and an optional process iterator, returning `ProcessMatch` objects. The optional iterator is a form of **dependency injection**: production omits it and gets real psutil processes; tests inject fakes.

Lines 28-32 use a dictionary comprehension. Each safe target becomes `casefolded_name: original_spelling`. Dictionary lookup provides exact complete-name matching. Protected names are removed even if a caller bypasses settings validation.

Line 33 uses `process_iterator or ...`: a truthy supplied iterator wins; otherwise psutil enumerates current processes and preloads only `pid` and `name` into each object's `.info` dictionary. A subtle consequence is that an intentionally supplied empty list is falsey and would accidentally trigger real enumeration. The present tests never pass an empty list.

Line 34 creates the typed output list. Lines 36-48 visit processes. The `try` exists because a process can disappear or become inaccessible between enumeration and inspection—a normal race in process management.

Line 38 reads the name safely with `.get`. Line 39 requires a nonempty name and an exact folded dictionary-key match. Lines 40-46 build and append a record using the configured spelling, PID, and original process object.

Lines 47-48 ignore access-denied, disappeared, and zombie processes and continue scanning. Line 50 returns all matches, including multiple processes with the same executable name.

#### Lines 53-64: binding matches to configured targets

`close_previewed_processes` accepts configured targets, already-previewed matches, a five-second graceful timeout, a three-second forced timeout, and an injectable window-closing function. Production uses the Windows wrapper; tests pass harmless functions.

Line 59 materializes targets as a list. This matters if the caller supplied a one-use generator and preserves display order.

Line 60 creates a dictionary whose folded target names map to empty lists. Lines 61-64 group only matches whose target is still configured and not protected. A random injected `ProcessMatch` for another executable is ignored.

#### Graceful close before forced fallback

The outer loop produces exactly one result per configured target. A target with no previewed match becomes `Not running`, then `continue` skips to the next target.

For each match, Airlock first posts `WM_CLOSE` to its top-level windows. If a window accepts the message, Airlock waits up to five seconds for normal process exit. Applications may clean up, show a save prompt, ignore the request, or take time to exit. Processes with no window or which remain alive become survivors.

Only survivors reach psutil's `terminate()`, which is forceful on Windows. Airlock waits another three seconds to verify forced exit and reports graceful and forced counts separately.

If the process already vanished, `NoSuchProcess` is treated as effectively gone. `AccessDenied` becomes a clear message. Other psutil errors are stringified into a PID-specific failure. Catching `psutil.Error` does not swallow unrelated programming errors.

#### Waiting and reporting

Each wait has a timeout, so the app does not wait forever. Expected disappearance, permission, and timeout races become structured results.

If the process vanishes during the wait, that is success and `pass` does nothing. A timeout means it did not close in time. Access denial at verification time means closure could not be confirmed.

If any failure exists for a target, lines 96-97 return one `Failed` result with messages joined by semicolons. Otherwise lines 98-100 report `Closed` and the number of previewed matches. Line 102 returns the ordered results.

One edge case remains: an application can display a save prompt after `WM_CLOSE` but still be force-terminated when the five-second grace period expires. The confirmation warns about the fallback.

### 4.5 `windows.py`

This module is the narrow wrapper around the native Windows `user32` API. `ctypes` calls Windows DLL functions without adding a dependency; `wintypes` supplies correctly sized Windows types; `sys.platform` prevents loading user32 on non-Windows systems.

`WM_CLOSE = 0x0010` is the Windows message meaning “please close this window.” It follows an application's normal window event path rather than killing its process.

`request_window_close(pid)` loads user32 and declares exact signatures for `EnumWindows`, `GetWindowThreadProcessId`, and `PostMessageW`. Exact signatures and the `WINFUNCTYPE` callback calling convention are important on 64-bit Windows.

The nested callback examines every top-level window, asks Windows which PID owns it, and posts `WM_CLOSE` only when that PID exactly matches. `nonlocal` lets the callback increment the surrounding posted-message counter. Returning `True` tells Windows to keep enumerating.

`PostMessageW` is asynchronous: it queues the request but does not wait for the application to handle it. The process workflow performs that wait. The function returns the number of windows that accepted the message and raises `OSError` only when enumeration supplies an actual Windows error.

### 4.6 `gui.py`

Tkinter is event-driven: code builds widgets and registers callbacks, then the event loop calls those callbacks when buttons are clicked.

#### Lines 1-13: imports and settings location

`Path` handles the settings path. `tkinter as tk` gives the classic widgets a short namespace. `messagebox` supplies modal dialogs; `ttk` supplies themed widgets.

The multiline import brings in the match record and two process functions. The settings import brings in the custom error and loader.

`SETTINGS_PATH = Path.cwd() / "airlock_settings.json"` takes the current working directory and joins a filename with `/`. For `Path`, `/` means path joining, not arithmetic division. This requires launching from the repository root or another directory containing that file.

#### Lines 16-43: constructing `AirlockApp`

The class name uses `PascalCase`. Its initializer receives the Tk root and validated target list. `-> None` says initialization returns no useful value.

Lines 18-20 store state on `self`: root window, targets, and the most recent preview matches.

Lines 22-24 set the title, initial size (`width x height` pixels), and minimum resizable dimensions.

Lines 26-27 create a themed frame with 20 pixels of internal padding, then pack it to fill available width and height and expand with the window.

Line 29 creates the heading label using Segoe UI at 20-point bold and packs it west (`w`, left). Lines 30-33 create explanatory text and add vertical padding of 4 pixels above and 14 below.

Lines 35-36 create a classic multiline `Text` widget. It starts disabled so the user cannot edit status text, wraps by words, and expands with the window.

Lines 38-41 create a bottom row and two buttons. Crucially, `command=self.refresh_preview` passes the function object without parentheses; Tk will invoke it later. Adding parentheses here would call it during construction. Packing one left and the other right separates the actions.

Line 43 immediately populates the initial preview.

#### Lines 45-49: updating read-only output

`show_lines` temporarily changes the text widget to normal, deletes from text index `1.0` (line 1, character 0) through `end`, inserts newline-joined strings, then disables editing again. Centralizing this avoids repeating widget-state manipulation.

#### Lines 51-63: refreshing the preview

Line 52 performs a fresh OS scan and replaces stale matches. Line 53 builds an ordered mapping from every target to an empty PID list. Lines 54-55 add discovered PIDs.

Line 57 begins the display with a heading and blank line. Lines 58-62 produce either `Running` with comma-separated PIDs or `Not running`. `map(str, pids)` converts integers because `join` accepts strings only. Line 63 displays the completed list.

#### Lines 65-83: End Workday callback

Line 66 refreshes immediately before confirmation. This narrows the time gap between what is shown and what will be acted on.

If no enabled target is running, lines 67-69 show an informational dialog and return early.

Line 71 creates one preview line per exact match. Lines 72-75 ask a yes/no question. The embedded `\n` values create blank lines in the dialog. The answer is a Boolean.

Lines 76-77 stop if the user says No. Lines 79-83 terminate only the saved preview matches and display one formatted result per configured target. The em dash improves readability but has no program meaning.

#### Lines 86-96: application bootstrap

`main` creates the Tk root. The settings load is wrapped because a missing, malformed, or unsafe file should produce a friendly dialog instead of a raw traceback.

On `SettingsError`, lines 90-93 show the message, destroy the otherwise-empty root window, and return.

On success, line 95 constructs the app. Line 96 enters `mainloop`, which blocks while Windows/Tk dispatches paint, resize, button, and dialog events. Closing the root ends that loop and allows Python to exit.

Current GUI limitations include a potentially frozen window while sequential waits occur, no settings editor, no scroll bar, and a settings path tied to the launch directory.

## 5. Automated tests

### 5.1 Why these tests are safe

The tests never call `psutil.process_iter()` without an injected iterator and never pass a real process object to termination. `FakeProcess` implements only the tiny interface production code needs. This is a **test double**: a controlled substitute for a dangerous external dependency.

### 5.2 `tests/test_settings.py`

- Line 1 imports JSON so tests can create valid settings text.
- Line 3 imports pytest for exception assertions and fixtures.
- Line 5 imports the public settings behavior under test.
- Each test receives `tmp_path`, a pytest-created temporary `Path`, so it never edits the real settings file.

`test_loads_only_enabled_targets` writes the expected one-key object as UTF-8, calls the loader, and compares the exact returned list. `assert` fails the test if the expression is false.

`test_rejects_protected_windows_process` configures `explorer.exe`. `pytest.raises` is a context manager: the indented call must raise `SettingsError`, and its message must match the supplied regular-expression fragment.

`test_rejects_extra_persisted_settings` adds a `theme` key and verifies the strict one-key persistence rule.

`test_rejects_wrong_json_shape` writes a syntactically valid JSON array and verifies that structurally invalid Airlock data is rejected.

These four tests do not currently cover missing files, malformed JSON, non-string entries, invalid extensions, whitespace normalization, or case-insensitive duplicate removal.

### 5.3 `tests/test_processes.py`

Line 1 imports psutil only for its exception classes. Lines 3-7 import the records/functions under test.

`FakeProcess.__init__` stores a psutil-like `.info` dictionary, optional errors, and a call-tracking flag. Its `terminate` method marks the call and raises a configured error if present. Its `wait` method similarly raises a configured wait error or returns exit code 0. These methods never touch Windows.

`test_finds_only_complete_case_insensitive_names` creates exact, differently capitalized, and partial/helper names. It injects all three and asserts only the two complete names match, with their PIDs. This proves exact matching is not substring matching.

`test_protected_process_is_never_matched` bypasses the settings layer deliberately and proves the process layer independently rejects Explorer.

`test_force_terminates_only_previewed_processes_without_windows` simulates no closable window and proves only a previewed process reaches forced fallback. `test_graceful_close_does_not_force_terminate` proves a successful normal exit never calls psutil termination.

`test_reports_access_denied_without_crashing` configures the fake to raise `psutil.AccessDenied`. It proves the exception becomes a `Failed` result rather than escaping.

`test_force_terminates_after_graceful_timeout` proves a graceful timeout reaches forced fallback. `test_reports_failure_when_force_termination_times_out` covers an unverifiable forced exit.

Together the two modules currently contain eleven tests.

## 6. Planning and reference documents

These Markdown files do not execute. They explain intent and history. Their Wiki-style links (`[[...]]`) came from an Obsidian vault and many point to notes not copied into this repository.

### 6.1 `docs/Project_Home.md`

The opening `---` block is YAML front matter: structured note metadata declaring project, status, date, category, role, platform, and an early stack candidate.

Sections 0-3 define the note's purpose, lock the Airlock name, explain the work-to-off-duty transition, reject optimizer/cloud/scheduler scope, and position the app as a small utility node.

Section 4 says implementation has not begun. That was true when the source note was written but is now stale.

Section 5 describes the v0.1 behavior that now exists: one button, configured targets, and visible status.

Sections 6-8 are an index into a larger Obsidian knowledge base. They are contextual references, not local file paths guaranteed to exist.

Section 9 lists candidate applications and emphasizes real executable names. Section 10's immediate steps have largely been completed. Section 11 preserves open product questions about forced closure, Steam, launcher helpers, and Hobby Mode. Section 12 compresses the identity into one sentence.

### 6.2 `docs/Scope_and_Vision.md`

The front matter marks this as an active scope note dated 2026-03-19.

Section 0 calls it the anti-scope-creep document. Sections 1-3 define Airlock as a transition ritual, not a general automation platform, and define the desired emotional/user outcome.

Section 4 separates v0.1 inclusions from exclusions. The implemented MVP remains inside those boundaries: no tray icon, schedule, daemon, cloud, accounts, preferences UI, or broad automation.

Section 5 states six design principles: local-first, explicit action, visible results, a small complete slice, user agency, and ritual over clutter. The current confirmation and JSON allowlist support those principles.

Section 6 lists valid future evolution and invalid product drift. Section 7 defines both technical and emotional success. Section 8 supplies the one-sentence scope summary.

### 6.3 `docs/Process_Targets.md`

This note explains why brand names are insufficient: Windows process APIs operate on executable/process names.

The candidate list includes Discord, Telegram, WhatsApp, RingCentral, Epic, Ubisoft, and optional Steam. Its verification table is now partly stale: the actual JSON uses `WhatsApp.Root.exe`, `RingCentral.exe`, and `upc.exe`, while the table still marks them TBD/unconfirmed or predicts another Ubisoft name.

The PowerShell example has malformed Markdown fencing around `Select-Object ProcessName`; this affects rendering, not application behavior.

The verification procedure is sound: launch each app, inspect processes, record the exact name, test shutdown, and note helpers. Later sections discuss subprocesses, relaunch behavior, inclusion/exclusion policy, Steam's optional status, and follow-up research.

### 6.4 `docs/Tech_Notes.md`

The front matter identifies a practical learning note. Sections 1-10 explain GUI tooling, psutil, JSON, process names, forced closure, terminal-first prototyping, a minimal layered architecture, and useful learning outcomes.

This document proposes CustomTkinter, but the repository rules and implementation use standard-library Tkinter. It also speaks prospectively (“may use”) even though psutil and JSON are now implemented. Treat it as early background rather than current technical truth.

Its layered model maps neatly to current files: `gui.py` is presentation/control, `processes.py` is process management, and `settings.py` is configuration.

### 6.5 `docs/Explanation.md`

This is the document you are reading. It is generated as a learning-oriented snapshot but remains ordinary Markdown. Updating code can make line references and claims stale, so it should be reviewed after meaningful implementation changes.

## 7. Generated and tool-owned files

### 7.1 `.venv/`

This contains the local Python interpreter, pip, dependencies, scripts, and installed metadata. It isolates Python packages, not operating-system privileges: Airlock running inside it can still inspect and terminate Windows processes available to the user.

### 7.2 `__pycache__/` and `.pyc`

Python compiles source into bytecode cached in files such as `gui.cpython-314.pyc`. `cpython-314` identifies CPython 3.14. These binary files are performance caches, are reproducible, and should not be manually edited.

### 7.3 `.pytest_cache/`

Pytest writes run metadata here. Deleting it would not delete tests; pytest would recreate it.

### 7.4 `src/airlock.egg-info/`

Editable installation generated:

- `PKG-INFO`: package name, version, Python requirement, and dependency metadata.
- `requires.txt`: normalized dependency lines.
- `dependency_links.txt`: legacy dependency-link metadata; currently effectively empty.
- `top_level.txt`: the top-level import package, `airlock`.
- `SOURCES.txt`: files setuptools considers part of the source distribution.

These files derive from `pyproject.toml` and package discovery and are ignored by Git.

### 7.5 `.git/`

Git's private database lives here: repository configuration, object storage, references, and staging data. It should not be manually edited. At this snapshot, the `main` branch has no commits and all project files are untracked.

## 8. Full runtime example

Suppose Discord PID 120 and two Epic launcher processes PIDs 300 and 301 are running.

1. Python executes `airlock.__main__`.
2. `main()` creates Tk and loads the six configured names.
3. The settings loader validates structure, extensions, protected names, and duplicates.
4. `AirlockApp` builds widgets and calls `refresh_preview`.
5. Psutil enumerates process names and PIDs.
6. Exact folded lookups create three `ProcessMatch` objects.
7. The GUI shows Discord and Epic as running and all other targets as not running.
8. The user clicks End Workday.
9. Airlock rescans so the confirmation is fresher.
10. The confirmation lists all three exact PIDs.
11. If the user says Yes, only those captured objects are passed to termination.
12. Airlock requests termination, waits up to three seconds per accepted request, and collects errors.
13. The output displays one result per configured executable.

A new matching process launched after the confirmation is not in `self.matches` and is therefore not terminated by that action. This is an important preview-bound safety property.

## 9. What the safety model guarantees

- Only configured names are eligible.
- Configuration is restricted to one field.
- Several critical Windows names are blocked twice.
- Matching compares complete executable names, case-insensitively.
- Live matches and PIDs are displayed.
- A fresh scan occurs immediately before confirmation.
- The user must explicitly approve.
- Only previewed process objects reach termination.
- Expected races and permission failures become results instead of crashes.
- Automated tests use fake processes only.

## 10. What the safety model does not guarantee

- The denylist is not an exhaustive list of all important processes.
- A correctly targeted application may contain unsaved work.
- A survivor is force-terminated after five seconds even if it opened a save prompt.
- Helper processes with different names remain alive unless independently configured.
- Apps or services may relaunch themselves.
- PIDs and process state can change between scan and action.
- The GUI can become unresponsive while waiting sequentially.
- There is no tested real-process integration path.
- There is no guarantee the settings file is found outside the repository root.

## 11. Test coverage: proven and unproven

The suite proves valid settings loading, strict persistence shape, protected-name rejection, wrong-shape rejection, exact case-insensitive matching, helper-name exclusion, process-layer denylisting, preview-only termination, missing-target reporting, access-denied reporting, and timeout reporting.

It does not prove every validation branch, every protected name, GUI behavior, actual Windows process behavior, graceful closing, helper policy, relaunch behavior, settings-path portability, PID reuse, or UI responsiveness.

## 12. Current inconsistencies and technical debt

1. The VS Code launch profile targets Node rather than Python.
2. `Project_Home.md` still says implementation has not started.
3. `Tech_Notes.md` discusses CustomTkinter while the locked MVP uses Tkinter.
4. `Process_Targets.md` is behind the executable names in the live JSON.
5. `AGENTS.md` references a missing `MVP_BUILD_PLAN.md` and uses different filename capitalization from the real files.
6. The settings path depends on the current working directory.
7. `process_iterator or psutil.process_iter(...)` mishandles an explicitly injected empty iterable.
8. Executable validation permits path-like strings if they end in `.exe`.
9. The GUI waits on the event thread.
10. Version `0.1.0` is duplicated in two files.
11. The native user32 wrapper is tested indirectly through injection, not by sending a real `WM_CLOSE` during automated tests.

These are documented observations, not changes made as part of this explanation.

## 13. Why this is still a good MVP

The code is small enough to hold in one person's head. Each module has a clear responsibility. The dangerous behavior is isolated and tested through dependency injection. The user sees the exact targets and confirms the action. Expected operating-system failures do not crash the app. Setup and test commands are short.

That is the right shape for a learning project: a complete vertical slice with real utility, visible boundaries, practical tests, and honest limitations. Airlock now has a genuine graceful Windows window-close path followed by a disclosed forced fallback. A useful future refinement would be asking for a second confirmation before force-terminating survivors.
