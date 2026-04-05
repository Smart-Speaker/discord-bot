from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BotConfig:
    token: str
    prefix: str
    owner_id: int | None
    data_dir: str
    ai_enabled: bool
    ollama_url: str
    ollama_model: str
    gelbooru_auth: str
    gelbooru_global_include: str
    gelbooru_global_exclude: str

    @classmethod
    def from_env(cls) -> "BotConfig":
        token = os.getenv("DISCORD_TOKEN")
        prefix = os.getenv("BOT_PREFIX", "!")
        owner_id_raw = os.getenv("OWNER_ID")
        data_dir = os.getenv("BOT_DATA_DIR", "/appdata")
        ai_enabled = os.getenv("AI_ENABLED", "false").lower() == "true"
        ollama_url = os.getenv("OLLAMA_URL", "http://192.168.0.240:11434/api/generate")
        ollama_model = os.getenv("OLLAMA_MODEL", "ram")
        gelbooru_auth = os.getenv("GELBOORU_AUTH", "")
        gelbooru_global_include = os.getenv("GELBOORU_GLOBAL_INCLUDE", "")
        gelbooru_global_exclude = os.getenv("GELBOORU_GLOBAL_EXCLUDE", "")

        if not token:
            raise ValueError("DISCORD_TOKEN is not set")

        if not owner_id_raw:
            return cls(
                token=token,
                prefix=prefix,
                owner_id=None,
                data_dir=data_dir,
                ai_enabled=ai_enabled,
                ollama_url=ollama_url,
                ollama_model=ollama_model,
                gelbooru_auth=gelbooru_auth,
                gelbooru_global_include=gelbooru_global_include,
                gelbooru_global_exclude=gelbooru_global_exclude,
            )

        try:
            owner_id = int(owner_id_raw)
        except ValueError as exc:
            raise ValueError("OWNER_ID must be a valid Discord user ID number") from exc

        return cls(
            token=token,
            prefix=prefix,
            owner_id=owner_id,
            data_dir=data_dir,
            ai_enabled=ai_enabled,
            ollama_url=ollama_url,
            ollama_model=ollama_model,
            gelbooru_auth=gelbooru_auth,
            gelbooru_global_include=gelbooru_global_include,
            gelbooru_global_exclude=gelbooru_global_exclude,
        )
