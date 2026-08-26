import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNED = [ROOT / "data", ROOT / "evaluation"]


def main() -> None:
    violations = []
    for directory in SCANNED:
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix in {".json", ".jsonl", ".yaml", ".yml"}:
                if re.search(r"https?://", path.read_text(encoding="utf-8")):
                    violations.append(str(path.relative_to(ROOT)))
    if violations:
        raise SystemExit("External URLs found: " + ", ".join(violations))
    print("No external URLs in fixtures or evaluation config")


if __name__ == "__main__":
    main()

