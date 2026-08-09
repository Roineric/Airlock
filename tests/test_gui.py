import queue

import airlock.gui as gui
from airlock.gui import AirlockApp, app_display_name
from airlock.processes import ProcessMatch, ProcessResult


class FakeButton:
    def __init__(self):
        self.options = {}

    def configure(self, **options):
        self.options.update(options)


def make_pollable_app(outcome, value):
    app = AirlockApp.__new__(AirlockApp)
    app.closing = True
    app.workday_ended = False
    app.closure_queue = queue.Queue()
    app.closure_queue.put((outcome, value))
    app.refresh_button = FakeButton()
    app.end_button = FakeButton()
    app.shown_lines = []
    app.show_lines = app.shown_lines.extend
    return app


def test_successful_closure_marks_workday_ended():
    results = [ProcessResult("Discord.exe", "Closed", "Gracefully closed 1.")]
    app = make_pollable_app("results", results)

    app.poll_closure()

    assert app.closing is False
    assert app.workday_ended is True
    assert app.refresh_button.options["state"] == "normal"
    assert app.end_button.options == {"text": "Workday Ended ✓", "state": "disabled"}


def test_process_failure_restores_end_workday_button():
    results = [ProcessResult("Discord.exe", "Failed", "Access denied.")]
    app = make_pollable_app("results", results)

    app.poll_closure()

    assert app.workday_ended is False
    assert app.end_button.options == {"text": "End Workday", "state": "normal"}
    assert app.shown_lines[0] == "End Workday results:"


def test_unexpected_worker_error_restores_button_and_reports_error():
    app = make_pollable_app("error", RuntimeError("unexpected test error"))

    app.poll_closure()

    assert app.workday_ended is False
    assert app.end_button.options == {"text": "End Workday", "state": "normal"}
    assert app.shown_lines == ["End Workday failed:", "", "unexpected test error"]


def test_known_executable_uses_friendly_application_name():
    assert app_display_name("EpicGamesLauncher.exe") == "Epic Games Launcher"
    assert app_display_name("UPC.EXE") == "Ubisoft Connect"


def test_unknown_executable_hides_only_exe_suffix():
    assert app_display_name("Example App.exe") == "Example App"


def test_results_show_application_name_instead_of_executable():
    results = [ProcessResult("Discord.exe", "Closed", "Gracefully closed 1.")]
    app = make_pollable_app("results", results)

    app.poll_closure()

    assert app.shown_lines == [
        "End Workday results:",
        "",
        "Closed: Discord — Gracefully closed 1.",
    ]


def test_preview_shows_application_names_without_enumerating_processes(monkeypatch):
    matches = [ProcessMatch("EpicGamesLauncher.exe", 42, object())]
    monkeypatch.setattr(gui, "find_target_processes", lambda targets: matches)
    app = AirlockApp.__new__(AirlockApp)
    app.targets = ["EpicGamesLauncher.exe", "Telegram.exe"]
    app.closing = False
    app.workday_ended = False
    app.end_button = FakeButton()
    app.shown_lines = []
    app.show_lines = app.shown_lines.extend

    app.refresh_preview()

    assert app.shown_lines == [
        "Current app preview:",
        "",
        "Running: Epic Games Launcher",
        "Not running: Telegram",
    ]
    assert all(".exe" not in line.casefold() for line in app.shown_lines)


def test_confirmation_shows_application_name_without_starting_worker(monkeypatch):
    captured = {}

    def capture_confirmation(title, message):
        captured["title"] = title
        captured["message"] = message
        return False

    monkeypatch.setattr(gui.messagebox, "askyesno", capture_confirmation)
    app = AirlockApp.__new__(AirlockApp)
    app.matches = [ProcessMatch("Discord.exe", 73, object())]
    app.refresh_preview = lambda: None

    app.end_workday()

    assert captured["title"] == "Confirm End Workday"
    assert "Discord (PID 73)" in captured["message"]
    assert "Discord.exe" not in captured["message"]
