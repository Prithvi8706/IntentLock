from guard.admissibility import check_listing
from guard.intent_store import verify_intent_hash
from guard.schemas import Intent, Listing


def final_validate(intent: Intent, listing: Listing) -> bool:
    return intent.confirmed_by_user and verify_intent_hash(intent) and check_listing(intent, listing).eligible

