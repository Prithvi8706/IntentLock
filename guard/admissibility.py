from dataclasses import dataclass

from guard.schemas import Intent, Listing, Usage


@dataclass(frozen=True)
class GateResult:
    eligible: bool
    failures: tuple[str, ...]


def check_listing(intent: Intent, listing: Listing) -> GateResult:
    failures: list[str] = []
    if listing.category != intent.category:
        failures.append("CATEGORY_MISMATCH")
    if intent.usage != Usage.ANY and listing.usage.value not in (intent.usage.value, "all"):
        failures.append("USAGE_MISMATCH")
    if listing.price_paise > intent.max_price_paise:
        failures.append("PRICE_EXCEEDS_CAP")
    if listing.stock < intent.quantity:
        failures.append("INSUFFICIENT_STOCK")
    for key, value in intent.required_attributes.items():
        if listing.attributes.get(key) != value:
            failures.append(f"ATTRIBUTE_MISMATCH:{key}")
    return GateResult(not failures, tuple(failures))


def gate(intent: Intent, listings: list[Listing]) -> tuple[list[Listing], dict[str, tuple[str, ...]]]:
    results = {item.sku_id: check_listing(intent, item) for item in listings}
    return [item for item in listings if results[item.sku_id].eligible], {k: v.failures for k, v in results.items() if not v.eligible}

