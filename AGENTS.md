# Repository Guidelines

## Project Purpose

Airlock is a small Windows 10 desktop application that closes selected distracting applications at the end of a workday. Keep the MVP simple and beginner-friendly: Python 3, `tkinter` for the GUI, `psutil` for process handling, JSON for local settings, and `pytest` for practical tests.

## Project Structure & Module Organization

The repository contains a working MVP. Keep its straightforward layout:

- `src/airlock/`: GUI, process-control, and settings modules.
- `tests/`: tests mirroring module names, such as `test_processes.py`.
- `assets/`: optional icons or other static resources.
- `README.md`: Windows setup and local run instructions.

Keep process termination separate from GUI code so safety behavior can be tested without opening a window.

## Build, Test, and Development Commands

Run commands from the repository root in PowerShell:

- `py -m venv .venv`: create a local virtual environment.
- `.\.venv\Scripts\Activate.ps1`: activate it.
- `py -m pip install -r requirements.txt`: install dependencies.
- `py -m airlock`: run the application when the package entry point is available.
- `py -m pytest`: run all automated tests.

Document any new setup step in `README.md`.

## Coding Style & Naming Conventions

Use four-space indentation and standard Python naming: `snake_case` for functions and files, `PascalCase` for classes, and `UPPER_CASE` for constants. Add type hints where they clarify inputs and outputs. Prefer short functions and plain-language comments that explain why, not what. If formatting or linting tools are added, configure them in `pyproject.toml` and run them before commits.

## Testing & Process Safety

Name tests `test_*.py` and test functions `test_<behavior>`. Mock process access in unit tests; tests must never terminate real user processes. Production code must match executable names exactly, reject Windows system processes, preview targets before termination, and handle missing processes or permission errors without crashing. Persist only enabled-target settings in a simple local JSON file.

## Commits & Pull Requests

Use concise imperative commits such as `Add exact-name process matching`. Create checkpoints at meaningful, working milestones. Pull requests should explain the user-visible change, list tests run, link relevant issues, and include screenshots for GUI changes. Keep changes small; do not rewrite unrelated code.

## Contributor Workflow

Before substantial work, inspect the repository, state the intended small change, implement it, and run relevant checks. Explain changes, reasoning, and how components connect in beginner-friendly language; briefly define unfamiliar terms and call out remaining risks.

## Source documents

Use these numbered documents as core project context:

- `docs/00_Project_Home.md`
- `docs/01_Scope_and_Vision.md`
- `docs/02_Process_Targets.md`
- `docs/03_Tech_Notes.md`

Use these documents for the current implementation state and completed safety
work:

- `docs/AIRLOCK_EXPLANATION.md`
- `docs/PROGRAM_FLOW_WALKTHROUGH.md`
- `docs/PROCESS_MATCHING_SAFETY_REVIEW.md`
- the most recent dated `docs/HANDOFF_*.md`

Priority order:

1. AGENTS.md defines the current weekend MVP and overrides older plans.
2. `docs/01_Scope_and_Vision.md` defines the intended product boundaries.
3. The latest dated handoff defines the current stopping point but does not
   override product scope or safety requirements.
4. Other documents are implementation reference or background context only.

Do not implement future phases unless explicitly requested.
