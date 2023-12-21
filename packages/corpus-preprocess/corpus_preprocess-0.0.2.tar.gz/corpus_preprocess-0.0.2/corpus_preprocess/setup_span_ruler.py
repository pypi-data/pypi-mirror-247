from pathlib import Path

from .asset_axioms import axiom
from .asset_extractors import create_concept_patterns
from .patterns_date import patterns_date
from .patterns_docket import patterns_docket
from .patterns_report import create_generic_report, patterns_report
from .patterns_statute import patterns_statute
from .patterns_unit import patterns_unit
from .utils import label_jsonl_patterns, label_txt_pattern, make_uniform_lines, validated_path


def extract_ents(path: Path):
    ents = []
    ents.extend(
        list(
            create_generic_report(
                label="cite",
                tokens=set(make_uniform_lines(path.joinpath("report_publisher_variants.txt"), 1)),
            )
        )
    )
    ents.extend(
        label_txt_pattern(
            label="title",
            path=path,
            stems={"casenames", "fn_casenames", "eyecite_goodnames", "goodnames_1", "clean_statute_titles"},
        )
    )
    ents.extend(label_jsonl_patterns("date", patterns_date))
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
