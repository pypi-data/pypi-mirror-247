from pathlib import Path

axiom_file = Path().home().joinpath("code/corpus-assets/misc/axioms.txt")

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

matcher_patterns = [
    [prep_nodes, desc_nodes, verb_nodes, {"LOWER": "that", "OP": "?"}],
    [prep_nodes, settle_nodes, verb_nodes, {"LOWER": "that", "OP": "?"}],
    [prep_nodes, rule_nodes, {"LOWER": "is"}, settle_nodes, {"LOWER": "that", "OP": "?"}],
    [settle_nodes, {"LOWER": "is"}, {"LOWER": "the"}, rule_nodes],
    [prep_nodes, {"LOWER": "jurisdiction"}],
    [settle_nodes, rule_nodes],
]
axiom_matcher_patterns = [
    {"id": "axiom", "label": "axiom", "pattern": p} for p in axiom_file.read_text().splitlines() + matcher_patterns
]
