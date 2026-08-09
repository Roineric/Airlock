import json

import pytest

from airlock.settings import SettingsError, load_enabled_targets


def test_loads_only_enabled_targets(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps({"enabled_targets": ["Discord.exe", "Telegram.exe"]}),
        encoding="utf-8",
    )

    assert load_enabled_targets(settings_path) == ["Discord.exe", "Telegram.exe"]


def test_rejects_protected_windows_process(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps({"enabled_targets": ["explorer.exe"]}),
        encoding="utf-8",
    )

    with pytest.raises(SettingsError, match="Protected Windows process"):
        load_enabled_targets(settings_path)


def test_rejects_extra_persisted_settings(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps({"enabled_targets": [], "theme": "dark"}),
        encoding="utf-8",
    )

    with pytest.raises(SettingsError, match="only 'enabled_targets'"):
        load_enabled_targets(settings_path)


def test_rejects_wrong_json_shape(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("[]", encoding="utf-8")

    with pytest.raises(SettingsError, match="only 'enabled_targets'"):
        load_enabled_targets(settings_path)
