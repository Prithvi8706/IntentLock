import argparse
import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "data/fixtures/benign.jsonl", ROOT / "data/fixtures/calibration_attacks.jsonl",
           ROOT / "data/fixtures/heldout_attacks.jsonl", ROOT / "data/intents/scenarios.json",
           ROOT / "evaluation/frozen_config.yaml"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-new-version", action="store_true")
    args = parser.parse_args()
    config_path = ROOT / "evaluation/frozen_config.yaml"
    config = yaml.safe_load(config_path.read_text())
    hashes_path = ROOT / "data/fixtures/FIXTURE_HASHES.txt"
    if config.get("frozen") and hashes_path.exists() and not args.force_new_version:
        raise SystemExit("Already frozen. Use --force-new-version to create a new version.")
    config["version"] = int(config.get("version", 0)) + int(args.force_new_version)
    config["frozen"] = True
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}" for path in TARGETS]
    hashes_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Frozen version {config['version']}")


if __name__ == "__main__":
    main()

