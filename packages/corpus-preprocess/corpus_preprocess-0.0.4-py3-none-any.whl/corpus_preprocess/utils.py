import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import srsly  # type: ignore
from pydantic import BaseModel, StringConstraints
from pydantic.functional_validators import AfterValidator
from rich.jupyter import print
from spacy.language import Language
from spacy.tokens import Doc
from typing_extensions import Annotated

camel_case_pattern = re.compile(r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)")


def uncamel(text: str) -> list[str]:
    """For text in camelCaseFormatting, convert into a list of strings."""
    return [m.group(0) for m in camel_case_pattern.finditer(text)]


def check_titlecased_word(v: str) -> str:
    assert all(bit.istitle for bit in v.split("-")), f"{v} is not titlecased."
    return v


TitledString = Annotated[str, AfterValidator(check_titlecased_word)]


def create_regex_options(texts: Iterable[str]):
    return "(" + "|".join(texts) + ")"


def spacy_re(v: str, anchored: bool = True, op: str | None = None) -> dict[str, Any]:
    """Helper function to add an anchored, i.e. `^`<insert value `v` here>`$`
    regex pattern, following `{"TEXT": {"REGEX": f"^{v}$"}}` spacy convention,
    unless modified by arguments.
    """
    if anchored:
        v = f"^{v}$"
    result = {"TEXT": {"REGEX": v}}
    return result | {"OP": op} if op else result


def spacy_in(v_list: list[str], default: str = "ORTH", op: str | None = None):
    """Helper function to add a specific list of options following
    `{"ORTH": {"IN": v_list}}` spacy convention, unless modified by arguments.
    """
    result = {default: {"IN": v_list}}
    return result | {"OP": op} if op else result


def set_optional_node():
    """Deal with nodes like (R.A.), [PD]"""
    _open = create_regex_options(texts=("\\(", "\\["))
    _close = create_regex_options(texts=("\\)", "\\]"))
    _in = "[\\w\\.]+"
    regex = "".join([_open, _in, _close])
    return spacy_re(v=regex, op="?")


def validated_path(f: str) -> Path:
    patterns_path = Path(f)  # type: ignore
    if not patterns_path.exists():
        raise Exception(f"Invalid {f=}")
    return patterns_path


def see(doc: Doc):
    """Rich jupyter-based print spacy-entities and span groups from `doc`."""

    def extract_ents(doc):
        for key in list(set(ent.label_ for ent in doc.ents)):
            data = {"label": key, "ents": []}
            for ent in doc.ents:
                if ent.label_ == key:
                    data["ents"].append(ent.text)
            yield data

    print(list(extract_ents(doc)))
    for spans_key, group in doc.spans.items():
        if spans := [f"{idx}: {v}" for idx, v in enumerate(group)]:
            print(f"{spans_key=}: {spans=}")


def make_uniform_lines(file: Path, min_char: int = 5) -> list[str]:
    """Updates file with sorted lines, filtering those not reaching `min_char` length."""
    raw_lines = file.read_text().splitlines()
    lines = sorted(set(bit for bit in raw_lines if bit.strip() and len(bit) > min_char))
    file.write_text("\n".join(lines))
    return lines


def extract_lines_from_txt_files(files: Iterable[Path]) -> Iterator[str]:
    """Accepts an iterator of `*.txt` files and yields each
    line (after sorting the same and ensuring uniqueness of content).
    """
    for file in files:
        if file.suffix != ".txt":
            raise Exception(f"{file=} must be a .txt file separated by lines.")
        yield from make_uniform_lines(file)  # sort before split


def label_txt_pattern(
    label: str,
    path: Path,
    stems: set[str],
    include_only_if_regex: str | None = None,
    exclude_always_if_regex: str | None = None,
):
    files = path.glob("*.txt")
    files = (f for f in files if f.stem in stems)
    lines = extract_lines_from_txt_files(files)
    uniqs = set()
    for line in lines:
        if include_only_if_regex:
            if not re.search(include_only_if_regex, line):
                continue

        if exclude_always_if_regex:
            if re.search(exclude_always_if_regex, line):
                continue

        uniqs.add(line)
    return ({"label": label, "pattern": uniq} for uniq in uniqs)


def label_jsonl_patterns(label: str, patterns: list[list[dict[str, Any]]]):
    return ({"label": label, "pattern": pattern} for pattern in patterns)


def read_txt_lines_from_structured_path(
    path: Path, label: str, path_pattern: str = "**/q.txt"
) -> Iterator[dict[str, str]]:
    """Create _phrase_ pattern from structured path. Assumes nested folder to generate id from the location of the
    _txt_ file; this is usually applied to files in the `concepts` directory of the corpus-assets package."""
    for txt_file in path.glob(path_pattern):
        for line in make_uniform_lines(txt_file):
            yield {
                "label": label,
                "pattern": line,
                "id": f"{txt_file.parent.parent.stem}/{txt_file.parent.stem}",
            }


def read_jsonl_lines_from_structured_path(
    path: Path, label: str, path_pattern: str = "**/patterns.json"
) -> Iterator[dict[str, str | list[dict[str, Any]]]]:
    """Create _matcher_ pattern from structured path. Assumes nested folder to generate id from the location of the
    _jsonl file_; this is usually applied to files in the `concepts` directory of the corpus-assets package."""
    for json_file in path.glob(path_pattern):
        matchers = srsly.read_json(json_file)
        if matchers and isinstance(matchers, list):
            for matcher_pattern in matchers:
                yield {
                    "label": label,
                    "pattern": matcher_pattern,
                    "id": f"{json_file.parent.parent.stem}/{json_file.parent.stem}",
                }


