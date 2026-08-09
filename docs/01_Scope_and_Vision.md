---
type: scope
project: Airlock
status: active
date: 2026-03-19
---

# Airlock — Scope and Vision

## 0) Why this note exists
This note defines what **Airlock** is trying to achieve, what problem it exists to solve, and what boundaries protect it from becoming a different project.

Its purpose is to keep the project aligned around:
- identity,
- core purpose,
- user outcome,
- and scope limits.

This note is the main anti-scope-creep document for Airlock.

---

# 1) Project identity

## 1.1 What Airlock is
Airlock is a **tiny Windows session-transition utility**.

It exists to create a deliberate boundary between:
- **work session**
- **off-duty / hobby session**

Its first mechanism for doing that is simple:
- close selected background apps
- reduce lingering communication/distraction noise
- create a visible, repeatable end-of-workday action

Airlock is not just an app closer.  
It is a **session-control ritual utility**.

---

## 1.2 What Airlock is not
Airlock is not:
- a general-purpose system optimizer
- a cloud service
- a task scheduler at v0.1
- a background daemon platform
- a full Windows environment manager
- a giant automation framework

Its value comes from staying narrow, honest, and immediately useful.

---

# 2) Core problem

## 2.1 Problem statement
Working from home creates weak boundaries between work and personal time.

At the end of the workday, multiple apps often remain open in the background:
- messengers
- communication tools
- launcher/client noise
- optional distraction apps

Even when work is technically over, these apps keep the machine — and the user’s attention — in a semi-work state.

Manual shutdown is:
- repetitive
- inconsistent
- mentally noisy

---

## 2.2 Why this problem matters
Airlock exists because the transition from work to hobby/personal time should be:
- explicit
- low-friction
- repeatable
- psychologically clean

Without that transition, off-duty time is partially contaminated by lingering work-state noise.

---

# 3) Primary goal

## 3.1 Main objective
Provide a **single explicit action** that moves the machine from:

**Work Session → Off-Duty Session**

Initial mechanism:
- close selected background apps
- report the result clearly

---

## 3.2 User outcome
Airlock should help the user feel:
- the work session is truly over
- work/noise apps are no longer lingering
- hobby/personal time is protected
- the transition is clean and repeatable

---

# 4) v0.1 scope

## 4.1 Included
Airlock v0.1 includes:
- Windows-only local app behavior
- one-button action: **End Workday**
- target process lookup
- target process shutdown
- visible result/status output
- minimal desktop UI

---

## 4.2 Excluded
Airlock v0.1 does not include:
- tray icon behavior
- automatic scheduling
- startup/background daemon behavior
- cloud sync
- user accounts or profile systems
- advanced preferences UI
- multi-mode workflow system
- Windows focus integration
- broad environment-state automation

These exclusions are intentional.

---

## 4.3 Why the scope is narrow
v0.1 should prove only the smallest useful slice:
- can Airlock identify the target apps?
- can it shut them down?
- can it show the result clearly?
- does that already feel useful?

Everything else comes later, if needed.

---

# 5) Design principles

## 5.1 Local-first
Airlock runs entirely on the local machine.

It should not require:
- cloud services
- accounts
- remote state
- online dependency for core behavior

---

## 5.2 Explicit action
Airlock should not begin as a silent automation system.

The user performs a deliberate action:
- opens Airlock
- presses **End Workday**
- sees the result

This preserves agency and makes the state transition visible.

---

## 5.3 Visible result
Airlock should clearly report what happened.

Examples:
- Closed: Discord
- Not running: Telegram
- Failed: RingCentral

The app should not quietly do things without feedback.

---

## 5.4 Small complete slice
A tiny finished utility is better than a large half-built concept.

Airlock should be built as:
- one useful action
- one clear path
- one understandable result

---

## 5.5 Agency-protecting design
The user should control:
- which apps are targets
- what counts as noise
- what remains optional

Airlock should help with boundaries, not impose them opaquely.

---

## 5.6 Ritual over clutter
Airlock should feel like a clean transition, not another noisy dashboard.

Its experience should support:
- closure
- separation
- off-duty clarity

---

# 6) Product boundaries

## 6.1 Valid future evolution
Airlock may later evolve into:
- configurable target selection
- Hobby Mode launch actions
- tray access
- named modes
- smoother session rituals

These are valid future expansions because they preserve the core identity.

---

## 6.2 Invalid drift
Airlock should not drift into:
- full Windows management suite
- performance optimizer
- generalized automation control center
- “productivity platform”
- endless feature bucket

That would make it a different project.

---

# 7) Success criteria

## 7.1 v0.1 success condition
Airlock v0.1 is successful if:
- it launches reliably
- it identifies configured target apps
- it closes them when possible
- it reports results clearly
- it feels useful immediately
- the code remains small enough to understand

---

## 7.2 Emotional success condition
Airlock also succeeds if it creates a real sense of:
- “work is over”
- “the noise is gone”
- “I can safely switch modes now”

That emotional/ritual dimension is part of the project’s value, not decorative fluff.

---

# 8) One-sentence summary
Airlock is a tiny local Windows session-transition utility that closes selected background apps and creates a deliberate boundary between work mode and off-duty mode.