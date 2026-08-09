# Airlock — GitHub Publishing Guide

## Repository policy

- Source, tests, settings source, and current documentation are committed.
- Generated `build/`, `dist/`, and `.spec` outputs are ignored.
- `Airlock.exe` and its copied settings file are published as GitHub Release
  assets, not committed to the repository.
- Release notes record SHA-256 hashes for both assets.
- Commit authors use their GitHub-provided no-reply email when email privacy is
  desired.

## Pre-push checks

Run from the repository root:

```powershell
git status --short
git diff --check
.\.venv\Scripts\python.exe -m pytest
```

Review staged content before committing:

```powershell
git diff --cached --stat
git diff --cached
```

Confirm that sensitive or generated files are not tracked:

```powershell
git ls-files
git check-ignore -v dist\Airlock.exe
```

## Build release assets

Install the pinned contributor dependencies, run tests, and build with the
authoritative CLI:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m PyInstaller `
  --noconfirm --clean --onefile --windowed `
  --name Airlock --paths src `
  src\airlock\__main__.py
Copy-Item airlock_settings.json dist\airlock_settings.json -Force
```

Verify and record hashes:

```powershell
Get-FileHash dist\Airlock.exe -Algorithm SHA256
Get-FileHash dist\airlock_settings.json -Algorithm SHA256
```

Manually launch the packaged executable from the `dist` directory. Confirm that
the preview uses friendly application names and that the settings file contains
only the intended enabled targets. Do not select **End Workday** merely as a
packaging test.

## Publish source

Create a concise checkpoint commit only after reviewing the entire staged diff.
Push `main` to the existing `origin`; do not initialize another repository or
add a duplicate remote.

## Publish a GitHub Release

1. Create a version tag such as `v0.1.0` from the reviewed source commit.
2. Create a GitHub Release for that tag.
3. Attach `dist\Airlock.exe` and `dist\airlock_settings.json`.
4. Include both SHA-256 hashes in the release notes.
5. Mention that the executable is Windows-only and unsigned.
6. Download the published assets once and compare their hashes with the local
   release hashes.

## Privacy

A public repository necessarily displays its owner alias in its URL. Keep the
personal email private by enabling GitHub email privacy and configuring this
repository with the exact GitHub-provided no-reply address shown in GitHub's
email settings. Historical commits must also use that address before the first
public push.
