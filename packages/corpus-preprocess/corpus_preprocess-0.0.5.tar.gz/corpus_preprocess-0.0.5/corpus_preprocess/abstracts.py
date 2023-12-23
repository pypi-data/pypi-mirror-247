from pathlib import Path
from typing import Any

from .preprocessor import (
    create_vs_patterns,
    patterns_date,
    patterns_docket,
    patterns_juridical,
    patterns_report,
    patterns_statute,
    patterns_unit,
)
from .preprocessor.utils import label_jsonl_patterns, label_txt_pattern, make_uniform_lines, spacy_re


def create_numbered_document(label: str):
    patterns: list[list[dict[str, Any]]] = []
    num_signal = {"LOWER": {"IN": ["no", "nos", "no.", "nos."]}}
    nodes: list[dict[str, Any]] = [{"LIKE_NUM": 1}, {"IS_DIGIT": 1}, {"POS": "NUM"}, spacy_re(r".*\d.*")]
    for node in nodes:
        patterns.append([{"IS_TITLE": 1, "OP": "+"}, num_signal, node | {"OP": "+"}])
    return label_jsonl_patterns(label, patterns)


def create_short_publisher_doc(label: str, src: Path):
    patterns: list[list[dict[str, Any]]] = []
    short_publisher = list(make_uniform_lines(src, min_char=1))
    nodes: list[dict[str, Any]] = [{"IS_DIGIT": True}, {"TEXT": {"REGEX": "\\d+[,-]\\d+"}}]
    for node in nodes:
        patterns.append([{"IS_DIGIT": True}, {"ORTH": {"IN": short_publisher}, "OP": "{1,4}"}, node])
    return label_jsonl_patterns(label, patterns)


def create_abstractions(txt_path: Path):
    """The abstracted patterns are supplemented by the txt_path which contains assocaited phrases."""
    spans = []
    # actor
    spans.extend(label_jsonl_patterns("actor", patterns_juridical))
    spans.extend(label_txt_pattern(label="actor", path=txt_path, stems={"juridical"}))

    # unit
    spans.extend(label_jsonl_patterns("unit", patterns_unit))

    # date
    spans.extend(label_jsonl_patterns("date", patterns_date))

    # title
    spans.extend(
        label_txt_pattern(
            label="title",
            path=txt_path,
            stems={
                "casenames",
                "fn_casenames",
                "eyecite_goodnames",
                "goodnames_1",
                "clean_statute_titles",
            },
        )
    )
    spans.extend(label_jsonl_patterns("title", create_vs_patterns()))

    # serial title
    spans.extend(create_numbered_document("serial"))
    for serial_pattern in (patterns_statute, patterns_docket):
        spans.extend(label_jsonl_patterns("serial", serial_pattern))

    # ref
    spans.extend(create_short_publisher_doc(label="ref", src=txt_path.joinpath("report_publisher_variants.txt")))
    spans.extend(label_jsonl_patterns("ref", patterns_report))
    return spans
