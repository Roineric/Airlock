# Process-matching safety review

## Review date

2026-08-09

## Scope

This review examined Airlock's process-discovery and process-closure paths for
behavior that could select or terminate an unrelated Windows process.

Files reviewed:

- `src/airlock/processes.py`
- `src/airlock/settings.py`
- `src/airlock/windows.py`
- `tests/test_processes.py`

No real process was terminated during this review.

## Exact executable-name matching

Airlock uses exact, case-insensitive executable-name matching.

Configured targets are stored in a dictionary using their complete case-folded
names:

```python
safe_targets = {
    target.casefold(): target
    for target in targets
    if target.casefold() not in PROTECTED_PROCESS_NAMES
}
```

Each running process is accepted only when its complete case-folded name is a
dictionary key:

```python
if name and name.casefold() in safe_targets:
```

This is equality-based dictionary membership. It does not use substring,
prefix, suffix, wildcard, or regular-expression matching.

Therefore, a target of `Discord.exe` matches capitalization variants such as
`DISCORD.EXE`, but does not match:

- `DiscordHelper.exe`
- `DiscordUpdater.exe`
- `MyDiscord.exe`
- `Discord.exe.backup`
- Any other partially or similarly named executable

The resulting `ProcessMatch` stores the exact psutil process object and PID that
were included in the preview. Closure operates on those previewed objects rather
than performing a broad name-based termination command.

## Existing safety layers confirmed

- Settings entries must be strings ending in `.exe`.
- Known protected Windows process names are rejected by the settings layer.
- The process-discovery layer independently filters protected names again.
- Discovery uses complete-name dictionary membership.
- Only configured and previewed matches are grouped for closure.
- The GUI performs a fresh scan immediately before confirmation.
- The confirmation lists exact executable names and PIDs.
- Graceful `WM_CLOSE` and forced fallback operate only on stored preview matches.
- Psutil checks PID identity and creation time before Windows force termination,
  protecting its `terminate()` operation from PID reuse.

## Genuine safety problems found and fixed

### 1. Empty injected process source could scan the real machine

Previous code selected the process iterator with:

```python
iterator = process_iterator or psutil.process_iter(["pid", "name"])
```

An explicitly supplied empty list is false in a Boolean context. Passing `[]`
therefore caused Airlock to ignore the supplied source and enumerate real host
processes instead.

This was changed to an explicit `None` check:

```python
iterator = (
    process_iterator
    if process_iterator is not None
    else psutil.process_iter(["pid", "name"])
)
```

An empty injected source now remains empty. Production still enumerates real
processes only when no source is supplied.

### 2. Window closure used a PID before checking previewed-process identity

The graceful-close path previously sent `WM_CLOSE` using the stored numeric PID
before checking whether the previewed psutil object still represented the
original process. If that process exited and Windows quickly reused its PID,
the window message could have been sent to the replacement process.

Airlock now verifies both conditions before sending any window message:

```python
if match.process.pid != match.pid:
    failures.append(f"PID {match.pid}: process identity mismatch; skipped")
    continue
if not match.process.is_running():
    graceful_count += 1
    continue
```

`psutil.Process.is_running()` verifies identity using both PID and creation time.
If the original process exited or its PID was reused, Airlock skips window
closure and forced termination. A manually inconsistent stored PID is reported
as a failure and skipped.

Expected psutil errors during identity verification are also handled by
recording a failure and skipping the process:

```python
except psutil.Error as error:
    failures.append(
        f"PID {match.pid}: could not verify process identity: {error}"
    )
    continue
```

The safe failure mode is therefore to leave the process alone when identity
cannot be verified.

## Tests added

### Empty injected source

`test_empty_injected_process_list_stays_empty` replaces
`psutil.process_iter()` with a function that fails if called, then supplies an
empty list. The test proves real enumeration does not occur.

### Similarly named process

`test_similarly_named_process_never_reaches_closure` supplies
`DiscordHelper.exe` while the configured target is `Discord.exe`.

The test proves:

- No match is produced.
- No PID reaches the window-closing function.
- The fake process's termination method is never called.
- Airlock reports the configured target as `Not running`.

### Reused or exited PID

`test_reused_pid_is_not_closed_or_terminated` supplies a preview record whose
process identity is no longer running.

The test proves:

- No PID reaches the window-closing function.
- Forced termination is not called.
- The vanished original process is treated as already closed.

### Mismatched stored identity

`test_mismatched_process_identity_is_skipped` supplies a `ProcessMatch` whose
stored PID differs from the psutil process object's PID.

The test proves:

- No window message is requested.
- Forced termination is not called.
- The result is `Failed` with an identity-mismatch explanation.

## Verification result

The complete automated suite was run after the fixes:

```text
collected 15 items
tests/test_processes.py ...........
tests/test_settings.py ....
15 passed in 0.05s
```

All tests use fake process objects for closure behavior. No real application or
unrelated process was terminated.

## Conclusion

Airlock matches complete executable names exactly and case-insensitively. A
similarly named process cannot enter the closure path merely because its name
contains, begins with, or resembles a configured target.

The two genuine safety weaknesses discovered during this review were corrected:
empty injected sources can no longer trigger host enumeration, and process
identity is now checked before graceful window closure. The closure path fails
safely by skipping a process whenever its stored identity is inconsistent or
cannot be verified.
