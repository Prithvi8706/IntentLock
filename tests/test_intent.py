from guard.canonical import hash_object
from guard.intent_compiler import IntentCompiler, rupees_to_paise
from guard.intent_store import IntentStore, verify_intent_hash


def test_money_conversion_and_missing_fields():
    assert rupees_to_paise("5999.99") == 599999
    assert rupees_to_paise("6000") == 600000
    try:
        IntentCompiler().compile("something nice")
    except ValueError:
        pass
    else:
        raise AssertionError("missing hard fields must not be guessed")


def test_confirmation_and_revision_are_hash_versioned():
    draft = IntentCompiler().compile("outdoor basketball shoes under 6000")
    store = IntentStore()
    first = store.confirm(draft)
    second = store.confirm(store.revise(first, max_price_paise=500000))
    assert verify_intent_hash(first) and verify_intent_hash(second)
    assert first.intent_hash != second.intent_hash and second.intent_version == 2
    assert len(store.versions(first.intent_id)) == 2


def test_canonical_hash_ignores_field_and_sorts_nested_data():
    one = {"b": {"y": 2, "x": 1}, "a": 3, "intent_hash": "old"}
    two = {"a": 3, "b": {"x": 1, "y": 2}, "intent_hash": "different"}
    assert hash_object(one, "intent_hash") == hash_object(two, "intent_hash")

