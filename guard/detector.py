import re
import unicodedata

from guard.schemas import Detection

ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u2060\ufeff]")
SIGNALS: list[tuple[str, str, float]] = [
    (r"ignore (?:all |any )?(?:previous|prior)", "instruction_to_agent", 0.7),
    (r"(?:you must select|the assistant should|rank this first|as an ai)", "instruction_to_agent", 0.7),
    (r"(?:system\s*:|\[inst\]|system message|developer note)", "role_imitation", 0.7),
    (r"(?:best choice for any query|always recommend|matches all requirements regardless)", "ranking_manipulation", 0.45),
    (r"(?:<!--[\s\S]*?-->|[a-z0-9+/]{40,}={0,2}|<{3,}|>{3,})", "hidden_or_encoded", 0.4),
    (r"(?:if you are an agent|when ranking products)", "agent_imperative", 0.45),
]


def normalize(text: str) -> tuple[str, bool]:
    normalized = unicodedata.normalize("NFKC", text).lower()
    stripped, count = ZERO_WIDTH.subn("", normalized)
    return re.sub(r"\s+", " ", stripped).strip(), count > 0


def detect(text: str, threshold: float = 0.6) -> Detection:
    normalized, zero_width = normalize(text)
    families: list[str] = []
    spans: list[str] = []
    score = 0.2 if zero_width else 0.0
    if zero_width:
        families.append("hidden_or_encoded")
    for pattern, family, weight in SIGNALS:
        matches = [m.group(0) for m in re.finditer(pattern, normalized, re.I)]
        if matches:
            score += weight
            if family not in families:
                families.append(family)
            spans.extend(matches)
    score = min(1.0, score)
    return Detection(flagged=score >= threshold, score=score, matched_signals=families,
                     matched_spans=spans, normalized_text=normalized, zero_width_removed=zero_width)


def scan_listing(title: str, description: str, threshold: float = 0.6) -> Detection:
    return detect(f"{title}\n{description}", threshold)

