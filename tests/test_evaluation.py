import json
from pathlib import Path

from evaluation.metrics import summarize, wilson_interval

ROOT = Path(__file__).resolve().parents[1]


def rows(name):
    return [json.loads(x) for x in (ROOT / f"data/fixtures/{name}").read_text().splitlines() if x]


def test_fixture_contract_and_family_separation():
    calibration, heldout = rows("calibration_attacks.jsonl"), rows("heldout_attacks.jsonl")
    assert {x["family"] for x in calibration}.isdisjoint(x["family"] for x in heldout)
    required = {"attack_present","attack_stratum","attacker_sku","eligible_skus","acceptable_skus","expected_action"}
    assert all(required <= x.keys() for x in calibration + heldout + rows("benign.jsonl"))


def test_wilson_edges_and_known_summary():
    assert wilson_interval(0, 0) == (0.0, 1.0)
    low, high = wilson_interval(50, 100)
    assert round(low, 3) == 0.404 and round(high, 3) == 0.596
    result = summarize([])
    assert result["episodes"] == 0


def test_runner_source_never_imports_real_client():
    source = (ROOT / "evaluation/runner.py").read_text()
    assert "razorpay_client" not in source and "FakePaymentSink" not in source

