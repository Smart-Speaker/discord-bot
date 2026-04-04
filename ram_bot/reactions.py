import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from ram_bot.constants import OTAKU_GIFS_API_URL, ROLEPLAY_GIFS, ROLEPLAY_REACTIONS


def _fetch_reaction_gif_url(reaction: str) -> str | None:
    request_url = OTAKU_GIFS_API_URL.format(reaction=reaction)

    try:
        with urlopen(request_url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None

    return payload.get("url")


async def get_reaction_gif(action_name: str) -> str:
    reaction = ROLEPLAY_REACTIONS[action_name]
    gif_url = await asyncio.to_thread(_fetch_reaction_gif_url, reaction)

    if gif_url:
        return gif_url

    fallbacks = ROLEPLAY_GIFS[action_name]
    return fallbacks[0]
