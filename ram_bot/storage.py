import json
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def save(self):
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")


class GuildSettingsStore(JsonStore):
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        super().__init__(self.data_dir / "guild_settings.json")

    def get_guild(self, guild_id: int) -> dict[str, Any]:
        key = str(guild_id)
        if key not in self._data:
            self._data[key] = {}
        return self._data[key]

    def update_guild(self, guild_id: int, **fields):
        settings = self.get_guild(guild_id)
        for key, value in fields.items():
            if value is None:
                settings.pop(key, None)
            else:
                settings[key] = value
        self.save()
        return settings


class UserProfileStore(JsonStore):
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        super().__init__(self.data_dir / "user_profiles.json")

    def get_profile(self, scope_id: str, user_id: int) -> dict[str, Any]:
        scope = self._data.setdefault(scope_id, {})
        profile = scope.setdefault(
            str(user_id),
            {
                "xp": 0,
                "level": 0,
                "affinity": 0,
                "warnings": [],
                "last_daily": None,
                "last_checkin": None,
                "last_dailyhug": None,
                "daily_streak": 0,
                "last_interaction_at": None,
                "last_xp_at": None,
                "last_roleplay_at": None,
                "last_roleplay_action": None,
                "recent_interactions": [],
                "dm_relationship": "friends",
                "dm_mood": "neutral",
            },
        )
        profile.setdefault("last_interaction_at", None)
        profile.setdefault("recent_interactions", [])
        profile.setdefault("dm_relationship", "friends")
        profile.setdefault("dm_mood", "neutral")
        return profile

    def all_profiles(self, scope_id: str) -> dict[str, dict[str, Any]]:
        return self._data.setdefault(scope_id, {})

    def save_profile(self, scope_id: str, user_id: int, profile: dict[str, Any]):
        self._data.setdefault(scope_id, {})[str(user_id)] = profile
        self.save()


class ReminderStore(JsonStore):
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        super().__init__(self.data_dir / "reminders.json")
        self._data.setdefault("items", [])

    def add(self, reminder: dict[str, Any]):
        self._data.setdefault("items", []).append(reminder)
        self.save()

    def all(self) -> list[dict[str, Any]]:
        return self._data.setdefault("items", [])

    def remove_ids(self, reminder_ids: set[str]):
        self._data["items"] = [item for item in self.all() if item["id"] not in reminder_ids]
        self.save()
