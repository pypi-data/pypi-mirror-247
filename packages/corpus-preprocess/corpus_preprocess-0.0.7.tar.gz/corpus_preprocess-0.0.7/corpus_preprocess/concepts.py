from pathlib import Path
from typing import Any

from .preprocessor import read_jsonl_lines_from_structured_path, read_txt_lines_from_structured_path, validated_path


def create_concepts(path: str | Path) -> list[dict[str, Any]]:
    """Based on the `q.txt` and `patterns.json` files found in the path, generate
    patterns in a list of dicts where each dict consists of the following keys:

    1. `id`: <root-path>/<child-path>
    2. `label`: "concept"
    3. `pattern`: either a string or a list of dicts, following the spacy Matcher pattern
    style.
    """
    if isinstance(path, str):
        path = validated_path(path)
    patterns = list(read_jsonl_lines_from_structured_path(path, label="concept", path_pattern="**/patterns.jsonl"))
    phrases = list(read_txt_lines_from_structured_path(path, label="concept", path_pattern="**/q.txt"))
    return patterns + phrases


def get_concepts(concepts_path: str | Path):
    return [p for p in Path(concepts_path).iterdir() if p.is_dir()]
