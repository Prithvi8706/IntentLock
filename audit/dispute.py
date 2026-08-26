from audit.ledger import Ledger


def events_for_order(order_id: str, path: str = "audit/ledger.jsonl") -> list[dict]:
    return [event.model_dump(mode="json") for event in Ledger(path).events() if order_id in str(event.payload)]

