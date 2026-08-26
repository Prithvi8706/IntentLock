import re
from decimal import ROUND_HALF_UP, Decimal
from uuid import uuid4

from guard.schemas import Intent, Usage


def rupees_to_paise(value: str | int | Decimal) -> int:
    return int((Decimal(str(value)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


class IntentCompiler:
    """Conservative local compiler. Missing hard fields remain a manual-form concern."""

    def compile(self, raw_request: str) -> Intent:
        lowered = raw_request.lower()
        price = re.search(r"(?:under|below|max(?:imum)?|₹|rs\.?)\s*([\d,]+(?:\.\d{1,2})?)", lowered)
        category = None
        for phrase, value in (
            ("basketball shoe", "basketball_shoes"),
            ("running shoe", "running_shoes"),
            ("headphone", "headphones"),
        ):
            if phrase in lowered:
                category = value
                break
        if not price or not category:
            raise ValueError("Please provide a category and maximum price")
        usage = Usage.OUTDOOR if "outdoor" in lowered else Usage.INDOOR if "indoor" in lowered else Usage.ANY
        brand = (match.group(1).strip() if (match := re.search(r"(?:prefer(?:ably)?|brand)\s+([a-z][a-z0-9 ]+)", lowered)) else None)
        return Intent(
            intent_id=f"int_{uuid4().hex[:12]}", intent_version=1, raw_request=raw_request,
            category=category, usage=usage, max_price_paise=rupees_to_paise(price.group(1).replace(",", "")),
            preferred_brand=brand,
        )

