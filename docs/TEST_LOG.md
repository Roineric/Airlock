# Airlock test log

## 2026-08-09 — Safe application smoke and process test

- Time completed: `2026-08-09 09:04:35 +05:00`
- Platform: Windows
- Python: CPython 3.14.7 from `.venv`
- Safety rule: no normal user application was configured or terminated during this test.

### Test design and safety boundary

The process test used a private copy of Windows `PING.EXE` named
`AirlockHarmlessProbe.exe` in the repository root. Its unique name was passed
directly to a temporary `AirlockApp` instance and was never added to
`airlock_settings.json`.

The probe was launched with PID `8748`, hidden and with its output discarded.
Only the exact executable name `AirlockHarmlessProbe.exe` was eligible for the
test callback. The normal configured targets—Discord, Telegram, WhatsApp,
RingCentral, Epic Games Launcher, and Ubisoft Connect—were not passed to the
termination test.

The confirmation dialog was replaced with a test-only function returning `True`
so the same `AirlockApp.end_workday()` callback used by the real button could be
exercised without manual interaction. Process discovery, exact-name matching,
closure logic, psutil waiting, and GUI result rendering remained real.

### Case 1: target process is not running

The real `AirlockApp` GUI was constructed with the sole target
`AirlockHarmlessProbe.exe` before the probe existed. The preview output was:

```text
Current exact-name preview:

Not running: AirlockHarmlessProbe.exe
```

Evidence:

- No probe process had been launched.
- Airlock reported the unique target as `Not running`.
- No End Workday action or termination call was made in this case.

Result: **Passed**.

### Case 2: one harmless test process is running

The uniquely named probe was launched as PID `8748`. Before the callback,
`subprocess.poll()` confirmed that it was alive:

```text
PROBE_RUNNING_BEFORE=True
```

Airlock's real preview reported:

```text
Current exact-name preview:

Running: AirlockHarmlessProbe.exe (PID 8748)
```

The test then invoked the same `end_workday()` function registered to the GUI
button. The result displayed by Airlock was:

```text
End Workday results:

Closed: AirlockHarmlessProbe.exe — Force-closed 1.
```

`PING.EXE` had no top-level GUI window, so there was no window that could accept
`WM_CLOSE`. The expected safe fallback was therefore used: force termination of
the already-previewed, uniquely named disposable PID.

Afterward:

```text
PROBE_EXIT_CODE=15
PROBE_RUNNING_AFTER=False
```

A final `Get-Process -Name AirlockHarmlessProbe` check returned no process. No
other executable name was supplied to the closure function.

Result: **Passed**.

### Case 3: settings survive application restart

Before startup, the settings file was 162 bytes and had this SHA-256 hash:

```text
008C72DEB5BD4D2405EDB10F28C2104B4EEF20EFBCD927DC65F61C83BBFEBF17
```

The real `gui.main()` startup and Tk `mainloop()` path was run twice. Each test
window hid itself and scheduled normal Tk destruction after 100 milliseconds.
The End Workday callback was not invoked during either restart.

```text
APP_RESTART_1=completed
APP_RESTART_2=completed
```

After both application runs, the settings file remained 162 bytes and had the
same SHA-256 hash:

```text
008C72DEB5BD4D2405EDB10F28C2104B4EEF20EFBCD927DC65F61C83BBFEBF17
```

An identical cryptographic hash is strong evidence that the exact file bytes
did not change across the two startup/shutdown cycles.

Result: **Passed**.

### Cleanup and regression evidence

- `AirlockHarmlessProbe.exe` was removed after the test.
- `Test-Path .\AirlockHarmlessProbe.exe` returned `False`.
- No process named `AirlockHarmlessProbe` remained.
- `airlock_settings.json` retained its original SHA-256 hash.
- The automated suite was rerun: **11 tests passed in 0.07 seconds**.

### Overall result

All three requested cases passed. The only terminated process was the disposable
probe created for this test. No unrelated process was targeted or terminated.
