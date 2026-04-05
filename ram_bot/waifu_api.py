import asyncio
import json
import random
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


WAIFU_IM_API_URL = "https://api.waifu.im/images"

WAIFU_IM_TAG_ALIASES = {
    "waifu": "waifu",
    "ero": "ero",
    "ecchi": "ecchi",
    "oppai": "oppai",
    "hentai": "hentai",
    "milf": "milf",
    "uniform": "uniform",
    "ass": "ass",
    "maid": "maid",
    "selfies": "selfies",
    "paizuri": "paizuri",
    "oral": "oral",
    "genshin impact": "genshin-impact",
    "genshin-impact": "genshin-impact",
    "raiden shogun": "raiden-shogun",
    "raiden-shogun": "raiden-shogun",
    "marin kitagawa": "marin-kitagawa",
    "marin-kitagawa": "marin-kitagawa",
    "mori calliope": "mori-calliope",
    "mori-calliope": "mori-calliope",
    "kamisato-ayaka": "kamisato-ayaka",
    "kamisato ayaka": "kamisato-ayaka",
    "arknights": "arknights",
    "black clover": "black-clover",
    "black-clover": "black-clover",
}


def normalize_waifu_tag(tag: str) -> str | None:
    cleaned = tag.strip().lower()
    if not cleaned:
        return None
    return WAIFU_IM_TAG_ALIASES.get(cleaned)


def _fetch_images(
    *,
    nsfw: bool,
    animated: bool | None,
    included_tags: list[str] | None,
    excluded_tags: list[str] | None,
    page: int,
    page_size: int,
    order_by: str,
) -> dict | None:
    params: list[tuple[str, str | int]] = [
        ("IsNsfw", str(nsfw)),
        ("OrderBy", order_by),
        ("Page", page),
        ("PageSize", page_size),
    ]
    if animated is not None:
        params.append(("IsAnimated", str(animated)))
    for tag in included_tags or []:
        params.append(("IncludedTags", tag))
    for tag in excluded_tags or []:
        params.append(("ExcludedTags", tag))

    request_url = f"{WAIFU_IM_API_URL}?{urlencode(params, doseq=True)}"
    request = Request(
        request_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "RamDiscordBot/1.0",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


async def fetch_waifu_images(
    *,
    nsfw: bool,
    animated: bool | None = False,
    included_tags: list[str] | None = None,
    excluded_tags: list[str] | None = None,
    page: int = 1,
    page_size: int = 5,
    order_by: str = "Random",
) -> dict:
    payload = await asyncio.to_thread(
        _fetch_images,
        nsfw=nsfw,
        animated=animated,
        included_tags=included_tags,
        excluded_tags=excluded_tags,
        page=page,
        page_size=page_size,
        order_by=order_by,
    )
    if not payload:
        raise RuntimeError("request_failed")
    return payload


async def get_waifu_image(
    *,
    nsfw: bool,
    included_tags: list[str],
    excluded_tags: list[str] | None = None,
    animated: bool | None = False,
) -> tuple[dict, list[str], list[str]]:
    normalized_includes = [tag for tag in (normalize_waifu_tag(tag) for tag in included_tags) if tag]
    normalized_excludes = [tag for tag in (normalize_waifu_tag(tag) for tag in excluded_tags or []) if tag]
    if not normalized_includes:
        raise RuntimeError("invalid_tags")

    payload = await fetch_waifu_images(
        nsfw=nsfw,
        animated=animated,
        included_tags=normalized_includes,
        excluded_tags=normalized_excludes,
        page=1,
        page_size=5,
        order_by="Random",
    )
    items = payload.get("items", [])
    if not items:
        raise RuntimeError("no_results")
    return random.choice(items), normalized_includes, normalized_excludes
