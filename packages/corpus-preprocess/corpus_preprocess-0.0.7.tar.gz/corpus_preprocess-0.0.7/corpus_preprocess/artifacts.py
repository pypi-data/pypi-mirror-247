from pathlib import Path

from .preprocessor.utils import Rule

prep_nodes = {
    "LOWER": {"IN": ["in", "it", "is", "has", "have", "been", "a", "an"]},
    "OP": "+",
}

desc_nodes = {
    "LOWER": {
        "IN": [
            "frequently",
            "consistently",
            "repeatedly",
            "often",
            "emphatically",
            "universally",
            "incontrovertible",
            "oft-repeated",
        ]
    },
    "OP": "?",
}


verb_nodes = {
    "LOWER": {
        "IN": [
            "ruled",
            "stated",
            "held",
            "observed",
            "recognized",
            "declared",
            "elucidated",
            "appreciated",
            "affirmed",
            "reaffirmed",
        ]
    }
}


settle_nodes = {
    "LOWER": {
        "IN": [
            "elementary",
            "axiomatic",
            "long-standing",
            "well-recognized",
            "recognized",
            "well-settled",
            "settled",
            "well-embedded",
            "embedded",
            "well-established",
            "established",
            "well-entrenched",
            "entrenched",
            "basic",
            "doctrinal",
            "hornbook",
            "jurisprudence",
            "fundamental",
            "cardinal",
            "hornbook",
        ]
    },
    "OP": "+",
}

rule_nodes = {
    "LOWER": {
        "IN": [
            "precept",
            "rule",
            "doctrine",
            "principle",
            "jurisprudence",
            "axiom",
            "tenet",
            "truism",
            "dictum",
        ]
    }
}


axiom = Rule(
    asset="artifact",
    asset_id="axiom",
    label="axiom",
    matchers=[
        [prep_nodes, desc_nodes, verb_nodes, {"LOWER": "that", "OP": "?"}],
        [prep_nodes, settle_nodes, verb_nodes, {"LOWER": "that", "OP": "?"}],
        [prep_nodes, rule_nodes, {"LOWER": "is"}, settle_nodes, {"LOWER": "that", "OP": "?"}],
        [settle_nodes, {"LOWER": "is"}, {"LOWER": "the"}, rule_nodes],
        [prep_nodes, {"LOWER": "jurisdiction"}],
        [settle_nodes, rule_nodes],
    ],
)

decorator = Rule(
    asset="artifact",
    asset_id="decorator",
    label="decorator",
)

money = Rule(
    asset="artifact",
    asset_id="money",
    label="money",
)


def create_artifacts(artifact_folder: Path):
    decorators = decorator.collect_patterns(artifact_folder)
    axioms = axiom.collect_patterns(artifact_folder)
    monies = money.collect_patterns(artifact_folder)
    return decorators + axioms + monies
