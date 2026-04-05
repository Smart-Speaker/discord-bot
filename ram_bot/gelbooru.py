import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from ram_bot.constants import GELBOORU_API_URL


def split_tag_csv(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def normalize_excluded_tag(tag: str) -> str:
    cleaned = tag.strip()
    if not cleaned:
        return ""
    return cleaned if cleaned.startswith("-") else f"-{cleaned}"


def build_gelbooru_tags(include_csv: str, exclude_csv: str, query: str) -> str:
    include_tags = split_tag_csv(include_csv)
    query_tags = split_tag_csv(query)
    exclude_tags = [normalize_excluded_tag(tag) for tag in split_tag_csv(exclude_csv)]
    all_tags = [tag for tag in [*include_tags, *query_tags, *exclude_tags] if tag]
    return "+".join(all_tags)


def _fetch_post(tags: str, auth_suffix: str) -> dict | None:
    request_url = f"{GELBOORU_API_URL}&tags={quote(tags, safe=':+-_()')}{auth_suffix}"

    try:
        with urlopen(request_url, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None

    posts = payload.get("post", [])
    if isinstance(posts, dict):
        posts = [posts]
    if not posts:
        return None

    for post in posts:
        if isinstance(post, dict) and post.get("file_url"):
            return post
    return None


async def get_gelbooru_post(auth_suffix: str, include_csv: str, exclude_csv: str, query: str) -> tuple[dict, str]:
    tags = build_gelbooru_tags(include_csv, exclude_csv, query)
    post = await asyncio.to_thread(_fetch_post, tags, auth_suffix)
    if not post:
        raise RuntimeError("request_failed")
    return post, tags
