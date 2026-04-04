import json
from pathlib import Path


class GuildSettingsStore:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / "guild_settings.json"
        self._data = self._load()

    def _load(self) -> dict[str, dict]:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def save(self):
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def get_guild(self, guild_id: int) -> dict:
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
