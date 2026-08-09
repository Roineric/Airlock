# Airlock — Program Flow Walkthrough

## Startup

```text
python -m airlock
    → src/airlock/__main__.py
    → gui.main()
    → create Tk root
    → load airlock_settings.json
    → validate exact executable targets
    → construct AirlockApp
    → refresh the preview
```

If settings cannot be read or validated, Airlock displays an error and exits
without scanning or closing processes.

## Preview

`refresh_preview()` passes the configured executable names to
`find_target_processes()`. Discovery performs exact, case-insensitive equality
matching and filters protected Windows process names.

The GUI keeps executable names internally but shows friendly labels:

```text
Current app preview:

Running: Discord
Not running: Telegram
```

The ordinary preview omits PIDs for readability.

## Confirmation

When the user selects **End Workday**, Airlock refreshes the preview again. If no
target is running, it reports that result and stops. Otherwise, the confirmation
dialog lists friendly application names plus exact PIDs. Declining confirmation
performs no closure work.

## Background closure

After confirmation:

```text
disable both buttons
    → show Ending Workday…
    → start daemon worker thread
    → verify each previewed process identity
    → request WM_CLOSE for its top-level windows
    → wait up to five seconds
    → force-terminate verified survivors
    → wait up to three seconds to verify exit
    → return ProcessResult values through a queue
```

Tkinter polls the queue on its main thread, keeping the window responsive while
process waits happen in the worker.

## Completion

Results use friendly application names and one of these statuses:

- `Closed`
- `Not running`
- `Failed`

Complete success changes the main button to disabled `Workday Ended ✓`. A
failure or unexpected worker exception restores the enabled `End Workday`
button. Refreshing after another configured target starts also restores the
normal action state.

## Safety boundary

Closure operates only on exact process objects captured by the refreshed
preview. Stored and live PIDs must agree, psutil must verify process identity,
and protected targets are filtered independently. If identity cannot be
verified, Airlock leaves the process alone and reports a failure.
