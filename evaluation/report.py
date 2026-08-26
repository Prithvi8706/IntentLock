import json
from pathlib import Path


def markdown_summary(summary_path: str | Path) -> str:
    data = json.loads(Path(summary_path).read_text())
    return f"# Evaluation\n\nEpisodes: {data['episodes']}\n\nModel: `{data['model_id']}`\n"

