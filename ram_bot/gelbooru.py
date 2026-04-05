import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
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


def normalize_image_url(url: str | None) -> str | None:
    if not url:
        return None
    cleaned = str(url).strip()
    if not cleaned:
        return None
    if cleaned.startswith("//"):
        return f"https:{cleaned}"
    if cleaned.startswith("/"):
        return f"https://gelbooru.com{cleaned}"
    if cleaned.startswith("http://"):
        return "https://" + cleaned[len("http://"):]
    return cleaned


def is_supported_embed_image(url: str | None) -> bool:
    if not url:
        return False
    path = urlparse(url).path.lower()
    return path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))


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
        if not isinstance(post, dict):
            continue
        candidates = [
            normalize_image_url(post.get("sample_url")),
            normalize_image_url(post.get("file_url")),
            normalize_image_url(post.get("preview_url")),
        ]
        image_url = next((candidate for candidate in candidates if is_supported_embed_image(candidate)), None)
        fallback_url = next((candidate for candidate in candidates if candidate), None)
        if image_url:
            post["image_url"] = image_url
            post["fallback_url"] = fallback_url or image_url
            return post
        if fallback_url:
            post["image_url"] = fallback_url
            post["fallback_url"] = fallback_url
            return post
    return None


async def get_gelbooru_post(auth_suffix: str, include_csv: str, exclude_csv: str, query: str) -> tuple[dict, str]:
    tags = build_gelbooru_tags(include_csv, exclude_csv, query)
    post = await asyncio.to_thread(_fetch_post, tags, auth_suffix)
    if not post:
        raise RuntimeError("request_failed")
    return post, tags
