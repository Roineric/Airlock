import psutil

from airlock.processes import (
    ProcessMatch,
    close_previewed_processes,
    find_target_processes,
)


class FakeProcess:
    def __init__(self, pid, name, terminate_error=None, wait_errors=None, running=True):
        self.pid = pid
        self.info = {"pid": pid, "name": name}
        self.terminate_error = terminate_error
        self.wait_errors = list(wait_errors or [])
        self.terminate_called = False
        self.running = running

    def is_running(self):
        return self.running

    def terminate(self):
        self.terminate_called = True
        if self.terminate_error:
            raise self.terminate_error

    def wait(self, timeout):
        if self.wait_errors:
            error = self.wait_errors.pop(0)
            if error:
                raise error
        return 0


def test_finds_only_complete_case_insensitive_names():
    exact = FakeProcess(10, "Discord.exe")
    different_case = FakeProcess(11, "telegram.EXE")
    partial = FakeProcess(12, "DiscordHelper.exe")

    matches = find_target_processes(
        ["discord.exe", "Telegram.exe"],
        process_iterator=[exact, different_case, partial],
    )

    assert [(match.target, match.pid) for match in matches] == [
        ("discord.exe", 10),
        ("Telegram.exe", 11),
    ]


def test_protected_process_is_never_matched():
    explorer = FakeProcess(20, "explorer.exe")

    assert find_target_processes(["explorer.exe"], [explorer]) == []


def test_empty_injected_process_list_stays_empty(monkeypatch):
    def fail_if_real_processes_are_scanned(*_args, **_kwargs):
        raise AssertionError("Real process enumeration must not run")

    monkeypatch.setattr(psutil, "process_iter", fail_if_real_processes_are_scanned)

    assert find_target_processes(["Discord.exe"], process_iterator=[]) == []


def test_similarly_named_process_never_reaches_closure():
    helper = FakeProcess(25, "DiscordHelper.exe")
    matches = find_target_processes(["Discord.exe"], [helper])
    closed_pids = []

    results = close_previewed_processes(
        ["Discord.exe"],
        matches,
        window_closer=lambda pid: closed_pids.append(pid),
    )

    assert matches == []
    assert closed_pids == []
    assert helper.terminate_called is False
    assert results[0].status == "Not running"


def test_reused_pid_is_not_closed_or_terminated():
    replaced_process = FakeProcess(27, "Discord.exe", running=False)
    match = ProcessMatch("Discord.exe", 27, replaced_process)
    closed_pids = []

    results = close_previewed_processes(
        ["Discord.exe"],
        [match],
        window_closer=lambda pid: closed_pids.append(pid),
    )

    assert closed_pids == []
    assert replaced_process.terminate_called is False
    assert results[0].status == "Closed"


def test_mismatched_process_identity_is_skipped():
    discord = FakeProcess(28, "Discord.exe")
    mismatched_match = ProcessMatch("Discord.exe", 29, discord)
    closed_pids = []

    results = close_previewed_processes(
        ["Discord.exe"],
        [mismatched_match],
        window_closer=lambda pid: closed_pids.append(pid),
    )

    assert closed_pids == []
    assert discord.terminate_called is False
    assert results[0].status == "Failed"
    assert "identity mismatch" in results[0].detail


def test_force_terminates_only_previewed_processes_without_windows():
    discord = FakeProcess(30, "Discord.exe")
    match = ProcessMatch("Discord.exe", 30, discord)

    results = close_previewed_processes(
        ["Discord.exe", "Telegram.exe"],
        [match],
        window_closer=lambda _pid: 0,
    )

    assert discord.terminate_called is True
    assert [result.status for result in results] == ["Closed", "Not running"]
    assert "Force-closed 1" in results[0].detail


def test_graceful_close_does_not_force_terminate():
    discord = FakeProcess(35, "Discord.exe")
    match = ProcessMatch("Discord.exe", 35, discord)

    results = close_previewed_processes(
        ["Discord.exe"],
        [match],
        window_closer=lambda pid: 1 if pid == 35 else 0,
    )

    assert discord.terminate_called is False
    assert results[0].status == "Closed"
    assert "Gracefully closed 1" in results[0].detail


def test_reports_access_denied_without_crashing():
    discord = FakeProcess(40, "Discord.exe", terminate_error=psutil.AccessDenied(40))
    match = ProcessMatch("Discord.exe", 40, discord)

    results = close_previewed_processes(
        ["Discord.exe"],
        [match],
        window_closer=lambda _pid: 0,
    )

    assert results[0].status == "Failed"
    assert "access denied" in results[0].detail


def test_force_terminates_after_graceful_timeout():
    discord = FakeProcess(
        50,
        "Discord.exe",
        wait_errors=[psutil.TimeoutExpired(5, pid=50), None],
    )
    match = ProcessMatch("Discord.exe", 50, discord)

    results = close_previewed_processes(
        ["Discord.exe"],
        [match],
        window_closer=lambda _pid: 1,
    )

    assert discord.terminate_called is True
    assert results[0].status == "Closed"
    assert "Force-closed 1" in results[0].detail


def test_reports_failure_when_force_termination_times_out():
    discord = FakeProcess(
        60,
        "Discord.exe",
        wait_errors=[psutil.TimeoutExpired(3, pid=60)],
    )
    match = ProcessMatch("Discord.exe", 60, discord)

    results = close_previewed_processes(
        ["Discord.exe"],
        [match],
        window_closer=lambda _pid: 0,
    )

    assert results[0].status == "Failed"
    assert "did not close after force termination" in results[0].detail
