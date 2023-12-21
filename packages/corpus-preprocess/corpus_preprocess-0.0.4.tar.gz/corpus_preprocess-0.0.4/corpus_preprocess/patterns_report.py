from typing import Any

covered = {"TEXT": {"REGEX": "^\\(\\d+\\)$"}, "OP": "?"}

publisher_short = {"ORTH": {"IN": ["SCRA", "Phil", "Phil.", "Phil.,", "OG", "O.G."]}}

publisher_words_phil = [
    {"ORTH": {"IN": ["Phil", "Phil.", "Phil.,"]}},
    {"ORTH": {"IN": ["Rep", "Rep.", "Rep.," "Reports"]}},
]

publisher_words_og = [
    {"ORTH": {"IN": ["Off", "Off."]}},
    {"ORTH": {"IN": ["Gaz", "Gazette"]}},
]

generic_start: list[dict[str, Any]] = [
    {"IS_DIGIT": True},
    publisher_short,
    {"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"},
]

generic_start_phil_words = (
    [{"IS_DIGIT": True}] + publisher_words_phil + [{"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"}]
)

generic_start_og_words = (
    [{"IS_DIGIT": True}] + publisher_words_og + [{"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"}]
)

special_volumes: list[dict[str, Any]] = [
    {"ORTH": {"IN": ["258-A", "290-A", "8-A"]}},  # Dashed letter vs. digit
    publisher_short,
    {"IS_DIGIT": True},
]

connected_comma_pages: list[dict[str, Any]] = [
    {"IS_DIGIT": True},
    publisher_short,
    {"TEXT": {"REGEX": "\\d+[,-]\\d+"}},  # 21 Phil 124,125
]

og_legacy: list[dict[str, Any]] = [
    {"IS_DIGIT": True},
    covered,
    {"ORTH": {"IN": ["OG", "O.G."]}},
    covered,
]


patterns_report: list[list[dict[str, Any]]] = [
    generic_start + [{"IS_DIGIT": True}],
    generic_start + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
    generic_start_phil_words + [{"IS_DIGIT": True}],
    generic_start_phil_words + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
    generic_start_og_words + [{"IS_DIGIT": True}],
    generic_start_og_words + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
    connected_comma_pages,
    special_volumes,
    og_legacy + [{"IS_DIGIT": True}],
    og_legacy + [{"LIKE_NUM": True}],  # e.g. fourth, fifth
]


def create_generic_report(label: str, tokens: set[str]):
    options = {"ORTH": {"IN": list(tokens)}, "OP": "{1,4}"}
    return [
        {
            "label": label,
            "pattern": [{"IS_DIGIT": True}, options, {"IS_DIGIT": True}],
        },
        {
            "label": label,
            "pattern": [{"IS_DIGIT": True}, options, {"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
        },
    ]
