import pytest

from guard.admissibility import check_listing
from guard.intent_compiler import IntentCompiler
from guard.intent_store import IntentStore
from guard.schemas import Listing


@pytest.fixture
def intent():
    return IntentStore().confirm(IntentCompiler().compile("outdoor basketball shoes under 6000"))


def listing(**changes):
    data = {"sku_id":"sku","merchant_namespace":"m","title":"Shoe","description":"Clean",
            "category":"basketball_shoes","usage":"outdoor","price_paise":600000,"stock":1,
            "attributes":{"colour":"black"},"fixture_label":"benign"}
    data.update(changes)
    return Listing.model_validate(data)


def test_exact_cap_and_usage_all_pass(intent):
    assert check_listing(intent, listing(usage="all")).eligible


@pytest.mark.parametrize(("change", "reason"), [
    ({"category":"fashion"}, "CATEGORY_MISMATCH"), ({"usage":"indoor"}, "USAGE_MISMATCH"),
    ({"price_paise":600001}, "PRICE_EXCEEDS_CAP"), ({"stock":0}, "INSUFFICIENT_STOCK")])
def test_hard_failures(intent, change, reason):
    assert reason in check_listing(intent, listing(**change)).failures

