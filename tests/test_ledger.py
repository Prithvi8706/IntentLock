import json
from concurrent.futures import ThreadPoolExecutor

from audit.ledger import GENESIS_HASH, Ledger, verify_chain
from guard.schemas import EventType


def test_chain_verifies_and_tamper_breaks(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger = Ledger(path)
    first = ledger.append(EventType.INTENT_COMPILED, {"x": 1})
    ledger.append(EventType.DECIDED, {"x": 2}, "dec_1")
    assert first.previous_hash == GENESIS_HASH and verify_chain(path)[0]
    rows = path.read_text().splitlines()
    row = json.loads(rows[0])
    row["payload"]["x"] = 9
    rows[0] = json.dumps(row)
    path.write_text("\n".join(rows) + "\n")
    assert not verify_chain(path)[0]


def test_concurrent_appends_do_not_interleave(tmp_path):
    ledger = Ledger(tmp_path / "ledger.jsonl")
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda n: ledger.append(EventType.RANKED, {"n": n}), range(10)))
    assert len(ledger.events()) == 10 and verify_chain(ledger.path)[0]
