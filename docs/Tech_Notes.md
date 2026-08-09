---
type: notes
project: Airlock
status: active
date: 2026-03-19
---

# Airlock — Tech Notes

## 0) Why this note exists
This note stores short technical explanations and practical learning notes for **Airlock**.

It exists so the project remains understandable while building, especially when new tools, libraries, or architecture terms appear.

This is not formal design documentation.  
It is a practical learning/reference note.

---

# 1) CustomTkinter

## 1.1 What it is
CustomTkinter is a Python desktop UI library built on top of Tkinter.

Practical meaning:
- Tkinter is the older standard Python GUI toolkit
- CustomTkinter is a more modern-looking UI layer on top of it

## 1.2 Why Airlock may use it
- simpler than heavier desktop frameworks
- easier to learn for a small local utility
- enough for a neat one-window app
- cleaner visual result than raw default Tkinter widgets

## 1.3 Airlock use case
- create the app window
- add the **End Workday** button
- display result/status text

---

# 2) psutil

## 2.1 What it is
`psutil` means Python system and process utilities.

It is a Python library used to inspect and manage system processes and system information.

## 2.2 Why Airlock may use it
- find running processes
- inspect their names
- detect target apps
- stop matching processes from Python

## 2.3 Why this matters
Airlock is basically a small control panel over Windows process shutdown.  
That makes `psutil` a natural fit.

---

# 3) JSON config

## 3.1 What it is
JSON is a simple text format for storing structured data.

## 3.2 Why Airlock may use it
- store the list of apps to close
- later store apps to launch
- later store lightweight preferences

## 3.3 Why this is useful
- keeps configuration separate from code
- easier to edit later
- makes the program cleaner

---

# 4) Process name vs app name

## 4.1 Important rule
Airlock must act on **real process names**, not human-facing app names.

Example:
The app you think of as “Epic Games Store” may actually run under a process like `EpicGamesLauncher`.

## 4.2 Practical consequence
Implementation must always verify the real Windows process name first.

---

# 5) Force-close behavior

## 5.1 Basic issue
Some apps may close cleanly.  
Some may need forced termination.

## 5.2 Why it matters
- force-close is reliable
- but it can interrupt unsaved state
- and some apps may leave helper/background processes behind

## 5.3 Airlock implication
Airlock may eventually need a clearer rule here, but v0.1 can stay simple.

---

# 6) Terminal prototype

## 6.1 Why it comes first
Before building the UI, Airlock should first exist as a small terminal script.

## 6.2 Reason
- proves the real process-management behavior
- isolates the OS/process problem
- avoids getting distracted by GUI work too early
- makes debugging easier

This is the correct first implementation slice.

---

# 7) Minimal architecture model

## 7.1 Presentation layer
The visible window and controls.

## 7.2 Control layer
Receives user actions and coordinates app flow.

## 7.3 Process-management layer
Finds and stops target apps.

## 7.4 Configuration layer
Stores target lists and later preferences.

This model is intentionally small and beginner-friendly.

---

# 8) Why Airlock is a good first app project
Airlock teaches:
- file structure
- functions
- config handling
- process interaction
- UI vs logic separation
- visible action pipelines

It also solves a real problem immediately, which makes the learning loop much better.

---

# 9) Terms to expand later
Potential future notes to add here:
- event-driven UI
- Python entry point
- dependency management
- packaging into `.exe`
- graceful close vs force kill
- helper/background subprocesses

---

# 10) One-sentence summary
Airlock uses simple pieces:
- Python for logic
- CustomTkinter for UI
- psutil for process control
- JSON for config

The goal is not technical cleverness.  
The goal is a small understandable utility.