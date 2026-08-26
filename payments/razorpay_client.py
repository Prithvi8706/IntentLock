from typing import Any

import razorpay

from audit.ledger import Ledger
from guard.schemas import Action, DecisionRecord, EventType, Listing


def validate_test_key(key_id: str) -> None:
    if not key_id.startswith("rzp_test_"):
        raise ValueError("Decision Guard accepts Razorpay Test Mode keys only")


class RazorpayOrderClient:
    def __init__(self, key_id: str, key_secret: str, ledger: Ledger | None = None) -> None:
        validate_test_key(key_id)
        self.client = razorpay.Client(auth=(key_id, key_secret))
        self.ledger = ledger or Ledger()

    def create_order(self, decision: DecisionRecord, listing: Listing, quantity: int) -> dict[str, Any]:
        if decision.action != Action.ALLOW or not decision.intent_hash:
            raise PermissionError("a validated ALLOW decision is required")
        if existing := self.ledger.existing_order(decision.decision_id):
            return existing
        payload = {"amount": listing.price_paise * quantity, "currency": "INR", "receipt": decision.decision_id,
                   "notes": {"decision_id": decision.decision_id,
                             "intent_hash_prefix": decision.intent_hash.removeprefix("sha256:")[:16], "sku_id": listing.sku_id}}
        try:
            order = self.client.order.create(payload)
            self.ledger.append(EventType.ORDER_CREATED, order, decision.decision_id)
            return order
        except Exception as exc:
            self.ledger.append(EventType.ORDER_FAILED, {"error_class": type(exc).__name__}, decision.decision_id)
            raise

