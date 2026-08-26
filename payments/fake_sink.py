from guard.schemas import Action, DecisionRecord, Listing


class FakePaymentSink:
    def __init__(self) -> None:
        self.orders: dict[str, dict] = {}

    def create_order(self, decision: DecisionRecord, listing: Listing, quantity: int) -> dict:
        if decision.action != Action.ALLOW or not decision.intent_hash:
            raise PermissionError("a validated ALLOW decision is required")
        if decision.decision_id in self.orders:
            return self.orders[decision.decision_id]
        order = {"id": f"order_fake_{len(self.orders) + 1}", "amount": listing.price_paise * quantity,
                 "currency": "INR", "receipt": decision.decision_id}
        self.orders[decision.decision_id] = order
        return order

