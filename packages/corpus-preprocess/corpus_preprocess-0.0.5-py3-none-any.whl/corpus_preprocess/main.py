import sqlite3
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from .abstracts import create_abstractions
from .artifacts import create_artifacts
from .preprocessor import (
    StructuredQuery,
    extract_ruling_segments,
    read_jsonl_lines_from_structured_path,
    read_txt_lines_from_structured_path,
    validated_path,
)
from .tokenizer import customize_tokenizer, set_single_tokens


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


def set_patterns(path: Path):
    artifacts = create_artifacts(path.joinpath("artifact"))
    concepts = create_concepts(path.joinpath("concept"))
    spans = create_abstractions(path.joinpath("text"))
    return artifacts + concepts + spans


def get_concepts(concepts_path: str | Path):
    return [p for p in Path(concepts_path).iterdir() if p.is_dir()]


def add_rules_to_nlp(nlp: Language, special_token_rules: dict, patterns: Iterable[dict[str, Any]]):
    """_summary_

    Args:
        nlp (Language): Must have tagger/parser/lemmatizer to take advantage of `patterns` defined.
        special_token_rules (dict): Will enable special cases to be defined on the custom tokenizer.
        patterns (Iterable[dict[str, Any]]): Patterns constructed, defined by `corpus-assets` + `corpus-preprocess`

    Returns:
        _type_: _description_
    """
    nlp.tokenizer = customize_tokenizer(nlp, special_token_rules)
    ruler = nlp.add_pipe(
        "span_ruler",
        config={
            "spans_key": "ruler",
            "phrase_matcher_attr": "LOWER",
            "spans_filter": {"@misc": "spacy.first_longest_spans_filter.v1"},
        },
    )
    ruler.add_patterns(patterns)  # type: ignore
    return nlp


def build_nlp(model_name: str, path: Path) -> Language:
    """Wrapper around `add_rules_to_nlp` based, requires at least `en_core_web_sm`.
    Generally takes ~2m to load ruler-based patterns consisting of over 130k entries."""
    nlp = spacy.load(model_name, exclude="senter")
    patterns = set_patterns(path)
    special_rules = set_single_tokens(path)
    revised_nlp = add_rules_to_nlp(nlp=nlp, special_token_rules=special_rules, patterns=patterns)
    return revised_nlp


def apply_concept_q_filter(
    nlp: Language,
    db_file: Path,
    filter_path: Path,
    max_segments: int = 500,
    min_char_segment: int = 200,
    max_char_segment: int = 3000,
    batch_size: int = 500,
    n_process: int = 2,
) -> Iterator[Doc]:
    """The `q.txt` files recursively fetched within the `filter_path` is dissected into individual
    lines, the lines are combined to form an sqlite-fts5 query string to be used as criteria to fetch
    relevant segments from the database.

    Args:
        nlp (Language): What language to apply to the fetched segments from the database
        db_file (Path): Requires Fts-enabled on the "text" column of an "opinion_segments" table.
        filter_path (Path): Where to source the raw queries
        max_segments (int, optional): Limited number of docs _per_ q.txt file, so if the q.txt file contains 80 lines,
                these lines will be used to form the fts expression to retrieve the `max_segments`. Defaults to 500.
        min_char_segment (int, optional): Fetch segment only with min num of characters. Defaults to 200.
        max_char_segment (int, optional): Fetch segment not exceeding max num of characters. Defaults to 3000.
        batch_size (int, optional): Size of batch on `nlp.pipe(batch_size=x)`. Defaults to 500.
        n_process (int, optional): Number of processes `nlp.pipe(n_process=x)`. Defaults to 2.

    Yields:
        Iterator[Doc]: Fragments that match the queries found in collected q.txt files
    """
    for query in StructuredQuery.collect_queries(conn=sqlite3.connect(db_file), folder_source=filter_path):
        for doc, idx in nlp.pipe(
            texts=query.get_rulings(
                min_char_segment=min_char_segment,
                max_char_segment=max_char_segment,
                max_count=max_segments,
            ),
            as_tuples=True,
            batch_size=batch_size,
            n_process=n_process,
        ):
            doc.user_data = {"segment_id": idx}
            yield doc


def apply_label_filter(
    nlp: Language,
    db_file: Path,
    filter_labels: set[str],
    filter_count: int = 500,
    min_char_segment: int = 200,
    max_char_segment: int = 3000,
    batch_size: int = 500,
    n_process: int = 2,
) -> Iterator[Doc]:
    """Extract all database-sourced docs as a formatted generator, if the doc contains a span with a
    label found in the `filter_labels` variable, include the doc in the yielded generator.

    Args:
        nlp (Language): What language to apply to the fetched segments from the database
        db_file (Path): Requires Fts-enabled on the "text" column of an "opinion_segments" table.
        filter_labels (set[str]): Limits retrieved docs, only keep if doc contains a span with matching label.
        filter_count (int, optional): Ensures that only a limited number of docs will be retrieved. Defaults to 500.
        min_char_segment (int, optional): Fetch segment only with min num of characters. Defaults to 200.
        max_char_segment (int, optional): Fetch segment not exceeding max num of characters. Defaults to 3000.
        batch_size (int, optional): Size of batch on `nlp.pipe(batch_size=x)`. Defaults to 500.
        n_process (int, optional): Number of processes `nlp.pipe(n_process=x)`. Defaults to 2.

    Yields:
        Iterator[Doc]: Fragments that contain spans that have a filter label.
    """
    counter = 0  # the counter refers to the matches
    for doc, idx in nlp.pipe(
        texts=extract_ruling_segments(
            conn=sqlite3.connect(db_file),
            min_char_segment=min_char_segment,
            max_char_segment=max_char_segment,
        ),
        as_tuples=True,
        batch_size=batch_size,
        n_process=n_process,
    ):
        for span in doc.spans["ruler"]:
            if span.label_ in filter_labels:
                counter += 1
                doc.user_data = {"segment_id": idx}
                yield doc
                break  # go to next doc in outer for-loop (prevent duplicates)
        if counter == filter_count:
            break
