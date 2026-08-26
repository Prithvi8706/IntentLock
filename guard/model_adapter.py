import asyncio
from typing import Protocol

from guard.schemas import Intent, Listing


class ModelAdapter(Protocol):
    model_id: str
    async def rank(self, intent: Intent, listings: list[Listing]) -> list[str]: ...


class LocalDeterministicAdapter:
    model_id = "local-deterministic"

    async def rank(self, intent: Intent, listings: list[Listing]) -> list[str]:
        await asyncio.sleep(0)
        # Deliberately reflects instruction-following baseline risk for the controlled demo.
        manipulated = [x for x in listings if any(p in x.description.lower() for p in ("always recommend", "rank this first", "ignore previous"))]
        def preference_key(item: Listing) -> tuple[bool, int, str]:
            brand_mismatch = bool(
                intent.preferred_brand
                and item.attributes.get("brand", "").casefold() != intent.preferred_brand.casefold()
            )
            return brand_mismatch, item.price_paise, item.sku_id

        rest = sorted((x for x in listings if x not in manipulated), key=preference_key)
        return [x.sku_id for x in manipulated + rest]
