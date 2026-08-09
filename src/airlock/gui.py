from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from airlock.processes import (
    ProcessMatch,
    close_previewed_processes,
    find_target_processes,
)
from airlock.settings import SettingsError, load_enabled_targets


SETTINGS_PATH = Path.cwd() / "airlock_settings.json"


class AirlockApp:
    def __init__(self, root: tk.Tk, targets: list[str]) -> None:
        self.root = root
        self.targets = targets
        self.matches: list[ProcessMatch] = []

        root.title("Airlock")
        root.geometry("560x430")
        root.minsize(480, 360)

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Airlock", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="Preview the configured apps, then end the workday when ready.",
        ).pack(anchor="w", pady=(4, 14))

        self.output = tk.Text(frame, height=14, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True)

        button_row = ttk.Frame(frame)
        button_row.pack(fill="x", pady=(14, 0))
        ttk.Button(button_row, text="Refresh Preview", command=self.refresh_preview).pack(side="left")
        ttk.Button(button_row, text="End Workday", command=self.end_workday).pack(side="right")

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

        lines = ["Current exact-name preview:", ""]
        for target, pids in matches_by_target.items():
            if pids:
                lines.append(f"Running: {target} (PID {', '.join(map(str, pids))})")
            else:
                lines.append(f"Not running: {target}")
        self.show_lines(lines)

    def end_workday(self) -> None:
        self.refresh_preview()
        if not self.matches:
            messagebox.showinfo("Airlock", "None of the enabled targets are running.")
            return

        preview = "\n".join(f"{match.target} (PID {match.pid})" for match in self.matches)
        confirmed = messagebox.askyesno(
            "Confirm End Workday",
            "Airlock will ask these exact matches to close normally, wait up to "
            f"5 seconds, then force-close survivors:\n\n{preview}\n\nContinue?",
        )
        if not confirmed:
            return

        results = close_previewed_processes(self.targets, self.matches)
        self.show_lines(
            ["End Workday results:", ""]
            + [f"{result.status}: {result.target} — {result.detail}" for result in results]
        )


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
