# Airlock — Process Targets

## Purpose of This Note
This note tracks the actual applications Airlock is expected to close, plus the real Windows process names needed for implementation.

**Important**:
Airlock shuts down **process names**, not just brand names.

That means every target must be verified on the actual machine.

---

## Current Enabled Targets

- Discord
- Telegram
- RingCentral
- Epic Games Launcher
- Ubisoft Connect

Possible future additions:
- Slack
- Teams
- browser profiles/windows if relevant
- other work-only communication tools

---

## Verification Table

| App | Exact Process Name | Confirmed? | Status | Notes |
|---|---|---:|---|---|
| Discord | Discord.exe | Yes | Enabled | Exact-name target |
| Telegram | Telegram.exe | Yes | Enabled | Exact-name target |
| RingCentral | RingCentral.exe | Yes | Enabled | Exact-name target |
| Epic Games Launcher | EpicGamesLauncher.exe | Yes | Enabled | Exact-name target |
| Ubisoft Connect | upc.exe | Yes | Enabled | Exact-name target |
| WhatsApp | WhatsApp.Root.exe | Yes | Excluded | Shutdown warning observed |
| Steam | steam.exe | No | Future option | Verify before enabling |

---

## Verification Commands

### PowerShell  
```powershell  
Get-Process | Sort-Object ProcessName | Select-Object ProcessName
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
- Exact enabled process names are recorded in `airlock_settings.json`.
- WhatsApp (`WhatsApp.Root.exe`) is temporarily excluded from enabled targets.

### WhatsApp safety note — 2026-08-09

After Airlock closed `WhatsApp.Root.exe`, WhatsApp displayed an error when it was
launched again. This suggests that WhatsApp experienced the current forced
termination fallback as an unclean shutdown.

Until the fallback is improved, WhatsApp must remain absent from
`airlock_settings.json`. Reconsider enabling it only after Airlock can:

1. allow a longer graceful-close period;
2. report processes that remain open instead of automatically forcing them; and
3. request a separate user confirmation before force termination.

The exact WhatsApp error text was not captured, so this note records the observed
behavior without claiming that application data was corrupted.

---

## Follow-Up Tasks

- improve the forced-fallback confirmation flow;
- retest enabled targets after that change;
- reconsider WhatsApp only after it closes cleanly; and
- record new process-name or relaunch edge cases here.
