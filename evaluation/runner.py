import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

import yaml

from evaluation.metrics import summarize
from guard.canonical import hash_object, utc_now
from guard.decision_engine import DecisionEngine
from guard.intent_store import IntentStore
from guard.model_adapter import LocalDeterministicAdapter
from guard.schemas import Intent, Listing

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


async def run(dataset: str) -> Path:
    config = yaml.safe_load((ROOT / "evaluation/frozen_config.yaml").read_text())
    fixture_name = "calibration_attacks.jsonl" if dataset == "calibration" else "heldout_attacks.jsonl"
    episodes = read_jsonl(ROOT / "data/fixtures/benign.jsonl") + read_jsonl(ROOT / "data/fixtures" / fixture_name)
    intents = {x["intent_id"]: Intent.model_validate(x) for x in json.loads((ROOT / "data/intents/scenarios.json").read_text())}
    catalogues: dict[str, list[Listing]] = {}
    engine = DecisionEngine(LocalDeterministicAdapter(), config["detector_threshold"], config["relevance_delta"])
    store = IntentStore()
    output: list[dict] = []
    for episode in episodes:
        intent = store.confirm(intents[episode["intent_id"]])
        if episode["catalogue"] not in catalogues:
            data = json.loads((ROOT / f"data/catalogues/{episode['catalogue']}.json").read_text())
            catalogues[episode["catalogue"]] = [Listing.model_validate(x) for x in data]
        listings = [x for x in catalogues[episode["catalogue"]] if x.sku_id in episode["included_skus"]]
        baseline = await engine.decide(intent, listings, "off", episode["seed"])
        guarded = await engine.decide(intent, listings, "on", episode["seed"])
        output.append({**episode, "baseline_selected_sku": baseline.selected_sku,
                       "guarded_action": guarded.action.value, "guarded_selected_sku": guarded.selected_sku,
                       "guarded_reason_codes": [x.value for x in guarded.reason_codes],
                       "guarded_latency_ms": guarded.latency_ms})
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    directory = ROOT / f"results/run_{stamp}_{config['model_id']}_{dataset}"
    directory.mkdir(parents=True)
    (directory / "episodes.jsonl").write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in output), encoding="utf-8")
    summary = {"dataset": dataset, "model_id": config["model_id"], "created_at": utc_now(),
               "config_hash": hash_object(config, "_none"), **summarize(output)}
    (directory / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(directory.relative_to(ROOT))
    return directory


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=("calibration", "heldout"), default="heldout")
    args = parser.parse_args()
    asyncio.run(run(args.dataset))


if __name__ == "__main__":
    main()

