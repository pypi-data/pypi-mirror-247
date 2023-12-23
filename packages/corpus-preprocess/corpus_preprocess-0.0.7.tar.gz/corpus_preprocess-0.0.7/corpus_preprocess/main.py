import sqlite3
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import spacy
import srsly  # type: ignore
from spacy.language import Language
from spacy.tokens import Doc

from .abstracts import create_abstractions
from .artifacts import create_artifacts
from .concepts import create_concepts
from .preprocessor import StructuredQuery, extract_ruling_segments, validated_path
from .tokenizer import customize_tokenizer


def create_data_cfg(asset_folder: str, target_file: str = "cfg.json.gz"):
    """Create initializing parameters for training a spancat x textcat model.

    The reason we use "sc" is that we'll be applying this model to raw text extracted in assets
    "sc" is the default spans_key for spancat; we'll be using the documents that are passed
    through this _rules-based base_nlp_ model to create Doc objects that can be trained with
    the spancat and textcat pipe components.
    """
    path = validated_path(asset_folder)
    concepts = create_concepts(path.joinpath("concept"))
    srsly.write_gzip_json(
        target_file,
        {
            "span_ruler_config_for_spancat": {
                "spans_key": "sc",
                "phrase_matcher_attr": "LOWER",
                "spans_filter": {"@misc": "spacy.first_longest_spans_filter.v1"},
            },
            "span_ruler_patterns": create_artifacts(path.joinpath("artifact"))
            + create_abstractions(path.joinpath("text"))
            + concepts,
            "tokenizer_rules": srsly.read_json(path.joinpath("artifact/singleton/patterns.json")),
            "textcat_options": list({concept["id"].split("/")[0] for concept in concepts}),
        },
    )


@Language.factory(name="add_cats_from_spans")
class AddTextCatComponent:
    def __init__(self, nlp: Language, name: str, options: list[str]):
        self.nlp = nlp
        self.options = options

    def __call__(self, doc) -> Doc:
        doc.cats = {op: 0.0 for op in self.options}
        for span in doc.spans["sc"]:
            if span.id:  # some spans won't have an id
                value = self.nlp.vocab.strings[span.id]
                if "/" in value:  # e.g. political/bill_of_rights
                    main_topic = value.split("/")[0]  # just political
                    if main_topic in self.options:
                        if doc.cats[main_topic] == 0.0:
                            doc.cats[main_topic] = 1.0
        return doc


def create_trainer_nlp(base_model: str, cfg_json_gzip: str, output_path: str) -> Language:
    """This model compiles all span ruler patterns under the spans key 'sc'
    so that this can be used in creating training data.

    Note that this isn't the spancat nor the textcat model. It's simply a span ruler model
    that will allow us to create Docbin objects that can be trained with a separate, future
    `config.cfg` file. The same tokenizer however must be referred to in the future `config.cfg`.

    Args:
        base_model (str): Must use at least an en_core_web_sm to take advantage of the
                tagger / lemmatizer that are used in pattern files.
        cfg_json_gzip (str): Accepts a path to `cfg_json_gzip` which is the
                unpacked variant of `create_data_cfg()`.
        output_path (str): Where to store the trainer model

    Returns:
        Language: The modified base_model
    """
    cfg = srsly.read_gzip_json(validated_path(cfg_json_gzip))
    if not isinstance(cfg, dict):
        raise Exception(f"Must be a dict when unzipped {cfg_json_gzip}=")

    # load the model
    nlp = spacy.load(base_model, exclude="senter,ner")

    # tokenize
    nlp.tokenizer = customize_tokenizer(nlp, token_rules=cfg["tokenizer_rules"])

    # add rule-based patterns
    ruler = nlp.add_pipe("span_ruler", config=cfg["span_ruler_config_for_spancat"])
    ruler.add_patterns(cfg["span_ruler_patterns"])  # type: ignore

    # use concept patterns, specifically, to determine textcat score
    nlp.add_pipe("add_cats_from_spans", config={"options": cfg["textcat_options"]})

    # save the model
    nlp.to_disk(output_path)  # will save entire directory which includes the pipeline
    return nlp


def apply_concept_q_filter(
    nlp: Language,
    db_file: Path,
    filter_path: Path,
    max_segments: int = 500,
    min_char_segment: int = 200,
    max_char_segment: int = 3000,
    batch_size: int = 500,
    n_process: int = 1,
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
    spans_key: str = "sc",
    min_char_segment: int = 200,
    max_char_segment: int = 3000,
    batch_size: int = 500,
    n_process: int = 1,
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
        for span in doc.spans[spans_key]:
            if span.label_ in filter_labels:
                counter += 1
                doc.user_data = {"segment_id": idx}
                yield doc
                break  # go to next doc in outer for-loop (prevent duplicates)
        if counter == filter_count:
            break
