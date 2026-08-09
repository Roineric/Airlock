# Airlock — Future Features

## Purpose

This document records ideas for future Airlock updates. These items are not
part of the current weekend MVP and should only be implemented when explicitly
selected as a focused future change.

## Feature Ideas

### Show application names in the process list — Implemented

Display friendly application names, such as `Discord` or `Epic Games Launcher`,
in the preview and confirmation lists instead of exposing executable filenames
such as `Discord.exe` or `EpicGamesLauncher.exe`.

Airlock should still use exact executable names internally for process matching
and termination safety. A future implementation could store a display name
alongside each executable name, keeping the user-facing label separate from the
process identity.

Example:

| Displayed to the user | Internal executable name |
|---|---|
| Discord | `Discord.exe` |
| Telegram | `Telegram.exe` |
| Epic Games Launcher | `EpicGamesLauncher.exe` |

The normal process list should show app names without PIDs. The confirmation
screen should continue showing PIDs where they help the user distinguish the
exact processes Airlock is about to close.

Implemented on 2026-08-09 in the preview, confirmation, and results displays.
Exact executable names remain unchanged in settings and process-control code.