def split_data(texts: list[str], ratio: float = 0.80) -> dict[str, set[str]]:
    """given a list of text strings, split the same into two groups and return a dictionary
    containing these groups based on the ratio provided (defaults to 0.80)

    The result of splitting `texts` on a ratio = text strings for each category, e.g.:
    {"dev": list of strings (the first 20%), "train": list of strings (the balance of 80%)}
    """
    max_count = len(texts)
    train_count = int(max_count * ratio)
    dev_count = max_count - train_count
    res: dict[str, set[str]] = {"train": set(), "dev": set()}
    for idx, text in enumerate(texts):
        category = res["dev"] if idx < dev_count else res["train"]
        category.add(text)
    return res


def annotate_lines(
    nlp: Language,
    texts: set[str],
    is_readable: bool = True,
) -> Iterator[tuple[str, dict[str, Any]]]:
    """Collects annotated data, consisting of tuples where first item is a string,
    second item is a dict with an `entities` key. If `is_readable is `True`, the annotated texts
    are gathered into a separate `readables` key per entry. Readables not necessary for training
    and are used here to help determine whether the annotations are correct."""
    for doc in nlp.pipe(texts):
        data: dict[str, Any] = {}
        if not doc.ents:
            continue
        data["entities"] = [[e.start, e.end, e.label_] for e in doc.ents]
        if is_readable:
            data["readables"] = [doc[e.start : e.end].text for e in doc.ents]
        yield (doc.text, data)


def annotate_fragments(nlp: Language, target_file: Path, txt_files: Iterable[Path]):
    """Helper function to consolidate all the `txt_files` and extract each line from
    the same for the purpose of annotating it based on the `nlp` object. Each annotation
    will then be written into a `target_file`."""
    texts = set(extract_lines_from_txt_files(txt_files))
    data: list[tuple[str, dict[str, Any]]] = list(annotate_lines(nlp=nlp, texts=texts))
    srsly.write_json(path=target_file, data=data)
    return target_file


class Rule(BaseModel):
    """`patterns` associated with a single `label`. See generally:

    1. https://spacy.io/usage/rule-based-matching#entityruler-files
    2. https://spacy.io/usage/rule-based-matching#spanruler-files

    A `Rule` enables the creation of such pattern objects containing the same `Label`
    and custom `id`, if provided. Sample rule:

    ```py
    sample = Rule(
        asset_type="artifact",
        asset_id="some-office",
        label="GOVT",
        matchers=[
            [
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "ministry"},
                {"LOWER": "of"},
                {"LOWER": "labor"},
            ]
        ],
    )
    ```
    """

    asset: str
    asset_id: str
    label: Annotated[
        str,
        StringConstraints(strip_whitespace=True, pattern=r"^[A-Za-z]+$"),
    ]
    matchers: list[list[dict[str, Any]]] | None = None

    def __str__(self) -> str:
        return f"{self.asset}-{self.asset_id}"

    def __repr__(self) -> str:
        return f"<Rule {self.asset}/{self.asset_id}>"

    @property
    def id(self):
        return str(self)

    @property
    def matcher_path(self):
        return "/".join([self.asset, self.asset_id, "patterns.json"])

    @property
    def phrase_path(self):
        return "/".join([self.asset, self.asset_id, "q.txt"])

    def create_patterns(self, objs):
        return [{"label": self.label, "pattern": obj, "id": self.id} for obj in objs]

    def check_path(self, folder: Path, filename: str) -> Path:
        if not folder.exists():
            raise Exception(f"Missing {folder=}")
        return folder.joinpath(filename)

    def phrases_from_disk(self, folder: Path) -> list[str]:
        """Get rule's phrases from expected location."""
        file = self.check_path(folder, self.phrase_path)
        if not file.exists():
            return []
        return make_uniform_lines(file)

    def convert_phrases_to_patterns(self, folder: Path) -> list[dict[str, Any]]:
        """Use `phrases_from_disk` to construct a list of patterns."""
        objs = self.phrases_from_disk(folder)
        patterns = self.create_patterns(objs)
        return patterns

    def matchers_to_disk(self, folder: Path) -> Path:
        """Overwrites conventional patterns.json file in a proper folder."""
        file = self.check_path(folder, self.matcher_path)
        srsly.write_json(path=file, data=self.matchers)
        return file

    def matchers_from_disk(self, folder: Path) -> list[list[dict[str, Any]]]:
        """Get rule's patterns from expected location."""
        file = self.check_path(folder, self.matcher_path)
        if not file.exists():
            return []

        data = srsly.read_json(path=file)
        if not isinstance(data, list):
            raise Exception(f"Improper {data=}")

        return data

    def convert_matchers_to_patterns(self, folder: Path) -> list[dict[str, Any]]:
        """Use `matchers_from_disk` to construct a list of patterns."""
        objs = self.matchers_from_disk(folder)
        patterns = self.create_patterns(objs)
        return patterns

    def collect_patterns(self, folder: Path):
        phrases = self.convert_phrases_to_patterns(folder)
        matchers = self.convert_matchers_to_patterns(folder)
        patterns = phrases + matchers
        return patterns
