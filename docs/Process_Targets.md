# Airlock — Process Targets

## Purpose of This Note
This note tracks the actual applications Airlock is expected to close, plus the real Windows process names needed for implementation.

**Important**:
Airlock shuts down **process names**, not just brand names.

That means every target must be verified on the actual machine.

---

## Candidate Target Apps  
Initial candidates:  
- Discord  
- Telegram  
- WhatsApp
- RingCentral  
- Epic Games Store  
- Ubisoft Connect
- Steam (optional)  

Possible future additions:
- Slack
- Teams
- browser profiles/windows if relevant
- other work-only communication tools

---

## Verification Table

| App | Expected Process Name | Confirmed? | Close Cleanly? | Force Needed? | Notes |
|---|---|---:|---:|---:|---|
| Discord | Discord.exe | No | TBD | TBD | verify on machine |
| Telegram | Telegram.exe | No | TBD | TBD | verify on machine |
| WhatsApp | TBD | No | TBD | TBD | verify exact process name on machine |
| RingCentral | TBD | No | TBD | TBD | likely needs exact inspection |
| Steam | steam.exe | No | TBD | TBD | optional target |
| Epic Games Store | EpicGamesLauncher.exe | No | TBD | TBD | verify on machine |
| Ubisoft Connect | UbisoftConnect.exe | No | TBD | TBD | may also expose helper/background processes |

---

## Verification Commands

### PowerShell  
```powershell  
Get-Process | Sort-Object ProcessName | Select-Object ProcessName```
```

### Command Prompt

`tasklist`

---

## Verification Procedure

For each target app:
1. Launch the app normally
2. Run process listing command
3. Find the actual process name
4. Record it in the table
5. Test whether it closes cleanly
6. Record whether force-close is required
7. Note any helper/background subprocesses

---

## Notes on Process Reality

Some apps may:
- have multiple subprocesses
- keep background helpers alive
- use process names different from the visible brand name
- relaunch on update/service activity

So this note is not just a list — it is part of implementation research.

---

## Inclusion Rules

A good Airlock target is usually:
- work-related
- attention-draining after hours
- safe enough to close automatically
- not something the user normally needs to keep alive off-duty

A questionable target may be:
- hobby-related
- part of personal leisure time
- something with unsaved-state risk
- something better left optional

Example:  
Steam should probably remain **optional**, not mandatory.

---

## Exclusion Considerations

Potential exclusions:
- apps that often hold unsaved drafts
- apps that the user uses both for work and hobby
- apps that restart themselves automatically
- apps where force-close creates recurring annoyance

---

## Current Decisions

- Airlock is intended to target background messengers / communication apps first.
- Steam is considered optional rather than core.
- Exact process names must be confirmed before coding against them.

---

## Follow-Up Tasks

- confirm real process names on the machine
- test each app for shutdown behavior
- note edge cases
- update this file as ground truth for implementation
