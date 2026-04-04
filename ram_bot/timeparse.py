import re
from datetime import timedelta


TIME_PATTERN = re.compile(r"(?P<value>\d+)(?P<unit>[smhd])", re.IGNORECASE)


def parse_duration(text: str) -> timedelta | None:
    matches = list(TIME_PATTERN.finditer(text.strip()))
    if not matches:
        return None

    total = timedelta()
    consumed = "".join(match.group(0) for match in matches)
    if consumed.lower() != text.replace(" ", "").lower():
        return None

    for match in matches:
        value = int(match.group("value"))
        unit = match.group("unit").lower()
        if unit == "s":
            total += timedelta(seconds=value)
        elif unit == "m":
            total += timedelta(minutes=value)
        elif unit == "h":
            total += timedelta(hours=value)
        elif unit == "d":
            total += timedelta(days=value)

    return total if total.total_seconds() > 0 else None
