from pathlib import Path

from spacy.language import Language

from .asset_axioms import axiom
from .asset_extractors import create_concept_patterns
from .patterns_date import patterns_date
from .patterns_docket import patterns_docket
from .patterns_juridical import patterns_juridical
from .patterns_report import patterns_report
from .patterns_statute import patterns_statute
from .patterns_unit import patterns_unit
from .utils import label_jsonl_patterns, label_txt_pattern

casenames = {
    "casenames",
    "fn_casenames",
    "eyecite_goodnames",
    "goodnames_1",
    "clean_statute_titles",
}
actors = {
    "juridicals",
    "naturals",
    "fml_names",
    "last_names",
    "first_names",
    "parties",
}
cites = {
    "us",
    "us2",
    "ph",
    "ph2",
    "fn_reporter",
    "fn_docketnums",
    "fn_provisions",
}


def extract_ents(path: Path):
    ents = []
    ents.extend(label_txt_pattern("title", path, casenames))
    ents.extend(label_txt_pattern("actor", path, actors))
    ents.extend(label_txt_pattern("cite", path, cites))
    ents.extend(label_jsonl_patterns("date", patterns_date))
    ents.extend(label_jsonl_patterns("actor", patterns_juridical))
    ents.extend(label_jsonl_patterns("cite", patterns_report))
    ents.extend(label_jsonl_patterns("cite", patterns_statute))
    ents.extend(label_jsonl_patterns("cite", patterns_unit))
    ents.extend(label_jsonl_patterns("cite", patterns_docket))
    return ents


def set_patterns_from_assets(path: Path):
    axioms = axiom.collect_patterns(path.joinpath("meta"))
    concepts = create_concept_patterns(path.joinpath("concepts"))
    ents = extract_ents(path.joinpath("ents"))
    return axioms + concepts + ents
