from pathlib import Path
from typing import Any

import srsly  # type: ignore

from .build_abbreviations import Abbv
from .build_digits import PreUnit
from .patterns_docket import admin_case, admin_matter, bar_matter, general_register
from .patterns_generic import ao
from .patterns_statute import (
    batas_pambansa,
    commonwealth_act,
    executive_order,
    pres_decree,
    republic_act,
)
from .utils import make_uniform_lines

members = (
    admin_case,
    admin_matter,
    bar_matter,
    general_register,
    ao,
    batas_pambansa,
    commonwealth_act,
    executive_order,
    pres_decree,
    republic_act,
)
serialized_abbvs = {k: v for member in members if member.initials for k, v in member.initials.as_token.items()}
generic_abbreviations = {
    f"{bit}.": [{"ORTH": f"{bit}."}] for style in (None, "lower", "upper") for bit in Abbv.set_abbvs(cased=style)
}
preunit_abbreviations = {
    f"{bit}.": [{"ORTH": f"{bit}."}] for style in (None, "lower", "upper") for bit in PreUnit.set_abbvs(cased=style)
}


def make_special_dotted():
    """Add a period after every text item to consider each a single token.
    These patterns can be used as a special rule in creating a custom tokenizer."""
    text = "Rep Sen vs Vs v s et al etc no nos Ll p Pp PP P.P R.P H.E H.B S.B a.k.a CA-G.R Exh Ed ed"  # noqa: E501
    return {f"{t}.": [{"ORTH": f"{t}."}] for t in text.split() if not t.endswith(".")}


def set_single_tokens():
    """Results in a dict of various exceptional rules for use in spacy tokenizer, e.g.:

    ```pycon
    >>> treat_as_single_token()
    {'A.C.': [{'ORTH': 'A.C.'}],
    'A.M.': [{'ORTH': 'A.M.'}],
    'B.M.': [{'ORTH': 'B.M.'}],
    'G.R.': [{'ORTH': 'G.R.'}],
    'A.O.': [{'ORTH': 'A.O.'}],
    'B.P.': [{'ORTH': 'B.P.'}],
    'C.A.': [{'ORTH': 'C.A.'}],
    ...}
    ```

    How to use:

    ```
    from spacy.tokenizer import Tokenizer
    Tokenizer(
        nlp.vocab,
        rules=set_single_tokens(),
    )
    """
    return serialized_abbvs | generic_abbreviations | preunit_abbreviations | make_special_dotted()


def export_data_tokens(asset_path: Path):
    exported_singles = asset_path.joinpath("data/single_tokens.json")
    srsly.write_json(exported_singles, set_single_tokens())

    reports_src = asset_path.joinpath("ents/report_publisher_variants.txt")
    exported_reports = asset_path.joinpath("data/report_publishers.json")
    reports_data = {line: [{"ORTH": line}] for line in make_uniform_lines(reports_src, min_char=2)}
    srsly.write_json(exported_reports, reports_data)


def import_data_tokens(data_path: Path):
    data: dict[str, list[dict[str, Any]]] = {}
    files = ("single_tokens.json", "report_publishers.json")
    for file in files:
        data |= srsly.read_json(data_path.joinpath(file))  # type: ignore
    return data
