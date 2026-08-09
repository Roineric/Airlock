from dataclasses import dataclass
from typing import Iterable

import psutil

from airlock.settings import PROTECTED_PROCESS_NAMES
from airlock.windows import request_window_close


@dataclass(frozen=True)
class ProcessMatch:
    target: str
    pid: int
    process: psutil.Process


@dataclass(frozen=True)
class ProcessResult:
    target: str
    status: str
    detail: str


def find_target_processes(
    targets: Iterable[str],
    process_iterator=None,
) -> list[ProcessMatch]:
    """Return processes whose complete executable names match enabled targets."""
    safe_targets = {
        target.casefold(): target
        for target in targets
        if target.casefold() not in PROTECTED_PROCESS_NAMES
    }
    iterator = (
        process_iterator
        if process_iterator is not None
        else psutil.process_iter(["pid", "name"])
    )
    matches: list[ProcessMatch] = []

    for process in iterator:
        try:
            name = process.info.get("name")
            if name and name.casefold() in safe_targets:
                matches.append(
                    ProcessMatch(
                        target=safe_targets[name.casefold()],
                        pid=process.info["pid"],
                        process=process,
                    )
                )
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue

    return matches


def close_previewed_processes(
    targets: Iterable[str],
    matches: Iterable[ProcessMatch],
    graceful_timeout: float = 5.0,
    force_timeout: float = 3.0,
    window_closer=request_window_close,
) -> list[ProcessResult]:
    """Ask previewed apps to close, then force-terminate only survivors."""
    target_list = list(targets)
    grouped = {target.casefold(): [] for target in target_list}
    for match in matches:
        key = match.target.casefold()
        if key in grouped and key not in PROTECTED_PROCESS_NAMES:
            grouped[key].append(match)

    results: list[ProcessResult] = []
    for target in target_list:
        target_matches = grouped[target.casefold()]
        if not target_matches:
            results.append(ProcessResult(target, "Not running", "No exact match found."))
            continue

        failures: list[str] = []
        graceful_count = 0
        survivors: list[ProcessMatch] = []
        for match in target_matches:
            try:
                if match.process.pid != match.pid:
                    failures.append(f"PID {match.pid}: process identity mismatch; skipped")
                    continue
                if not match.process.is_running():
                    graceful_count += 1
                    continue
            except psutil.Error as error:
                failures.append(f"PID {match.pid}: could not verify process identity: {error}")
                continue

            try:
                posted_windows = window_closer(match.pid)
            except psutil.NoSuchProcess:
                continue
            except OSError:
                posted_windows = 0

            if not posted_windows:
                survivors.append(match)
                continue

            try:
                match.process.wait(timeout=graceful_timeout)
                graceful_count += 1
            except psutil.NoSuchProcess:
                graceful_count += 1
            except (psutil.TimeoutExpired, psutil.AccessDenied):
                survivors.append(match)

        forced_count = 0
        force_requested: list[ProcessMatch] = []
        for match in survivors:
            try:
                match.process.terminate()
                force_requested.append(match)
            except psutil.NoSuchProcess:
                graceful_count += 1
            except psutil.AccessDenied:
                failures.append(f"PID {match.pid}: force-close access denied")
            except psutil.Error as error:
                failures.append(f"PID {match.pid}: force-close failed: {error}")

        for match in force_requested:
            try:
                match.process.wait(timeout=force_timeout)
                forced_count += 1
            except psutil.NoSuchProcess:
                forced_count += 1
            except psutil.TimeoutExpired:
                failures.append(f"PID {match.pid}: did not close after force termination")
            except psutil.AccessDenied:
                failures.append(f"PID {match.pid}: could not verify force closure")

        if failures:
            results.append(ProcessResult(target, "Failed", "; ".join(failures)))
        else:
            detail_parts = []
            if graceful_count:
                detail_parts.append(f"gracefully closed {graceful_count}")
            if forced_count:
                detail_parts.append(f"force-closed {forced_count}")
            detail = ", ".join(detail_parts) or "Process already exited."
            results.append(ProcessResult(target, "Closed", detail.capitalize() + "."))

    return results
