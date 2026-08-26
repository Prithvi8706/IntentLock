from copy import deepcopy

from guard.canonical import hash_object, utc_now
from guard.schemas import Intent


class IntentStore:
    def __init__(self) -> None:
        self._versions: dict[str, list[Intent]] = {}

    def confirm(self, intent: Intent) -> Intent:
        data = intent.model_dump()
        data.update(confirmed_by_user=True, confirmed_at=utc_now(), intent_hash=None)
        data["intent_hash"] = hash_object(data, "intent_hash")
        confirmed = Intent.model_validate(data)
        self._versions.setdefault(intent.intent_id, []).append(deepcopy(confirmed))
        return confirmed

    def revise(self, intent: Intent, **changes: object) -> Intent:
        data = intent.model_dump()
        data.update(changes)
        data.update(intent_version=intent.intent_version + 1, confirmed_by_user=False, confirmed_at=None, intent_hash=None)
        return Intent.model_validate(data)

    def get_by_hash(self, intent_hash: str) -> Intent | None:
        return next((deepcopy(i) for versions in self._versions.values() for i in versions if i.intent_hash == intent_hash), None)

    def versions(self, intent_id: str) -> list[Intent]:
        return deepcopy(self._versions.get(intent_id, []))


def verify_intent_hash(intent: Intent) -> bool:
    return bool(intent.intent_hash and intent.intent_hash == hash_object(intent.model_dump(), "intent_hash"))

