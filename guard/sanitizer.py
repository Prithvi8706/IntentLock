import re

from guard.detector import SIGNALS, ZERO_WIDTH


def sanitize(text: str, flagged: bool) -> str:
    if not flagged:
        return text
    cleaned = ZERO_WIDTH.sub("", text)
    for pattern, _, _ in SIGNALS:
        cleaned = re.sub(pattern, "[removed]", cleaned, flags=re.I)
    return cleaned

