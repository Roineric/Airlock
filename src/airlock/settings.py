import json
from pathlib import Path


PROTECTED_PROCESS_NAMES = frozenset(
    {
        "csrss.exe",
        "dwm.exe",
        "explorer.exe",
        "lsass.exe",
        "services.exe",
        "smss.exe",
        "svchost.exe",
        "system",
        "wininit.exe",
        "winlogon.exe",
    }
)


class SettingsError(ValueError):
    """Raised when the local settings file is unsafe or malformed."""


def load_enabled_targets(path: Path) -> list[str]:
    """Load and validate exact executable names from a JSON settings file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SettingsError(f"Could not read {path}: {error}") from error

    if not isinstance(data, dict) or set(data) != {"enabled_targets"}:
        raise SettingsError("Settings must contain only 'enabled_targets'.")

    targets = data["enabled_targets"]
    if not isinstance(targets, list) or not all(isinstance(item, str) for item in targets):
        raise SettingsError("'enabled_targets' must be a list of executable names.")

    normalized: list[str] = []
    seen: set[str] = set()
    for target in targets:
        clean_target = target.strip()
        folded_target = clean_target.casefold()
        if not clean_target or not clean_target.casefold().endswith(".exe"):
            raise SettingsError(f"Invalid executable name: {target!r}")
        if folded_target in PROTECTED_PROCESS_NAMES:
            raise SettingsError(f"Protected Windows process is not allowed: {clean_target}")
        if folded_target not in seen:
            normalized.append(clean_target)
            seen.add(folded_target)

    return normalized
