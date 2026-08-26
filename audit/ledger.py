from pathlib import Path
from uuid import uuid4

from filelock import FileLock

from guard.canonical import hash_object, utc_now
from guard.schemas import EventType, LedgerEvent

GENESIS_HASH = "sha256:" + "0" * 64


class Ledger:
    def __init__(self, path: str | Path = "audit/ledger.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = FileLock(str(self.path) + ".lock")

    def events(self) -> list[LedgerEvent]:
        if not self.path.exists():
            return []
        return [LedgerEvent.model_validate_json(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line]

    def append(self, event_type: EventType, payload: dict, decision_id: str | None = None) -> LedgerEvent:
        with self.lock:
            events = self.events()
            data = {"event_id": f"evt_{uuid4().hex[:12]}", "event_type": event_type,
                    "timestamp": utc_now(), "decision_id": decision_id, "payload": payload,
                    "previous_hash": events[-1].event_hash if events else GENESIS_HASH, "event_hash": ""}
            data["event_hash"] = hash_object(data, "event_hash")
            event = LedgerEvent.model_validate(data)
            with self.path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(event.model_dump_json() + "\n")
            return event

    def existing_order(self, decision_id: str) -> dict | None:
        for event in self.events():
            if event.event_type == EventType.ORDER_CREATED and event.decision_id == decision_id:
                return event.payload
        return None


def verify_chain(path: str | Path) -> tuple[bool, int | None, str | None]:
    ledger = Ledger(path)
    previous = GENESIS_HASH
    for index, event in enumerate(ledger.events()):
        if event.previous_hash != previous or event.event_hash != hash_object(event.model_dump(), "event_hash"):
            return False, index, event.event_type.value
        previous = event.event_hash
    return True, None, None
