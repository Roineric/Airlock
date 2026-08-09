from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from airlock.processes import (
    ProcessMatch,
    ProcessResult,
    close_previewed_processes,
    find_target_processes,
)
from airlock.settings import SettingsError, load_enabled_targets


SETTINGS_PATH = Path.cwd() / "airlock_settings.json"

APP_DISPLAY_NAMES = {
    "discord.exe": "Discord",
    "telegram.exe": "Telegram",
    "ringcentral.exe": "RingCentral",
    "epicgameslauncher.exe": "Epic Games Launcher",
    "upc.exe": "Ubisoft Connect",
}


def app_display_name(executable_name: str) -> str:
    """Return a friendly label without changing the exact process target."""
    known_name = APP_DISPLAY_NAMES.get(executable_name.casefold())
    if known_name:
        return known_name
    if executable_name.casefold().endswith(".exe"):
        return executable_name[:-4]
    return executable_name


class AirlockApp:
    def __init__(self, root: tk.Tk, targets: list[str]) -> None:
        self.root = root
        self.targets = targets
        self.matches: list[ProcessMatch] = []
        self.closing = False
        self.workday_ended = False
        self.closure_queue: queue.Queue[
            tuple[str, list[ProcessResult] | Exception]
        ] = queue.Queue()

        root.title("Airlock")
        root.geometry("560x430")
        root.minsize(480, 360)

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Preview the configured apps, then end the workday when ready.",
        ).pack(anchor="w", pady=(0, 14))

        self.output = tk.Text(frame, height=14, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True)

        button_row = ttk.Frame(frame)
        button_row.pack(fill="x", pady=(14, 0))
        self.refresh_button = ttk.Button(
            button_row,
            text="Refresh Preview",
            command=self.refresh_preview,
        )
        self.refresh_button.pack(side="left")
        self.end_button = ttk.Button(
            button_row,
            text="End Workday",
            command=self.end_workday,
        )
        self.end_button.pack(side="right")

        self.refresh_preview()

    def show_lines(self, lines: list[str]) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", "\n".join(lines))
        self.output.configure(state="disabled")

    def refresh_preview(self) -> None:
        self.matches = find_target_processes(self.targets)
        matches_by_target: dict[str, list[int]] = {target: [] for target in self.targets}
        for match in self.matches:
            matches_by_target[match.target].append(match.pid)

        lines = ["Current app preview:", ""]
        for target, pids in matches_by_target.items():
            display_name = app_display_name(target)
            if pids:
                lines.append(f"Running: {display_name}")
            else:
                lines.append(f"Not running: {display_name}")
        self.show_lines(lines)

        if not self.closing and self.workday_ended and self.matches:
            self.workday_ended = False
            self.end_button.configure(text="End Workday", state="normal")
        elif not self.closing and self.workday_ended:
            self.end_button.configure(text="Workday Ended ✓", state="disabled")

    def end_workday(self) -> None:
        self.refresh_preview()
        if not self.matches:
            messagebox.showinfo("Airlock", "None of the enabled targets are running.")
            return

        preview = "\n".join(
            f"{app_display_name(match.target)} (PID {match.pid})"
            for match in self.matches
        )
        confirmed = messagebox.askyesno(
            "Confirm End Workday",
            "Airlock will ask these exact matches to close normally, wait up to "
            f"5 seconds, then force-close survivors:\n\n{preview}\n\nContinue?",
        )
        if not confirmed:
            return

        self.closing = True
        self.end_button.configure(text="Ending Workday…", state="disabled")
        self.refresh_button.configure(state="disabled")
        matches = list(self.matches)
        worker = threading.Thread(
            target=self.run_closure,
            args=(matches,),
            daemon=True,
        )
        worker.start()
        self.root.after(50, self.poll_closure)

    def run_closure(self, matches: list[ProcessMatch]) -> None:
        """Run slow process waits outside Tkinter's event thread."""
        try:
            results = close_previewed_processes(self.targets, matches)
        except Exception as error:
            self.closure_queue.put(("error", error))
        else:
            self.closure_queue.put(("results", results))

    def poll_closure(self) -> None:
        """Collect worker output on Tkinter's event thread."""
        try:
            outcome, value = self.closure_queue.get_nowait()
        except queue.Empty:
            self.root.after(50, self.poll_closure)
            return

        self.closing = False
        self.refresh_button.configure(state="normal")
        if outcome == "error":
            self.end_button.configure(text="End Workday", state="normal")
            self.show_lines(["End Workday failed:", "", str(value)])
            return

        results = value
        self.show_lines(
            ["End Workday results:", ""]
            + [
                f"{result.status}: {app_display_name(result.target)} — {result.detail}"
                for result in results
            ]
        )
        if all(result.status != "Failed" for result in results):
            self.workday_ended = True
            self.end_button.configure(text="Workday Ended ✓", state="disabled")
        else:
            self.end_button.configure(text="End Workday", state="normal")


def main() -> None:
    root = tk.Tk()
    try:
        targets = load_enabled_targets(SETTINGS_PATH)
    except SettingsError as error:
        messagebox.showerror("Airlock settings error", str(error), parent=root)
        root.destroy()
        return

    AirlockApp(root, targets)
    root.mainloop()
