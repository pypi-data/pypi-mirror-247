from pathlib import Path

import srsly  # type: ignore

from .patterns_date import patterns_date
from .patterns_docket import patterns_docket
from .patterns_generic import patterns_generic, patterns_generic_rules
from .patterns_juridical import patterns_juridical
from .patterns_report import patterns_report
from .patterns_statute import patterns_statute
from .patterns_unit import patterns_unit
from .utils import Rule

"""
dates = Rule(label="DATE", patterns=patterns_date)
jurs = Rule(label="JUR", patterns=patterns_juridical)
statutes = Rule(id="base-statute", label="STATUTE", patterns=patterns_statute)
generic_statutes = Rule(id="generic-statute", label="STATUTE", patterns=patterns_generic_rules)
units = Rule(label="UNIT", patterns=patterns_unit)
dockets = Rule(label="DOCKET", patterns=patterns_docket)
generic = Rule(label="PAPER", patterns=patterns_generic)
reports = Rule(label="REF", patterns=patterns_report)


def create_rules(folder: Path):
    for rule in [dates, jurs, dockets, reports, generic, statutes, generic_statutes, units]:
        target = folder.joinpath(f"{rule.ent_id}.jsonl")
        srsly.write_jsonl(path=target, lines=rule.model_dump())
"""
