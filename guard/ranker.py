import random

from guard.model_adapter import ModelAdapter
from guard.schemas import Intent, Listing


async def rank(adapter: ModelAdapter, intent: Intent, listings: list[Listing], seed: int) -> tuple[list[str], list[str]]:
    candidates = list(listings)
    random.Random(seed).shuffle(candidates)
    order = [x.sku_id for x in candidates]
    ranked = await adapter.rank(intent, candidates)
    if not ranked or len(ranked) != len(set(ranked)) or any(sku not in order for sku in ranked):
        raise ValueError("ranker returned invalid SKU list")
    return ranked, order

