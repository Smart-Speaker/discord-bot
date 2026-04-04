from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BotConfig:
    token: str
    prefix: str
    owner_id: int | None
    data_dir: str

    @classmethod
    def from_env(cls) -> "BotConfig":
        token = os.getenv("DISCORD_TOKEN")
        prefix = os.getenv("BOT_PREFIX", "!")
        owner_id_raw = os.getenv("OWNER_ID")
        data_dir = os.getenv("BOT_DATA_DIR", "/appdata")

        if not token:
            raise ValueError("DISCORD_TOKEN is not set")

        if not owner_id_raw:
            return cls(token=token, prefix=prefix, owner_id=None, data_dir=data_dir)

        try:
            owner_id = int(owner_id_raw)
        except ValueError as exc:
            raise ValueError("OWNER_ID must be a valid Discord user ID number") from exc

        return cls(token=token, prefix=prefix, owner_id=owner_id, data_dir=data_dir)
