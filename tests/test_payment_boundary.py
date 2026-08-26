import pytest

from guard.canonical import utc_now
from guard.schemas import Action, DecisionRecord, Listing, ReasonCode
from payments.fake_sink import FakePaymentSink
from payments.razorpay_client import validate_test_key


def decision(action):
    return DecisionRecord(decision_id="dec_1",intent_hash="sha256:"+"1"*64,guard_mode="on",selected_sku="s",
        action=action,reason_codes=[ReasonCode.NO_ELIGIBLE_SKU if action == Action.BLOCK else ReasonCode.DETECTOR_FLAGGED if action == Action.ESCALATE else ReasonCode.HARD_CONSTRAINTS_PASS],
        candidate_count_before=1,candidate_count_after_gate=1,candidate_order_seed=1,model_id="test",latency_ms=0,created_at=utc_now())


def item():
    return Listing(sku_id="s",merchant_namespace="m",title="t",description="d",category="c",usage="all",price_paise=12345,stock=1)


@pytest.mark.parametrize("action", [Action.BLOCK, Action.ESCALATE])
def test_non_allow_cannot_create_order(action):
    with pytest.raises(PermissionError):
        FakePaymentSink().create_order(decision(action), item(), 1)


def test_amount_and_idempotency():
    sink = FakePaymentSink()
    first = sink.create_order(decision(Action.ALLOW), item(), 2)
    second = sink.create_order(decision(Action.ALLOW), item(), 2)
    assert first == second and first["amount"] == 24690 and len(sink.orders) == 1


def test_only_test_keys():
    validate_test_key("rzp_test_example")
    with pytest.raises(ValueError):
        validate_test_key("rzp_live_forbidden")

