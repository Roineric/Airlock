---
type: project_home
project: Airlock
status: defined
date: 2026-03-19
category: utility_app
domain: personal_ops
ecosystem_role: session_control
platform: windows_local
stack_candidate:
  - Python
  - Tkinter
  - psutil
  - JSON
---

# Airlock

## 0) Why this note exists
This is the main home note for **Airlock**.

Its purpose is to act as the project’s front door:
- define what Airlock is,
- show its current state,
- link to the key internal project notes,
- point to locked decisions,
- and keep the next actions visible.

If someone opens only one Airlock note first, it should be this one.

---

# 1) Project identity

## 1.1 Name
**Airlock**

Important naming rule:
- the app title is locked as **Airlock**
- “Project Airlock” may still appear informally in planning discussion
- the actual product/app name is **Airlock**

---

## 1.2 What Airlock is
Airlock is a **tiny local desktop utility** whose purpose is to create a deliberate transition from **work mode** to **off-duty mode**.

Its first job is simple:
- close selected background apps at the end of the workday
- reduce distraction / communication noise
- create a clean boundary between work session and hobby/personal session

Airlock is not just an app closer.
It is a **session-transition tool**.

---

## 1.3 What Airlock is not
Airlock is:
- not a system optimizer
- not a cloud service
- not a scheduler at v0.1
- not a full Windows environment manager
- not a replacement for larger ecosystem tools

Its strength is being a small, honest utility.

---

# 2) Ecosystem role

## 2.1 Classification
- **Type:** utility app
- **Domain:** personal ops
- **Ecosystem role:** session control utility
- **Platform:** Windows local

## 2.2 Position in the ecosystem
Airlock is a **utility node**, not a backbone platform.

It supports the broader ecosystem by:
- improving environment-state transitions
- reducing lingering post-work noise
- reinforcing local-first, explicit-action design values
- acting as a small vertical-slice training project

# 3) Core problem

## 3.1 Problem statement
Working from home creates weak boundaries.

Background apps such as messengers, communication tools, and optional distraction apps remain open after work and continue pulling attention back into work-space.

Manual shutdown is:
- annoying
- inconsistent
- cognitively noisy

## 3.2 Desired outcome
Airlock should provide:
- one action,
- one clean machine-state change,
- one reliable transition into off-duty time.

---

# 4) Current state

## 4.1 Status
**Working v0.1 MVP**

## 4.2 Current project state
Airlock has a working Tkinter interface, exact-name process matching, guarded
process closure, local JSON settings, automated tests, and a reproducible
PyInstaller CLI build. Current implementation details and open risks are tracked
in the latest dated handoff.

---

# 5) v0.1 goal

## 5.1 Goal
Build a tiny Windows desktop app with:
- one button: **End Workday**
- a small configured list of target apps/processes
- visible result/status output

## 5.2 Expected first product slice
When the user clicks **End Workday**, Airlock should:
1. inspect configured target processes
2. stop matching running apps
3. report what happened clearly

That is the complete intended v0.1 slice.

---

## 6) Notes index

## 6.1 Project spine

- `01_Scope_and_Vision.md`
- `02_Process_Targets.md`
- `03_Tech_Notes.md`
- `AIRLOCK_EXPLANATION.md`
- `PROGRAM_FLOW_WALKTHROUGH.md`
- the latest dated `HANDOFF_*.md`

---

# 7) Current handoff

Use the most recent dated `HANDOFF_*.md` in this directory as the current
implementation snapshot.

---

# 9) Current target app scope

## 9.1 Enabled target list
Current Airlock targets:
- Discord
- Telegram
- RingCentral
- Epic Games Store
- Ubisoft Connect

WhatsApp is temporarily excluded after an unclean shutdown warning. Steam
remains an optional future target.

## 9.2 Ground-truth source
The detailed verification state for target apps is tracked in:

- `02_Process_Targets.md`

Important implementation rule:
Airlock must target **real process names**, not only human-facing brand names.

---

# 10) Next actions

## 10.1 Immediate next steps
1. verify actual process names on the machine
2. build terminal-only prototype first
3. test shutdown behavior
4. wrap prototype in a minimal desktop UI
5. keep v0.1 scope tight

---

# 11) Open questions

## 11.1 Force-close behavior
Should Airlock default to force-close when needed, or only force when graceful shutdown fails?

## 11.2 Steam policy
Should Steam remain optional, or become a normal default target?

## 11.3 Launcher subprocess behavior
Will Epic Games Store and Ubisoft Connect require handling beyond their main visible launcher process?

## 11.4 Hobby Mode timing
Should **Launch Hobby Mode** wait until v0.2 or later?

---

# 12) One-sentence identity
**Airlock is a tiny local Windows session-control utility that closes selected background apps and creates a deliberate transition into off-duty mode.**
