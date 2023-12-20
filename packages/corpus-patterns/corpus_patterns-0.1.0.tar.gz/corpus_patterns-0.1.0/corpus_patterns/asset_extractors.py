from collections.abc import Iterator
from pathlib import Path
from typing import Any

import srsly  # type: ignore


def extract_concept_txts(path: Path) -> Iterator[dict[str, str]]:
    for txt_file in path.glob("**/q.txt"):
        for line in txt_file.read_text().splitlines():
            if line.strip():
                yield {
                    "label": "concept",
                    "pattern": line,
                    "id": f"{txt_file.parent.parent.stem}/{txt_file.parent.stem}",
                }


def extract_concept_jsonl(path: Path) -> Iterator[dict[str, str | list[dict[str, Any]]]]:
    for json_file in path.glob("**/patterns.json"):
        matchers = srsly.read_json(json_file)
        if matchers and isinstance(matchers, list):
            for matcher_pattern in matchers:
                yield {
                    "label": "concept",
                    "pattern": matcher_pattern,
                    "id": f"{json_file.parent.parent.stem}/{json_file.parent.stem}",
                }


def validated_path(f: str) -> Path:
    patterns_path = Path(f)  # type: ignore
    if not patterns_path.exists():
        raise Exception(f"Invalid {f=}")
    return patterns_path


def create_concept_patterns(path: str | Path):
    if isinstance(path, str):
        path = validated_path(path)
    return list(extract_concept_jsonl(path)) + list(extract_concept_txts(path))
