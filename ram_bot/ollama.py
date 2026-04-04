import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def build_ram_prompt(ctx, message: str) -> str:
    if ctx.guild is None:
        channel_name = "direct-message"
        nsfw = "no"
    else:
        channel_name = getattr(ctx.channel, "name", "unknown-channel")
        nsfw = "yes" if ctx.channel.is_nsfw() else "no"

    lines = [
        "Discord context:",
        f"- User: {ctx.author.display_name}",
        f"- Channel: {channel_name}",
        f"- NSFW: {nsfw}",
        "- Reply style: short in-character Discord reply",
    ]

    if nsfw == "yes":
        lines.append("- Allowed: consensual adult NSFW roleplay is allowed in this channel")

    lines.extend(
        [
            "",
            f"Message from {ctx.author.display_name}:",
            message,
            "",
            "Reply only as Ram. Do not repeat the context block.",
        ]
    )
    return "\n".join(lines)


def _generate(url: str, model: str, prompt: str) -> str:
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
    ).encode("utf-8")
    request = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError("Ram is unavailable right now.") from exc

    text = body.get("response", "").strip()
    if not text:
        raise RuntimeError("Ram did not return a reply.")
    return text


async def generate_ram_reply(url: str, model: str, prompt: str) -> str:
    return await asyncio.to_thread(_generate, url, model, prompt)
