from guard.schemas import Intent, Listing, Usage


def structured_score(intent: Intent, listing: Listing) -> float:
    usage = 1.0 if intent.usage == Usage.ANY or listing.usage.value == intent.usage.value else 0.5 if listing.usage.value == "all" else 0.0
    brand = 1.0 if not intent.preferred_brand else float(listing.attributes.get("brand", "").casefold() == intent.preferred_brand.casefold())
    required = 1.0 if not intent.required_attributes else sum(listing.attributes.get(k) == v for k, v in intent.required_attributes.items()) / len(intent.required_attributes)
    price = max(0.0, min(1.0, 1 - listing.price_paise / intent.max_price_paise))
    return 0.40 * usage + 0.25 * brand + 0.20 * required + 0.15 * price


def rank_structured(intent: Intent, listings: list[Listing]) -> list[Listing]:
    return sorted(listings, key=lambda item: (-structured_score(intent, item), item.sku_id))

